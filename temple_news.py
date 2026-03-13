"""
temple_news.py
The TempleNews module fetches the latest news and alerts from Temple University
using the Reddit API (r/temple and r/TempleU subreddits). This module is free
to use and requires no API key. It provides a display function that renders
a Temple News screen within the Pygame application.
"""
 
import pygame
import urllib.request
import json
import threading
 
# Temple Cherry Red color (official Temple brand color)
TEMPLE_RED = (157, 34, 53)
TEMPLE_WHITE = (255, 255, 255)
DARK_BG = (20, 20, 30)
CARD_BG = (40, 40, 55)
CARD_BORDER = (157, 34, 53)
 
 
def fetch_temple_news():
    """
    Fetches the latest posts from the r/temple subreddit using Reddit's
    free JSON API (no key required). Returns a list of dicts with
    'title', 'author', 'score', and 'url' fields.
    Falls back to a static message if network is unavailable.
    """
    results = []
    urls_to_try = [
        ("r/temple", "https://www.reddit.com/r/temple/new.json?limit=6"),
        ("r/TempleUniversity", "https://www.reddit.com/r/TempleUniversity/new.json?limit=4"),
    ]
    headers = {"User-Agent": "CheckersPlusApp/1.0 (CIS3296 Project)"}
 
    for source, url in urls_to_try:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                posts = data.get("data", {}).get("children", [])
                for post in posts[:5]:
                    p = post["data"]
                    results.append({
                        "title": p.get("title", "No title"),
                        "author": p.get("author", "unknown"),
                        "score": p.get("score", 0),
                        "source": source,
                        "url": "reddit.com" + p.get("permalink", ""),
                    })
        except Exception:
            continue
 
    if not results:
        # Fallback static content when offline
        results = [
            {"title": "Could not fetch live news. Check your internet connection.", 
             "author": "System", "score": 0, "source": "Offline", "url": ""},
            {"title": "Visit temple.edu/news for the latest Temple University news.",
             "author": "System", "score": 0, "source": "Offline", "url": ""},
            {"title": "Visit twitter.com/TempleAlert for emergency alerts.",
             "author": "System", "score": 0, "source": "Offline", "url": ""},
        ]
    return results
 
 
def wrap_text(text, font, max_width):
    """
    Wraps a string of text into multiple lines that each fit within max_width pixels.
    Returns a list of strings.
    """
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test = current_line + (" " if current_line else "") + word
        if font.size(test)[0] <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines if lines else [""]
 
 
def show_temple_news(screen, Width, Height, SONG_END, music_loop_fn):
    """
    Displays the Temple University News screen. Fetches posts from Reddit
    in a background thread so the UI stays responsive. Shows a loading
    indicator while fetching, then renders each post as a card.
 
    Parameters:
        screen       - the pygame display surface
        Width        - screen width
        Height       - screen height
        SONG_END     - pygame event type for song ending
        music_loop_fn - function to call to advance to next music track
    """
    news_screen = pygame.display.set_mode([Width, Height])
    clock = pygame.time.Clock()
 
    # --- Fonts ---
    title_font   = pygame.font.Font(None, 52)
    subtitle_font = pygame.font.Font(None, 28)
    card_title_font = pygame.font.Font(None, 26)
    card_meta_font  = pygame.font.Font(None, 22)
    btn_font     = pygame.font.Font(None, 32)
    loading_font = pygame.font.Font(None, 36)
 
    # --- Fetch news in background thread ---
    news_data = []
    loading = [True]  # mutable so thread can modify it
 
    def _fetch():
        news_data.extend(fetch_temple_news())
        loading[0] = False
 
    thread = threading.Thread(target=_fetch, daemon=True)
    thread.start()
 
    # --- Exit button ---
    exit_text    = btn_font.render("Return to Main Menu", True, TEMPLE_WHITE)
    exit_rect    = exit_text.get_rect(center=(Width // 2, Height - 35))
    exit_bg_rect = pygame.Rect(exit_rect.left - 15, exit_rect.top - 8,
                               exit_rect.width + 30, exit_rect.height + 16)
 
    # --- Refresh button ---
    refresh_text    = btn_font.render("Refresh", True, TEMPLE_WHITE)
    refresh_rect    = refresh_text.get_rect(center=(Width - 90, Height - 35))
    refresh_bg_rect = pygame.Rect(refresh_rect.left - 12, refresh_rect.top - 8,
                                  refresh_rect.width + 24, refresh_rect.height + 16)
 
    dot_count = 0
    dot_timer = 0
 
    running = True
    while running:
        clock.tick(30)
        dt = clock.get_time()
        dot_timer += dt
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_bg_rect.collidepoint(event.pos):
                    return
                if refresh_bg_rect.collidepoint(event.pos) and not loading[0]:
                    # Re-fetch
                    news_data.clear()
                    loading[0] = True
                    thread2 = threading.Thread(target=_fetch, daemon=True)
                    thread2.start()
            elif event.type == SONG_END:
                music_loop_fn()
 
        # Animate loading dots
        if dot_timer > 500:
            dot_count = (dot_count + 1) % 4
            dot_timer = 0
 
        # --- Draw background ---
        news_screen.fill(DARK_BG)
 
        # --- Header bar ---
        pygame.draw.rect(news_screen, TEMPLE_RED, pygame.Rect(0, 0, Width, 70))
        # Temple "T" accent line
        pygame.draw.rect(news_screen, TEMPLE_WHITE, pygame.Rect(0, 68, Width, 3))
 
        header_text = title_font.render("Temple University News", True, TEMPLE_WHITE)
        header_rect = header_text.get_rect(center=(Width // 2, 35))
        news_screen.blit(header_text, header_rect)
 
        source_text = subtitle_font.render("Live from Reddit · r/temple · r/TempleUniversity", True, (220, 180, 180))
        source_rect = source_text.get_rect(center=(Width // 2, 58))
        news_screen.blit(source_text, source_rect)
 
        # --- Content area ---
        if loading[0]:
            dots = "." * dot_count
            load_surf = loading_font.render(f"Fetching latest Temple news{dots}", True, TEMPLE_WHITE)
            load_rect = load_surf.get_rect(center=(Width // 2, Height // 2))
            news_screen.blit(load_surf, load_rect)
        else:
            # Draw news cards
            card_x = 30
            card_y = 85
            card_w = Width - 60
            card_h = 85
            card_spacing = 10
 
            for i, item in enumerate(news_data[:6]):
                cy = card_y + i * (card_h + card_spacing)
                if cy + card_h > Height - 60:
                    break
 
                # Card background + border
                card_rect = pygame.Rect(card_x, cy, card_w, card_h)
                pygame.draw.rect(news_screen, CARD_BG, card_rect, border_radius=8)
                pygame.draw.rect(news_screen, CARD_BORDER, card_rect, width=2, border_radius=8)
 
                # Left accent bar
                accent_rect = pygame.Rect(card_x, cy, 5, card_h)
                pygame.draw.rect(news_screen, TEMPLE_RED, accent_rect,
                                 border_top_left_radius=8, border_bottom_left_radius=8)
 
                # Title (wrapped)
                title_lines = wrap_text(item["title"], card_title_font, card_w - 80)
                for li, line in enumerate(title_lines[:2]):
                    t_surf = card_title_font.render(line, True, TEMPLE_WHITE)
                    news_screen.blit(t_surf, (card_x + 15, cy + 10 + li * 24))
 
                # Meta info: source, author, score
                meta_str = f"  {item['source']}  |  u/{item['author']}  |  ▲ {item['score']}"
                meta_surf = card_meta_font.render(meta_str, True, (160, 160, 180))
                news_screen.blit(meta_surf, (card_x + 12, cy + card_h - 24))
 
        # --- Buttons ---
        mouse = pygame.mouse.get_pos()
 
        # Exit button
        exit_color = (100, 20, 35) if exit_bg_rect.collidepoint(mouse) else TEMPLE_RED
        pygame.draw.rect(news_screen, exit_color, exit_bg_rect, border_radius=6)
        news_screen.blit(exit_text, exit_rect)
 
        # Refresh button (disabled while loading)
        if not loading[0]:
            ref_color = (60, 60, 80) if refresh_bg_rect.collidepoint(mouse) else (50, 50, 70)
            pygame.draw.rect(news_screen, ref_color, refresh_bg_rect, border_radius=6)
            pygame.draw.rect(news_screen, TEMPLE_RED, refresh_bg_rect, width=2, border_radius=6)
            news_screen.blit(refresh_text, refresh_rect)
 
        pygame.display.flip()
"""
Main.py
The main file holds menu operations for the game including sound, settings, leaderboard, tutorial, and board customization.
"""
import pygame
from SecondMenu import SecondMenu
from constants import BLUE, YELLOW, RED, GREEN
from ScoreManager import ScoreManager
from temple_news import show_temple_news

pygame.init()
pygame.mixer.init() # initialize pygame mixer for music

# set up the drawing window
Width, Height = 1000, 700 # updated size
screen = pygame.display.set_mode([Width, Height])
#title of the game for screen 
pygame.display.set_caption("Checkers+")

# Temple Brand Color
TEMPLE_RED_BRAND = (157, 34, 53)

# background music
tracks = ["music/Track1.mp3", "music/Track2.mp3", "music/Track3.mp3", "music/Track4.mp3", "music/Track5.mp3", "music/Track6.mp3", "music/Track7.mp3", "music/Track8.mp3"] 
current_track = 0
SONG_END = pygame.USEREVENT + 1
second_menu = SecondMenu(tracks)

def music_loop():
    """
    The music loop function loops through the music tracks in the tracks list.
    """
    global current_track
    pygame.mixer.music.load(tracks[current_track])
    pygame.mixer.music.set_volume(0.1) # 0.1-1.0
    pygame.mixer.music.play()
    current_track = (current_track + 1) % len(tracks)

music_loop()
pygame.mixer.music.set_endevent(SONG_END) # create event for song ending/looping

# title for display
game_title = "Checkers+"
message = "Checkers with a twist! For all ages and skill levels!"
credits1 = "Developed by Wander Cerda-Torres, Barry Lin,"
credits2 = "Nathan McCourt, Jonathan Stanczak, and Geonhee Yu"
background_image = pygame.image.load("checkers.jpg")
background_image = pygame.transform.scale(background_image, (Width, Height))  
title_font = pygame.font.Font(None, 64)
message_font = pygame.font.Font(None, 32)
credits_font = pygame.font.Font(None, 25)

# Title text
title_text = title_font.render(game_title, True, (255, 255, 255))
title_rect = title_text.get_rect(center=(Width // 2, 22))
# Under title text
message_text = message_font.render(message, True, (255, 255, 255))
message_rect = message_text.get_rect(center=(Width // 2, 55))
# Credits text
credits_text1 = credits_font.render(credits1, True, (255, 255, 255))
credits_rect1 = credits_text1.get_rect(center=(Width // 2, 650))
credits_text2 = credits_font.render(credits2, True, (255, 255, 255))
credits_rect2 = credits_text2.get_rect(center=(Width // 2, 670))

second_menu_instance = SecondMenu(tracks)

def main():
    """
    The main function handles the main menu loop and button interactions.
    """
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                buttons = menu_buttons()
                if buttons[0].collidepoint(event.pos): 
                   second_menu_instance.start_game_menu()
                elif buttons[1].collidepoint(event.pos): 
                    settings()
                elif buttons[2].collidepoint(event.pos): 
                    tutorial()
                elif buttons[3].collidepoint(event.pos): 
                    show_leaderboard()
                elif buttons[4].collidepoint(event.pos): 
                    board_customization()
                elif buttons[5].collidepoint(event.pos): # New Temple News Button
                    show_temple_news(screen, Width, Height, SONG_END, music_loop)
            elif event.type == SONG_END:
                music_loop()

        screen.blit(background_image, (0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(message_text, message_rect)
        screen.blit(credits_text1, credits_rect1)
        screen.blit(credits_text2, credits_rect2)
        
        menu_buttons()
        pygame.display.flip()

    pygame.quit()

def menu_buttons():
    """
    Creates and draws buttons on the main menu. Returns rects for hit detection.
    """
    icon_size = (45, 45)
    button_height = 50
    spacing = 10
    color = (128, 128, 128)
    cursor_color = (100, 100, 100)
    button_font = pygame.font.Font(None, 32)
    mouse = pygame.mouse.get_pos()

    # Define button positions
    start_y = Height // 3 - 25
    
    # --- 1. Start Game ---
    start_pos = (Width // 2 - 150, start_y)
    start_rect = pygame.Rect(start_pos, (300, 50))
    # --- 2. Settings ---
    settings_pos = (Width // 2 - 150, start_y + (button_height + spacing) * 1)
    settings_rect = pygame.Rect(settings_pos, (300, 50))
    # --- 3. Tutorial ---
    tutorial_pos = (Width // 2 - 150, start_y + (button_height + spacing) * 2)
    tutorial_rect = pygame.Rect(tutorial_pos, (300, 50))
    # --- 4. Leaderboard ---
    leader_pos = (Width // 2 - 150, start_y + (button_height + spacing) * 3)
    leader_rect = pygame.Rect(leader_pos, (300, 50))
    # --- 5. Customize Board ---
    board_pos = (Width // 2 - 150, start_y + (button_height + spacing) * 4)
    board_rect = pygame.Rect(board_pos, (300, 50))
    # --- 6. Temple News (NEW) ---
    news_pos = (Width // 2 - 150, start_y + (button_height + spacing) * 5)
    news_rect = pygame.Rect(news_pos, (300, 50))

    all_rects = [start_rect, settings_rect, tutorial_rect, leader_rect, board_rect, news_rect]
    labels = ["Start Game", "Settings", "Tutorial", "View Rankings", "Customize Board", "Temple News"]
    
    # Load and Draw Icons if they exist
    icon_paths = ['pics/start_icon.png', 'pics/settings_icon.png', 'pics/tutorial_icon.png', 
                  'pics/leaderboard_icon.png', 'pics/colorwheel_icon.png', 'pics/tutorial_icon.png']

    for i, rect in enumerate(all_rects):
        # Hover logic
        draw_color = cursor_color if rect.collidepoint(mouse) else color
        # News button gets special color
        if i == 5:
            draw_color = (180, 50, 65) if rect.collidepoint(mouse) else TEMPLE_RED_BRAND
            
        pygame.draw.rect(screen, draw_color, rect, border_radius=6)
        
        # Text
        txt = button_font.render(labels[i], True, (255, 255, 255))
        txt_rect = txt.get_rect(center=rect.center)
        screen.blit(txt, txt_rect)
        
        # Try to draw icons
        try:
            icon = pygame.image.load(icon_paths[i])
            icon = pygame.transform.scale(icon, (35, 35))
            screen.blit(icon, (rect.left + 10, rect.top + 7))
        except:
            pass

    return all_rects

def tutorial(): 
    # (Existing tutorial code remains unchanged)
    checkers_icon = pygame.image.load('pics/checkersguy_icon.png')
    tutorial_screen = pygame.display.set_mode([Width, Height])
    tutorial_screen.fill((128, 128, 128))
    tutorial_font = pygame.font.Font(None, 64)
    tutorial_text = tutorial_font.render("Welcome to Checkers+!", True, (255, 255, 255))
    tutorial_rect = tutorial_text.get_rect(center=(Width // 2, 50))
    tutorial_screen.blit(tutorial_text, tutorial_rect)
    # ... (skipping for brevity but keep your original code) ...
    exit_button_font = pygame.font.Font(None, 32)
    exit_button_text = exit_button_font.render("Exit Tutorial", True, (255, 255, 255))
    exit_button_rect = exit_button_text.get_rect(center=(Width // 2, Height - 50))
    pygame.draw.rect(tutorial_screen, (64, 64, 64), exit_button_rect.inflate(20, 10))
    tutorial_screen.blit(exit_button_text, exit_button_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button_rect.collidepoint(event.pos): return
            elif event.type == SONG_END: music_loop()

def settings():
    # (Existing settings code remains unchanged)
    music_playing = True
    settings_screen = pygame.display.set_mode([Width, Height])
    # ... (keep your original logic here) ...
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # ... (keep your music toggle logic) ...
                return
            elif event.type == SONG_END: music_loop()

def show_leaderboard():
    # (Keep your existing leaderboard logic)
    leaderboard_screen = pygame.display.set_mode((1000, 700))
    # ... 
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN: return
            elif event.type == SONG_END: music_loop()

def board_customization(): 
    # (Keep your existing customization logic)
    board_customization_screen = pygame.display.set_mode([Width, Height])
    # ...
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # ... check color rects ...
                return
            elif event.type == SONG_END: music_loop()

if __name__ == "__main__":
    main()
# Welcome to Checkers+!

Checkers+ is an exciting Python-based game that offers a modern twist on the classic game of checkers. Upon launching the game, users are presented with a prompt to choose between two game modes: Player vs. Player (PvP) or Player vs. AI. The game adheres to standard checkers rules with a few intriguing alterations. Checkers+ is a game for people of all ages and skill levels. This game is a continuation of code and game logic from this repository: https://github.com/techwithtim/Python-Checkers-AI. We hope you enjoy!

# Build Overview

- Use this github repository: https://github.com/cis3296f23/Project-02-checkers.git
- For the most stable release and latest changes, please refer to the main branch.
- Python is the programming language of choice for this project. For Python installation instruction please refer to this link: https://wiki.python.org/moin/BeginnersGuide/Download
- May use any IDE to assist in Python development
- Pygame will be used for this project. For Pygame installation instructions, please refer to this link: https://www.pygame.org/wiki/GettingStarted

# Build and Installation Guide (Windows)

- Download the latest release from this repository. For Windows users, inside the release should be a folder containing the Checkers+ application. After extracting the folder,
  simply run the application from inside the folder.
- If you would like to download the repository and build the application using Python tools yourself (for users who are interested in contributing or changing code):
- First, if your machine does not have Python, download the latest version of Python. This can be found here: https://www.python.org/downloads/
- Create a folder and download the most recent release in this repository. Import all files into this folder.
- Open the command prompt on your machine, and type "pip install pyinstaller". This will install PyInstaller in your Python's Scripts Folder. The Scripts folder can be found inside your Python folder.
- If you're having trouble finding this location, open your file explorer and search this PC for "pyinstaller.exe". This should allow you to open the location of pyinstaller. Copy this path.
- Inside of your created folder, open the command prompt and paste the path, followed by "\pyinstaller main.py --clean --onefile --windowed". This will create an application for Checkers+.
- Once PyInstaller is finished, your folder containing the files should now have a new folder inside titled "dist". Inside this folder is the Checkers+ application under the title "main".
- If you try running the application, you will notice there are errors that prevent you from doing so. To fix this, copy and paste the application outside of the "dist" folder, where all the files from the current release are held.
- Running the application should now work!

# Build and Installation Guide (MAC)

- Modern macOS environments often require a Virtual Environment to prevent conflicts with system-wide Python settings. Run these four commands in order inside your Project-02-checkers folder:

python3 -m venv venv
source venv/bin/activate

- (You should now see (venv) appear at the start of your terminal prompt.)
  pip install pygame
  python Main.py
- (The game should now be running)

# Brainstorming Board

- This board contains the initial features list as a path we would expect an intermediate player to take using Checkers+.
- https://lucid.app/lucidspark/128ef961-9edf-4a88-8eaf-992d7faa5d74/edit?viewport_loc=-350%2C-445%2C3025%2C1429%2C0_0&invitationId=inv_e2d583a2-18f2-4676-8253-7a01ce813867

# How to contribute

Follow this project board to know the latest status of the project: https://github.com/orgs/cis3296f23/projects/116

# Link to Documentation

Click here to view the full documentation for Checkers+: https://github.com/cis3296f23/Project-02-checkers/tree/main/html_documentation

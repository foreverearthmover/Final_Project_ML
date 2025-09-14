# Catventure - Hungry Cat Simulator 
by Lilli (https://github.com/foreverearthmover) and Maja (https://github.com/MajaPapayo)

<img width="1504" height="1064" alt="Image" src="https://github.com/user-attachments/assets/b3424071-85d2-48fb-ae7b-0cee08a73c73" />

### Description
Have you ever wondered what your cat does when you're not around?  
Find out with this game - by playing a cat who can't reach their owner even though it's time for food.  

### Quickstart
To install required dependencies/libraries:

    pip install -r requirements.txt

### Usage
To play our game, please have all files in one directory and run this from the project root in your terminal:

    python -m src.main

#### Controls
- Move: WASD or Arrow Keys
- Interact: Mouse click
- Open/Close Inventory: "E"
- Skip: Click or Enter

### Navigation

```
Final_Project_ML/
├── assets/ # Game resources
│   └── media/
│   		└── items/ # images for items
│        			├── Bow.png
│       			├── Cabinet.png
│       			├── Carton.png
│       			…
│   				└── YarnBall.png
│   		└── backgrounds/ # room backgrounds
│        			├── bathroom.png
│       			├── empty_bathroom.png
│       			├── garden.png
│   				└── living_room.png
│   		└── endings/ # ending scene images
│        			├── ending.png
│       			├── lose_ending.png
│       			├── love_ending_1.png
│       			├── love_ending_2.png
│       			├── love_ending_3.png
│   				└── win_ending.png
│   		└── sounds/ # sound effects
│   				└── cat_hiss.mp3
│   				└── shower.wav
│   		└── sprites/ # character sprites
│        			├── Asja.png
│       			├── Asja_bow.png
│       			├── Jimmy.png
│       			├── ...
│   				└── Tommy_bow.png
│   		└── text/ # fonts and text formatting preset
│       			├── 8-bit_wonder.tff
│       			├── fonts.py
│   				└── retro_gaming.tff
├── src/ # source code
│   ├── main.py # game entry point
│   ├── game.py # core game logic
│   └── scenes/ # scenes for the game
│        ├── bathroom.py
│        ├── boss_fight.py
│        ├── character_select.py
│        ├── garden.py
│        └── living_room.py
│   └── objects/ # game object classes
│        ├── boss_cat.py
│        ├── item.py
│        └── player.py
│   └── ui/ # user interface and helper file
│         ├── helper.py
│         ├── intro.py
│         └── menu.py
│
├── docs/ # documentation
│   ├── gifs/ # gifs of stages of of development
│         ├── gif_06.08.2025.gif
│         ...
│         └── gif_25.07.2025.gif
│   ├── gif_log.md # timeline of screencaps 
│   └── documentation.pdf # documentation file 
│
├── requirements.txt # dependencies
├── .gitignore
├── LICENSE
└── README.md # you are here
```
---
  
| Item                               | Description                                                              |
|------------------------------------|--------------------------------------------------------------------------|
| [assets](./assets)                 | Asset files (images, sprites, sounds, fonts, etc.) are here.             |
| [docs](./docs)                     | Documentation for our game.                                              |
| [src](./src)                       | Python code for the game is here.                                        |  
| [requirements](./requirements.txt) | All the libraries and dependencies you'll need to install are here.      |
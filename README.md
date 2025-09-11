# Catventure - Hungry Cat Simulator 
by Lilli (https://github.com/foreverearthmover) and Maja (https://github.com/MajaPapayo)

#### Description
Have you ever wondered what your cat does when you're not around?  
Find out with this game - by playing a cat who can't reach their owner even though it's time for food.  

#### Quickstart
To install required dependencies/libraries:

    pip install -r requirements.txt


#### Usage
To play our game, please have all files in one directory and run this in your terminal:

    python main.py

#### Navigation

```
Final_Project_ML/
├── assets/
│   └── media/
│   		└── items/
│        			├── Bow.png
│       			├── Cabinet.png
│       			├── Carton.png
│       			…
│   				└── YarnBall.png
│   		└── backgrounds/
│        			├── bathroom.png
│       			├── empty_bathroom.png
│       			├── garden.png
│   				└── living_room.png
│   		└── endings/
│        			├── ending.png
│       			├── lose_ending.png
│       			├── love_ending_1.png
│       			├── love_ending_2.png
│       			├── love_ending_3.png
│   				└── win_ending.png
│   		└── sounds/
│   				└── cat_hiss.mp3
│   		└── sprites/
│        			├── Asja.png
│       			├── Asja_bow.png
│       			├── Jimmy.png
│       			├── ...
│   				└── Tommy_bow.png
│   		└── text/
│       			├── 8-bit_wonder.tff
│       			├── fonts.py
│   				└── retro_gaming.tff
├── src/
│   ├── main.py
│   ├── game.py
│   └── scenes/
│        ├── bathroom.py
│        ├── boss_fight.py
│        ├── character_select.py
│        ├── garden.py
│        └── living_room.py
│   └── objects/
│        ├── boss_cat.py
│        ├── item.py
│        └── player.py
│   └── ui/
│         ├── helper.py
│         ├── intro.py
│         └── menu.py
│
├── docs/
│   ├── documentation
│   └── work_distribution
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```
---
  
| Item                               | Description                                                              |
|------------------------------------|--------------------------------------------------------------------------|
| [assets](./assets)                 | Asset files (images, sprites, sounds, fonts, etc.) are here.             |
| [docs](./docs)                     | Documentation for our game.                                              |
| [src](./src)                       | Python code for the game is here.                                        |  
| [requirements](./requirements.txt) | All the libraries and dependencies you'll need to install are here.      |
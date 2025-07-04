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

    python run main.py

#### Navigation

```
Final_Project_ML/
├── assets/
│   └── sprites/
│       ├── my_cat.png
│       ├── enemy_cat.png
│       ├── squirrel.png
│       └── items/
│           ├── yarn.png
│           ├── ribbon.png
│           ├── toilet_paper.png
│           ├── carton.png
│           ├── ...
│           └── cable.png
│   └── media/
│     └── backgrounds/
│        ├── living_room.png
│        ├── bathroom.png
│        └── garden.png
├── src/
│   ├── main.py
│   ├── game.py
│   └── scenes/
│        ├── living_room.py
│        ├── bathroom.py
│        └── garden.py
│   └── objects/
│        ├── player.py
│        ├── item.py
│        └── cat_enemy.py
│   └── ui/
│         ├── inventory.py
│         └── fight.py
│
├── docs/
│   ├── documentation
│   └── work_distribution
│
├── requirements.txt
├── .gitignore
└── README.md
```
---
  
| Item                               | Description                                                                       |
|------------------------------------|-----------------------------------------------------------------------------------|
| [assets](./assets)                 | Asset files (images, animation sprites, sounds, etc.) are here.                   |
| [docs](./docs)                     | Documentation for our game.                                                       |
| [src](./src)                       | Python code for the game is here.                                                 |  
| [requirements](./requirements.txt) | All the libraries and dependencies you'll need to install are here. (coming soon) |
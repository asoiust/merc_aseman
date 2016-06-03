tags = ['Action', 'Indie', '', 'Casual', 'Simulation', 'Strategy', 'Stealth', 'Retro', 'Classic', 'Funny',
                    'Difficult', 'Pixel Graphics', 'Adventure', 'Point & Click', 'Singleplayer', 'Silent Protagonist',
                    'Atmospheric', 'Horror', 'Psychological Horror', 'Memes', 'Crime', 'Early Access', 'Multiplayer',
                    'FPS', 'Shooter', 'Free to Play', 'Open World', 'First-Person', 'Co-op', 'Physics', 'Online Co-Op',
                    'VR', 'Sports', 'Pool', 'Local Multiplayer', 'Anime', 'Female Protagonist', "Beat 'em up", 'Nudity',
                    'Hack and Slash', 'Ninja', 'Cute', 'Arcade', 'Rogue-lite', "Shoot 'Em Up", 'Top-Down Shooter',
                    'Perma Death', 'Twin Stick Shooter', 'Procedural Generation', 'Rogue-like', 'Destruction',
                    'Action RPG', 'RPG', 'Space', '2D', 'Sci-fi', 'Crafting', 'Top-Down', 'Visual Novel', 'Mystery',
                    'Short', 'Exploration', 'Great Soundtrack', 'Story Rich', 'Interactive Fiction', 'Arena Shooter',
                    'Mechs', 'Third-Person Shooter', 'Time Manipulation', 'Puzzle', 'Platformer', 'Side Scroller',
                    'Colorful', '2.5D', 'Family Friendly', 'Hand-drawn', 'Puzzle-Platformer', 'Music', 'Cartoon',
                    'Racing', 'Hidden Object', 'Dungeon Crawler', 'Fantasy', 'Fast-Paced', 'Tower Defense', 'Steampunk',
                    'Walking Simulator', 'Survival', 'Card Game', 'Turn-Based', 'Turn-Based Strategy', 'Trains',
                    'Cartoony', 'Comedy', 'Dark Humor', '4X', 'Wargame', 'Grand Strategy', 'Massively Multiplayer',
                    'PvP', 'PvE', 'Post-apocalyptic', 'Clicker', 'Relaxing', 'Level Editor', 'Multiple Endings', 'Dark',
                    'Music-Based Procedural Generation', 'Local Co-Op', 'RPGMaker', 'RTS', 'Survival Horror', 'Robots',
                    'Building', 'Politics', 'Trading Card Game', 'Horses', 'Bullet Hell', 'Management', 'Flight',
                    'Realistic', 'Software Training', 'Controller', 'Sandbox', 'TrackIR', 'Military',
                    'Spectacle fighter', 'Character Action Game', 'Comic Book', 'Real Time Tactics', 'Isometric',
                    'Games Workshop', 'War', 'Dark Fantasy', 'Tactical', 'Gore', 'Warhammer 40K', 'Otome', 'Romance',
                    'Time Travel', 'Noir', 'Action-Adventure', 'Score Attack', 'Rhythm', 'Runner', 'Zombies', 'Violent',
                    'Remake', 'Economy', 'Replay Value', 'Medieval', 'Choose Your Own Adventure', 'Dating Sim',
                    'Fighting', '2D Fighter', 'Parody ', 'Satire', 'Based On A Novel', 'Dinosaurs', 'Science',
                    'Underwater', 'Education', 'Historical', '4 Player Local', 'City Builder', 'Metroidvania',
                    'God Game', 'Crowdfunded', 'Character Customization', 'Illuminati', 'Space Sim', 'Gothic',
                    'Resource Management', 'Stylized', 'Real-Time', 'Turn-Based Tactics', 'MOBA', '1980s', 'Driving',
                    'Turn-Based Combat', 'Asynchronous Multiplayer', 'Party-Based RPG', 'Choices Matter', 'Detective',
                    'Pirates', 'Swordplay', 'Hacking', 'Software', 'Futuristic', 'Surreal', 'Alternate History',
                    'Cyberpunk', 'Animation & Modeling', 'Cinematic', 'Abstract', 'Experimental', 'Golf', 'Narration',
                    'Aliens', 'e-sports', 'Football', 'Loot', 'Agriculture', 'Magic', 'Competitive', 'World War II',
                    'Strategy RPG', 'Mystery Dungeon', 'Moddable', 'Touch-Friendly', 'Inventory Management',
                    'Lore-Rich', 'Blood', 'Trading', 'Mars', 'Base-Building', 'Dystopian ', 'Utilities', 'Board Game',
                    'Third Person', 'JRPG', 'Design & Illustration', 'Demons', 'Psychological', 'Movie', 'Voxel',
                    'Match 3', 'Co-op Campaign', 'Tactical RPG', 'Supernatural', 'Psychedelic', 'MMORPG', 'Parkour',
                    'On-Rails Shooter', 'Fishing', 'Cult Classic', 'Linear', 'Tanks', 'Typing', 'Naval', 'Drama',
                    '3D Platformer', 'Dark Comedy', 'Mini Golf', 'Dragons', 'Chess', 'Soccer', 'Grid-Based Movement',
                    'Kickstarter', 'Minimalist', 'Programming', 'Star Wars', 'Lovecraftian', 'Time Attack',
                    'Split Screen', 'Capitalism', 'Real-Time with Pause', "1990's", 'Mature', 'Mouse only', 'Western',
                    'Hex Grid', 'Offroad', 'Steam Machine', 'Sailing', 'Lemmings', '3D Vision', 'GameMaker', '6DOF',
                    'Mythology', 'Heist', 'Superhero', 'Villain Protagonist', 'CRPG', 'Episodic', 'Thriller',
                    'Game Development', 'Assassin', 'Hunting', 'Modern', 'Political', 'Cold War', 'World War I',
                    'America', 'Rome', 'Mining', 'Pinball', 'Conspiracy', 'Dynamic Narration', 'FMV',
                    'Audio Production', 'Transhumanism', 'Class-Based', 'Bullet Time', 'Spelling', 'Word Game',
                    'Martial Arts', 'Team-Based', 'Soundtrack', 'Werewolves', 'Sokoban', 'Quick-Time Events',
                    'Philisophical', 'LEGO', 'Batman', 'Mod', 'Documentary', 'Vampire', 'Basketball', 'Sniper',
                    'Lara Croft', 'Diplomacy', 'Gun Customization', 'Bowling', 'Gambling', 'Benchmark', 'Underground']
genre = ['Action', 'Indie', '0', 'Casual', 'Strategy', 'Adventure', 'Simulation', 'EarlyAccess', 'Sports',
                     'RPG', 'FreetoPlay', 'Racing', 'MassivelyMultiplayer']


def check(tup, st):
    if st == 'tg':
        res = [0 for i in tags]
        for item in tup:
            for ke in range(len(tags)):
                if tags[ke] in item[0]:
                    res[ke] += 1
        return res
    if st == 'ge':
        res = [0 for i in genre]
        for item in tup:
            for ke in range(len(genre)):
                if genre[ke] in item[0]:
                    res[ke] += 1
        return res
# Code Shift
A game named Code Shift fom the 3eM-DJ team for the Ostrava CodeJam 10/2025

# About
a game where you code your way through the levels

# How to run
1. open the `dist/` folder
2. run `game.exe`

or run _this_ in shell
```shell
./dist/game.exe
```

# Controls
`ESC` - exit game

`TAB` - switch between gamemodes

### --platformer mode--
`wasd & arrow keys` - movement

`space` - jump

### --dev mode--
`wasd` - movement

`space` - auto select block (depending on direction)

`arrow keys` - specific block selection

# SOURCE BUILD
**NOTE:** this is only for development and if you'd like to run the project yourself

## Setup
1. create a virtual enviroment
```shell
python -m venv .venv
```

2. activate it
```shell
# Linux, Bash
$ source .venv/bin/activate
# Linux, Fish
$ source .venv/bin/activate.fish
# Linux, Csh
$ source .venv/bin/activate.csh
# Linux, PowerShell Core
$ .venv/bin/Activate.ps1
# Windows, cmd.exe
> .venv\Scripts\activate.bat
# Windows, PowerShell
> .venv\Scripts\Activate.ps1
```

_At this point you might run into some issues, if you do please run `cd .` to refresh the console location_


3. Update pip if you haven't
```shell
python.exe -m pip install --upgrade pip
```

4. Install all required packages
```
pip install -r requirements.txt
```

5. Once you're done and you want to exit everything (close even the project)
```shell
deactivate
```

## Running the project
```shell
python src/main.py
```

### Pyinstaller build
This step is not necessary at all<br>
_note: needs to have pyinstaler installed_
```shell
pyinstaller src/main.py --add-data "Textures;Textures" --add-data "Music;Music" --add-data "Levels;Levels"
```

**If you run into any issues, please make sure to report them.**

# Contributors
- https://github.com/Miras3210
- https://github.com/alvareez
- https://github.com/LeoNex28
- https://github.com/E422Real
- https://github.com/DejvDajo

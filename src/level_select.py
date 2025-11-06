import pygame
# from pathlib import Path
from location_helper import project_root

root_dir = project_root()
levels_dir = root_dir / "Levels"
ticker = 0

current_level: int
level_count: int
level_nums: list[int]
unlocked_levels: int = 1

def save_config():
    with open(root_dir / "player.cnf", "wt") as f:
        f.write(f"unlocked={unlocked_levels}")

def initialize(width:int=0, height:int=0) -> None:
    global level_count, level_nums
    if not (root_dir / "player.cnf").exists(): save_config()

    files = [file for file in levels_dir.glob("level*.grid")]
    level_nums = sorted([int(file.name[5:-5]) for file in files])
    level_count = len(level_nums)

def update(key: int) -> str:
    return ""

def draw(window: pygame.Surface) -> None:
    window.fill((0,0,0))

initialize(0,0)
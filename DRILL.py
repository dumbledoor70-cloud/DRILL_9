from dataclasses import dataclass, field
from typing import NamedTuple

from pico2d import clear_canvas, close_canvas, load_image, open_canvas, update_canvas


CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024
BACKGROUND_PATH = "TUK_GROUND.png"
SPRITE_SHEET_PATH = "animation_sheet.png"
SPRITE_SHEET_WIDTH = 802
SPRITE_SHEET_HEIGHT = 402
FRAME_WIDTH = 100
FRAME_HEIGHT = 100
FRAME_COLUMNS = 8
ANIMATION_ROWS = 4
ROW_IDLE_RIGHT = 0
ROW_IDLE_LEFT = 1
ROW_MOVE_RIGHT = 2
ROW_MOVE_LEFT = 3
FRAME_INTERVAL_SECONDS = 0.05
MOVEMENT_SPEED = 100.0
SPRITE_SCALE = 1.0
CENTER_X = CANVAS_WIDTH // 2
CENTER_Y = CANVAS_HEIGHT // 2


class FrameRect(NamedTuple):
    x: int
    y: int
    width: int
    height: int

    def to_pico2d(self, sheet_height):
        return self.x, sheet_height - self.y - self.height, self.width, self.height


def grid_frame_rect(row, column):
    if not 0 <= row < ANIMATION_ROWS:
        raise IndexError("Animation row is outside the sprite sheet")
    if not 0 <= column < FRAME_COLUMNS:
        raise IndexError("Frame column is outside the sprite sheet")
    return FrameRect(
        column * FRAME_WIDTH,
        row * FRAME_HEIGHT,
        FRAME_WIDTH,
        FRAME_HEIGHT,
    )


@dataclass
class CharacterState:
    x: float = CANVAS_WIDTH / 2
    y: float = CANVAS_HEIGHT / 2
    facing_right: bool = True
    pressed_keys: set = field(default_factory=set)
    frame_index: int = 0
    current_row: int = ROW_IDLE_RIGHT
    next_frame_time: float = 0.0


IDLE_RIGHT_FRAMES = tuple(
    grid_frame_rect(ROW_IDLE_RIGHT, column)
    for column in range(FRAME_COLUMNS)
)


def draw_background(background):
    clear_canvas()
    background.draw(CENTER_X, CENTER_Y)
    update_canvas()


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        background = load_image(BACKGROUND_PATH)
        sprite_sheet = load_image(SPRITE_SHEET_PATH)
        draw_background(background)
    finally:
        background = None
        sprite_sheet = None
        close_canvas()


if __name__ == "__main__":
    main()
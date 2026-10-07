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
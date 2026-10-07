from pico2d import close_canvas, open_canvas


CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024


def main():
    open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        pass
    finally:
        close_canvas()


if __name__ == "__main__":
    main()
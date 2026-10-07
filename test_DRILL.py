import unittest
from unittest.mock import patch

import DRILL


class DrillStartupTests(unittest.TestCase):
    def test_canvas_size_matches_background(self):
        self.assertEqual((DRILL.CANVAS_WIDTH, DRILL.CANVAS_HEIGHT), (1280, 1024))

    def test_main_closes_canvas_after_startup(self):
        with (
            patch.object(DRILL, "open_canvas") as open_canvas,
            patch.object(DRILL, "close_canvas") as close_canvas,
        ):
            DRILL.main()

        open_canvas.assert_called_once_with(1280, 1024)
        close_canvas.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
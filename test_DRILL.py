import unittest
from unittest.mock import patch

import DRILL


class DrillStartupTests(unittest.TestCase):
    def test_canvas_size_matches_background(self):
        self.assertEqual((DRILL.CANVAS_WIDTH, DRILL.CANVAS_HEIGHT), (1280, 1024))

    def test_sprite_and_timing_settings_match_assets_and_spec(self):
        self.assertEqual(DRILL.BACKGROUND_PATH, "TUK_GROUND.png")
        self.assertEqual(DRILL.SPRITE_SHEET_PATH, "animation_sheet.png")
        self.assertEqual((DRILL.SPRITE_SHEET_WIDTH, DRILL.SPRITE_SHEET_HEIGHT), (802, 402))
        self.assertEqual((DRILL.FRAME_COLUMNS, DRILL.ANIMATION_ROWS), (8, 4))
        self.assertEqual(DRILL.FRAME_INTERVAL_SECONDS, 0.05)
        self.assertEqual(DRILL.MOVEMENT_SPEED, 100.0)

    def test_main_closes_canvas_after_startup(self):
        with (
            patch.object(DRILL, "open_canvas") as open_canvas,
            patch.object(DRILL, "load_image", return_value=object()) as load_image,
            patch.object(DRILL, "close_canvas") as close_canvas,
        ):
            DRILL.main()

        open_canvas.assert_called_once_with(1280, 1024)
        self.assertEqual(
            [call.args[0] for call in load_image.call_args_list],
            ["TUK_GROUND.png", "animation_sheet.png"],
        )
        close_canvas.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
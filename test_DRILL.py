import unittest
from types import SimpleNamespace
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

    def test_frame_rect_converts_top_origin_to_pico2d_coordinates(self):
        frame = DRILL.FrameRect(10, 20, 30, 40)

        self.assertEqual(frame.to_pico2d(402), (10, 342, 30, 40))

    def test_grid_has_eight_columns_and_four_in_bounds_rows(self):
        self.assertEqual(
            (DRILL.FRAME_COLUMNS, DRILL.ANIMATION_ROWS),
            (8, 4),
        )
        for row in range(DRILL.ANIMATION_ROWS):
            for column in range(DRILL.FRAME_COLUMNS):
                frame = DRILL.grid_frame_rect(row, column)
                self.assertLessEqual(frame.x + frame.width, DRILL.SPRITE_SHEET_WIDTH)
                self.assertLessEqual(frame.y + frame.height, DRILL.SPRITE_SHEET_HEIGHT)
        with self.assertRaises(IndexError):
            DRILL.grid_frame_rect(4, 0)
        with self.assertRaises(IndexError):
            DRILL.grid_frame_rect(0, 8)

    def test_character_state_starts_centered_facing_right_and_idle(self):
        state = DRILL.CharacterState()

        self.assertEqual((state.x, state.y), (640, 512))
        self.assertTrue(state.facing_right)
        self.assertEqual(state.pressed_keys, set())
        self.assertEqual(state.frame_index, 0)
        self.assertEqual(state.current_row, DRILL.ROW_IDLE_RIGHT)

    def test_right_idle_animation_has_eight_ordered_frames(self):
        self.assertEqual(len(DRILL.IDLE_RIGHT_FRAMES), 8)
        self.assertEqual(DRILL.IDLE_RIGHT_FRAMES[0], DRILL.FrameRect(0, 0, 100, 100))
        self.assertEqual(DRILL.IDLE_RIGHT_FRAMES[-1], DRILL.FrameRect(700, 0, 100, 100))

    def test_left_idle_animation_uses_second_sprite_row(self):
        self.assertEqual(len(DRILL.IDLE_LEFT_FRAMES), 8)
        self.assertEqual(DRILL.IDLE_LEFT_FRAMES[0], DRILL.FrameRect(0, 100, 100, 100))
        self.assertEqual(DRILL.IDLE_LEFT_FRAMES[-1], DRILL.FrameRect(700, 100, 100, 100))

    def test_right_move_animation_uses_third_sprite_row(self):
        self.assertEqual(len(DRILL.MOVE_RIGHT_FRAMES), 8)
        self.assertEqual(DRILL.MOVE_RIGHT_FRAMES[0], DRILL.FrameRect(0, 200, 100, 100))
        self.assertEqual(DRILL.MOVE_RIGHT_FRAMES[-1], DRILL.FrameRect(700, 200, 100, 100))

    def test_left_move_animation_uses_fourth_sprite_row(self):
        self.assertEqual(len(DRILL.MOVE_LEFT_FRAMES), 8)
        self.assertEqual(DRILL.MOVE_LEFT_FRAMES[0], DRILL.FrameRect(0, 300, 100, 100))
        self.assertEqual(DRILL.MOVE_LEFT_FRAMES[-1], DRILL.FrameRect(700, 300, 100, 100))

    def test_animation_row_selection_covers_idle_and_move_facings(self):
        self.assertEqual(DRILL.select_animation_row(False, True), DRILL.ROW_IDLE_RIGHT)
        self.assertEqual(DRILL.select_animation_row(False, False), DRILL.ROW_IDLE_LEFT)
        self.assertEqual(DRILL.select_animation_row(True, True), DRILL.ROW_MOVE_RIGHT)
        self.assertEqual(DRILL.select_animation_row(True, False), DRILL.ROW_MOVE_LEFT)

    def test_animation_advance_uses_elapsed_frame_intervals(self):
        state = DRILL.CharacterState()

        self.assertEqual(DRILL.update_animation(state, False, 1.0), DRILL.FrameRect(0, 0, 100, 100))
        self.assertEqual(DRILL.update_animation(state, False, 1.049), DRILL.FrameRect(0, 0, 100, 100))
        self.assertEqual(DRILL.update_animation(state, False, 1.05), DRILL.FrameRect(100, 0, 100, 100))
        self.assertEqual(DRILL.update_animation(state, True, 1.06), DRILL.FrameRect(0, 200, 100, 100))
        self.assertEqual(state.frame_index, 0)

    def test_keydown_keyup_updates_pressed_keys_and_facing(self):
        state = DRILL.CharacterState()

        DRILL.handle_key_event(state, SimpleNamespace(type=DRILL.SDL_KEYDOWN, key=DRILL.SDLK_LEFT))
        self.assertIn(DRILL.SDLK_LEFT, state.pressed_keys)
        self.assertFalse(state.facing_right)

        DRILL.handle_key_event(state, SimpleNamespace(type=DRILL.SDL_KEYUP, key=DRILL.SDLK_LEFT))
        self.assertNotIn(DRILL.SDLK_LEFT, state.pressed_keys)

        DRILL.handle_key_event(state, SimpleNamespace(type=DRILL.SDL_KEYDOWN, key=DRILL.SDLK_RIGHT))
        self.assertTrue(state.facing_right)

    def test_escape_and_window_close_request_shutdown(self):
        for event in (
            SimpleNamespace(type=DRILL.SDL_KEYDOWN, key=DRILL.SDLK_ESCAPE),
            SimpleNamespace(type=DRILL.SDL_QUIT),
        ):
            with self.subTest(event=event):
                state = DRILL.CharacterState()
                DRILL.handle_key_event(state, event)
                self.assertFalse(state.running)

    def test_movement_vector_supports_diagonal_and_opposing_keys_cancel(self):
        state = DRILL.CharacterState()
        state.pressed_keys.update((DRILL.SDLK_RIGHT, DRILL.SDLK_UP))
        x_direction, y_direction = DRILL.get_movement_vector(state)
        self.assertAlmostEqual(x_direction, 2 ** -0.5)
        self.assertAlmostEqual(y_direction, 2 ** -0.5)
        self.assertAlmostEqual((x_direction**2 + y_direction**2) ** 0.5, 1.0)

        state.pressed_keys.update((DRILL.SDLK_LEFT, DRILL.SDLK_DOWN))
        self.assertEqual(DRILL.get_movement_vector(state), (0.0, 0.0))

    def test_main_closes_canvas_after_startup(self):
        class FakeBackground:
            def __init__(self):
                self.draw_calls = []

            def draw(self, x, y):
                self.draw_calls.append((x, y))

        background = FakeBackground()
        loaded_images = iter([background, object()])
        with (
            patch.object(DRILL, "open_canvas") as open_canvas,
            patch.object(DRILL, "load_image", side_effect=lambda _path: next(loaded_images)) as load_image,
            patch.object(DRILL, "clear_canvas"),
            patch.object(DRILL, "update_canvas"),
            patch.object(DRILL, "close_canvas") as close_canvas,
        ):
            DRILL.main()

        open_canvas.assert_called_once_with(1280, 1024)
        self.assertEqual(
            [call.args[0] for call in load_image.call_args_list],
            ["TUK_GROUND.png", "animation_sheet.png"],
        )
        self.assertEqual(background.draw_calls, [(640, 512)])
        close_canvas.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
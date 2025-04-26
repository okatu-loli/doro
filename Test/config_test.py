import unittest

from src.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_default_values(self):
        """Test default values in the config"
        This test only check the default values of the config file.
        """
        self.assertEqual(self.config.window_width, 200)
        self.assertEqual(self.config.window_height, 200)
        self.assertEqual(self.config.animation_fps, 30)
        self.assertTrue(self.config.show_info)
        self.assertEqual(self.config.current_theme, "粉色主题")
        self.assertTrue(self.config.allow_random_movement is True)

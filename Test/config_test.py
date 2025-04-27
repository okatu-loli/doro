import unittest

from src.config import Config
import os


class TestConfig(unittest.TestCase):
    def setUp(self):
        # reset config file
        config_path = "resources/config/config.json"
        if os.path.exists(config_path):
            os.remove(config_path)
        self.config: Config = Config()

    def test_default_values(self):
        """Test default values in the config
        This test only check the default values of the config file.
        """
        self.assertEqual(self.config.config["WINDOW"]["WINDOW_WIDTH"], 200)
        self.assertEqual(self.config.config["WINDOW"]["WINDOW_HEIGHT"], 200)
        self.assertEqual(self.config.config["ANIMATION"]["ANIMATION_FPS"], 30)
        self.assertTrue(self.config.config["INFO"]["SHOW_INFO"] is True)
        self.assertEqual(self.config.config["THEME"]["DEFAULT_THEME"], "粉色主题")
        self.assertTrue(
            self.config.config["WORKSPACE"]["ALLOW_RANDOM_MOVEMENT"] is True
        )

    def test_modify_config(self):
        """Test modify config"""
        self.config.config["WINDOW"]["WINDOW_WIDTH"] = 300
        self.config.config["WINDOW"]["WINDOW_HEIGHT"] = 300
        self.config.save()
        new_config = Config()
        self.assertEqual(new_config.config["WINDOW"]["WINDOW_WIDTH"], 300)
        self.assertEqual(new_config.config["WINDOW"]["WINDOW_HEIGHT"], 300)

    def tearDown(self) -> None:
        # delete config file
        config_path = "resources/config/config.json"
        if os.path.exists(config_path):
            os.remove(config_path)

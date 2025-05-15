import os
import sys
import unittest

from src.MainLayer import MainLayer
from src.config import Config

from PySide6.QtWidgets import QApplication

app = QApplication.instance() or QApplication(sys.argv)


class TestConfig(unittest.TestCase):
    def setUp(self):
        # reset config file
        self.main_layer = MainLayer()
        config_path = "resources/config/config.json"
        if os.path.exists(config_path):
            os.remove(config_path)
        self.config: Config = Config(self.main_layer)

    def test_default_values(self):
        """Test default values in the config
        This test only check the default values of the config file.
        """
        self.assertEqual(self.config.config["Window"]["Width"], 200)
        self.assertEqual(self.config.config["Window"]["Height"], 200)
        self.assertEqual(self.config.config["Animation"]["FPS"], 30)
        self.assertTrue(self.config.config["Info"]["ShowInfo"] is True)
        self.assertEqual(self.config.config["Theme"]["DefaultTheme"], "粉色主题")
        self.assertTrue(self.config.config["Workspace"]["AllowRandomMovement"] is True)

    def test_modify_config(self):
        """Test modify config"""
        self.config.config["Window"]["Width"] = 300
        self.config.config["Window"]["Height"] = 300
        self.config.save()
        new_config = Config(self.main_layer)
        self.assertEqual(new_config.config["Window"]["Width"], 300)
        self.assertEqual(new_config.config["Window"]["Height"], 300)

    def tearDown(self) -> None:
        # delete config file
        config_path = "resources/config/config.json"
        if os.path.exists(config_path):
            os.remove(config_path)


if __name__ == "__main__":
    unittest.main()

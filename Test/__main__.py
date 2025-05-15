import unittest

suite = unittest.TestSuite()

suite.addTest(
    unittest.defaultTestLoader.discover(start_dir="Test", pattern="test_*.py")
)

runner = unittest.TextTestRunner()

runner.run(suite)

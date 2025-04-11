import unittest
from app.main import get_timezone_from_city

class TestTimezoneFinder(unittest.TestCase):
    def test_valid_city(self):
        tz = get_timezone_from_city("New York")
        self.assertEqual(tz, "America/New_York")

    def test_invalid_city(self):
        tz = get_timezone_from_city("ThisCityDoesNotExist")
        self.assertIsNone(tz)

if __name__ == '__main__':
    unittest.main()

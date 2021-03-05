from parameterized import parameterized

from django.test import TestCase

from quasar_fire_app.domain.get_message import get_message
from quasar_fire_app.utils.math import is_close

class TestCaseIsClose(TestCase):

    @parameterized.expand([
        (10, 20),
        (100, 200),
        (50, 0),
        (100.55, 100.60),
    ])
    def test_should_return_false_for_numbers_with_great_difference(self, number1, number2):
        """Test that is_close returns False when the numbers to evaluate
        differ by more than quasar_fire_app.utils.math.APPROXIMATION_CONSTANT.
        """
        
        result = is_close(number1, number2)

        assert result is False

    @parameterized.expand([
        (100.0001, 100.00011),
        (10.00000006, 10.00000007),
    ])
    def test_should_return_true_for_numbers_with_very_little_difference(self, number1, number2):
        """Test that is_close returns True when the numbers to evaluate
        differ by less than quasar_fire_app.utils.math.APPROXIMATION_CONSTANT.
        """
        
        result = is_close(number1, number2)

        assert result is True

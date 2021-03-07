from django.test import TestCase

from quasar_fire_app.domain.satellite import get_all_satellites_info
from quasar_fire_app.models.satellite import Satellite


class TestCaseGetAllSatelitesInfo(TestCase):

    def test_should_retrieve_all_satellites_from_db(self):
        """Test that get_all_satellites_info retrieves all the satellites from the DB."""        
        expected_result = Satellite.objects.all()

        result = get_all_satellites_info()

        assert len(result) == len(expected_result)
        for i in range(len(result)):
            assert result[i] == expected_result[i]

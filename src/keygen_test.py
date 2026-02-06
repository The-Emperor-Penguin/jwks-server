import unittest
from datetime import UTC, datetime

from keygen import create_key_pair


class TestKeyGen(unittest.TestCase):
    def test_kid(self):
        assert (create_key_pair(datetime(2029,10,10,5,5, tzinfo=UTC))["kid"] !=
                create_key_pair(datetime(2029,10,10,5,5, tzinfo=UTC))["kid"])

    def test_experation_creation(self):
        try:
            create_key_pair(datetime(2000,1,1, tzinfo=UTC))
        except OSError:
            create_key_pair(datetime(3000,1,1, tzinfo=UTC))
        else:
            raise AssertionError

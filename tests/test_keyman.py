import os
import sys
import time
import unittest
from datetime import datetime, timedelta, UTC


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import keyman


class KeyManagerTests(unittest.TestCase):
    def setUp(self):
        self.manager = keyman.KeyManager()
        self.manager.keys.clear()

    def test_create_key_rejects_past_expiration_without_debug(self):
        past = datetime.now(UTC) - timedelta(minutes=1)
        with self.assertRaises(IOError):
            self.manager.create_key(past)

    def test_create_key_allows_past_with_debug(self):
        past = datetime.now(UTC) - timedelta(minutes=1)
        self.manager.create_key(past, debug=True)
        self.assertEqual(len(self.manager.keys), 1)

    def test_all_valid_keys_filters_expired(self):
        now = datetime.now(UTC)
        self.manager.create_key(now + timedelta(minutes=5))
        self.manager.create_key(now - timedelta(minutes=5), debug=True)

        valid_keys = self.manager.all_valid_keys()
        self.assertEqual(len(valid_keys), 1)
        self.assertGreater(valid_keys[0]["exp"], now)

    def test_newest_valid_key_picks_latest(self):
        now = datetime.now(UTC)
        self.manager.create_key(now + timedelta(minutes=5))
        time.sleep(0.01)
        self.manager.create_key(now + timedelta(minutes=10))

        newest = self.manager.newest_valid_key()
        self.assertEqual(newest, self.manager.keys[-1])

    def test_newest_expired_key_picks_latest(self):
        now = datetime.now(UTC)
        self.manager.create_key(now - timedelta(minutes=10), debug=True)
        time.sleep(0.01)
        self.manager.create_key(now - timedelta(minutes=5), debug=True)

        newest = self.manager.newest_expired_key()
        self.assertEqual(newest, self.manager.keys[-1])

    def test_newest_valid_key_returns_empty_when_none(self):
        now = datetime.now(UTC)
        self.manager.create_key(now - timedelta(minutes=5), debug=True)

        newest = self.manager.newest_valid_key()
        self.assertEqual(newest, {})

    def test_newest_expired_key_returns_empty_when_none(self):
        now = datetime.now(UTC)
        self.manager.create_key(now + timedelta(minutes=5))

        newest = self.manager.newest_expired_key()
        self.assertEqual(newest, {})


if __name__ == "__main__":
    unittest.main()

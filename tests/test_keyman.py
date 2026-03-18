import os
import sqlite3
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
        os.environ["DATABASENAME"] = os.path.join(ROOT_DIR, "test_keyman.db")
        self.manager = keyman.KeyManager()
        with sqlite3.connect(self.manager.databasepath) as conn:
            conn.execute("DELETE FROM keys")
            conn.commit()

    def test_create_key_rejects_past_expiration_without_debug(self):
        past = datetime.now(UTC) - timedelta(minutes=1)
        with self.assertRaises(IOError):
            self.manager.create_key(past)

    def test_create_key_allows_past_with_debug(self):
        past = datetime.now(UTC) - timedelta(minutes=1)
        self.manager.create_key(past, debug=True)
        with sqlite3.connect(self.manager.databasepath) as conn:
            count = conn.execute("SELECT COUNT(*) FROM keys").fetchone()[0]
        self.assertEqual(count, 1)

    def test_all_valid_keys_filters_expired(self):
        now = datetime.now(UTC)
        self.manager.create_key(now + timedelta(minutes=5))
        self.manager.create_key(now - timedelta(minutes=5), debug=True)

        valid_keys = self.manager.all_valid_keys()
        self.assertEqual(len(valid_keys), 1)
        self.assertGreater(valid_keys[0][2], int(now.timestamp()))

    def test_valid_key_picks_latest(self):
        now = datetime.now(UTC)
        self.manager.create_key(now + timedelta(minutes=5))
        time.sleep(0.01)
        self.manager.create_key(now + timedelta(minutes=10))

        expected_latest = self.manager.all_valid_keys()[0]
        newest = self.manager.valid_key()
        self.assertEqual(newest, expected_latest)

    def test_expired_key_picks_latest(self):
        now = datetime.now(UTC)
        self.manager.create_key(now - timedelta(minutes=10), debug=True)
        time.sleep(0.01)
        self.manager.create_key(now - timedelta(minutes=5), debug=True)

        newest = self.manager.expired_key()
        self.assertEqual(newest[2], int((now - timedelta(minutes=5)).timestamp()))

    def test_valid_key_returns_empty_when_none(self):
        now = datetime.now(UTC)
        self.manager.create_key(now - timedelta(minutes=5), debug=True)

        newest = self.manager.valid_key()
        self.assertEqual(newest, {})

    def test_expired_key_returns_empty_when_none(self):
        now = datetime.now(UTC)
        self.manager.create_key(now + timedelta(minutes=5))

        newest = self.manager.expired_key()
        self.assertEqual(newest, {})


if __name__ == "__main__":
    unittest.main()

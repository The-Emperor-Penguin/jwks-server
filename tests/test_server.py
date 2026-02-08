import os
import sys
import unittest
from datetime import datetime, timedelta, UTC

import jwt


ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

import server  # noqa: E402


class ServerTests(unittest.TestCase):
    def setUp(self):
        server.key_manager.keys.clear()
        now = datetime.now(UTC)
        server.key_manager.create_key(now + timedelta(hours=1))
        server.key_manager.create_key(now - timedelta(hours=1), debug=True)
        self.client = server.app.test_client()

    def test_auth_default_uses_valid_key(self):
        response = self.client.post("/auth")
        self.assertEqual(response.status_code, 200)
        token = response.json["token"]

        payload = jwt.decode(
            token,
            options={"verify_signature": False, "verify_exp": False},
        )
        exp = payload["exp"]
        exp_ts = exp if isinstance(exp, (int, float)) else int(exp.timestamp())
        self.assertGreater(exp_ts, int(datetime.now(UTC).timestamp()))

        header = jwt.get_unverified_header(token)
        valid_kids = {k["jwk"]["kid"] for k in server.key_manager.all_valid_keys()}
        self.assertIn(header["kid"], valid_kids)

    def test_auth_expired_true_uses_expired_key(self):
        response = self.client.post("/auth?expired=true")
        self.assertEqual(response.status_code, 200)
        token = response.json["token"]

        payload = jwt.decode(
            token,
            options={"verify_signature": False, "verify_exp": False},
        )
        exp = payload["exp"]
        exp_ts = exp if isinstance(exp, (int, float)) else int(exp.timestamp())
        self.assertLess(exp_ts, int(datetime.now(UTC).timestamp()))

        header = jwt.get_unverified_header(token)
        expired_kid = server.key_manager.newest_expired_key()["jwk"]["kid"]
        self.assertEqual(header["kid"], expired_kid)

        jwks = self.client.get("/.well-known/jwks.json").json["keys"]
        jwks_kids = {k["kid"] for k in jwks}
        self.assertNotIn(expired_kid, jwks_kids)

    def test_jwks_only_valid_keys(self):
        response = self.client.get("/.well-known/jwks.json")
        self.assertEqual(response.status_code, 200)
        keys = response.json["keys"]

        expected_kids = {k["jwk"]["kid"] for k in server.key_manager.all_valid_keys()}
        actual_kids = {k["kid"] for k in keys}
        self.assertSetEqual(actual_kids, expected_kids)


if __name__ == "__main__":
    unittest.main()

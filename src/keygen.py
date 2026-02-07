import datetime
import uuid
import base64
from cryptography.hazmat.primitives.asymmetric import rsa


def create_key_pair():
    """The Experation date must be in UTC or will be converted to UTC
    """

    EXPONENT = 65537

    private_key = rsa.generate_private_key(
        public_exponent=EXPONENT,
        key_size=2048,
    )

    public_key = private_key.public_key()


    numbers = public_key.public_numbers()
    exponent = numbers.e
    mod = numbers.n

    kid = uuid.uuid4()

    def _int_to_base64url(value: int) -> str:
        byte_len = (value.bit_length() + 7) // 8 or 1
        raw = value.to_bytes(byte_len, "big")
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    jkw = {
        "kty": "RSA",
        "kid": str(kid),
        "alg": "RS256",
        "use": "sig",
        "e": _int_to_base64url(exponent),
        "n": _int_to_base64url(mod),
    }

    return (private_key, public_key, jkw)



if __name__ == "__main__":
    create_key_pair()

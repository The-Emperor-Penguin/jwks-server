import datetime
import uuid
from cryptography.hazmat.primitives.asymmetric import rsa


def create_key_pair(experation: datetime.datetime):
    """The Experation date must be in UTC or will be converted to UTC
    """

    EXPONENT = 65537

    experation = experation.astimezone(datetime.UTC)


    if (experation < datetime.datetime.now(datetime.UTC)):
        print("Warning experation date is in the past!")
        raise OSError

    private_key = rsa.generate_private_key(
        public_exponent=EXPONENT,
        key_size=2048,
    )

    public_key = private_key.public_key

    kid = uuid.uuid4()

    jkw = {"kty": "rsa", "kid": kid, "experation": str(experation), "e": EXPONENT}

    return jkw



create_key_pair(datetime.datetime(2027,5,5,5,5,5))

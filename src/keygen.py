import datetime
import uuid
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

    kid = uuid.uuid4()

    jkw = {"kty": "RSA", "kid": str(kid),"alg": "RS256", "use": "sig", "e": EXPONENT}

    return (private_key, public_key, jkw)



if __name__ == "__main__":
    create_key_pair()

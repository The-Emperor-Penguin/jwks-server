import datetime

def create_key_pair(experation: datetime.datetime):
    '''
    The Experation date must be in UTC or will be converted to UTC
    '''
    from cryptography.hazmat.primitives.asymmetric import rsa
    import uuid

    experation = experation.astimezone(datetime.timezone.utc)


    if (experation < datetime.datetime.now(datetime.timezone.utc)):
            print("Warning experation date is in the past!")
            raise IOError

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    public_key = private_key.public_key

    kid = uuid.uuid4()

    jkw = {"public_key": public_key, "kid": kid, "experation": experation}
    print(jkw)


    

create_key_pair(datetime.datetime(2027,5,5,5,5,5))
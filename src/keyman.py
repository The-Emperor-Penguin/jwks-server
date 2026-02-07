import keygen
from datetime import datetime, UTC

class KeyManager:
    keys = []
    def __init__(self):
        pass
    def create_key(self, experation: datetime, debug=False):

        experation = experation.astimezone(UTC)
        print(experation)
        if (experation < datetime.now(UTC)) and not debug:
            print("Warning experation date is in the past!")
            raise IOError

        private_key, public_key, jwk = keygen.create_key_pair()
        self.keys.append({"private_key": private_key, "public_key": public_key, "jwk": jwk, "exp": experation, "tcreat": datetime.now(UTC)})

    def all_valid_keys(self):
        keys = []
        for key in self.keys:
            if key['exp'] > datetime.now(tz=UTC):
                keys.append(key)
        return keys

    def newest_valid_key(self):
        now = datetime.now(UTC)
        valid_keys = [key for key in self.keys if key["exp"] > now]
        if not valid_keys:
            return {}
        return max(valid_keys, key=lambda key: key["tcreat"])
    
    def newest_expired_key(self):
        now = datetime.now(UTC)
        expired_keys = [key for key in self.keys if key["exp"] <= now]
        if not expired_keys:
            return {}
        return max(expired_keys, key=lambda key: key["tcreat"])

    def obtain_key(self, kid: str):
        '''
        May not be used to obtain an expired key.
        Inorder to obtain an expired key you must call obtain_exp_key function with safe = False.
        
        :param kid: the key ID for the key that is requested
        '''
        return self.obtain_exp_key(kid)

    def obtain_exp_key(self, kid, safe = True):
        '''
        May be used to obtain an expired key.
        To obtain an expired key you must have safe = False.
        
        :param kid: the key ID for the key that is requested
        :param safe: Allow expired keys to be returned?
        '''
            
        
        for keypair in self.keys:
            if keypair['jwk']['kid'] == kid:
                if (keypair['exp'] <= datetime.now(tz=datetime.UTC)) and safe:
                    print("Requested expired key")
                    return {}
                return keypair

        return {}

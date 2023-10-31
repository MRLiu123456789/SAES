from decrypt import decrypt
from re_encrypt import div_round_keys

c = 0x4922
round_keys = 0x1f2ebbad

def re_decrypt(c, round_keys):
    key1, key2 = div_round_keys(round_keys)
    return decrypt(int(decrypt(c, key2),16), key1)

print(re_decrypt(c, round_keys))
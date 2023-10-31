from decrypt import decrypt
from tri_encrypt import tri_div_round_keys


def tri_decrypt(c, round_keys):
    key1, key2, key3 = tri_div_round_keys(round_keys)
    # print(key1, key2, key1*2**16+key2)
    # print(encrypt(p, key1),key1)
    # 由于encrypt()输出的是str， 所以通过int(_, 2)将其转换为整型
    return decrypt(int(decrypt(int(decrypt(c, key3), 16), key2), 16), key1)


c = 0x65a4
round_keys = 0x124f01df246d
print("jiamijieguo:")
print(tri_decrypt(c,round_keys))
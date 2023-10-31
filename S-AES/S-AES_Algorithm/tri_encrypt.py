from encrypt import encrypt

def tri_div_round_keys(round_keys):
    key1 = round_keys >> 32
    key2 = (round_keys & 0xffff0000) // (2*16)
    key3 = round_keys & 0xffff
    return key1, key2, key3

p = 0xadc4
round_keys = 0x124f01df245c

def tri_encrypt(p, round_keys):
    key1, key2, key3 = tri_div_round_keys(round_keys)
    # print(key1, key2, key1*2**16+key2)
    # print(encrypt(p, key1),key1)
    # 由于encrypt()输出的是str， 所以通过int(_, 2)将其转换为整型
    return encrypt(int(encrypt(int(encrypt(p, key1), 16), key2), 16), key3)

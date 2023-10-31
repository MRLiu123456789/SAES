from encrypt import encrypt

def div_round_keys(round_keys):
    key1 = round_keys >> 16
    key2 = round_keys & 0xffff
    return key1, key2

p = 0x65a4
round_keys = 0x01df245c

def re_encrypt(p, round_keys):
    key1, key2 = div_round_keys(round_keys)
    # print(key1, key2, key1*2**16+key2)
    # print(encrypt(p, key1),key1)
    # 由于encrypt()输出的是str， 所以通过int(_, 2)将其转换为整型
    return encrypt(int(encrypt(p, key1), 16), key2)


from encrypt import *

# P盒(即逆S盒）
p_box = [
    [10, 5, 9, 11],
    [1, 7, 8, 15],
    [6, 0, 2, 3],
    [12, 4, 13, 14]
]

def in_nibble_sub(input):
    in_sub = 0
    count = 1
    for i in range(4):
        nibble = input & 0xf
        row = nibble >> 2
        col = nibble & 0x03
        in_sub += p_box[row][col] * count
        count *= 16
        input = input >> 4
    return in_sub

def in_mix_columns(input):
    s = [[0,0],[0,0]]
    mix_matirx = [
        [9, 2],
        [2, 9]
    ]
    result = [[0,0],[0,0]]
    for i in range(2):
        for j in range(2):
            s[1-i][1-j] = input & 0xf
            input = input >> 4
    for i in range(2):
        for j in range(2):
            result[i][j] = gf_multi(mix_matirx[i][0],s[0][j]) ^ gf_multi(mix_matirx[i][1],s[1][j])
    mix_input = 0
    count = 1
    for i in range(2):
        for j in range(2):
            mix_input += result[1-i][1-j]*count
            count *= 16
    return mix_input

def decrypt(c, round_keys):
    key1, key2, key3 = expand_round_keys(round_keys)
    p = add_keys(in_nibble_sub(row_shift(in_mix_columns(add_keys(in_nibble_sub(row_shift(add_keys(trans(c), key3))), key2)))), key1)
    return hex(trans(p))

c = '?Q'
round_keys = '2b'

def ascii_decrypt(c, keys):
    key1 = ord(keys[0])
    key2 = ord(keys[1])
    keys = key2 + key1*256
    byte1 = ord(c[0])
    byte2 = ord(c[1])
    int_c = byte2 + byte1*256
    int_ascii = int(decrypt(int_c, keys), 16)
    print(hex(int_ascii), hex(int_c))
    char2 = chr(int_ascii&0xff)
    int_ascii >>= 8
    char1 = chr(int_ascii&0xff)
    return char1+char2

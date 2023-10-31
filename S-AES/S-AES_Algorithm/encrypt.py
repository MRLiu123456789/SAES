import numpy as np

s_box = [
    [9, 4, 10, 11],
    [13, 1, 8, 5],
    [6, 2, 0, 3],
    [12, 14, 15, 7]
]

#由于明文和密钥输入时是先行后列，所以做一个转置
def trans(input):
    front_1 = input >> 12
    back_1 = input & 0xf
    mid_1 = (input & 0xf0) // 16
    mid_2 = (input & 0xf00) // 256
    trans_input = front_1*2**12 + mid_1*2**8 + mid_2*2**4 + back_1
    return trans_input

def div_round_keys(round_keys):
    temp_round_keys = round_keys
    dived = np.zeros(4)
    for i in range(4):
        dived[3-i] = temp_round_keys & 0xf
        temp_round_keys = temp_round_keys >> 4
    temp = dived[2]
    dived[2] = dived[1]
    dived[1] = temp
    return dived

def sub_nib(byte):
    row1 = byte >> 6
    col1 = (byte&0x30)//16
    row2 = (byte&0xc)//4
    col2 = byte & 0x3
    n0 = s_box[row1][col1]
    n1 = s_box[row2][col2]
    return n0*16 + n1

def rot_nib(nibble):
    left = int(nibble) >> 4
    right = int(nibble) & 0xf
    return right*16 + left

def expand_round_keys(round_keys):
    key1 = round_keys
    w0 = key1 >> 8
    w1 = key1 &0xff
    rcon1 = 0b10000000
    rcon2 = 0b00110000
    w2 = int(w0) ^ rcon1 ^ sub_nib(rot_nib(w1))
    w3 = int(w1) ^ w2
    w4 = w2 ^ rcon2 ^ sub_nib(rot_nib(w3))
    w5 = w3 ^w4
    key1 = round_keys
    key2 = w2*256 + w3
    key3 = w4*256 + w5
    return key1, key2, key3

def add_keys(temp_p, round_keys):
    p = temp_p
    c = 0
    count = 1
    round_keys_list = div_round_keys(round_keys)
    for i in range(4):
        c += ((temp_p & 0xf) ^ int(round_keys_list[3-i])) * count
        temp_p = temp_p >> 4
        count *= 16
    # print(bin(p),bin(c)[2:].zfill(16),bin(round_keys),hex(c))
    return c

def nibble_sub(input):
    sub = 0
    count = 1
    for i in range(4):
        nibble = input & 0xf
        row = nibble >> 2
        col = nibble & 0x03
        sub += s_box[row][col] * count
        count *= 16
        input = input >> 4
    return sub

def row_shift(input):
    row2 = input & 0xFF
    row2_2 = row2 >> 4
    row2_1 = row2 & 0xF
    result = input - row2 + row2_1 * 16 + row2_2
    # print(hex(result))
    return result

def gf_multi(a, b):
    product = 0
    for i in range(4):
        if(b & 1):
            product ^= a
        a <<= 1
        if(a&0x10 != 0):
            a ^= 0b10011
        b >>= 1
    return product & 0xf

def mix_columns(input):
    s = [[0,0],[0,0]]
    mix_matirx = [
        [1, 4],
        [4, 1]
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

def encrypt(p, round_keys):
    key1, key2, key3 = expand_round_keys(round_keys)
    c = add_keys(row_shift(nibble_sub(add_keys(mix_columns(row_shift(nibble_sub(add_keys(trans(p), key1)))), key2))), key3)
    return hex(trans(c))

p = 0xa749
round_keys = 0xc289
def ascii_encrypt(p, keys):
    key1 = ord(keys[0])
    key2 = ord(keys[1])
    keys = key2 + key1*256
    byte1 = ord(p[0])
    byte2 = ord(p[1])
    int_p = byte2 + byte1*256
    int_ascii = int(encrypt(int_p, keys), 16)
    print(hex(int_ascii), hex(int_p))
    char2 = chr(int_ascii&0xff)
    int_ascii >>= 8
    char1 = chr(int_ascii&0xff)
    return char1+char2

p = 0xadc4
keys = 0x1526

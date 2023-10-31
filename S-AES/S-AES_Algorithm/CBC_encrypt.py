from encrypt import encrypt
from random import randint

def div_str_to_int_list(p):
    len_p = len(p)
    if len_p % 2 != 0:
        len_p += 1
        p = p + ' '
    list_p = [0 for _ in range(len_p // 2)]
    for i in range(len_p // 2):
        list_p[i] = ord(p[2*i])*256 + ord(p[2*i+1])
    return list_p

def ascii_int(int_16_bit):
    right = chr(int_16_bit & 0xff)
    int_16_bit >>= 8
    left = chr(int_16_bit)
    str_int = left + right
    return str_int

def int_str(str):
    result = ord(str[0])*256 + ord(str[1])
    return result

def CBC_encrypt(p, keys):
    IV = randint(0, 2**16-1)
    c = ''
    list_p = div_str_to_int_list(p)
    c += ascii_int(int(encrypt(IV, keys), 16))
    for i in range(len(list_p)):
        if i == 0:
            c += ascii_int(int(encrypt((IV ^ list_p[i]), keys), 16))
        else:
            c += ascii_int(int(encrypt((int_str(c[2*i:2*i+2]) ^ list_p[i]), keys), 16))
    return c


p = 'as5'
keys = 0x4546
print(CBC_encrypt(p,keys))

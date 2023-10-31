from CBC_encrypt import *
from decrypt import decrypt

def CBC_decrypt(c, keys):
    list_c = div_str_to_int_list(c)
    for i in range(len(c)//2):
        if i == 0:
            p = ''
            IV = int(decrypt(list_c[0], keys), 16)
        elif i == 1:
            p += ascii_int(IV ^ int(decrypt(list_c[i], keys), 16))
        else:
            p += ascii_int(list_c[i-1] ^ int(decrypt(list_c[i], keys), 16))
    return p

c = CBC_encrypt(p, keys)
print(CBC_decrypt(c, keys))
from encrypt import *
from decrypt import *

# 经测试，明密文对<3时，存在多个可行密钥，无法判断出准确密钥，当明密文对>=3时，可以得到准确密钥（不完全测试）
def meet_in_the_middle_attack(p, c):
    for key1 in range(2**16):# 754
        print(key1)
        for key2 in range(2**16):
            c1 = encrypt(p[0], key1)
            c2 = encrypt(p[1], key1)
            c3 = encrypt(p[2], key1)
            if(decrypt(c[0], key2) == c1 and decrypt(c[1], key2) == c2 and decrypt(c[2], key2) == c3):
                print(hex(key1*(2**16)+key2))

p = [0x567f, 0x5acf, 0xadc4]
keys = 0x1526
c = [0xdc51, 0xd181, 0xcc6f]
# p = [0x5a5f, 0xacdb]
# c = [0x1fff, 0x7f3a]


meet_in_the_middle_attack(p, c)

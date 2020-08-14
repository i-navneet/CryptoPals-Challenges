from random import randint
from Crypto.Cipher import AES
def xor_bytes(s1,s2):
    ans=b''
    for i in range(len(s1)):
        ans=ans + bytes([s1[i]^s2[i]])
    return ans
def random_key():
    ans=b''
    for i in range(16):
        byte = randint(0,255)
        ans = ans + bytes([byte])
    return ans
def AES_ECB_encrypt(m,key):
    aes = AES.new(key,AES.MODE_ECB)
    return aes.encrypt(m)
def AES_CBC_encrypt(m,key):
    aes = AES.new(key,AES.MODE_ECB)
    c0 = cipher = random_key()
    ans = b''
    for i in range(0,len(m),16):
        c0 = cipher
        cipher = aes.encrypt(xor_bytes(c0,m[i:i+16]))
        ans = ans + cipher
    return ans


def oracle(m):
    key = random_key()
    p = m
    for i in range(randint(5,10)):
        p = bytes([randint(0,255)]) + p
    for i in range(randint(5,10)):
        p = p + bytes([randint(0,255)])
    if(len(p)%16!=0):
        pad = 16 - len(p) % 16
        p = p + bytes([pad]) * pad
    mode = randint(0,1)
    if(mode==1):
        return AES_ECB_encrypt(p,key)
    else:
        return AES_CBC_encrypt(p,key)

def detect_mode(cipher):
    state  = [False for i in range(0,len(cipher),16)]
    max = 0
    for i in range(0,len(cipher),16):
        count = 0
        if(state[i//16]==False):
            for j in range(i+16,len(cipher),16):
                if(cipher[i:i+16] == cipher[j:j+16]):
                    state[j//16] = True
                    count = count + 1
        if(count > max):
            max = count
    return max
m = b'0' * 48
cipher = oracle(m)
if(detect_mode(cipher) == 1):
    print("ECB")
else:
    print("CBC")
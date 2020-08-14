from Crypto.Cipher import AES
from random import randint
from base64 import b64decode
def xor_string(s1,s2):
    ans=b''
    if(type(s1)==type("")):
        s1=s1.encode()
    if(type(s2)==type("")):
        s2=s2.encode()
    for i in range(len(s1)):
        ans = ans + bytes([s1[i]^s2[i]])
    return ans
key = b'YELLOW SUBMARINE'
aes = AES.new(key,AES.MODE_ECB)
def AES_CTR_encrypt_and_decrypt(m):
    nonce = 0
    initial = nonce.to_bytes(length=8,byteorder='little')
    count = 0
    ans = b''
    if(len(m)%16!=0):
        pad = 16 - len(m)%16
        m = m + bytes([pad]) * pad
    for i in range(0,len(m),16):
        keystream = initial + count.to_bytes(length = 8,byteorder='little')
        ans = ans + xor_string(aes.encrypt(keystream),m[i:i+16])
        count+=1
    return ans
s = b64decode(b'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==')
print(AES_CTR_encrypt_and_decrypt(s))
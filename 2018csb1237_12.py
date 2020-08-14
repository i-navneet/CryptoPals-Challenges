from Crypto.Cipher import AES
from random import randint
from base64 import b64decode
def random_key():
    ans=b''
    for i in range(16):
        byte = randint(0,255)
        ans = ans + bytes([byte])
    return ans
key = random_key()
aes = AES.new(key,AES.MODE_ECB)
def AES_ECB_encrypt(m):
    if(len(m)%16!=0):
        pad = 16 - (len(m) % 16)
        m = m + bytes([pad]) * pad
    return aes.encrypt(m)
def oracle(m):
    unknown_string = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    m = m + b64decode(unknown_string)
    return AES_ECB_encrypt(m)
def detect_block_size():
    j = 1
    state = 0
    state0 = 0
    while(True):
        state0 = state
        if(j==1):
            m = b'A' * j
            cipher = oracle(m)
            state = len(cipher)
            j = j + 1
            continue
        else:
            m = b'A' * j
            state = len(oracle(m))
            j = j + 1
            if(state0 != state):
                return state-state0

def detect_ecb():
    m = b'0' * 64
    cipher = oracle(m)
    block_size = detect_block_size()
    ans = True
    for j in range(0,3*block_size,block_size):
        if(cipher[j:j+16] == cipher[j+16:j+32]):
            ans = ans & True
        else:
            ans = False
            break
    return ans
def decrypt_unknown_meassage():
    block_size = detect_block_size()
    ans = b''
    if(detect_ecb()==True):
        for k in range(0,len(oracle(b'')),block_size):
            for j in range(1,block_size+1):
                m = b'A' * (block_size - j)
                matching_string = oracle(m)[k:k+block_size]
                for i in range(0,256):
                    p = m + ans + bytes([i])
                    cipher = oracle(p)
                    if (cipher[k:k+block_size]==matching_string):
                        ans = ans + bytes([i])
                        break
    else:
        print('ECB not found')
    return ans
print(decrypt_unknown_meassage().decode())
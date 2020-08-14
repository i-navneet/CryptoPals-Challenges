from Crypto.Cipher import AES
from random import randint
from base64 import b64decode
def random_key(size):
    ans=b''
    for i in range(size):
        byte = randint(0,255)
        ans = ans + bytes([byte])
    return ans
key = random_key(16)
aes = AES.new(key,AES.MODE_ECB)
def AES_ECB_encrypt(m):
    if(len(m)%16!=0):
        pad = 16 - (len(m) % 16)
        m = m + bytes([pad]) * pad
    return aes.encrypt(m)
random_prefix = random_key(randint(0,128))
def oracle(m):
    unknown_string = b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
    m = random_prefix + m + b64decode(unknown_string)
    pad = 16 - len(m) %16
    if(pad!=16):
        m = m + bytes([pad]) * pad
    return AES_ECB_encrypt(m)

def attacker():
    state = 0
    state1 = 0
    off = 0
    attack = b''
    while(True):
        state1 = state
        state = len(oracle(attack))
        if(state1!=state and state1!=0):
            break
        attack += b'A'
    block_size = state - state1
    attack = b'A' * (4*block_size)
    cipher = oracle(attack)
    offset = -1
    for i in range(0,len(cipher)-block_size,block_size):
        if(cipher[i:i+block_size]==cipher[i+block_size:i+2*block_size]):
            offset = i // block_size
            break
    if(offset == -1):
        print("ECB Not Found!")
        return b''
    check1 = b'a'
    check = b'b'
    attack = b"A"
    while(check1!=check):
        check1 = check
        check = oracle(attack)[offset * block_size:(offset+1)*block_size]
        off = off + 1
        attack += b"A"
    off = off - 1
    off = off % 16
    ans = b''
    for k in range(0,len(oracle(b'A'*off))-offset*block_size,block_size):
        for j in range(1,block_size+1):
            m = b'A' * off + b'A' * (block_size - j)
            matching_string = oracle(m)[offset*block_size+k:offset*block_size+k+block_size]
            for i in range(0,256):
                p = m + ans + bytes([i])
                cipher = oracle(p)
                if (cipher[offset * block_size + k:k+(offset+1)*block_size]==matching_string):
                    ans = ans + bytes([i])
                    break
    return ans
        
print(attacker().decode())
    
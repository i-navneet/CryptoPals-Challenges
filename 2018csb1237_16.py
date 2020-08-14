from Crypto.Cipher import AES
from random import randint
def xor_string(s1,s2):
    ans=b''
    if(type(s1)==type("")):
        s1=s1.encode()
    if(type(s2)==type("")):
        s2=s2.encode()
    for i in range(len(s1)):
        ans = ans + bytes([s1[i]^s2[i]])
    return ans
def random_key(size):
    ans=b''
    for i in range(size):
        byte = randint(0,255)
        ans = ans + bytes([byte])
    return ans
key = random_key(16)
aes = AES.new(key,AES.MODE_ECB)
def xor_bytes(s1,s2):
    ans=b''
    for i in range(len(s1)):
        ans=ans + bytes([s1[i]^s2[i]])
    return ans
IV = random_key(16)
def AES_CBC_encrypt(m):
    c0 = cipher = IV
    ans = b''
    for i in range(0,len(m),16):
        c0 = cipher
        cipher = aes.encrypt(xor_bytes(c0,m[i:i+16]))
        ans = ans + cipher
    return ans
def AES_CBC_decrypt(c):
    ans = b''
    cipher = IV
    for i in range(0,len(c),16):
        c0 = cipher
        cipher = c[i:i+16]
        xored_against = aes.decrypt(cipher)
        ans = ans + xor_string(xored_against,c0)
    return ans
def oracle(m):
    prepend = b"comment1=cooking%20MCs;userdata="
    append = b";comment2=%20like%20a%20pound%20of%20bacon"
    if(type(m)==type("")):
        m = m.encode()
    m = m.replace(b";",b"\";\"")
    m = m.replace(b"=",b"\"=\"")
    m = prepend + m + append  
    pad = 16 - len(m)%16
    if(pad!=16):
        m =  m + bytes([pad]) * pad
    return AES_CBC_encrypt(m)
def is_admin(s):
    if(type(s)==type("")):
        s = s.encode()
    plain = AES_CBC_decrypt(s)
    if(plain.find(b";admin=True;")!=-1):
        return True
    return False
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
block_size = detect_block_size()
def attacker():
    attack = b"A" * 16 + b';dmi=ru;'
    cipher = oracle(attack)
    new_cipher = bytearray(cipher)
    new_cipher[34] = new_cipher[34] ^ ord(b'"') ^ ord(b'a')
    new_cipher[38] = new_cipher[38] ^ ord(b'"') ^ ord(b'n')
    new_cipher[40] = new_cipher[40] ^ ord(b'"') ^ ord(b'T')
    new_cipher[43] = new_cipher[43] ^ ord(b'"') ^ ord(b'e')
    new_cipher = bytes(new_cipher)
    return is_admin(new_cipher)
print(attacker())
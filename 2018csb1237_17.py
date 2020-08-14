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
def AES_CBC_encrypt(m,IV):
    c0 = cipher = (IV)
    ans = b''
    for i in range(0,len(m),16):
        c0 = cipher
        cipher = aes.encrypt(xor_bytes(c0,m[i:i+16]))
        ans = ans + cipher
    return ans
def AES_CBC_decrypt(c,IV):
    ans = b''
    cipher = (IV)
    for i in range(0,len(c),16):
        c0 = cipher
        cipher = c[i:i+16]
        xored_against = aes.decrypt(cipher)
        ans = ans + xor_string(xored_against,c0)
    return ans
s = [b64decode(b'MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc='),b64decode(b'\
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic='),b64decode(b'\
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw=='),b64decode(b'\
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg=='),b64decode(b'\
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl'),b64decode(b'\
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA=='),b64decode(b'\
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw=='),b64decode(b'\
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8='),b64decode(b'\
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g='),b64decode(b'\
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93')]
def oracle():
    IV = (random_key(16))
    m = s[randint(0,9)]
    if(len(m)%16!=0):
        pad = 16 - len(m) % 16
        m = m + bytes([pad]) * pad
    return (AES_CBC_encrypt(m,IV),IV)
def padding_oracle(m,IV):
    if(type(m)==type("")):
        m = m.encode()
    m = AES_CBC_decrypt(m,IV)
    if(m[-1]>16):
        return True
    if(m[-m[-1]:]==m[-1:]*m[-1]):
        return True
    else:
        return False
def attacker():
    (c,iv) = oracle()
    c1 = bytearray(c)
    ans = b''
    for i in range(len(c)-16,15,-16):
        for j in range(15,-1,-1):
            for k in range(256):
                c1[i+j] = c[i+j] ^ k
                if(padding_oracle(c1,iv)==True):
                    ans = bytes([k^(16-j)]) + ans
                    l = i
                    m = j
                    a = 0
                    while((l+m)%16!=0):
                        c1[l+m] = c[l+m] ^ ans[a] ^ (j+1)
                        a += 1
                        m += 1
                    break
        c1 = c1[:-16]
    iv1 = bytearray(iv)
    for j in range(15,-1,-1):
        for k in range(256):
            iv1[j] = iv[j] ^ k
            if(padding_oracle(c1,bytes(iv1))==True):
                ans = bytes([k^(16-j)]) + ans
                m  = j
                a = 0
                while((m)%16!=0):
                    iv1[m] = iv[m] ^ ans[a] ^ (j+1)
                    a+=1
                    m+=1
                break
    return ans
print((attacker()))
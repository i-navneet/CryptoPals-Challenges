from Crypto.Cipher import AES
from random import randint
def random_key():
    ans=b''
    for i in range(16):
        byte = randint(0,255)
        ans = ans + bytes([byte])
    return ans
key = random_key()
aes = AES.new(key,AES.MODE_ECB)
def parse_equal_and(s):
    ans = {}
    if(type(s) == type('')):
        s = s.encode()
    a = s.split(b'&')
    for i in a:
        b = i.split(b'=')
        ans[b[0]] = b[1]
    return ans
def profile_for(s):
    if(type(s)== type('')):
        s = s.encode()
    temp = s.replace(b'&',b'')
    temp = temp.replace(b'=',b'')
    plaintext = (b'email='+temp+b'&userid=10&role=user')
    if(len(plaintext) % 16 != 0):
        pad = 16 - (len(plaintext) % 16)
        plaintext = plaintext + bytes([pad]) * pad
    return aes.encrypt(plaintext)
def decrypt_and_parse_ECB(c):
    return parse_equal_and(aes.decrypt(c))
def detect_block_size():
    j = 1
    state = 0
    state0 = 0
    while(True):
        state0 = state
        if(j==1):
            m = b'A' * j
            cipher = profile_for(m)
            state = len(cipher)
            j = j + 1
            continue
        else:
            m = b'A' * j
            state = len(profile_for(m))
            j = j + 1
            if(state0 != state):
                return state-state0
block_size = detect_block_size()
def detect_ecb():
    m = b'0' * 64
    cipher = profile_for(m)
    ans = True
    for j in range(0,2*block_size,block_size):
        if(cipher[j:j+16] == cipher[j+16:j+32]):
            ans = ans & True
        else:
            ans = False
            break
    return ans

def attacker():
    dummy_paste = b'email=&userid=10&role='
    email_size_paste = ((len(dummy_paste) - 1) // block_size + 1) * block_size - len(dummy_paste)
    email_paste = b'A' * email_size_paste
    pad = block_size - len(b'admin')
    dummy_cut = b'email='
    email_size_cut = ((len(dummy_cut) - 1) // block_size + 1) * block_size - len(dummy_cut)
    email_cut = b'A' * email_size_cut + b'admin' + bytes([pad]) * pad
    cut = profile_for(email_cut)[block_size:2*block_size]
    cipher = profile_for(email_paste)
    ans_cipher = cipher[:-block_size] + cut
    return decrypt_and_parse_ECB(ans_cipher)
print(attacker())
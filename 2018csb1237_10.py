from base64 import b64decode
from Crypto.Cipher import AES
from binascii import unhexlify
def hex_xor(s1,s2):
    a1=(s1)-48 if((s1)>=48 and (s1)<=57) else (s1)-87
    a2=(s2)-48 if((s2)>=48 and (s2)<=57) else (s2)-87
    a = a1^a2
    ans=hex(a)
    ans=ans[2:]
    return ans.encode()
def xor_string(s1,s2):
    ans=b''
    temp1=s1.encode()
    temp2=s2.encode()
    for i in range(len(temp1)):
        ans=ans+hex_xor(temp1[i],temp2[i])
    return ans
def AES_CBC_decrypt(c,key):
    prp = AES.new(key,AES.MODE_ECB)
    ans = b''
    cipher = b'\x00' * 16
    # if(len(c)%16!=0):
    #     pad = len(c) - len(c) % 16
    #     c = c + (bytes([pad])) * pad
    for i in range(0,len(c),16):
        c0 = cipher
        cipher = c[i:i+16]
        xored_against = prp.decrypt(cipher)
        ans = ans + xor_string(bytes.hex(xored_against),bytes.hex(c0))
    return ans


fp = open('10.txt','rb')
key = b'YELLOW SUBMARINE'
ciphertext = b''
for line in fp:
    ciphertext = ciphertext + b64decode(line)
if(len(ciphertext)%16!=0):
    pad = len(ciphertext) - len(ciphertext) % 16
    ciphertext = ciphertext + (bytes([pad])) * pad
ans = AES_CBC_decrypt(ciphertext,key)
print(unhexlify(ans.decode()).decode())
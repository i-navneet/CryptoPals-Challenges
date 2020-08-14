import base64
from Crypto.Cipher import AES
key=b'YELLOW SUBMARINE'
aes = AES.new(key,AES.MODE_ECB)
ciphertext=b''
fp=open('7.txt','rb')
for line in fp:
    ciphertext = ciphertext + base64.b64decode(line)
plaintext = aes.decrypt(ciphertext)
print(plaintext.decode())
def hex_to_base64(s):
    hex_to_bin_key=[b'0000',b'0001',b'0010',b'0011',b'0100',b'0101',b'0110',b'0111',b'1000',b'1001',b'1010',b'1011',b'1100',b'1101',b'1110',b'1111']
    base64key=[b'A',b'B',b'C',b'D',b'E',b'F',b'G',b'H',b'I',b'J',b'K',b'L',b'M',b'N',b'O',b'P',b'Q',b'R',b'S',b'T',b'U',b'V',b'W',b'X',b'Y',b'Z',b'a',b'b',b'c',b'd',b'e',b'f',b'g',b'h',b'i',b'j',b'k',b'l',b'm',b'n',b'o',b'p',b'q',b'r',b's',b't',b'u',b'v',b'w',b'x',b'y',b'z',b'0',b'1',b'2',b'3',b'4',b'5',b'6',b'7',b'8',b'9',b'+',b'/']
    t=s.encode()
    binary=b''
    for i in range(len(t)):
        if(t[i]>=ord(b'0') and t[i]<=ord(b'9')):
            binary = binary + hex_to_bin_key[t[i]-ord(b'0')]
        else:
            binary = binary + hex_to_bin_key[t[i]-ord(b'a')+10]
    ans=b''
    if(len(binary)%6!=0):
        binary = b'0' * (6-len(binary)%6) + binary
    for i in range(0,len(binary),6):
        digit = 0
        for j in range(i,i+6):
            digit = digit * 2 + binary[j] - ord(b'0')
        ans = ans + base64key[digit]
    return ans.decode()
s = input()
print(hex_to_base64(s))
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
    return ans.decode()
input1=input()
input2=input()
print(xor_string(input1,input2))

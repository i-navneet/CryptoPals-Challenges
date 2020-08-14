from binascii import hexlify
from binascii import unhexlify
from scipy.stats.stats import pearsonr
def hex_xor(s1,s2):
    a1=int(s1)-48 if(int(s1)>=48 and int(s1)<=57) else int(s1)-87
    a2=int(s2)-48 if(int(s2)>=48 and int(s2)<=57) else int(s2)-87
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
def dec_k(s,k):
    if(len(s)!=len(k)):
        temp= k*(len(s)//2)
    return xor_string(s,temp)
def score(s):
    A={}
    for i in range(256):
        A[hexlify(bytes([i]))]=0.0
    for i in range(0,len(s),2):
        A[s[i:i+2]]+=1
    for i in range(0,len(s),2):
        A[s[i:i+2]]=A[s[i:i+2]]*100/(len(s)/2)
    A1=[]
    for i in range(256):
        A1.append(A[hexlify(bytes([i]))])
    B=[]
    for i in range(256):
        B.append(0.0)
    C=[9,23,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,131]
    C1=[0.005700,0.000000,17.166201,0.007200,0.244200,0.017900,0.056100,0.016000,0.022600,0.244700,0.217800,0.223300,0.062800,0.021500,0.738400,1.373400,1.512400,0.154900,0.551600,0.459400,0.332200,0.184700,0.134800,0.166300,0.115300,0.103000,0.105400,0.102400,0.435400,0.121400,0.122500,0.022700,0.124200,0.147400,0.007300,0.313200,0.216300,0.390600,0.315100,0.267300,0.141600,0.187600,0.232100,0.321100,0.172600,0.068700,0.188400,0.352900,0.208500,0.184200,0.261400,0.031600,0.251900,0.400300,0.332200,0.081400,0.089200,0.252700,0.034300,0.030400,0.007600,0.008600,0.001600,0.008800,0.000300,0.115900,0.000900,5.188000,1.019500,2.112900,2.507100,8.577100,1.372500,1.559700,2.744400,4.901900,0.086700,0.675300,3.175000,1.643700,4.970100,5.770100,1.548200,0.074700,4.258600,4.368600,6.370000,2.099900,0.846200,1.303400,0.195000,1.133000,0.059600,0.002600,0.000700,0.002600,0.000300,0.0]
    j=0
    for i in C:
        B[i]=C1[j]
        j+=1
    (a,b)=pearsonr(B,A1)
    return a
s = input()
ans=b''
key=b''
max=-2.0
for i in range(0,256):
    temp2=hexlify(bytes([i]))
    if(len(temp2)%2!=0):
        temp2=b'0'+temp2
    temp1=temp2.decode()
    temp=dec_k(s,temp1)
    if(len(temp)%2!=0):
        temp=b'0'+temp
    if(score(temp)>max):
        print(score(temp))
        ans=unhexlify(temp)
        key=bytes([i])
print(ans,end=' ')
print(key)
fp=open('8.txt','r')
max = 0
ans = 0
k = 0
for line in fp:
    temp = bytes.fromhex(line)
    state = [False for i in range(0,len(temp),16)]
    k = k + 1
    for i in range(0,len(temp),16):
        count = 0
        if(state[i//16] == False):
            for j in range(i+16,len(temp),16):
                if(temp[i:i+16]==temp[j:j+16]):
                    state[j//16] = True
                    count = count + 1
        if(count > max):
            max = count
            ans = k
print(ans)
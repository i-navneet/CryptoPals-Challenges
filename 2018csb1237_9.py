def padding(key,n):
    t = s.encode()
    if(len(t)%n!=0):
        t = t + bytes([n-len(t)%n]) * (n-len(t)%n)
    return t
s = "YELLOW SUBMARINE"
print(padding(s,20))
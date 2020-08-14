class bad_padding(Exception):
    pass
def padding_validate(s):
    if(type(s)==type("")):
        s = s.encode()
    if(s[-s[-1]:]==s[-1:]*s[-1]):
        return s[:-s[-1]]
    else:
        raise bad_padding
print(padding_validate("ICE ICE BABY\x01\x02\x03\x04"))
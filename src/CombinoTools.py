def onlyascii(char):
    if ord(char) <= 0 or ord(char) > 127:
        return ''
    else:
        return char


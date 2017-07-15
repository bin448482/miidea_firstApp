class TokenToEncryption(object):
    def __init__(self):
        self.characterList = "abcdefghijklmnopqrstuvwxyz"

    def convert(self, token="helloworld", key="0123456789"):
        dict = {}
        i = 0
        j = 0
        for i in range(0, 10):
            if(i == 7 or i == 9):
                for j in range(j, j+4):
                    dict[self.characterList[j]] = key[i]
            elif i == 0 or i == 1:
                continue
            else:
                for j in range(j, j+3):
                    dict[self.characterList[j]] = key[i]
            j=j+1

        retuanValue = ''
        for c in token:
            if c in dict:
                retuanValue = retuanValue + dict[c]
            else:
                retuanValue = retuanValue + c

        return retuanValue







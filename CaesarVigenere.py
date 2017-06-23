cipher2 = []
wordz = []
letters ='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
cipher = []
pos_key = []
pos_text = []
pos_cipher = 0
key = []
plain = []
letters_len = 26

def encrypt(K, shift, text):
    wordz =list(K.upper())
    cipher2 = wordz
    x=0
    while x < len(cipher2):
            if (cipher2[x] == ' '):
                x= x+1
            else:
                cipher2[x] = chr((ord(cipher2[x]) + shift - 65) % 26 + 65)
                x= x+1
    return "" .join(cipher2)
def decrypt(text, result):
    P= text
    x = 0

    plain = list(P.upper())
    for letter in plain:
        y = letters.find(letter)

        if y == -1:
            cipher.append(letter)
        else:
            z = letters.find(result[x])
            y = (y - z) % len(letters)
            cipher.append(letters[y])
            x = x+1

            if x == len(result):
                x = 0

    result = "" .join(cipher)
    return result


def main():
    content = []
    with open('bogo.txt') as f:
        content = f.read().splitlines()

    shift = int(content[0])
    K = content[2]
    text = content[1]
    result = encrypt(K, shift, text)
    print decrypt(text, result)
main()
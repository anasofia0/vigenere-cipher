alphabet = 'abcdefghijklmnopqrstuvwxyz'
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

freq_port = [14.63, 1.04, 3.88, 4.99, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]
freq_eng = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

def table(letter1, letter2, big=False):
    
    idx1 = alphabet.find(letter1)
    idx2 = alphabet.find(letter2)
    return alphabet[(idx1+idx2)%26] if not big else ALPHABET[(idx1+idx2)%26]


def get_cipher(text, key):
    
    cipher = ''

    j = 0
    for i in range(len(text)):
        big = False
        if text[i].lower() in alphabet:
            if text[i] in ALPHABET: big=True
            cipher += table(text[i].lower(), key[j%len(key)].lower(), big)
            j += 1
        else:
            cipher += text[i]

    return cipher

def find_keysize(text):
    
    text = ''.join([i for i in text.lower() if i in alphabet])
    factors = [0 for i in range(20)]

    for i in range(len(text)-2):
        seq = text[i:i+3]

        for j in range(i+3, len(text)-2):
            if text[j:j+3] == seq:
                dist = j-i
                for k in range(2,21):
                    if dist%k==0:
                        factors[k-2] += 1
                break
    
    print(f'Tamanhos de chaves e sua quantidade de fatores encontrada:')

    for i in range(len(factors)):
        print(f'\t{i+2} - {factors[i]}')
    
    selected = int(input('Selecione o tamanho da chave desejada: '))
    
    return selected

def text_freq(text):
    
    frequency = [0 for i in range(26)]

    text = [i for i in text.lower() if i in alphabet]
    size = len(text)

    for i in text:
        frequency[alphabet.find(i)] += 1

    for i in range(len(frequency)):
        if frequency[i] != 0:
            frequency[i] /= size

    return frequency

def freq_analysis(letters, lang_freq):
    
    freq = text_freq(letters)
    dif = []
    for j in range(26):
        dif.append(sum([lang_freq[i]*freq[i] for i in range(26)]))
        freq.append(freq.pop(0))
    
    return dif.index(max(dif))

def get_key(cipher, keysize, english=True):
    
    cipher = ''.join([i for i in cipher.lower() if i in alphabet])
    key = ''

    if english:
        lang_freq = freq_eng
    else:
        lang_freq = freq_port

    for i in range(keysize):

        distr = ''.join([cipher[j] for j in range(i,len(cipher),keysize)])
        idx = freq_analysis(distr, lang_freq)
        key += alphabet[idx]

    return key

def get_plaintext(text, key):
    
    plaintext = ''

    j = 0
    for i in range(len(text)):
        if text[i].lower() in alphabet:
            idx2 = alphabet.find(key[j%len(key)])
            if text[i] in ALPHABET:
                idx1 = ALPHABET.find(text[i])
                plaintext += ALPHABET[(idx1-idx2)%26]
            else:
                idx1 = alphabet.find(text[i])
                plaintext += alphabet[(idx1-idx2)%26]
            j += 1
        else:
            plaintext += text[i]

    return plaintext

def read_file():
    import os

    path = input('Digite o nome do arquivo: ')

    if not os.path.exists(path):
        print(f'Arquivo {path} nao encontrado')
        return -1

    with open(path, encoding='utf-8') as f:
        return f.read()

def main():
    
    while True:

        print('\n\nEscolha a acao desejada')
        print('\t1- cifrar')
        print('\t2- decifrar')
        print('\t3- ataque')
        print('\t4- finalizar')
        acao = int(input('>'))

        if acao == 1:
            text = read_file()
            if text != -1:
                key = input('Digite chave desejada: ')
                cipher = get_cipher(text, key)
                print('Mensagem cifrada:')
                print(cipher)
            
        elif acao == 2:
            text = read_file()
            if text != -1:
                key = input('Digite chave: ')
                plaintext = get_plaintext(text, key)
                print('Mensagem decifrada:')
                print(plaintext)

        elif acao == 3:
            text = read_file()
            if text != -1:
                lang = input('O texto esta em ingles ou portugues (eng/port): ')
                lang = lang=='eng'

                not_found = True

                while not_found:
                    keysize = find_keysize(text)
                    key = get_key(text, keysize, english=lang)
                    plaintext = get_plaintext(text, key)
                    print(f'Chave encontrada: {key}')
                    print('Texto decifrado:')
                    print(plaintext, end='\n\n')

                    cont = input('Deseja tentar com outro tamanho de chave? (s/n): ')
                    not_found = cont == 's'

        elif acao == 4:
            break
        else:
            print('Entrada invalida')
        print()


if __name__ == '__main__':
    main()


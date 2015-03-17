'''versão v.02'''
import keyGen
from os import system

def cls():
    system('cls')

def firstScreen():
    cls()
    print("FHE over Integers")
    print("1-Geração de chaves")
    print("2-Teste com geração de chave")
    print("3-Teste com chave previamente gerada")
    print("0-Sair")
    a = input()
    return int(a)

def key():
    a=input('<Toy, Small, Medium, Large>? ').upper()
    if a=='T': keyGen.keygen('toy.txt', 'toy')
    elif a=='S': keyGen.keygen('small.txt', 'small')
    elif a=='M': keyGen.keygen('medium.txt', 'medium')
    elif a=='L': keyGen.keygen('large.txt', 'large')
    b = input('any to continue...')  # lint:ok

if __name__=='__main__':
    while True:
        a=firstScreen()
        if a==1: key()
        elif a==2: print('not yet')
        elif a==3: print('not yet')
        elif a==0: quit(0)  # lint:ok
        else: print('Are you sure you know how to handle me?')

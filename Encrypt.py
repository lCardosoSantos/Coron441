import fheKey
import random
from gmpy2 import mpz
import gmpy2
import time
from keyGen import randomMatrix, modNear
import math
import gc
debug = False

def printDebug(*args):
    if debug:
        for i in args:
            print (i, end=' ')  # lint:ok

def printM(y):
    if debug:
        for i in y:
            for j in i:
                print (j, end=' ')  # lint:ok
            print(' ')

def encrypt(pk, m):
    if m != 0 and m != 1:
        print('not a valid m')
        return 0

    alpha = pk.P._lambda  ##o fator de segurança alpha é igual a lambda, de acordo com Coron et. al.
    matrix = [[0 for i in range(pk.P._beta)] for j in range(pk.P._beta)]
    for i in range(pk.P._beta):
        for j in range(pk.P._beta):
            matrix[i][j]=random.randint(0, 2**alpha -1)
            #print(matrix[i][j], end=' ')
        #print(' ')
    pprime=2**pk.P._rho
    r=random.randint(-pprime, pprime)
    pkAsk=(pk.pkAsk).copy()
    x0=pkAsk.pop(0)
    xi0=pkAsk[::2]
    xj1=pkAsk[1::2]

    ## iniciando processo de encrypt
    ## computar somatorio
    somatorio=mpz(0)
    for i in range(pk.P._beta):
        for j in range(pk.P._beta):
            x=gmpy2.mul(xj1[j], xi0[i])
            somatorio += gmpy2.mul(matrix[i][j], x)
    c=(m+(2*r)+(2*somatorio))
    c=modNear(c,x0)
    return c


def expand(pk, cAsk):
    #cria uma matriz de sqrt(theta) elementos
    l=int(math.sqrt(pk.P._theta))
    y=[[0 for i in range(l)] for i in range(l)]
    kappa=pk.P._gamma+6

    n=4 ##coron 441, pg10
    gmpy2.get_context().precision=n #seta precisao do mpfr para 2
    #computa matriz y[i][j]
    for i in range(l):
        for j in range(l):
            y[i][j]=float(gmpy2.mpfr(randomMatrix(i, j, kappa, pk.se, l)/(2**kappa)))
    y[0][0]=float(gmpy2.mpfr(pk.u11/2**kappa))

    #seta precisão do mpfr de novo para o valor correto
    gmpy2.get_context().precision=1024 #valor feito com testes. Diretamente proporcional a velocidade do expand
    #gera matrix z e computa elementos
    expand = [[1 for i in range(l)] for i in range(l)]
    for i in range(l):
        for j in range(l):
            expand[i][j]=float((cAsk * y[i][j])%2)
    return expand

def decrypt(sk, cAsk, z):
    soma=0
    l=int(math.sqrt(sk.P._theta))
    for i in range(l):
        for j in range(l):
            soma+=(sk.s0[i]*sk.s1[j]*z[i][j])
    soma=mpz(gmpy2.round_away(soma))
    m=(cAsk-soma)%2
    return m

def add(pk, c1, c2):
    soma=gmpy2.add(c1,c2)
    return modNear(soma,pk.pkAsk[0])

def mul(pk, c1, c2):
    mul= gmpy2.mul(c1,c2)
    return modNear(mul,pk.pkAsk[0])


def teste():
    '''teste para funções com key'''
    par=['toy','small', 'medium', 'large']
    for i in par:
        f=open('temposEncryptDecryptExpand.txt', 'a')
        print('executing ', i)
        f.write(i+'\n')
        pk=fheKey.read('pk_pickle_'+i+'.txt')
        sk=fheKey.read('sk_pickle_'+i+'.txt')
        t=-time.clock()
        e0=encrypt(pk, 0)
        t+=time.clock()
        f.write('encrypt=='+str(t)+'\n')

        #e1=encrypt(pk, 1)
        #print('bit0==', e0)
        #print('bit1==', e1)
        #added=add(pk, e0, e1)
        #mult=mul(pk, e0, e1)

        t=-time.clock()
        ze0=expand(pk, e0)
        t+=time.clock()
        f.write('expand=='+str(t)+'\n')
        #ze1=expand(pk, e1)

        #zadd=expand(pk, added)
        #zmul=expand(pk, mult)
        t=-time.clock()
        d0=decrypt(sk, e0, ze0)
        t+=time.clock()
        f.write('decrypt=='+str(t)+'\n')

        #d1=decrypt(sk, e1, ze1)
        #print('isso deve ser um 1+0 =>', decrypt(sk, added, zadd))
        #print('isso deve ser um 1*0 =>', decrypt(sk, mult, zmul), '\n')
        f.close()

if __name__=='__main__':
    print('iniciada rotina de testes:')
    teste()
    gc.collect()



##def testEncrypt():
##    file='pk_pickle_toy.txt'
##    pk=fheKey.read(file)
##    c=encrypt(pk, 0)
##    return c
##
##def testExpand(c):
##    file='pk_pickle_toy.txt'
##    pk=fheKey.read(file)
##    return expand(pk, c)
##
##def testDecrypt(c, z):
##    file='sk_pickle_toy.txt'
##    sk=fheKey.read(file)
##    return decrypt(sk, c, z)


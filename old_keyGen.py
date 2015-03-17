#FHE on Integers
'''
http://eprint.iacr.org/2011/441.pdf
http://eprint.iacr.org/2011/440.pdf
https://github.com/coron/fhe
'''

from gmpy2 import mpz
import random
import gmpy2
import time
import math
import parameters
import fheKey

from sys import getsizeof as size
P=parameters.par()
P.setPar(tipo='toy') #seta parametos para o código

def mod(z,p, modo = 'mpz'):
    '''Return Z mod P utilizando MPZ'''
    z=mpz(z)
    p=mpz(p)
    mod = z - mpz(z/p)*p
    if modo == 'mpz': return mod
    else: return int(mod)

def genZi(eta):
    '''retorna um inteiro aleatorio impar de eta bits'''
    eta=mpz(eta)
    seed=int(time.time()*1000000) #time em microseconds
    state=gmpy2.random_state(seed) 
    while True:
        p=gmpy2.mpz_rrandomb(state, eta)
        if gmpy2.is_odd(p): return p
        
def genPrime(b):
    '''função retorna um primo MPZ de b bits'''
    while True:
        seed=int(time.time()*1000000) #time em microseconds
        state=gmpy2.random_state(seed)
        prime=gmpy2.mpz_rrandomb(state,b)
        prime=gmpy2.next_prime(prime)
        if len(prime)==b: return prime
    

def genX0(p, _gamma, _lambda):
    '''gera o elemento q0 no intervalo [0, (2**gamma)/p) como sendo o produto de
    dois primos de lambda**2 bits e retorna x0 como sendo q0*p
    o retorno da função é uma lista [q0, x0]
    '''
    teto=gmpy2.f_div(2**mpz(_gamma), p) #divisão com retorno de inteiro
    while True:
        q0=genPrime(_lambda**2)*genPrime(_lambda**2)
        if q0 < teto: break
    x0=gmpy2.mul(p, q0)
    return q0, x0

def qrand(q0):
    return random.randint(0, q0) #confirmar intervalo

def rrand(rho):
    limit=2**rho
    return random.randint(-limit, limit)

    
def genX(beta, rho, p, q0):
    '''Gera uma lista de beta pares x[i,0], x[i,1] seguindo a formula
       x[i,b]=p.q[i,b]+r[i,b] | 1<i<beta, 0<b<1
       onde q[i,b] são aleatorios no intervalo [0, q0] e r[i,b] são
       inteiros aleatorios no intervalo (-2**p, 2**p)
    '''
    x=list()
    for i in range(beta*2):
        result = gmpy2.mul(p, qrand(q0))
        result = gmpy2.add(result, rrand(rho))
        x.append(result)
    return x
        
def genSk_(theta, thetam):
    l=math.ceil(math.sqrt(theta))
    s0=[1]+[0]*(l-1)
    s1=[1]+[0]*(l-1)
    k=range(1,int(math.sqrt(thetam))+1)
    k1=random.sample(k, 2)
    k2=random.sample(k, 3)
    
    k1.sort()
    k2.sort()
    B=math.floor(math.sqrt(theta/thetam))
    print(k1,k2,B)
    
    for k in k1:
        index=random.randint(k*B+1,(k+1)*B)-1
        s0[index]=1
    for k in k2:
        index=random.randint(k*B+1,(k+1)*B)-1
        if index > len(s1)-1: index=random.randint(len(s1)-4, len(s1)-1)
        s1[index]=1
    return s0, s1

def genSk(theta, thetam):
    l=math.ceil(math.sqrt(theta)) #comprimento do vetor s
    s0 = [1]+[0]*(l-1)
    s1 = [1]+[0]*(l-1)
    k=range(0, 4)
    ks0=random.sample(k, 2)
    ks1=random.sample(k, 4)
    B=math.floor(math.sqrt(theta/thetam))
    for k in ks0:
        idx=random.randint((k*B)+1, (k+1)*B)
        s0[idx-1]=1 
    for k in ks1:
        idx=random.randint((k*B)+1, (k+1)*B)
        s1[idx-1]=1
    return s0, s1

def genU11(se, s0, s1, theta, kappa, p):
    '''função para gerar o elemento u(1,1)'''
    #gerar indices de elementos 1 dos vetores s0 e s1
    si, sj = list(), list()
    for i in range(len(s0)):
        if s0[i]==1: si.append(i)
    for j in range(len(s1)):
        if s1[j]==1: sj.append(j)
    #gerar matriz de raiz de thetha elementos
    l=math.ceil(math.sqrt(theta))
    matrix=[[0 for x in range(l)] for x in range (l)] #define o array bidimensinal
    #popula a matrix com numeros aleatorios em [0, 2^k+1]
    #utilizando o RNG do Python, com a semente se
    #por motivos de código, u[1][1] é gerado, mais depois substituido.
    random.seed(se)
    mx= 2**mpz(kappa+1)
    for i in range(l):
        for j in range(l):
            #matrix[i][j]=random.randint(0, mx-1)
            matrix[i][j]=random.getrandbits(kappa+1)
    matrix[0][0] = 0
    #computa somatorio
    xp=gmpy2.div(2**kappa,p)
    xp=mpz(gmpy2.round_away(xp))
    soma=xp%mx
    somatorio=0
    for i in si:
        for j in sj:
            somatorio += matrix[i][j]
    u=soma-somatorio
    return u

def encryptVector(s, p, q0, x0, rho):
    sigma=list()
    p2=2**rho
    for i in s:
        r = random.randint(-p2, p2)
        q = random.randint(0, q0-1)
        c = mod((i+2*r+p*q),x0)
        sigma.append(c)
    return sigma

def keygen(file, size='toy'):
    P.setPar(size)
    tempo=-time.time()

    p = genZi(P._eta)
    #print("p computado")
    q0, x0 = genX0(p, P._gamma, P._lambda)
    #print("q0,x0 computado")
    listaX = genX(P._beta, P._rho, p, q0)
    #print("listax computado")
    pkAsk = listaX
    pkAsk.insert(0, x0)
    #print("p* computado")
    while True:
        s0,s1=genSk(P._theta, P._thetam)
        if (s0.count(1)*s1.count(1)==15): break
        
    se=int(time.time()*1000) #seed para RNG
    _kappa=P._gamma+6 #variavel para o RNG, conforme pg9 coron
    u11=genU11(se, s0, s1, P._theta, _kappa, p)
    sigma0 = encryptVector(s0, p, q0, x0, P._rho)
    sigma1 = encryptVector(s1, p, q0, x0, P._rho)
    tempo+=time.time()
    #picle files
    
    public=fheKey.pk(pkAsk, se, u11, sigma0, sigma1, P)
    secret=fheKey.sk(s0, s1, P)
    fheKey.write(public, 'pk_pickle_'+file)
    fheKey.write(secret, 'sk_pickle_'+file)
    
    #write key to file
    f = open(file, 'w')
    f.write(("keygen executado em " +str(tempo) +" segundos"+'\n\n'))
    f.write(('p==' + str(p)+'\n\n'))
    f.write(('q0==' +str(q0)+'\n\n'))
    f.write(('pk*=='+str(pkAsk)+'\n\n'))
    f.write(('s0 =='+str(s0)+'\n\n'))
    f.write(('s1 =='+str(s1)+'\n\n'))
    f.write(('se =='+str(se)+'\n\n'))
    f.write(('u11 =='+str(u11)+'\n\n'))
    f.write(('sigma0 =='+str(sigma0)+'\n\n'))
    f.write(('sigma1 =='+str(sigma1)+'\n\n'))
    f.close
    print('arquivo salvo', file)
    
def testRoutine():
##    P.setPar('toy')
##    keygen('toy.txt')
##
##    P.setPar('small')
##    keygen('small.txt')
##
##    P.setPar('medium')
##    keygen('medium.txt')

    P.setPar('large')
    keygen('large.txt') ##no momento, esse teste estoura a ram do meu laptop

if __name__=='__main__':
    print("Biblioteca geradora de chaves. Função principal: keygen(file, [parametro de segurança)]")

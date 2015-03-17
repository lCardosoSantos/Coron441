import keyGen as key
import gmpy2

import random

##teste si coron-SAGE
def randSparse(n,h):
  v=[0 for i in range(n)]
  while sum(v)<h:
    i=random.randint(0,n) ##i=int(ZZ.random_element(n))
    if v[i]==0: v[i]=1
  return v

def sum2(li):
  empty=True
  for x in li:
    if empty:
      res=x
      empty=False
    else:
      res=res+x
  if empty:
    return 0
  else:
    return res

def testSi():
    B=150//15 #theta do toy e divisao inteira
    theta=15 #global nunca muda
   #self.s=[1]+[0 for i in range(B-1)]+sum2([randSparse(B,1) for i in range(theta-1)])
    s=[1]+[0 for i in range(B-1)]+sum2([randSparse(B,1) for i in range(theta-1)]) ##códgigo com list comprehension

    print(s)
    
##Teste PRIntegers
class PRIntegers: 	
  "A list of pseudo-random integers."
  def __init__(self,gam,ell):
    self.gam,self.ell=gam,ell
    self.li=[None for i in range(self.ell)]
    random.seed(0)
    self.se=0

  def __getitem__(self,i):
    return self.li[i]
    
  def __setitem__(self,i,val):
    self.li[i]=val

  def __iter__(self):
    random.seed(0)
    for i in range(self.ell):
      a=random.randint(0, 2**self.gam)
      if self.li[i]!=None:
        yield self.li[i]
      else:
        yield a

def testPR():
  p=PRIntegers(50, 10) #147456,150
  p[0]=0
  print('random number generator:')
  for i in p:
    print (i)
  print (p[2])

    
if __name__=='__main__':
    print('Escript de Testes')
    #print('teste si')
    #testSi()
    print('printegers')
    testPR()


#for i in range(10):
    #prime=key.genPrime(10)
    #if gmpy2.is_prime(prime) and len(prime)==10:
        #print("ok")
        #print(prime)
    #else: print('not ok')

#print('eta==', key.P._eta)
#for i in range(100):
    #zi=key.genZi(key.P._eta)
    #if gmpy2.is_odd(zi):print('eta valido')
    #else: print('eta invalido')


    #b=key.mod(10,5)
#c=key.mod(20,15)

#print(b)
#print(c)

import pickle
'''
biblioteca que implementa as classes para a chave publica e privada, além
das funções necessarias para escrever e ler esses objetos, usando pickle
'''
class pk():
    '''clase para armazenar a chave privada'''
    def __init__(self, pkAsk, se, u11, sigma0, sigma1, P):
        self.pkAsk=pkAsk
        self.se=se
        self.u11=u11
        self.sigma0=sigma0
        self.sigma1=sigma1
        self.P=P

class sk():
    '''classe para armazenar a chave publica'''
    def __init__(self, sz, su, P):
        self.s0=sz
        self.s1=su
        self.P=P

def write(obj, name):
    '''faz uma coserva de obj no arquivo name'''
    with open(name, 'wb') as arq:
        pickle.dump(obj, arq)

def read(name):
    '''abre o pote name e retorna o pickles'''
    with open(name, 'rb') as arq:
        return pickle.load(arq)

if __name__=='__main__':
    '''classe de testes'''
    publicKey=pk(1,2,3,4,5, 'parametros')
    secretkey=sk(7,8, 'parametros')



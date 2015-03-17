class par:
    '''classe para armazenar os parametros utilizados no sistema homomorfico
    parametos indicados no trabalho de coron et. al.
    '''
    _lambda=42
    _rho   =16
    _eta   =1088
    _gamma =160000
    _beta  =12
    _theta =144
    _thetam=15
    def setPar(self, tipo):
        if tipo == 'toy':
            self._lambda=42
            self._rho   =16
            self._eta   =1088
            self._gamma =160000
            self._beta  =12
            self._theta =144

        elif tipo == 'small':
            self._lambda=52
            self._rho   =24
            self._eta   =1632
            self._gamma =86000
            self._beta  =23
            self._theta =533

        elif tipo == 'medium':
            self._lambda=62
            self._rho   =32
            self._eta   =2176
            self._gamma =4200000
            self._beta  =44
            self._theta =1972

        elif tipo == 'large':
            self._lambda=72
            self._rho   =39
            self._eta   =2652
ria            self._gamma =19000000
            self._beta  =88
            self._theta =7897
        else:
            print('invalid argument')
            quit(0)  # lint:ok

    def __init__(self, tipo='toy'):
        self.setPar(tipo)


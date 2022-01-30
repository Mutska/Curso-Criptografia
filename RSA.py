import random
import math

ALFABETO_ESP = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
val = [i for i in range(0, len(ALFABETO_ESP))]
letter_value = dict(zip (ALFABETO_ESP, val))
value_letter = dict(zip (val, ALFABETO_ESP))
class RSA():
    
    def __init__(self):
        self.n = 0
        self.p = 0
        self.q = 0
        self.phi = 0
        self.e = 0
        self.d = 0
    
    
    def generaClaves(self):
        self.p = self.getPrime()
        self.q = self.getPrime()
        self.n = self.getMod(self.p,self.q)
        self.phi = self.minEuler(self.p, self.q)
        self.e = self.getCoprime(self.phi)
        self.d = self.modInverse(self.e, self.phi)

    def printPublicKey(self):
        print("Public Key: ")
        print("(n, e) = (", end= ' ')
        print(self.n, end=',')
        print(self.e, end=')')
        print()

    def printPrivateKey(self):
        print("Private Key: ")
        print("(n, d) = (", end= ' ')
        print(self.n, end=',')
        print(self.d, end=')')
        print()
    def printPrimes(self):
        print("Primes used")
        print("p = ", end=' ')    
        print(self.p)
        print("q = ", end=' ')    
        print(self.q)


    def mod(self, a, m):
        return ((a % m) + m) % m

    def modPow(self,b, p, m):
        '''Función auxiliar para calcular b^p mod m'''
        if p == 0: return 1
        ans = self.modPow(b, p//2, m)
        ans = self.mod(ans*ans, m)
        if p % 2 == 1: ans = self.mod(ans*b, m)
        return ans

    def extEuclid(self, a, b):
        '''Algoritmo extendido de euclides'''
        xx, yy = 0, 1
        x, y = 1, 0
        while b != 0:
            q = a//b
            a, b = b, a%b
            x, xx = xx, x-q*xx
            y, yy = yy, y-q*yy
        return a, x, y

    def modInverse(self, b, m):
        '''Algoritmo para calcular el inverso modular'''
        d, x, y = self.extEuclid(b, m)
        if d != 1: return -1
        return self.mod(x, m)


    def checkComposite(self, n, a, d, s):
        '''Funcion Auxiliar del algoritmo Miller-Rabin'''
        x = self.modPow(a, d, n)
        if(x == 1 or x == n - 1): return False
        for r in range (1, s):
            x = x * x % n
            if(x == n - 1): return False
        return True

    def rand(self):
        '''Funcion Auxiliar del algoritmo Miller-Rabin'''
        return random.randint(0, 100000000000000000000000000000000000000000000000000)

    def millerRabin(self, n, iter):
        '''Algoritmo Miller-Rabin para verificar que un numero es primo'''
        if(n < 4):
            return (n == 2 or  n == 3)
        s = 0
        d = n - 1
        while(d & 1 == 0):
            d >>= 1
            s += 1
        for i in range(0, iter):
            a = 2 + self.rand() % (n - 3)
            if(self.checkComposite(n, a, d, s)): return False
        return True

    def getNumber(self):
        '''Funcion auxiliar que regresa un numero aleatorio de 50 digitos'''
        return random.randint(10000000000000000000000000000000000000000000000000,100000000000000000000000000000000000000000000000000)

    def getPrime(self):
        '''Funcion auxiliar que regresa un numero primo de 50 digitos'''
        while(True):
            p = self.getNumber()
            if(self.millerRabin(p, 10)):
                return p

    def getMod(self, p, q):
        '''Funcion auxiliar que calcula n=pq para RSA'''
        return p*q

    def minEuler(self, p, q):
        '''Funcion auxiliar calcula phi(n) = phi(pq) para RSA'''
        return (p-1)*(q-1)


    def getCoprime(self, phi):
        '''Funcion auxiliar que calcula un primo relativo de phi(n) = phi(pq) para RSA'''
        while(True):
            e = random.randint(2, phi - 1)
            d = math.gcd(e, phi)
            if(d == 1): return e

    def normaliza_texto(self, text):
        '''Función auxiliar para normalizar texto'''
        accents = {
        'Á':'A',
        'É':'E',
        'Ó':'O',
        'Ú':'U',
        'Í':'I'
        }
        clean_text = ''
        for char in text:
            if (char in accents):
                clean_text+=accents[char] 
            else: 
                clean_text+=char
        return clean_text


    def codigo(self, c):
        '''Función auxiliar para encontrar la representacion numerica de una letra'''
        return letter_value[c]
    def value(self, n):
        '''Función auxiliar para encontrar la representacion de letra de un numero'''
        return value_letter[n]
    def convierte_a_numeros(self, texto):
        '''Función auxiliar para pasar de texto a representacion numérica'''
        return [self.codigo(c) for c in texto]
    def convierte_a_texto(self, numeros):
        '''Función auxiliar para pasar de representacion numérica a texto'''
        return [self.value(n) for n in numeros]

    def cifrado(self, mensaje):
        '''Función auxiliar para cifrar un mensaje'''
        cipher_list = []
        clear_list = self.convierte_a_numeros(mensaje)
        for number in clear_list:
            new_number = self.modPow(number, self.e, self.n)
            cipher_list.append(new_number)
        return cipher_list

    def descifrado(self, mensaje_cifrado):
        '''Función auxiliar para descifrar un mensaje'''
        clear_list = []
        cipher_list = mensaje_cifrado
        for number in cipher_list:
            new_number = self.modPow(number, self.d, self.n)
            clear_list.append(new_number)
        
        mensaje_descifrado = self.getText(self.convierte_a_texto(clear_list))
        return mensaje_descifrado

    def getText(self,l):
        return ''.join(l)

if __name__ == '__main__':
    #Nombre: Marco Antonio Velasco Flores 418004087 (mi compañero deserto :*( )
    #1._ Creamos una instance de RSA
    cypher = RSA()
    #2._ Generamos las claves y variables necesarias para RSA
    # (suponiendo que dos personas estan de acuerdo con las claves generadas)
    cypher.generaClaves()
    #3._ Se imprimen las claves y los primos usados 
    cypher.printPublicKey()
    cypher.printPrivateKey()
    cypher.printPrimes()
    #Ciframos el mensaje
    cifrado = cypher.cifrado("HELLO") #Suponemos que el texto pasado esta junto y sin espacios
    print("Texto cifrado: ")
    print(cifrado)
    #Desciframos el mensaje
    descifrado = cypher.descifrado(cifrado)
    print("Texto descifrado: ")
    print(descifrado)
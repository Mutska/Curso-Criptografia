import random
import math

class ECF():    

    def __init__(self):
        #punto al infinito
        self.infinity = [0, 1]

    def mod(self, a, m):
        '''Función auxiliar para obtener siempre el modulo positivo'''
        return ((a % m) + m) % m

    def extEuclid(self,a, b):
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
        d, x, _ = self.extEuclid(b, m)
        if d != 1: return -1
        return self.mod(x, m)

    def getLambda(self,P1, P2,a, m):
        '''Funcion auxiliar para calcular lambda'''
        x1 , y1  = P1
        x2 , y2  = P2
        x, y = 0, [] 
        if P1 == P2:
            x = (3*(x1**2) + a)
            y = self.modInverse(2*y1, m), 1
        else:
            x = self.mod(y2 - y1, m)
            y = self.modInverse(x2 - x1, m), 2
        if y[0] == -1:
            if y[1] == 1:
                return self.mod(2*y1, m), 0
            else:
                return self.mod(x2 - x1, m), 0
        Lambda = self.mod(x*y[0], m), 1
        return Lambda

    def pointAddition(self, P1, P2, a, m):
        '''Funcion auxiliar para calcular la adicion de dos puntos'''
        if P1 == self.infinity:
            return P2, -1
        if P2 == self.infinity:
            return P1, -1
        x1 , y1  = P1
        x2 , y2  = P2
        if x1 == x2 and self.mod(y1 + y2, m) == 0:
            return self.infinity, -1
        Lambda = self.getLambda(P1, P2, a,m)
        if Lambda[1] == 0:
            return self.infinity , Lambda[0]
        x3 = self.mod(Lambda[0]**2 - x1 - x2, m)
        y3 = self.mod(Lambda[0]*(x1 - x3) - y1, m)
        P3 = [x3, y3]
        return P3, -1

    def KP(self, P, a, m, K):
        '''Funcion auxiliar para calcular eficientenmente
           K veces el punto P usando la misma idea que
           exponienciacion binaria, computa KP en log(n)'''
        possible_factor = -1
        kp = self.infinity
        while K > 0:
            if K % 2 == 1:
                kp, possible_factor = self.pointAddition(P, kp, a, m)
            if possible_factor != -1:
                return self.infinity, possible_factor
            P, possible_factor = self.pointAddition(P, P, a, m)
            K  = K // 2
        return kp, possible_factor
    def factorize(self, n):
        '''Algoritmo de lenstra para factorizar n = pq'''
        print("n es {} ".format(n))
        # 1- Verificamos que 'n' no sea divisible por 2 o 3
        if self.mod(n, 2) == 0:
            print("Los factores de n son p = {} y  q = {}".format(2,n//2))
            print()
            return
        if self.mod(n, 3) == 0:
            print("Los factores de n son p = {} y  q = {}".format(3,n//3))
            print()
            return
        AC = 0
        maximum = 0
        attempts = 0
        while AC == 0:
            attempts += 1
            D = n
            a ,b , x, y = 0, 0, 0, 0
            while D == n:
                # 2- Escogemos a,x,y aleatorios entre 1 y n para construir nuestra curva
                a = random.randint(0, n-1)
                x = random.randint(0, n-1)
                y = random.randint(0, n-1)
                # 3- Calculamos b con = y^2 - x^3 - ax (mod n) 
                b = self.mod(y**2 - x**3 - a*x, n)
                # 4- Calculamos D = gcd(4a^3 + 27b^2, n), para verificar el discriminante con maximo comun divisor
                # Si 1 < D < n encontramos un factor no trivial de n
                # Si D == 1 continuamos con el algoritmo
                # Si D == n, buscamos una curva distinta
                D , _, _ = self.extEuclid(4*(a**3) + 27*(b**2), n)
            if 1 < D and D < n:
                print("Super suerte!!!")
                print("Los factores de n son p = {} y  q = {}".format(D,n//D))
                print("Encontrados en un maximo de {} intentos y un maximo de {} adiciones de puntos".format(attempts, maximum))
                print()
                AC += 1
            # 5- Sea E : y^2 = x^3 + ax + b, escogemos P = (x, y) un punto sobre la curva
            P = [x,y]
            # 6- Escogemos arbitrariamente una cota 'k' para empezar el calculo
            # 7- Calculamos kP(mod n)
            k = 2
            while k < 200:
                P, possible_factor = self.KP(P,a, n,k)
                if P == self.infinity:
                    factor, _, _ =  self.extEuclid(possible_factor, n)
                    maximum  = max(maximum, k)
                    if factor != 1 and factor != n:
                        p = factor
                        q = n // factor
                        print("Los factores de n son p = {} y  q = {}".format(p,q))
                        AC += 1
                    break
                k += 1
            # 8- Si no hay suerte intentamos de nuevo desde el principio
        print("Encontrados en un maximo de {} intentos y un maximo de {} adiciones de puntos".format(attempts, maximum))
        print()

if __name__ == '__main__':
    #Nombre: Marco Antonio Velasco Flores 418004087
    lenstra = ECF()
    #Ejemplo sobre numeros compuestos n=pq tomados de https://primes.utm.edu/lists/small/millions/:
    composite_numbers =[
        62, # 2 * 31
        21, # 3, 7
        802801, # 3359 * 239
        1177, # 107 * 11
        208374996624377839, #  275604541 * 756065179
        110104192630333877, #  613651349 * 179424673
        944871823102126331, #  982451653 * 961748927
        4039884295347256900771 # 47026280551*85906949221
        #este ultimo numero compuesto puede tardar dependiendo de
        #la suerte que tengas en encontrar una bonita curva, si se tarda es mejor
        #hacer el reset
    ]
    for n in composite_numbers:
        lenstra.factorize(n)
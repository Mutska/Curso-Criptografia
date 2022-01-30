import math

ALFABETO_ESP = 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZ'
val = [i for i in range(0, len(ALFABETO_ESP))]
letter_value = dict(zip (ALFABETO_ESP, val))
value_letter = dict(zip (val, ALFABETO_ESP))
N = len(ALFABETO_ESP)

class Hill():

    def __init__(self, clave):
        self.clave = clave
        self.dimension = math.sqrt(len(self.clave))

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

    def cifrado(self, mensaje, clave= None):
        '''
        Aplica el cifrado por el metodo de Hill
        Arguments:
            mensaje: string-- el mensaje a cifrar
            clave: string / None-- la clave para cifrar, si no se define
                                    se usa el atributo de clase
        ------------
        Returns:
            texto_cifrado: string
        '''
        if clave != None: self.clave = clave
        texto_plano = mensaje.upper().replace(' ', '')
        texto_plano = self.normaliza_texto(texto_plano)
        k = self.crea_matriz_k(texto_plano,self.clave)
        self.k = k
        texto_cifrado = []
        if(len(texto_plano) % self.dimension == 0):
            conversion = self.convierte_a_numeros(texto_plano)
            cachitos = self.crea_matriz(conversion, int(self.dimension))
            for cacho in cachitos:
                row = self.mult_matrix(k,self.fila_a_columna(cacho))
                row = self.columna_a_fila(row)
                row = self.convierte_a_texto(row)
                texto_cifrado += row
        return ''.join(texto_cifrado)

    def fila_a_columna(self, row):
        '''Función auxiliar para pasar de 1Xm a mX1'''
        col  = [ [] for _ in range(len(row)) ]
        for i,val in enumerate(row):
            col[i].append(val)
        return col

    def columna_a_fila(self, col):
        '''Función auxiliar para pasar de mX1 a 1Xm'''
        flatten_list = [j for sub in col for j in sub] 
        return flatten_list
    
    def descifrado(self, mensaje_cifrado):
        '''
        Aplica el descifrado por el metodo de Hill
        Arguments:
            mensaje_cifrado: string-- el mensaje a descifrar
        ------------
        Returns:
            texto_descifrado: string
        '''
        k = self.k
        adj = self.crea_matriz_adjunta(k,int(self.dimension))
        d = self.mod(self.determinante(k,int(self.dimension)),N)
        inverse = self.inverso_modular(d, N)
        K_I = [ [0] * int(self.dimension) for _ in range(int(self.dimension))]
        for i  in range(0,int(self.dimension)):
            for j in range(0,int(self.dimension)):
                K_I[i][j] = self.mod(adj[i][j] * inverse, N)
        mensaje_cifrado = mensaje_cifrado.upper().replace(' ', '')
        conversion = self.convierte_a_numeros(mensaje_cifrado)
        cachitos = self.crea_matriz(conversion, int(self.dimension))
        texto_descifrado = []
        for cacho in cachitos:
            row = self.mult_matrix(K_I,cypher.fila_a_columna(cacho))
            row = self.columna_a_fila(row)
            row = self.convierte_a_texto(row)
            texto_descifrado += row
        return ''.join(texto_descifrado)

    def crea_matriz_k(self, mensaje,clave):
        '''
        Crea la matriz K de cifrado para Hill,
        valida que la matriz pueda ser invertible
        y el mensaje sea multiplo de N
        Arguments:
            mensaje: string -- el mensaje a cifrar
            clave: string -- la clave para cifrar
        ------------
        Returns:
            matriz_k: matiz -- la matriz cuadrada K de NxN
        '''
        if(self.verifica_longitud(len(clave))): 
            if(len(mensaje) % self.dimension == 0):
                conversion =  self.convierte_a_numeros(clave)
                matriz_k = self.crea_matriz(conversion, int(self.dimension))
                if(self.es_invertible(matriz_k)):
                    return matriz_k
                else:
                    print("La matriz no es invertible")
            else:
                print("La longitud del mensaje no es divisible por la dimension de la matriz de cifrado")
        else:
            print("No se puede crear una matriz cuadrada")
                
    def convierte_a_numeros(self, texto):
        '''Función auxiliar para pasar de texto a representacion numérica'''
        return [self.codigo(c) for c in texto]

    def convierte_a_texto(self, numeros):
        '''Función auxiliar para pasar de representacion numérica a texto'''
        return [self.value(n) for n in numeros]

    def codigo(self, c):
        '''Función auxiliar para encontrar la representacion numerica de una letra'''
        return letter_value[c]
    def value(self, n):
        '''Función auxiliar para encontrar la representacion de letra de un numero'''
        return value_letter[n]

    def crea_matriz(self, l, n):
        '''
        Función auxiliar para crear matrices
        a partir de un input l
        Arguments:
            l: list -- un vector con el contenido
            n: int -- las columnas
        ------------
        Returns:
            matriz: matiz -- la matriz de nXl
        '''
        matriz = []
        for i in range (0, len(l), n):
            matriz.append(l[i:i+n])
        return matriz

    def verifica_longitud(self, longitud):
        '''Función auxiliar para verificar que la longitud de la clave sea un cuadrado perfecto'''
        raiz = math.sqrt(longitud)
        return (raiz - math.floor(raiz) == 0)
        
    def mult_matrix(self, A, B):
        '''
        Funcion auxiliar para el producto de 2 matrices
        arguments:
            A: matriz n*m
            B: matriz m*j
        Returns:
            producto: matriz n*j
        '''
        if(len(A[0]) != len(B)): print('Error, matrices de dimensión incorrecta para producto')
        producto  = [ [0] * (len(B[0])) for _ in range(len(A)) ]
        for i in range(len(A)):
          for j in range(len(B[0])):
              for k in range(len(B)):
                  producto[i][j] += A[i][k] * B[k][j]
              producto[i][j] = producto[i][j] % N
        return producto

    def es_invertible(self, matriz):
        '''
        Funcion auxiliar para determinar si una matriz es invertible
        arguments:
            matriz: matriz
        Returns:
            Boolean: si es invertible o nó
        '''
        return self.determinante(matriz, int(self.dimension)) != 0
    
    def calcula_cofactor(self, K, T, p, q, N):
        '''
        Funcion auxiliar para calcular el cofactor
        de una matriz T, se cambia los valores de T
        arguments:
            K: matriz
            T: matriz
            p: int -- indice de matriz
            q: int -- indice de matriz
            N: int -- dimensión
        Returns:
            None: None -- cambios en T por paso por referencia
        '''
        i = 0
        j = 0
        for row in range(0,N):
            for col in range(0, N):
                if(row != p and col != q):
                    T[i][j] = K[row][col]
                    j = j + 1
                    if(j == N - 1):
                        j = 0
                        i = i + 1

    def crea_matriz_adjunta(self, K, N):
        '''
        Funcion auxiliar para calcular la matriz
        adjunta de K
        arguments:
            K: matriz
            N: int -- dimensión
        Returns:
            Adj: matriz -- matriz adjunta de K
        '''
        sign = 1
        T = [ [0] * N for _ in range(N)]
        Adj = [ [0] * N for _ in range(N)]
        if(N == 1):
            Adj[0][0] = 1
            return Adj
        for i in range(0, N):
            for j in range(0, N):
                self.calcula_cofactor(K, T, i, j, N)
                sign  = 1 if ((i + j) % 2 == 0) else -1
                Adj[j][i] = sign * self.determinante(T, N - 1)
        return Adj
        

    def determinante(self, A, N):
        '''
        2da Funcion auxiliar para calcular el determinante
        de una matriz A
        arguments:
            A: matriz
            N: int -- dimensión
        Returns:
            D: int -- determinante de A
        '''
        D = 0
        if(N == 1): return A[0][0]
        T = [ [0] * N for _ in range(N)]
        sign = 1
        for i in range(0,N):
            self.calcula_cofactor(A, T, 0, i, N)
            D += sign * A[0][i] * self.determinante(T, N - 1)
            sign  = -sign
        return D

    def mod(self, a, m):
        '''Función auxiliar para sacar módulos, incluso negativos '''
        return ((a % m) + m) % m

    def euclides(self, a, b):
        '''Algoritmo extendido de euclides'''
        xx, yy = 0, 1
        x, y = 1, 0
        while b != 0:
            q = a//b
            a, b = b, a%b
            x, xx = xx, x-q*xx
            y, yy = yy, y-q*yy
        return a, x, y


    def inverso_modular(self, b, m):
        '''Calculo del inverso modular'''
        d, x, y = self.euclides(b, m)
        if d != 1:
            return -1
        return self.mod(x, m)


        
if __name__ == '__main__':
    '''
    Autor(es): Daniel Villegas Aguilar, Marco Antonio Velasco Flores 
    '''

    cypher = Hill('FORTALEZA')
    cifrado = cypher.cifrado('CONSUL')
    print(cifrado)
    descifrado = cypher.descifrado(cifrado)
    print(descifrado)
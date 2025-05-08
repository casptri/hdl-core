class ECC:
    d = 33
    k = 6
    p = 1
    odd = 1
    b = d + k + p

    def printParameters(self):
        print("data bits:",self.d)
        print("reduncant bits:",self.k)
        print("extra parrity bit:",self.p)
        print("odd parrity:",self.odd)
        print("encoded data length:",self.b)

    def insertRedundantBits(self,value):
        r = self.k
        j = 0
        m = self.d
        res = value
        for i in range(1, m + r+1):
            if(i == 2**j):
                pos = 2**j
                mask = ~((1<<(pos-1)) -1)
                intermediat = res & mask
                intermediat = intermediat << 1
                res_mod = res%(1<<(pos-1))
                res = intermediat + res_mod
                j += 1
        return res

    def calcParity(self,data):
        n = self.k + self.d
        par = self.odd^1
        for i in range(n):
            if (data & 1<<i):
                par ^= 1
        return par

    def calcParityOfR(self,data,r):
        n = self.k + self.d
        par = self.odd
        bit = r-1
        for i in range(1,n+1):
            if (i&(2**bit)):
                if (data&(1<<(i-1))):
                    par ^= 1
        return par

    def encode(self,value):
        n = self.k + self.d
        r_data = self.insertRedundantBits(value)
        for i in range(1,self.k+1):
            par = self.calcParityOfR(r_data,i)
            set_bit = par << (2**(i-1)-1)
            r_data |= set_bit
        par = self.calcParity(r_data)
        r_data |= par << self.b - 1
        return r_data

    def decode(self,value):
        res = 0
        for i in reversed(range(1,self.k+1)):
            par = self.calcParityOfR(value,i)
            res = res << 1
            res |= par
        par = self.calcParity(value)
        par ^= (value>>self.b - 1)&1
        return (par,res)

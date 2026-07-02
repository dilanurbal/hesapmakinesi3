import math

class bilimsel:
    def __init__(self):
        self.pi = math.pi
        self.e = math.e
        self.modDerece = False

    def dereceYap(self):
        self.modDerece = True

    def radyanYap(self):
        self.modDerece = False

    def aci_cevir(self, x):
        return math.radians(x) if self.modDerece else x

    def sonuc_cevir(self, x):
        return math.degrees(x) if self.modDerece else x

    def sin(self, x):
        return math.sin(self.aci_cevir(x))

    def cos(self, x):
        return math.cos(self.aci_cevir(x))

    def tan(self, x):
        return math.tan(self.aci_cevir(x))

    def asin(self, x):
        if x < -1 or x > 1:
            return "Hata: Tanım kümesi dışında olamaz."
        return self.sonuc_cevir(math.asin(x))

    def acos(self, x):
        if x < -1 or x > 1:
            return "Hata: Tanım kümesi dışında olamaz."
        return self.sonuc_cevir(math.acos(x))

    def atan(self, x):
        return self.sonuc_cevir(math.atan(x))

    def ln(self, x):
        if x <= 0:
            return "Hata: logaritma 0 veya negatif sayı için hesaplanamaz."
        return math.log(x)

    def log(self, x, taban):
        if x <= 0 or taban <= 0 or taban == 1:
            return "Hata: geçersiz logaritma işlemi"
        return math.log(x, taban)

    def faktoriyel(self, x):
        if x < 0:
            return "Hata: faktoriyel negatif sayılar için hesaplanamaz."
        if not isinstance(x, int):
            return "Hata: faktoriyel sadece tam sayılar için hesaplanabilir."
        return math.factorial(x)

    def mod_alma(self, a, b):
        if b == 0:
            return "Hata: sıfıra göre mod alınamaz."
        return a % b



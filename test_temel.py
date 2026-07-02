import unittest
import math
from temel import sembol_cevir, hesapla, bicimlendir

class TestTemel(unittest.TestCase):

    def test_sembol_cevir_temel(self):
        # Temel çarpma, bölme ve üs çevirileri
        self.assertEqual(sembol_cevir("2×3"), "2*3")
        self.assertEqual(sembol_cevir("10÷2"), "10/2")
        self.assertEqual(sembol_cevir("2^3"), "2**3")

    def test_sembol_cevir_karekok(self):
        # Karekök dönüşüm testleri
        self.assertEqual(sembol_cevir("√16"), "math.sqrt(16)")
        self.assertEqual(sembol_cevir("√(16+9)"), "math.sqrt(16+9)")
        self.assertEqual(sembol_cevir("√√16"), "math.sqrt(math.sqrt(16))")
        self.assertEqual(sembol_cevir("√25×2"), "math.sqrt(25)*2")
        # Boşluklu durumlar için testler
        self.assertEqual(sembol_cevir("√ 16"), "math.sqrt(16)")
        self.assertEqual(sembol_cevir("√ (16+9)"), "math.sqrt(16+9)")

    def test_sembol_cevir_pi(self):
        # Pi sayısı dönüşümü
        self.assertEqual(sembol_cevir("π"), str(math.pi))
        self.assertEqual(sembol_cevir("π×2"), f"{math.pi}*2")

    def test_sembol_cevir_e_harfi(self):
        # Euler sayısı dönüşümü (bağımsız e ve kelime içi e testleri)
        self.assertEqual(sembol_cevir("e"), str(math.e))
        self.assertEqual(sembol_cevir("e×2"), f"{math.e}*2")
        self.assertEqual(sembol_cevir("2^e"), f"2**{math.e}")
        # İlişkisiz e harflerinin değişmemesi gerekir
        self.assertEqual(sembol_cevir("hesapla"), "hesapla")
        self.assertEqual(sembol_cevir("teste"), "teste")
        self.assertEqual(sembol_cevir("√e"), f"math.sqrt({math.e})")

    def test_hesapla_temel(self):
        # Temel hesaplamalar
        self.assertEqual(hesapla("2+3"), 5)
        self.assertEqual(hesapla("10-2×3"), 4)
        self.assertEqual(hesapla("2^3"), 8)

    def test_hesapla_karekok(self):
        # Karekök hesaplamaları
        self.assertEqual(hesapla("√16"), 4)
        self.assertEqual(hesapla("√(16+9)"), 5)
        self.assertEqual(hesapla("√√16"), 2)
        self.assertEqual(hesapla("√ 16"), 4)
        self.assertEqual(hesapla("√ (16+9)"), 5)

    def test_hesapla_sifira_bolme(self):
        # Sıfıra bölme hatası yönetimi
        self.assertEqual(hesapla("10÷0"), "Hata: Sıfıra bölme yapılamaz!")

    def test_hesapla_guvenlik_ve_gecersiz_karakter(self):
        # Güvenlik ve geçersiz karakter engelleme testleri
        self.assertTrue("Geçersiz karakter" in hesapla("abc"))
        self.assertTrue("Geçersiz karakter" in hesapla("import os"))
        self.assertTrue("Geçersiz karakter" in hesapla("__import__('os')"))
        self.assertTrue("Geçersiz karakter" in hesapla("eval('1+1')"))

    def test_bicimlendir(self):
        # Sayı biçimlendirme testleri
        self.assertEqual(bicimlendir(2.500000000001), 2.5)
        self.assertEqual(bicimlendir(3.00000000000001), 3)
        self.assertEqual(bicimlendir(5.0), 5)

if __name__ == "__main__":
    unittest.main()

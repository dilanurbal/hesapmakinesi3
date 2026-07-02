import pytest
import math

from bilimsel import bilimsel
# temel.py içinde sınıf olmadığı için doğrudan kullanacağımız fonksiyonu çağırıyoruz:
from temel import hesapla


@pytest.fixture
def bilimsel_motor():
    return bilimsel()


# --- BİLİMSEL İŞLEMLER TESTLERİ (Sınıf Yapısı) ---
def test_sabitler(bilimsel_motor):
    assert bilimsel_motor.pi == math.pi
    assert bilimsel_motor.e == math.e


def test_trigonometri(bilimsel_motor):
    bilimsel_motor.dereceYap()
    assert math.isclose(bilimsel_motor.sin(90), 1.0)
    assert math.isclose(bilimsel_motor.cos(180), -1.0)


def test_logaritma_ve_faktoriyel(bilimsel_motor):
    assert math.isclose(bilimsel_motor.log(100, 10), 2.0)
    assert bilimsel_motor.faktoriyel(5) == 120


def test_bilimsel_hatalar(bilimsel_motor):
    assert "Hata" in str(bilimsel_motor.ln(0))
    assert "Hata" in str(bilimsel_motor.faktoriyel(-5))
    assert "Hata" in str(bilimsel_motor.mod_alma(10, 0))


# --- TEMEL İŞLEMLER TESTLERİ (Fonksiyon Yapısı) ---
def test_temel_islemler():
    # hesapla() fonksiyonuna doğrudan string göndererek test ediyoruz
    assert hesapla("5+3") == 8
    assert hesapla("(5+3)×2") == 16
    assert hesapla("√(16)") == 4
    assert hesapla("2^3") == 8


def test_temel_hatalar():
    # Güvenlik ve sıfıra bölünme hataları
    assert "Hata" in str(hesapla("10÷0"))
    assert "Hata" in str(hesapla("abc"))
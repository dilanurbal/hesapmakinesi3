"""
ui.py — Bilimsel Hesap Makinesi Arayuzu (Tkinter)
==================================================
Bu modul SADECE arayuzdur. Hesaplamayi kendisi yapmaz.
Guncellemeler: 
 - 0 tusu genisletildi (colspan=2).
 - Nokta, Arti ve Esittir tuslari saga kaydirilarak klasik ergonomik duzene gecildi.
"""

import tkinter as tk
from tkinter import font as tkfont

from temel import hesapla, bicimlendir
from bilimsel import bilimsel


# ---------------------------------------------------------------------------
# Renk paleti (Koyu, dingin bir tema)
# ---------------------------------------------------------------------------
BG          = "#1a1b26"   # pencere arka plani
EKRAN_BG    = "#16161e"   # ekran arka plani
METIN       = "#c0caf5"   # ana metin
GECMIS_METIN= "#565f89"   # islem gecmisi metni (soluk mavi/gri)

SAYI_BG     = "#292e42"   # rakam tuslari
OP_BG       = "#3b4261"   # islem tuslari (+ - x /)
OP_FG       = "#7aa2f7"   # islem tusu yazisi (mavi)
BILIM_BG    = "#24283b"   # bilimsel tuslar
BILIM_FG    = "#7dcfff"   # bilimsel tus yazisi (camgobegi)

SIL_FG      = "#f7768e"   # C ve <- yazisi (kirmizi)
ESIT_BG     = "#e0af68"   # "=" arka plani (amber)
ESIT_FG     = "#1a1b26"   # "=" yazisi (koyu)
MOD_BG      = "#24283b"   # DER/RAD tusu arka plan
MOD_FG      = "#9ece6a"   # DER/RAD yazisi (okunabilir parlak yesil)


class HesapMakinesiUI:
    def __init__(self, kok):
        self.kok = kok
        self.motor = bilimsel()      
        self.motor.dereceYap()       

        self.ifade = ""              
        self.taze = False            

        self.kok.title("Bilimsel Hesap Makinesi")
        self.kok.configure(bg=BG)
        self.kok.minsize(380, 560)

        self._ekran_kur()
        self._tuslari_kur()
        self._klavye_kur()

        for c in range(5):
            self.kok.grid_columnconfigure(c, weight=1)
        for r in range(2, 9):
            self.kok.grid_rowconfigure(r, weight=1)

    # ------------------------------------------------------------------ ekran
    def _ekran_kur(self):
        kucuk_font = tkfont.Font(family="Segoe UI", size=13)
        self.gecmis_ekran = tk.Label(
            self.kok, text="", anchor="e", bg=EKRAN_BG, fg=GECMIS_METIN,
            font=kucuk_font, padx=24, pady=5
        )
        self.gecmis_ekran.grid(row=0, column=0, columnspan=5,
                               sticky="nsew", padx=10, pady=(12, 0))

        buyuk_font = tkfont.Font(family="Segoe UI", size=32, weight="bold")
        self.ekran = tk.Label(
            self.kok, text="0", anchor="e", bg=EKRAN_BG, fg=METIN,
            font=buyuk_font, padx=24, pady=5
        )
        self.ekran.grid(row=1, column=0, columnspan=5,
                        sticky="nsew", padx=10, pady=(0, 12))

    # ------------------------------------------------------------------ tuslar
    def _tuslari_kur(self):
        # (metin, satir, sutun, tur[, colspan])
        # YENİ DÜZEN: En alt satırda "0" 2 sütun kaplıyor.
        tanimlar = [
            ("DER", 2, 0, "mod"), ("C", 2, 1, "sil"), ("←", 2, 2, "sil"),
            ("(", 2, 3, "op"), (")", 2, 4, "op"),

            ("sin", 3, 0, "bilim"), ("cos", 3, 1, "bilim"), ("tan", 3, 2, "bilim"),
            ("ln", 3, 3, "bilim"), ("log", 3, 4, "bilim"),

            ("asin", 4, 0, "bilim"), ("acos", 4, 1, "bilim"), ("atan", 4, 2, "bilim"),
            ("x!", 4, 3, "bilim"), ("√", 4, 4, "bilim"),

            ("7", 5, 0, "sayi"), ("8", 5, 1, "sayi"), ("9", 5, 2, "sayi"),
            ("÷", 5, 3, "op"), ("^", 5, 4, "op"),

            ("4", 6, 0, "sayi"), ("5", 6, 1, "sayi"), ("6", 6, 2, "sayi"),
            ("×", 6, 3, "op"), ("π", 6, 4, "bilim"),

            ("1", 7, 0, "sayi"), ("2", 7, 1, "sayi"), ("3", 7, 2, "sayi"),
            ("−", 7, 3, "op"), ("e", 7, 4, "bilim"),

            # En alt satirdaki degisiklik burasi:
            ("0", 8, 0, "sayi", 2), (".", 8, 2, "sayi"), ("+", 8, 3, "op"),
            ("=", 8, 4, "esit"),
        ]

        renkler = {
            "sayi":  (SAYI_BG, METIN),
            "op":    (OP_BG, OP_FG),
            "bilim": (BILIM_BG, BILIM_FG),
            "sil":   (SAYI_BG, SIL_FG),
            "mod":   (MOD_BG, MOD_FG),
            "esit":  (ESIT_BG, ESIT_FG),
        }
        
        fontlar = {
            "sayi":  tkfont.Font(family="Segoe UI", size=17, weight="bold"),
            "op":    tkfont.Font(family="Segoe UI", size=17),
            "bilim": tkfont.Font(family="Segoe UI", size=13),
            "sil":   tkfont.Font(family="Segoe UI", size=15),
            "mod":   tkfont.Font(family="Segoe UI", size=13, weight="bold"),
            "esit":  tkfont.Font(family="Segoe UI", size=18, weight="bold"),
        }

        self.mod_btn = None
        for tanim in tanimlar:
            metin, satir, sutun, tur = tanim[:4]
            colspan = tanim[4] if len(tanim) > 4 else 1
            arka, on = renkler[tur]
            tus_font = fontlar[tur]

            b = tk.Button(
                self.kok, text=metin, font=tus_font, bg=arka, fg=on,
                bd=0, relief="flat", activebackground=self._acik(arka),
                activeforeground=on, cursor="hand2",
                command=lambda m=metin, t=tur: self._tikla(m, t)
            )
            b.grid(row=satir, column=sutun, columnspan=colspan,
                   sticky="nsew", padx=4, pady=4, ipady=6)

            b.bind("<Enter>", lambda e, w=b, a=arka: w.config(bg=self._acik(a)))
            b.bind("<Leave>", lambda e, w=b, a=arka: w.config(bg=a))

            if tur == "mod":
                self.mod_btn = b

    # ------------------------------------------------------ tus tiklama mantigi
    def _tikla(self, metin, tur):
        if tur == "esit":
            self._esittir()
        elif metin == "C":
            self.ifade = ""
            self.taze = False
            self.gecmis_ekran.config(text="")  
            self._guncelle()
        elif metin == "←":
            self.ifade = self.ifade[:-1]
            self._guncelle()
        elif tur == "mod":
            self._mod_degistir()
        elif tur == "bilim":
            self._bilimsel(metin)
        else:
            self._yaz(metin)

    def _yaz(self, s):
        if self.taze:
            if s in "+−×÷^":       
                self.taze = False
                self.gecmis_ekran.config(text=f"Ans = {self.ifade}")
            else:                   
                self.ifade = ""
                self.taze = False
                self.gecmis_ekran.config(text="")
        self.ifade += s
        self._guncelle()

    def _esittir(self):
        if not self.ifade.strip():
            return
        eski_ifade = self.ifade
        sonuc = hesapla(self.ifade)
        
        self.gecmis_ekran.config(text=f"{eski_ifade} =")
        self.ifade = "" if isinstance(sonuc, str) and sonuc.startswith("Hata") else str(sonuc)
        self._sonuc_goster(sonuc)

    def _bilimsel(self, ad):
        if ad == "π":
            self._yaz("π"); return
        if ad == "e":
            self._yaz("e"); return
        if ad == "√":
            self._yaz("√("); return   

        if not self.ifade.strip():
            return

        eski_ifade = self.ifade
        deger = hesapla(self.ifade)
        if isinstance(deger, str):          
            self._sonuc_goster(deger); self.ifade = ""; return

        islemler = {
            "sin": self.motor.sin, "cos": self.motor.cos, "tan": self.motor.tan,
            "asin": self.motor.asin, "acos": self.motor.acos, "atan": self.motor.atan,
            "ln": self.motor.ln,
            "log": lambda d: self.motor.log(d, 10),  
            "x!": self.motor.faktoriyel,
        }
        sonuc = islemler[ad](deger)

        self.gecmis_ekran.config(text=f"{ad}({eski_ifade}) =")

        if isinstance(sonuc, str):          
            self._sonuc_goster(sonuc); self.ifade = ""
        else:
            self.ifade = str(bicimlendir(sonuc))
            self._sonuc_goster(self.ifade)

    def _mod_degistir(self):
        if self.motor.modDerece:
            self.motor.radyanYap()
            self.mod_btn.config(text="RAD")
        else:
            self.motor.dereceYap()
            self.mod_btn.config(text="DER")

    # ------------------------------------------------------------- gosterim
    def _guncelle(self):
        self.ekran.config(text=self.ifade if self.ifade else "0")

    def _sonuc_goster(self, sonuc):
        if isinstance(sonuc, str) and sonuc.startswith("Hata"):
            self.ekran.config(text="Hata")  
        else:
            self.ekran.config(text=str(sonuc) if str(sonuc) else "0")
        self.taze = True

    # ------------------------------------------------------------- klavye
    def _klavye_kur(self):
        self.kok.bind("<Return>", lambda e: self._esittir())
        self.kok.bind("<BackSpace>", lambda e: (self._tikla("←", "sil")))
        self.kok.bind("<Escape>", lambda e: self._tikla("C", "sil"))
        for tus in "0123456789.+-()":
            self.kok.bind(tus, lambda e, t=tus: self._yaz(self._klavye_sembol(t)))
        self.kok.bind("*", lambda e: self._yaz("×"))
        self.kok.bind("/", lambda e: self._yaz("÷"))
        self.kok.bind("^", lambda e: self._yaz("^"))

    def _klavye_sembol(self, t):
        return "−" if t == "-" else t

    # ------------------------------------------------------------- yardimci
    @staticmethod
    def _acik(hex_renk):
        hex_renk = hex_renk.lstrip("#")
        r, g, b = (int(hex_renk[i:i+2], 16) for i in (0, 2, 4))
        r, g, b = (min(255, int(k * 1.25)) for k in (r, g, b))
        return f"#{r:02x}{g:02x}{b:02x}"


if __name__ == "__main__":
    kok = tk.Tk()
    uygulama = HesapMakinesiUI(kok)
    kok.mainloop()
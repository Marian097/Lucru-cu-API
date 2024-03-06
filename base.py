import sqlite3

class Conexiune_cu_baza_de_date:
    def __init__(self, baza_de_date) -> None:
        self.baza_de_date=baza_de_date
        self.conexiune=None
        self.cursor=None
        
        
    def connect_baza_de_date(self) :
        self.conexiune=sqlite3.connect(self.baza_de_date)
        self.cursor=self.conexiune.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tabel_depozit_initial (Suma REAL, Moneda string)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tabel_depozit_de_schimb (Suma REAL, Moneda string)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tabel_castig (Suma REAL, Moneda string)")
        self.conexiune.commit()
      
        
        
    def disconnect_baza_de_date(self):
        if self.conexiune:
            self.conexiune.close()
            
            

conexiune_cu_baza_de_date=Conexiune_cu_baza_de_date("base_exchange.db")

conexiune_cu_baza_de_date.connect_baza_de_date()
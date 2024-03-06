import requests
from base import Conexiune_cu_baza_de_date

api_key ='04a6bda4d6cd0128aa13dad1'
base_currency =input('Introduce-ti moneda: ')
endpoint = f'https://open.er-api.com/v6/latest/{base_currency}'

response = requests.get(endpoint, headers={'apikey': api_key})
data = response.json()

if response.status_code == 200:
    print(data)
    rates = data.get('rates')  
    if rates:
        print(rates)
    else:
        print("Cheia 'rates' nu a fost găsită în răspunsul API.")
else:
    print(f"Eroare {response.status_code}: {data['error']['info']}")



class Casa_de_schimb:
    def __init__(self) -> None:
        self.depozit={}
        self.rates=rates
        self.conexiune_bd=Conexiune_cu_baza_de_date("base_exchange.db")
   
    def adauga_suma(self):
        self.conexiune_bd.connect_baza_de_date()
        suma=float(input("Indroduce-ti suma pe care vreti sa o schimbati: "))
        self.depozit={suma: base_currency}
        self.conexiune_bd.cursor.execute("INSERT INTO tabel_depozit_initial(Suma, Moneda) VALUES (?, ?)", (suma, base_currency, ))
        self.conexiune_bd.conexiune.commit()
        if suma in self.depozit:
            print("Suma adaugata cu succes")
        else:
            print("Ceva nu a mers  bine.")
        self.conexiune_bd.disconnect_baza_de_date()
            
    def sterge_suma(self):
        self.conexiune_bd.connect_baza_de_date()
        print("Doriti sa nu mai efectuati tranzactia?")
        raspuns=input("Raspuns: ")
        if raspuns == "DA":
            self.conexiune_bd.cursor.execute("DELETE FROM tabel_depozit_initial")
            self.conexiune_bd.conexiune.commit()
            print("Suma returnata.")
        if raspuns =="NU":
            return
        self.conexiune_bd.disconnect_baza_de_date()
        
    def schimba_suma(self):
        self.conexiune_bd.connect_baza_de_date()
        comision=0.02
        self.conexiune_bd.cursor.execute("SELECT Suma FROM tabel_depozit_initial")
        suma=self.conexiune_bd.cursor.fetchone()
        moneda=input("Introduce-ti moneda in care vreti sa schimbati suma: ")
        suma_schimbata=suma[0] * self.rates.get(moneda)
        suma_dupa_comision=suma_schimbata * (1-comision)
        castig=suma_schimbata - suma_dupa_comision
        for cheie, valoare  in self.rates.items():
            if cheie == moneda:
                self.conexiune_bd.cursor.execute("DELETE FROM tabel_depozit_initial")
                self.conexiune_bd.conexiune.commit()
                self.conexiune_bd.cursor.execute("INSERT INTO tabel_depozit_de_schimb (Suma, Moneda) VALUES (?, ?)", (suma_dupa_comision, moneda, ))
                self.conexiune_bd.conexiune.commit()
                self.conexiune_bd.cursor.execute("INSERT INTO tabel_castig (Suma, Moneda) VALUES (?, ?)", (castig, moneda, ))
                self.conexiune_bd.conexiune.commit()
                print("Conversie resita.")
                break
        self.conexiune_bd.disconnect_baza_de_date()
        
        
        
        
        
casa_de_schimb=Casa_de_schimb()
casa_de_schimb.schimba_suma()


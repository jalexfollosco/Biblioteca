# Import
import main as m
import query_sql as sql
import sqlite3
import oggetti as o
import datetime

'''
Questo script è uno dei sotto menu del mainMenu, dove posso 
inserire o cancellare un'autore. 
Per inserire autore devo digitare il numero 1
Per cancellare autore devo digitare il numero 2
Per tornare al Menu Principale devo digitare il numero 0 
'''

def MenuAutore(conn):
    
    simboli = [0, 1, 2]
    
    print('\n\n\n|--------**{  MENU\' AUTORE   }**--------|')
    print('|                            |          |')
    print('|-Torna al Menù principale   |-> press 0|')
    print('|-Inserisci Autore           |-> press 1|')
    print('|-cancella Autore            |-> press 2|')
    print('|                            |          |')
    print('|---------------------------------------|\n')

# Controllo eccezioni    
    while True:
        try:
            scelta = int(input('Premi per scegliere: '))
            if scelta in simboli:
                break
        except ValueError:
            continue
        
    if scelta == 1:
        AddAutore(conn)
        MenuAutore(conn)
    elif scelta == 2:
        DeleteAutore(conn)
        MenuAutore(conn)
    elif scelta == 0:
        m.Menu(conn)

# Funzione  crea autore con annesso controllo sul formato date da inserire        
def crea_autore():
    print('inserisci un nuovo autore:')
    nome = input('nome:').title()
    cognome = input('cognome: ').title()
    while True:
        try:
            data_nascita = input('data di nascita: ')
            date_format = datetime.datetime.strptime(data_nascita,'%d-%m-%Y').date()
            break
        except ValueError:
            print('il formato della data deve essere %d-%m-%Y')
            continue
    luogo_nascita = input('luogo di nascita: ').title()
    note = (input('note (descrizione): '))
    autore = o.autore(nome, cognome, date_format, luogo_nascita, note)
    return autore
        

# Funzione aggiungi autore   
def AddAutore(conn):

    # Controlla se ne db è gia presente l'autore scelto
    while True:
        try:
            autore = crea_autore()
            sql.add_general(conn, autore)
            break
        except sqlite3.IntegrityError:
            print('hai inserito un Autore già presente nel Db')
            continue
    return

# Funzione elimina autore se l'autore da eliminare è presente nel db
def DeleteAutore(conn):
    while True:
        
        try:
            autore = input('inserisci l autore da cancellare: ').title()
            autore = autore.split()
            if tuple(autore) in sql.esegui(conn, 'select nome, cognome from autore'):
                sql.delete_general(conn, autore, 3)
                break
            else:
                print('questo autore non è presente nel db')
                continue
        except ValueError:
            continue
    

#--------TEST-----
if __name__ == '__main__':
    conn = sql.createDb()
    MenuAutore(conn)
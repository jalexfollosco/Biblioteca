# Import
import main as m
import query_sql as sql
import sqlite3
import oggetti as o
from datetime import date

'''
Questo script è uno dei sotto menu del mainMenu, dove posso 
inserire o cancellare un utente. 
Per inserire un utente digitare il numero 1
Per cancellare un utente digitare il numero 2
Per tornare al Menu Principale devo digitare il numero 0 
'''

def MenuUtente(conn):
    
    simboli = [0, 1, 2]
    
    print('\n\n\n|--------**{  MENU\' UTENTE   }**--------|')
    print('|                            |          |')
    print('|-Torna al Menù principale   |-> press 0|')
    print('|-Inserisci Utente           |-> press 1|')
    print('|-cancella Utente            |-> press 2|')
    print('|                            |          |')
    print('|---------------------------------------|\n')
    
    while True:
        try:
            scelta = int(input('Premi per scegliere: '))
            if scelta in simboli:
                break
        except ValueError:
            continue
        
    if scelta == 1:
        AddUtente(conn)
        MenuUtente(conn)
    elif scelta == 2:
        DeleteUtente(conn)
        MenuUtente(conn)
    elif scelta == 0:
        m.Menu(conn)

# Funzione per creare un utente        
def crea_utente():
    print('inserisci un nuovo utente:')
    nome = input('nome: ').title()
    cognome = input('cognome: ').title()
    registrazione = date.today()
    telefono = input('telefono: ') 
    email = (input('email: '))
    indirizzo = (input('indirizzo: '))
    utente = o.utente(nome, cognome, registrazione, telefono, email, indirizzo, numero_tessera = '')
    return utente


def AddUtente(conn):
    while True:
        try:
            utente = crea_utente()
            n_tessera = sql.add_general(conn, utente)
            print(f'il numero di tessera del nuovo utente è: {n_tessera}')
            break
        except sqlite3.IntegrityError:
            print('hai inserito un numero telefonico già resgistrato al db, reinserire utente con un numero diverso')
            continue
    return

# Funzione per eliminare un utente
def DeleteUtente(conn):
    while True:
        
        # Controllo eccezione sull'utente e sulla sua tessera per vedere se è presente nel db o
        # se per errore si è inserito un numero di tessera sbagliato
        try:
            utente = int(input('inserisci il numero di tessera dell utente da cancellare'))
            if utente in sql.estrazione(conn, 'utente', 'id_tessera'):
                sql.delete_general(conn, utente, 1)
                break
            else:
                print('questo utente non è presente nel db, oppure hai inserito il numero della tessera errato')
                continue
        except ValueError:
            continue
    

#--------TEST-----
if __name__ == '__main__':
    conn = sql.createDb()
    MenuUtente(conn)
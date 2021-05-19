# Import
import main as m
import query_sql as sql
import sqlite3

'''
Questo script è uno dei sotto menu del mainMenu, dove posso 
inserire o cancellare una categoria. 
Per inserire categoria devo digitare il numero 1
Per cancellare categoria devo digitare il numero 2
Per tornare al Menu Principale devo digitare il numero 0 
'''

def MenuCategoria(conn):
    
    simboli = [0, 1, 2]
    
    print('\n\n\n|--------**{ MENU\' CATEGORIA }**--------|')
    print('|                            |          |')
    print('|-Torna al Menù principale   |-> press 0|')
    print('|-Inserisci Categoria        |-> press 1|')
    print('|-cancella Categoria         |-> press 2|')
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
        AddCategoria(conn)
        MenuCategoria(conn)
    elif scelta == 2:
        DeleteCategoria(conn)
        MenuCategoria(conn)
    elif scelta == 0:
        m.Menu(conn)
        
# Funzione aggiungi categoria 
# Con controllo se la categoria è gia presente nel db  
def AddCategoria(conn):
    while True:
        try:
            categoria = input('inserisci una nuova categoria: ')
            sql.add_general(conn, categoria)
            break
        except sqlite3.IntegrityError:
            print('hai inserito una categoria già esistente')
            continue
    return

# Funzione elimina categoria
# Con controllo se la categoria da eliminare è presente nel database
def DeleteCategoria(conn):
    while True:
        
        categoria = input('inserisci la categoria da cancellare: ')
        if categoria in sql.estrazione(conn, 'categoria', 'nome'):
            sql.delete_general(conn, categoria, 0)
            break
        else:
            print('questa categoria non esiste')
            continue
        





#--------TEST-----
if __name__ == '__main__':
    conn = sql.createDb()
    MenuCategoria(conn)
    
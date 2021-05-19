# Import
import main as m
import oggetti as o
import datetime
import query_sql as sql
import sqlite3

'''
Questo script è uno dei sotto menu del mainMenu, dove posso 
inserire, cancellare o aggiornare un libro. 
Per inserire libro digitare il numero 1
Per cancellare libro digitare il numero 2
Per aggiornare libro digitare il numero 3
Per tornare al Menu Principale devo digitare il numero 0 
'''

def MenuLibro(conn):
    
    simboli = [0, 1, 2, 3]
    
    print('\n\n\n|--------**{   MENU\' LIBRO   }**--------|')
    print('|                            |          |')
    print('|-Torna al Menù principale   |-> press 0|')
    print('|-Inserisci Libro            |-> press 1|')
    print('|-cancella Libro             |-> press 2|')
    print('|-aggiorna Libro             |-> press 3|')
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
        AddLibro(conn)
        MenuLibro(conn)
    elif scelta == 2:
        DeleteLibro(conn)
        MenuLibro(conn)
    elif scelta == 3 :
        UpdateLibro(conn)
        MenuLibro(conn)
    elif scelta == 0:
        m.Menu(conn)
        

# Funzione per creare un libro        
def create_libro():
    print('inserisci un nuovo libro:')
    while True:
        # Controllo eccezione sull'ISBN
        try:
            isbn = int(input('isbn: '))
            if len(str(isbn)) == 13:
                break
            else:
                print('ISBN è formato da 13 cifre')
        except ValueError:
            continue
        
    titolo = input('titolo: ').title()
    lingua = input('lingua: ').title()
    editore = input('editore: ').title()
    
    while True:
        # Controllo eccezione sull'anno che dve essere di tipo intero
        try:
            anno = int(input('anno: '))
            if anno <= datetime.datetime.today().year:
                break
        except ValueError:
            continue
    
    while True:
        # Controllo eccezione sul numero di copie che deve essere di tipo intero
        try:
            copie = int(input('numero copie: '))
            break
        except ValueError:
            continue
        
    cat_libro = []
    # Ciclo che permette di inserire più catgorie per uno stesso libro
    while True:
        cat_libro.append(input('inserisci categoria: '))
        x = input('desideri inserire altre categorie? s/n')
        if x == 's':
            continue
        else: break

    aut_libro = []
    # Ciclo che permette di inserire più autori per uno stesso libro
    while True:
        aut_libro.append(input('inserisci autore/i: ').title())
        y = input('questo libro ha più di un autore? s/n')
        if y == 's':
            continue
        else: break
    libro = o.Libro(isbn,titolo, lingua,aut_libro, editore, anno, copie, cat_libro)
    return libro 

# Funzione per aggiungere un libro
def AddLibro(conn):
    while True:
        # Controllo eccezione se un libro che si vuole inserire è gia presente nel database
        try:
            libro = create_libro()
            sql.add_general(conn, libro)
            break
        except sqlite3.IntegrityError:
            print('hai inserito un Libro già presente nel Db')
            continue
    return

# Funzione per eliminare un libro
def DeleteLibro(conn):
    while True:
        # Controllo eccezione sull'ISBN per poter cancellare il libro
        try:
            libro = int(input('inserisci l\'ISBN del libro da cancellare: '))
            if libro in sql.estrazione(conn, 'libro', 'isbn'):
                sql.delete_general(conn,libro, 2)
                break
            else:
                print('questo libro non è presente nel db, oppure hai inserito un isbn errato')
        except ValueError:
            continue

# Funzione per aggiornare un libro
'''
Sotto Menu di aggiorna libro che permette di scegliere,
attraverso un'iserimento di valori da 0 a 3, il valore che 
si vuole aggiornare del libro scelto
'''

def UpdateLibro(conn):
    while True:
        # Controllo eccezione sull'ISBN che deve essere presente nel db
        try:
            libro = int(input('inserisci l\'ISBN del libro da aggiornare: '))

            if libro in sql.estrazione(conn, 'libro', 'isbn'):
                # Sotto menu
                print('premi 0 per aggiornare la lingua ')
                print('premi 1 per aggiornare l\'editore ')
                print('premi 2 per aggiornare l\'anno ')
                print('premi 3 per aggiornare il numero di copie')
                simboli = [0, 1, 2, 3]
                scelta = int(input('premi per scegliere: '))

                if scelta in simboli:
                    if scelta == 0:
                        campo = 'lingua'
                        valore = input('inserisci la lingua: ')
                    elif scelta == 1:
                        campo = 'editore'
                        valore = input('inserisci l\'editore: ')
                        break
                    elif scelta == 2:
                        campo = 'anno'
                        valore = int(input('inserisci l\'anno: '))
                    elif scelta == 3:
                        campo = 'copie'
                        valore = int(input('inserisci il numero di copie: '))
                    sql.update_libroDB(conn, libro, campo, valore)
                    break
            else:
                print('questo libro non è presente nel db, oppure hai inserito un isbn errato')
        except ValueError:
            continue
            
        
        
#--------TEST-----
if __name__ == '__main__':
    conn = sql.createDb()
    MenuLibro(conn)
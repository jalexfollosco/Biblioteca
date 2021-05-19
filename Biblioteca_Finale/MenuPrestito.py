# Import
import main as m
import query_sql as sql

'''
Questo script è uno dei sotto menu del mainMenu, dove posso 
prendere in prestito o restituire un libro. 
Per prendere in prestito un libro digitare il numero 1
Per restituire un libro digitare il numero 2
Per tornare al Menu Principale devo digitare il numero 0 
'''

# Funzione prestito tramite un menu a scelta multipla
def MenuPrestito(conn):
    
    simboli = [0, 1, 2, 3]
    
    print('\n\n\n|--------**{  MENU\' PRESTITO }**--------|')
    print('|                            |          |')
    print('|-Torna al Menù principale   |-> press 0|')
    print('|-Presta un Libro            |-> press 1|')
    print('|-Restituisci un Libro       |-> press 2|')
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
        PrestaLibro(conn)
        MenuPrestito(conn)
    elif scelta == 2:
        RestituzioneLibro(conn)
        MenuPrestito(conn)
    elif scelta == 0:
        m.Menu(conn)

# Funzione presta libro   
def PrestaLibro(conn):
    while True:

        # Controllo eccezione dell'ISBN per sapere se il libro è presente nella biblioteca
        try:
            libro_isbn = int(input('inserisci isbn libro'))
            if libro_isbn in sql.estrazione(conn, 'libro', 'isbn'):
                libro = sql.ricerca_libro(conn,libro_isbn)
                if libro.copie > 0:
                    break
                else:
                    print('questo libro non è disponibile al prestito, scegliere un altro libro')
                    continue
            else:
                print('questo isbn non è presente nel db.')
                continue
        except ValueError:
            continue
    
    while True:

        # Controllo eccezione sul utente per sapere se quest'ultimo ha gia in prestito il libro scelto
        try:
            utente = int(input('inserisci il numero di tessera dell utente'))
            if utente in sql.estrazione(conn, 'utente', 'id_tessera'):
                break
        except ValueError:
            continue
      
    isbn_utente = tuple((utente, libro.ISBN))
    if isbn_utente in sql.ricerca_prestito(conn, utente):
        print('l\' utente ha già in prestito questo libro')
    else:
        sql.prestito(conn, libro, utente)
        
    return

# Funzione restituzione libro
def RestituzioneLibro(conn):
    while True:
        
        # Controllo eccezione sull'ISBN per sapere se il libro risulta prestato
        try:
            libro_isbn = int(input('inserisci l isbn del libro da riconsegnare'))
            if libro_isbn in sql.estrazione(conn, 'prestito', 'isbn_libro'):
                libro = sql.ricerca_libro(conn,libro_isbn)
                break
            else:
                print('questo libro non risulta nei prestiti')
                continue
        except ValueError:
            continue
    
    while True:

        # Controlll eccezione sull'numero di tessera dell'utente
        # per sapere se quest'ultimo ha in prestio libri
        try:
            utente = int(input('inserisci il numero di tessera dell utente'))
            if utente in sql.estrazione(conn, 'prestito', 'tessera_id'):
                break
            else:
                print('numero di tessera inesistente')
                continue
        except ValueError:
            continue
        
    isbn_utente = tuple((utente, libro_isbn))
    if isbn_utente in sql.ricerca_prestito(conn, utente):
        sql.restituzione(conn,libro, utente)
        print('restituzione avvenuta con successo')
    else:
        print('non risulta che questo utente abbia preso in prestito questo libro')
        
    return

#--------TEST-----
if __name__ == '__main__':
    conn = sql.createDb()
    MenuPrestito(conn)
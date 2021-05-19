#MAIN

# Import
import query_sql as sql
import MenuCategoria as c
import MenuUtente as u
import MenuAutore as a
import MenuLibro as l
import MenuPrestito as p
import MenuRicerca as r
import sys

'''
In questo script abbiamo il Menu, con cui l'utilizzatore del programma 
può effettuare le chiamate con il database a seconda dell'iterazione che vuole svolgere.
Può svolgere queste azioni:
- Aggiungere, Cancellare, Modificare Libro
- Aggiungere, Cancellare Utente
- Aggiungere, Cancellare Autore
- Aggiungere, Cancellare Categoria
- Prestare, Restituire Libro
- Catalogo Libri
- Uscita dal programma
'''

# Menu principale accessibile tramite l'inserimento di 
# un numero intero corrispondente alla funzione da svolgere
def Menu(conn):
    
    simboli = [0, 1, 2, 3, 4, 5, 6, 7]
    
    print('\n\n\n|--------------**{ MENU\' PRINCIPALE }**--------------|')
    print('|                                        |           |')
    print('|-Aggiungi / Cancella / Modifica Libro   |-> press 1 |')
    print('|-Aggiungi / Cancella Utente             |-> press 2 |')
    print('|-Aggiungi / cancella Autore             |-> press 3 |')
    print('|-Aggiungi / Cancella Categoria          |-> press 4 |')
    print('|-Prestito / Restituzione Libro          |-> press 5 |')
    print('|-Ricerca Prestiti / Libri               |-> press 6 |')
    print('|-Catalogo                               |-> press 7 |')
    print('|-Exit                                   |-> press 0 |')
    print('|                                        |           |')
    print('|----------------------------------------------------|\n')
    

    # Controllo eccezioni
    while True:
        try:
            scelta = int(input('Premi per scegliere: '))
            if scelta in simboli:
                break
        except ValueError:
            continue
    
    if scelta == 1:
        l.MenuLibro(conn)
    elif scelta == 2:
        u.MenuUtente(conn)
    elif scelta == 3:
        a.MenuAutore(conn)
    elif scelta == 4:
        c.MenuCategoria(conn)
    elif scelta == 5:
        p.MenuPrestito(conn)
    elif scelta == 6:
        r.MenuRicerca(conn)
    elif scelta == 7:
        catalogo(conn)
        Menu(conn)
    elif scelta == 0:
        sys.exit()
        
    return 

# Funzione catalogo, mostra tutti i libri presenti nel database della biblioteca
def catalogo(conn):
    libri = sql.estrazione(conn, 'libro', 'isbn')
    for i in libri:
        libro = sql.ricerca_libro(conn, i)
        libro.view()

#------------TEST---------------
if __name__ == '__main__' :
    conn = sql.createDb()
    Menu(conn)
    
    




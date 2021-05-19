# vari import
import MenuAutore as a
import oggetti as o
import datetime
import sqlite3
import os

# CREAZIONE DB INIZIALE

def createDb():

    # creo un secondo db solo per l'esempio poichè esiste giò chinook.sqlite
    db_filename = 'bibliotecaDB1.db' 

    # Importo lo schema
    schema= 'biblioteca.sql'

    # importo il dml
    dml = 'dml_biblioteca.sql'
    schema_filename = os.path.abspath(schema)
    dml_filename = os.path.abspath(dml)
    
    db_is_new = not os.path.exists(db_filename)
    '''
    Se il data base e lo schema esistono non me li ricrea di nuovo, 
    altrimenti mi creerà il databse su SQLite con il file biblioteca.sql
    e lo popolerà con il file dml_biblioteca.sql 
    '''
    with sqlite3.connect(db_filename) as conn:

        if db_is_new:
            print('Creazione dello schema')
            with open(schema_filename, 'rt') as f:
                schema = f.read()
            conn.executescript(schema)
            f.close()
    
            print('Popolamento del db in corso...')

            with open(dml_filename, 'rt') as g:
                schema_dml = g.read()
            conn.executescript(schema_dml)
            g.close()
                    
        else:
            print('Il database esiste, si suppone che esista anche lo schema.')
            
    return conn

# Con il blocco with ci cauteliamo da errori imprevisti
# Cur.fetchall() restituisce tutte le righe come un elenco di tuple; 
# se non ci sono record da recuperare, viene restituito un elenco vuoto.
def esegui(conn,query, params=()):

    """
Esegue una query usando la connessione conn, e ritorna la lista di risultati 
ottenuti. In params, possiamo mettere una lista di parametri per la query. 
"""
    with conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

# La funzione estrazione estrarrà la colonna di una tabella e la metterà in una lista
def estrazione(conn, tabella, colonna):
    '''
    Estrae da una tabella del db, tutti gli elementi di una determinata colonna
    esempio --> estrazione("libro", "titolo")

    Parameters
    ----------
    tabella : str
        Inserire il nome di una tabella dello schema del db.
    colonna : str
        Inserire il nome di una colonna della tabella seguente.

    Returns
    -------
    zz : list

    '''

    zz = []
    estrai = f'SELECT {colonna} FROM {tabella}'
    tupla = esegui(conn, estrai)
    for estrai in tupla:         
        zz.append(estrai[0])
    return zz 

# La funzione id_generator crea i vari id (identificatori) degli oggetti --> utente, categoria, libro, autore
def id_generator(conn, oggetto): 
    '''
    Genera una chiave id per le classi utente, libro, autore e categoria.
    la  nuova chiave si ottiene sommando la chiave massima di 1.

    Parameters
    ----------
    oggetto : classe utente, str, Libro o autore.

    Returns
    -------
    idd : int.

    '''

    if oggetto.__class__.__name__ == 'utente':
        estrai = '''SELECT MAX(id_tessera) FROM utente;'''
    if oggetto.__class__.__name__ == 'str':
        estrai = '''SELECT MAX(id) FROM categoria;'''
    if oggetto.__class__.__name__ == 'Libro':
        estrai = '''SELECT MAX(id) FROM categoria;'''
    if oggetto.__class__.__name__ == 'autore':
        estrai = '''SELECT MAX(id) FROM autore;'''
    x = esegui(conn, estrai)
    idd = x[0][0] + 1
    return idd 

def add_general(conn,oggetto):
    '''
    La funzione add_general mi permetterà di inserire l'utente, la categoria, il libro e l'autore, 
    attraverso le query in SQL, senza creare funzioni in più inutili di aggiunta.
    Esegue le query sql di INSERT INTO per aggiungere un oggetto nel db. 
    In base al tipo di oggetto che si mette come parametro (Libro, utente, categoria, autore)
    esegue la query sulla tabella associata del db.

    Parameters
    ----------
    conn : connessione.
    oggetto : classe utente, str, Libro o autore.

    Returns
    -------
    codice : int
    restituisce la primary key generata.

    '''

    codice = id_generator(conn, oggetto)
    # Query per l'inserimento dell'utente
    query_utente = '''INSERT INTO utente (id_tessera, data_registrazione, nome, cognome, telefono, indirizzo, email) 
    values (?, ?, ?, ?, ?, ?, ?)'''

    # Query per l'inserimento della categoria
    query_categoria = '''INSERT INTO categoria (id, nome) values (?, ?)'''

    # Query per l'inserimento del libro
    query_libro = '''INSERT INTO libro (isbn, titolo, lingua, editore, anno, copie)
    values (?, ?, ?, ?, ?, ?)'''

    # Query per l'inserimento dell'autore del libro
    query_autore = '''INSERT INTO autore (id, nome, cognome, data_nascita, luogo_nascita, note) 
    values (?, ?, ?, ?, ?, ?)'''  
    
    # implementazione ad oggetti delle classi
    if oggetto.__class__.__name__ == 'utente':
        esegui(conn, query_utente,(codice,oggetto.registrazione, oggetto.nome, oggetto.cognome, oggetto.telefono, oggetto.indirizzo, oggetto.email))
        
    elif oggetto.__class__.__name__ == 'str': 
        esegui(conn, query_categoria,(codice,oggetto))
        
    elif oggetto.__class__.__name__ == 'Libro':
        esegui(conn, query_libro,(oggetto.ISBN, oggetto.titolo, oggetto.lingua, oggetto.editore, oggetto.anno, oggetto.copie))
        link = '''INSERT INTO bridge_categoria (isbn_libro, id_categoria) 
        values (?, ?)''' 

         # Questo ciclo for ci permette di aggiungere una nuova categoria se non presente nel DB
        cat_id = []
        for c in oggetto.categoria:
            if c not in estrazione(conn, 'categoria', 'nome'): 
                print(f'la categoria {c} non è presente nel db, creazione della nuova categoria in corso...')
                nuova_categoria = c

                # Crea nuova categoria e gli assegna un id nuovo grazie alla funzione if_generator
                key_id = id_generator(conn, nuova_categoria) 
                esegui(conn, query_categoria, (key_id, nuova_categoria))
                cat_id.append(key_id)
            else:
                # Fetch restituisce una tupla con solo gli id
                # e con cat_id estraggo il valore id della tupla 
                fetch = esegui(conn,'SELECT id FROM categoria WHERE nome = :cat ', {'cat' : c}) 
                cat_id.append(fetch[0][0])
        for cod in cat_id:
            esegui(conn, link, (oggetto.ISBN,cod))
        link_autore = '''INSERT INTO bridge_autore (isbn_libro, id_autore) 
        values (?, ?)''' 
        aut_id = []
        for c in oggetto.autore:
            if (tuple(c.split())) not in esegui(conn, 'SELECT nome,cognome FROM autore'): #crea nuovo autore
                 print(f'autore {c} non presente nel db, creazione del nuovo autore:\n')
                 new_autore = a.crea_autore()
                 autore_id = id_generator(conn, new_autore)
                 esegui(conn, query_autore, (autore_id, new_autore.nome, new_autore.cognome, new_autore.data_nascita, new_autore.luogo_nascita, new_autore.note)) 
                 aut_id.append(autore_id)
            else:
                fetch1 = esegui(conn,'SELECT id FROM autore WHERE nome = :n and cognome = :cn ', {'n' : c.split()[0], 'cn' : c.split()[1]})
                aut_id.append(fetch1[0][0])
        for cod_autore in aut_id:
                esegui(conn, link_autore, (oggetto.ISBN,cod_autore))
                
    elif oggetto.__class__.__name__ == 'autore':
        esegui(conn, query_autore,(codice, oggetto.nome, oggetto.cognome, oggetto.data_nascita, oggetto.luogo_nascita, oggetto.note)) 
    conn.commit()
    return codice

def delete_general(conn,row, table):
    '''
    La funzione delete_general mi permette di eliminare la categoria, l'utente e il libro, 
    attraverso le query in SQL, senza creare funzioni in più inutili di eliminazione.
    Esegue le query sql di DELETE per rimuovere una riga nel db. 
    
    Parameters
    ----------
    conn : connesione.
    row : int/str. riga da cancellare.
    table : INT
        valore --> 0 per cancellare nella tabella categoria del db
        valore --> 1 per cancellare nella tabella utente del db 
        valore --> 2 per cancellare nella tabella libro del db
        valore --> 3 per cancellare nella tabella autore del db
        
    Returns
    -------
    None.
    '''

    if table == 0:

        # Cancella la categoria solo se non è associata a più libri
        lista_categorie= esegui(conn, 'select * from categoria')
        for i in range(len(lista_categorie)):
            if row == lista_categorie[i][1]:
                id_categoria = lista_categorie[i][0]

        if id_categoria not in estrazione(conn, 'bridge_categoria', 'id_categoria'):
            cancella = '''DELETE FROM categoria WHERE nome = :category '''
            esegui(conn, cancella, {"category" :row})
            print('la categoria seguente è stata cancellata')
        else:
            print('la categoria seguente non può essere cancellata, perchè asoociata a uno o più libri')
            
    elif table == 1:

        # Cancella solo se l'utente non ha libri in prestito quindi non restituiti
        check_prestito= 'SELECT tessera_id FROM prestito WHERE data_restituzione is NULL AND tessera_id = :tessera'
        
        if len(esegui(conn, check_prestito, {'tessera':row})) > 0:
            print('L utente non può essere cancellata, perchè asoociata a uno o più libri in prestito')
        else:
            print('canccellato')
            cancella = '''DELETE FROM utente WHERE id_tessera = :userid '''
            esegui(conn, cancella, {"userid" :row}) 
            
    elif table == 2:

        # Cancella il libro solo se non è in prestito da un utente
        check_prestito= 'SELECT isbn_libro FROM prestito WHERE data_restituzione is NULL AND isbn_libro = :isbn'
        
        if len(esegui(conn, check_prestito, {'isbn':row})) > 0:
            print('Libro non può essere cancellato, perchè asoociata a uno o più utenti che l hanno preso in prestito')
        else:

            # Eliminazione in cascata 
            print('canccellato')
            cancella = '''DELETE FROM libro WHERE isbn = :isbn ''' 
            esegui(conn, cancella, {"isbn" :row})
            cascade_categoria= '''DELETE FROM bridge_categoria WHERE isbn_libro = :isbn '''
            esegui(conn, cascade_categoria, {"isbn" :row})
            cascade_autore = '''DELETE FROM bridge_autore WHERE isbn_libro = :isbn '''
            esegui(conn, cascade_autore, {"isbn" :row})
            cascade_prestito = '''DELETE FROM prestito WHERE isbn_libro = :isbn '''
            esegui(conn, cascade_prestito, {"isbn" :row})
            
    elif table == 3:

        # Cancella l'autore se non è associato a più libri
        get_id = esegui(conn,'SELECT id FROM autore WHERE nome = :nome AND cognome = :cognome',{'nome':row[0], 'cognome':row[1]})
        get_id= get_id[0][0]
        if get_id not in estrazione(conn, 'bridge_autore', 'id_autore'):
            cancella = '''DELETE FROM autore WHERE id = :id '''
            esegui(conn, cancella, {"id" :get_id})
            print('l autore seguente è stato cancellato')
        else:
            print('l autore seguente non può essere cancellato, perchè associato a uno o più libri')
                
    conn.commit()
    return

# Funzione ricerca_libro permette di inserire il risultato, ottenuto attraverso
# una query SQL, nella variabile ricerca per la visualizzazione
def ricerca_libro (conn,ricerca):
    '''
    Ricerca il libro (tramite isbn) all'interno del database e restituisce un oggetto libro

    Parameters
    ----------
    conn : connessione.
    ricerca : int. 

    Returns
    -------
    libro : classe libro.

    '''

    concat = '''SELECT libro.isbn, libro.titolo, libro.lingua, libro.editore, libro.anno, libro.copie, group_concat(distinct categoria.nome), group_concat(distinct autore.cognome)
                FROM libro
                join bridge_categoria ON libro.isbn = bridge_categoria.isbn_libro
                join categoria ON categoria.id = bridge_categoria.id_categoria
                join bridge_autore ON libro.isbn = bridge_autore.isbn_libro
                join autore ON autore.id = bridge_autore.id_autore
                WHERE libro.isbn = :filtro
                group by libro.isbn '''
    cursor = conn.cursor()
    cursor.execute(concat, {'filtro': ricerca})
    isbn, titolo, lingua, editore, anno, copie, categorie, autori = cursor.fetchone()
    libro = o.Libro(isbn,titolo, lingua,autori, editore, anno, copie, categorie)
    return libro 

# Funzione che ricerca i ritardi per la riconsegna del libro
def ritardi(conn, utente):

    '''
    Cerca nel db i libri presi in prestito dall'utente che non sono stati restituiti entro la data di
    scadenza.

    Parameters
    ----------
    conn : connessione
    utente : int
        Numero di tessera dell'utente.

    Returns
    -------
    ritardi_isbn : list
        Fornisce una lista degli isbn dei libri non consegnati entro la data 
        di scadenza.

    '''

    check_ritardi= 'SELECT data_prestito FROM prestito WHERE data_restituzione is NULL AND tessera_id = :tessera'
    data_prestiti = []
    ritardi_isbn = []
    for estrai in esegui(conn, check_ritardi, {'tessera' :utente}): 

        #estrae dal db la data e la aggiunge in una lista trasformandola da str a data
        data_prestiti.append(datetime.datetime.strptime(estrai[0], "%Y-%m-%d").date()) 
    
    for data in data_prestiti:
        scadenza = data + datetime.timedelta(days = 30)
        if scadenza <= datetime.date.today():
            delays = esegui(conn, 'SELECT isbn_libro FROM prestito WHERE data_prestito = :date',{'date':data})
            ritardi_isbn.append(delays[0][0])
            
    return ritardi_isbn

# Funzione per prendere in prestito un libro
def prestito(conn, libro, utente):
    '''
    Inserisce nel db il libro e l'utente che lo ha preso in prestito,
    calcola la data di prestito e di restituzione del libro (30 gg) e aggiorna il numero
    di copie del libro presi in prestito.

    Parameters
    ----------
    conn : connessione
    libro : classe libro.
    utente : int
            numero tessera utente.

    Returns
    -------
    None.

    '''

    check_prestito= 'SELECT tessera_id FROM prestito WHERE data_restituzione is NULL AND tessera_id = :tessera'
    if len(esegui(conn, check_prestito, {'tessera':utente})) < 5:
        n_ritardi = len(ritardi(conn,utente))
       
        if n_ritardi == 0:
            now = datetime.date.today()
            # I giorni massi per l'uso frutto del libro sono 30
            riconsegna = now + datetime.timedelta(days = 30)

            query = '''INSERT INTO prestito(isbn_libro, tessera_id, data_prestito, data_restituzione)
            values(?, ?, ?, NULL)'''
            esegui(conn, query, (libro.ISBN, utente, now))

            update_copie = '''UPDATE libro SET copie = :n_copie WHERE isbn = :filtro'''
            esegui(conn, update_copie, {'n_copie': libro.copie-1, 'filtro': libro.ISBN})
            print(f'l utente deve risconsegnare il libro entro il: {riconsegna}')
        else:
            print('l utente non può prendere in prestito i libri in quanto ha dei ritardi nella riconsegna')
    
    else:
        print('l utente ha raggiunto il massimo di libri concesi in prestito')
    
    conn.commit()
    return

# Funzione aggiorna libro
def update_libroDB(conn, libro, campo, valore):
    '''
    aggiorna un campo della tabella libro (lingua, editore, anno o copie) del db

    Parameters
    ----------
    conn : connessione.
    libro : int
        isbn del libro.
    campo : str
        mettere il nome del campo da aggiornare (lingua, editore, anno o copie).
    valore : int/ str
        valore desiderato da aggiornare.

    Returns
    -------
    None.

    '''
    query= f'UPDATE libro SET {campo} = :valore WHERE isbn = :filtro '
    esegui(conn, query, {'valore': valore, 'filtro': libro})
    conn.commit()
    
    return

# Funzione restituzione di un libro
def restituzione(conn, libro, utente):
    

    update_copie = '''UPDATE libro SET copie = :n_copie WHERE isbn = :filtro'''
    esegui(conn, update_copie, {'n_copie': libro.copie+1, 'filtro': libro.ISBN})

    riconsegna = datetime.date.today()
    query = '''UPDATE prestito SET data_restituzione = :data 
    WHERE isbn_libro = :filtro AND tessera_id = :filtro2 '''

    esegui(conn, query, {'data': riconsegna, 'filtro': libro.ISBN, 'filtro2': utente})
    conn.commit()
    
    return

# Funzione per ricercare i prestiti
def ricerca_prestito(conn, utente):
    
    query='SELECT tessera_id, isbn_libro FROM prestito WHERE data_restituzione is NULL AND tessera_id = :tessera'
    x = esegui(conn, query, {'tessera':utente})
    return x

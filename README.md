# sql-exporter
Esporta dati da query a file csv a host ftp

## DIPENDENZE:
* per sqlite dbs: none
* per mssql dbs: pymssql v. 2.1

## UTILIZZO
Da riga di comando:

	python exporter.py
	
	
Lo script necessita di file di configurazione nella stessa cartella chiamato `config.json` con la seguente struttura



	{

	    "db" : {
	        "type" : "sqlite",
	        "database" : "test.sqlite"

	    },

	    "ftp" : {
	        "host" : "some.ftp.net",
	        "user" : "anonymous",
	        "password" : "someone@somewhere.com",
	        "cwd" : "incoming"
	    },

	    "queries" : [
	        {   
	            "sql" : "CREATE TABLE IF NOT EXISTS test2 as SELECT * FROM test"
	        },

	        { 
	            "sql" : "SELECT * FROM test",
	            "csv" : "out_[%Y_%m_%d__%H_%M_%S].csv"
	        },

	        {
	            "sql" : "DROP TABLE test2"
	        }

    	]

	}
	
	
## CONFIGURAZIONE

### DATABASE
I parametri di connessione a db sono nell'oggetto db:

* type: il tipo di db (`sqlite` o `mssql`)
* user
* password
* database (nome file per sqlite)
* host


### FTP
I parametri di connessione a ftp sono nell'oggetto ftp:

* host
* user
* password
* cwd: cartella di scrittura

### QUERY
l'oggetto `queries` della configurazione contiene una lista di query che vengono eseguite in succesione.

Ogni query è codificata con un oggetto, con le seguenti proprietà:

* sql: il codice sql da eseguire
* sql-file: il file in cui trovare il codice sql da eseguire (alernativo a proprietà `sql`)
*  csv: se la query genera risultati da serializzare in csv, il nome del file da scrivere. In questo nome è possibile sostituire la data ed ora corrente utilizzando il formato `strftime` in una stringa all'interno dei separatori `[` e `]` quindi ad esempio `out_[%Y_%m_%D].csv` viene trasformato il giorno 04/05/2015 in `out_2015_05_04.csv`


# TODO (possibili):
* passare il file di configurazione da riga di comando

* specificare il delimiter/quoting csv nella configurazione(... e utilizzare lib csv per scrivere)

* estendere ad altri db server (postgres, mysql)

* astrarre la modalità di consegna del file (ad esempio via mail)

* astrarre la modalità di consegna del log di errori(ad esempio via mail)

* scrivere help e usare argparser per le opzioni a riga di comando
import sqlite3

class dbService:

    def __init__(self):
        print("Initializing the DATABASE MANGEEEEEEER...")
        self.createTables()     

    def createTables(self):
        conn = None
        try:
            conn = sqlite3.connect('contentDb.db')
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    date_added DATE DEFAULT CURRENT_DATE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT,
                    content_type TEXT,
                    url_id INTEGER,
                    FOREIGN KEY (url_id) REFERENCES urls(id)
                )
            ''')
            
            
            conn.commit()
            print("Tablas creadas exitosamente")
            
        except sqlite3.Error as e:
            print(f"Error creando tablas: {str(e)}")
        finally:
            if conn:
                conn.close()


    def addScrappedWeb(self, title, url, content, content_type):
        conn = sqlite3.connect('contentDb.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO urls (url) 
                VALUES (?)
            ''', (url,))
            
            cursor.execute('SELECT id FROM urls WHERE url = ?', (url,))
            url_id = cursor.fetchone()[0]
            
            cursor.execute('''
                INSERT INTO content (title, content, url_id, content_type)
                VALUES (?, ?, ?, ?)
            ''', (title, content, url_id, content_type))
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error insertando datos: {str(e)}")
        finally:
            conn.close()
            
    def searchUrlInDb(self, url):
        conn = sqlite3.connect('contentDb.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM urls WHERE url = ?', (url,))
        result = cursor.fetchone() 
        if result is not None:
            #print(f"URL exists already in the database: {url} with id: {result[0]}")  
            return True
        return False    
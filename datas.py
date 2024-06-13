import sqlite3


db = sqlite3.connect('my_db.db')
cursor = db.cursor()

async def start_db():
    global db,cursor
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars(
               model TEXT,
               year INTEGER,
               probeg TEXT,
               colour TEXT,
               cena TEXT,
               poziciya INTEGER,
               dvigatel INTEGER,
               photo TEXT
)    
            ''')
async def add_to_db(modeli, reni, probegi, jili, cenasi, poziciyasi, dvigateli, fotosi):
    cursor.execute('''
    INSERT INTO cars(
              model, year, probeg, colour, cena, poziciya, dvigatel, photo
)
            VALUES(?,?,?,?,?,?,?,?)

''', (modeli, reni, probegi, jili, cenasi, poziciyasi, dvigateli, fotosi))
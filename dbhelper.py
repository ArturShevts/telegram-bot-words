import sqlite3


class DBHelper:
    def __init__(self, dbname="words.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
     
        query = "CREATE TABLE IF NOT EXISTS words (word TEXT, phonetic TEXT, etymology TEXT, meaning TEXT, synonyms TEXT, example TEXT, is_favourite INTEGER DEFAULT 0,  PRIMARY KEY (word))"
        self.conn.execute(query)
        self.conn.commit()
        
        # self.conn.execute(q1)
        # self.conn.commit()
        
         
       
        

    def add_word(self, word, phonetic,etymology, meaning, synonyms, example):
        
        stmt = "INSERT INTO words ( word, phonetic,etymology, meaning, synonyms, example) VALUES (?, ?, ?, ?, ?)"
        args = (word, phonetic,etymology, meaning, synonyms, example)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_word(self, word):
        stmt = "DELETE FROM words WHERE word = (?)"
        args = (word, )
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def update_word(self, word, phonetic,etymology, meaning, synonyms, example):
        stmt = "UPDATE words SET phonetic = (?), etymology = (?), meaning = (?), synonyms = (?), example = (?) WHERE word = (?)"
        args = (phonetic, etymology, meaning, synonyms, example, word)
        self.conn.execute(stmt, args)
        self.conn.commit()
        
    def get_word(self, word):
        stmt = "SELECT phonetic,etymology, meaning, synonyms, example FROM words WHERE word = (?)"
        args = (word )
        return self.conn.execute(stmt, args)
    def get_all_words(self):
        stmt = "SELECT word FROM words"
        return [x[0] for x in self.conn.execute(stmt)]
    def get_random_word(self):
        stmt = "SELECT * FROM words ORDER BY RANDOM() LIMIT 1"
        return self.conn.execute(stmt).fetchone()
    
    
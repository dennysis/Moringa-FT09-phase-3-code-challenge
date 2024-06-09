from database.connection import get_db_connection

class Author:
    all = {}
    def __init__(self, id, name):
        self.id = id
        self._name = name

    def __repr__(self):
        return f'<Author {self.id} {self.name}>'
    

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if isinstance(id, int):
            self._id = id


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed after initialization")
        else:
            if isinstance(new_name, str):
                if len(new_name) > 0:
                    self._name = new_name


    def save(self):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            INSERT INTO authors (name)
            VALUES (?)
        """
        CURSOR.execute(sql, (self.name,))
        conn.commit()
        
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    @classmethod
    #creates a new entry in the authors table of the database
    def create(cls, name):
        author = cls(name)
        author.save()
        return author
    
    def get_author_id(self):
        return self.id

    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns a list of articles wriitten by this author"""
        sql = """
            SELECT ar.*
            FROM articles ar
            INNER JOIN authors a ON ar.author = a.id
            WHERE a.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        article_data = CURSOR.fetchall()

        articles = []
        for row in article_data:
            articles.append(Article(*row))
        return articles
    

    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """Retrieves and returns a list of Magazine objects where this Author has written articles"""
        sql = """
            SELECT DISTINCT m.*
            FROM magazines m
            INNER JOIN articles ar ON ar.magazine = m.id
            INNER JOIN authors a ON ar.author = a.id
            WHERE a.id = ?
        """

        CURSOR.execute(sql, (self.id,))
        magazine_data = CURSOR.fetchall()

        magazines = []
        for row in magazine_data:
            magazines.append(Magazine(*row))
        return magazines
    

    @classmethod
    def instance_from_db(cls, row):
        """Return an Author object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        author = cls.all.get(row[0])
        if author:
            # ensure attribute matches row value in case local instance was modified
            author.name = row[1]
        else:
            # not in dictionary, create new instance and add to dictionary
            author = cls(None, row[1])
            author.id = row[0]
            cls.all[author.id] = author
        return author
    
    @classmethod
    def list_all_authors(cls):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM authors
        """

        CURSOR.execute(sql)
        author_data = CURSOR.fetchall()

        authors = []
        for row in author_data:
            authors.append(cls.instance_from_db(row))
        return authors
#atricle.py 
from database.connection import get_db_connection
class Article:
    all = {}
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
    

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if hasattr(self, '_title'):
            raise AttributeError("Cannot change title after it has been set")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = value

    def author(self):
        from models.author import Author
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns the author who wrote this article"""
        sql = """
            SELECT a.*
            FROM authors a
            INNER JOIN articles ar ON ar.author = a.id
            WHERE ar.id = ?
        """
        CURSOR.execute(sql, (self.id))
        author_data = CURSOR.fetchone()

        if author_data:
            return Author(*author_data)
        else:
            return None

    def magazine(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        CURSOR = conn.cursor()
        """retrieves and returns the magazine in which this article is published"""
        sql = """
            SELECT m.*
            FROM magazines m
            INNER JOIN articles ar ON ar.magazine = m.id
            WHERE ar.id = ?
        """
        CURSOR.execute(sql, (self.id))
        magazine_data = CURSOR.fetchone()

        if magazine_data:
            return Magazine(*magazine_data)
        else:
            return None
        
    @classmethod
    def instance_from_db(cls, row):
            article = cls.all.get(row[0])
            if article:
                article.title = row[1]
                article.content = row[2]
                article.author_id = row[3]
                article.magazine_id = row[4]
            else:
                article = cls(row[0], row[1], row[2], row[3], row[4])
                cls.all[article.id] = article
            return article
    
    @classmethod
    def list_all_articles(cls):
        conn = get_db_connection()
        CURSOR = conn.cursor()
        sql = """
            SELECT *
            FROM articles
        """
        CURSOR.execute(sql)
        article_data = CURSOR.fetchall()
        articles = []
        for row in article_data:
            articles.append(cls.instance_from_db(row))
        return articles
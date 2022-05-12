from random import choices, randint
from sqlite3 import connect
import re
import string
from time import time

db = connect("links.db", check_same_thread=0)
cursor = db.cursor()

class Shortener(object):
    def __init__(self, id: int = None, link: str = None, short_url: str = None, alias: str = "", is_active: bool = False, has_alias: bool = False):
        self.__create__()
        self.link = link
        self.alias = alias
        self.short_url = (short_url or (self.create_short_url())) if not alias else alias
        self.has_alias = bool(self.alias)
        self.is_active = bool(link)
        self.match = re.match("(^http\:\/\/|^https\:\/\/|^www\.)?(www)?\.?(\w+)\.{1}([a-z]+)", str(link)) if not re.search("\:\/\/\W", str(link)) else None
        self.is_url = bool(self.match)
        self.id = self.create_url_id()
    def create_url_id(self):
        if self.is_url:
            return (len(self.link) + int(time())) * (len(self.link) % 5)
        return randint(111111111, 9999999999)

    def create_short_url(self):
        letters = string.ascii_letters
        digits = string.digits
        chars = letters + digits
        short_url = "".join(choices(chars, k=7))
        
        if self.is_short_url_exists(short_url = short_url):
            return self.create_short_url()
        else:
            return short_url

    def is_short_url_exists(self, short_url: str = None):
        short_url = self.short_url if not short_url else short_url
        if short_url:
            selection = db.execute(f"SELECT * FROM links where short_url = '{short_url}'").fetchall()
            if len(selection) > 0:
                return True
        return False
    
    def is_alias_exists(self, _alias: str = None):
        alias = self.__get__().alias if not _alias else _alias
        if alias:
            selection = db.execute(f"SELECT * FROM links where alias = '{alias}'").fetchall()
            if len(selection) > 0:
                return True
        return False

    
    def __create__(self):
        db.execute("CREATE TABLE IF NOT EXISTS links (id int, link text, short_url text, alias text primary key, is_active int, has_alias int)")
    
    def __add__(self):
        db.execute(f"INSERT INTO links VALUES ({self.create_url_id()}, '{self.link}', '{self.short_url}', '{self.alias}', {self.is_url}, {self.has_alias})")
        db.commit()
    
    def __get__(self, param: str = ""):
        param = param if param else (self.short_url if not self.alias else self.alias)
        if self.is_short_url_exists(param):
            link = db.execute(f"SELECT * FROM links WHERE short_url = '{param}'").fetchone()
            return Shortener(*link)
        elif self.is_alias_exists(param):
            link = db.execute(f"SELECT * FROM links WHERE alias = '{param}'").fetchone()
            return Shortener(*link)
        return Shortener()
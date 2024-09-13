from pymongo import MongoClient
from random import choices, randint
import re, os
import string
from time import time
from dotenv import load_dotenv

load_dotenv()

cstring = os.getenv("STRING")

# MongoDB'ye bağlantı oluşturma
client = MongoClient(cstring)
db = client['poems']
collection = db['links']

class Shortener(object):
    def __init__(self, id: int = None, link: str = None, short_url: str = None, alias: str = "", is_active: bool = False, has_alias: bool = False):
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
        
        if self.is_short_url_exists(short_url=short_url):
            return self.create_short_url()
        else:
            return short_url

    def is_short_url_exists(self, short_url: str = None):
        short_url = self.short_url if not short_url else short_url
        if short_url:
            selection = collection.find_one({"short_url": short_url})
            if selection:
                return True
        return False

    def is_alias_exists(self, _alias: str = None):
        alias = self.alias if not _alias else _alias
        if alias:
            selection = collection.find_one({"alias": alias})
            if selection:
                return True
        return False

    def __add__(self):
        document = {
            "id": self.create_url_id(),
            "link": self.link,
            "short_url": self.short_url,
            "alias": self.alias,
            "is_active": int(self.is_url),
            "has_alias": int(self.has_alias)
        }
        collection.insert_one(document)

    def __get__(self, param: str = ""):
        param = param if param else (self.short_url if not self.alias else self.alias)
        if self.is_short_url_exists(param):
            link = collection.find_one({"short_url": param})
            if link:
                link.pop("_id")
                return Shortener(**link)
        elif self.is_alias_exists(param):
            link = collection.find_one({"alias": param})
            if link:
                link.pop("_id")
                return Shortener(**link)
        return Shortener()

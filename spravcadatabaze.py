from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import create_engine

Base = declarative_base()

class Uzivatel(Base):
    __tablename__ = 'uzivatel'
    user_id = Column(Integer, primary_key=True)
    meno = Column(String, nullable=False)
    email = Column(String, nullable=False)
    heslo = Column(String, nullable=False)
    rola = Column(Integer, nullable=False)


class Relacia(Base):
    __tablename__ = 'relacia'
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    expires = Column(DateTime)


class Clanok(Base):
    __tablename__ = 'clanok'
    id_clanku = Column(Integer, primary_key=True)
    typ = Column(String, nullable=False)
    titulok = Column(String, nullable=False)
    datum_vytvorenia = Column(DateTime, nullable=False)
    autor = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)
    pocet_paragarfov = Column(Integer, nullable=False)
    obrazok_clanku = Column(String)
    datum_upravy = Column(DateTime)


class Paragraf(Base):
    __tablename__ = 'paragraf'
    id_paragra = Column(Integer, ForeignKey('clanok.id_clanku'), primary_key=True)
    cislo_paragrafu = Column(Integer, primary_key=True)
    text_paragrafu = Column(String, nullable=False)


class ParagrafMedium(Base):
    __tablename__ = 'paragraf_medium'
    id_paragra = Column(Integer, ForeignKey('clanok.id_clanku'), primary_key=True)
    cislo_paragrafu = Column(Integer, primary_key=True)
    cesta = Column(String, ForeignKey('nahratemedia.cesta'), nullable=False)


class Komentar(Base):
    __tablename__ = 'komentar'
    id_komentar = Column(Integer, primary_key=True)
    typ_komentovaneho = Column(Integer, nullable=False)
    id_komentovaneho = Column(Integer, nullable=False)
    komentator = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)
    komentar = Column(String, nullable=False)
    datum = Column(DateTime, nullable=False)
    pozitivne = Column(Integer, nullable=False)
    negativne = Column(Integer, nullable=False)


class Hodnotenie(Base):
    __tablename__ = 'hodnotenie'
    id_hodnotenia = Column(Integer, primary_key=True)
    pozitivne = Column(Boolean, nullable=False)
    hodnotitel = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)


class NahrateMedia(Base):
    __tablename__ = 'nahratemedia'
    cesta = Column(String, primary_key=True)
    typ_media = Column(Boolean, nullable=False)
    uzivatel = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)


class Databaza:
    def __init__(self):
        self.cestakdatabaze = 'sqlite:///webdb.db'

    def vytvor_databazu(self):
        engine = create_engine('sqlite:///webdb.db')
        Base.metadata.create_all(engine)

    def otvor_databazu(self):
        pass

    def zatvor_databazu(self):
        pass

    def vykonaj(self, dotaz:str):
        pass


class VyhladavacDB:
    def __init__(self, databaza: Databaza):
        self.databaza = databaza

    def ziskaj_heslo(self, db_id: int):
        pass


if __name__ == '__main__':
    print("l")
    Databaza().vytvor_databazu()

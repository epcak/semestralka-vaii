from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import select, desc
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy import create_engine

Base = declarative_base()

class Uzivatel(Base):
    __tablename__ = 'uzivatel'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    meno = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    heslo = Column(String, nullable=False)
    rola = Column(Integer, nullable=False)


class Relacia(Base):
    __tablename__ = 'relacia'
    session_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)
    expires = Column(DateTime)
    vytvorene = Column(DateTime)


class Clanok(Base):
    __tablename__ = 'clanok'
    id_clanku = Column(Integer, primary_key=True, autoincrement=True)
    typ = Column(String, nullable=False)
    titulok = Column(String, nullable=False)
    datum_vytvorenia = Column(DateTime, nullable=False)
    autor = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)
    pocet_paragarfov = Column(Integer, nullable=False)
    obrazok_clanku = Column(String)
    datum_upravy = Column(DateTime)


class Paragraf(Base):
    __tablename__ = 'paragraf'
    id_clanku = Column(Integer, ForeignKey('clanok.id_clanku'), primary_key=True)
    cislo_paragrafu = Column(Integer, primary_key=True)
    text_paragrafu = Column(String, nullable=False)


class ParagrafMedium(Base):
    __tablename__ = 'paragraf_medium'
    id_clanku = Column(Integer, ForeignKey('clanok.id_clanku'), primary_key=True)
    cislo_paragrafu = Column(Integer, primary_key=True)
    cesta = Column(String, ForeignKey('nahratemedia.cesta'), nullable=False)


class Komentar(Base):
    __tablename__ = 'komentar'
    id_komentar = Column(Integer, primary_key=True, autoincrement=True)
    typ_komentovaneho = Column(Integer, nullable=False)
    id_komentovaneho = Column(Integer, nullable=False)
    komentator = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)
    komentar = Column(String, nullable=False)
    datum = Column(DateTime, nullable=False)


class Hodnotenie(Base):
    __tablename__ = 'hodnotenie'
    hodnotitel = Column(Integer, ForeignKey('uzivatel.user_id'), primary_key=True)
    komentar = Column(Integer, ForeignKey('komentar.id_komentar'), primary_key=True)
    pozitivne = Column(Boolean, nullable=False)


class NahrateMedia(Base):
    __tablename__ = 'nahratemedia'
    cesta = Column(String, primary_key=True)
    typ_media = Column(Boolean, nullable=False)
    uzivatel = Column(Integer, ForeignKey('uzivatel.user_id'), nullable=False)


class Forum(Base):
    __tablename__ = 'forum'
    id_forum = Column(Integer, primary_key=True, autoincrement=True)
    nazov = Column(String, nullable=False)
    text = Column(String, nullable=False)


class Databaza:
    def __init__(self):
        self.cestakdatabaze = 'sqlite:///webdb.db'
        self.dbsession = None
        self.dbengine = None

    def vytvor_databazu(self):
        engine = create_engine(self.cestakdatabaze)
        Base.metadata.create_all(engine)

    def otvor_databazu(self):
        if self.dbengine is None:
            self.dbengine = create_engine(self.cestakdatabaze)
        if self.dbsession is None:
            self.dbsession = sessionmaker(bind=self.dbengine)

    def zatvor_databazu(self):
        if self.dbsession is not None:
            self.dbsession.close()
            self.dbsession = None

    def vykonaj(self, dotaz):
        if self.dbengine is not None:
            with self.dbsession() as relacia:
                return relacia.execute(dotaz)

    def pridaj_do_databazy(self, na_pridanie: list):
        if self.dbengine is not None:
            with self.dbsession() as relacia:
                relacia.add_all(na_pridanie)
                relacia.commit()


class VyhladavacDB:
    def __init__(self, databaza: Databaza):
        self.databaza = databaza

    def ziskaj_heslo(self, db_id: int):
        try:
            dotaz = select(Uzivatel).filter_by(user_id=db_id)
            odpoved = self.databaza.vykonaj(dotaz)
            return odpoved.all()[0].heslo
        except:
            return None

    def ziskaj_uzivatela(self, meno: str = "", email: str = ""):
        dotaz = ""
        if meno != "":
            dotaz = select(Uzivatel).filter_by(meno=meno)
        elif email != "":
            dotaz = select(Uzivatel).filter_by(email=email)
        try:
            odpoved = self.databaza.vykonaj(dotaz)
            return odpoved.all()[0].user_id
        except:
            return None

    def ziskaj_info_session(self, sid: int):
        try:
            dotaz = select(Relacia).filter_by(session_id=sid)
            odpoved = self.databaza.vykonaj(dotaz)
            return odpoved.all()[0]
        except:
            return None

    def ziskaj_clanky(self, db_id: int, typ="sprava"):
        try:
            dotaz = select(Clanok).filter_by(autor=db_id, typ=typ)
            odpoved = self.databaza.vykonaj(dotaz)
            return odpoved.all()
        except:
            return None

    def ziskaj_komentare(self, typ_komentovaneho: str, id_komentovaneho: int):
        dotaz = ""
        if typ_komentovaneho == "komentar":
            dotaz = select(Komentar).filter_by(id_komentar=id_komentovaneho)
        elif typ_komentovaneho == "sprava":
            dotaz = select(Clanok).filter_by(id_clanku=id_komentovaneho, typ="sprava")
        elif typ_komentovaneho == "blog":
            dotaz = select(Clanok).filter_by(id_clanku=id_komentovaneho, typ="blog")
        elif typ_komentovaneho == "forum":
            dotaz = select(Forum).filter_by(id_forum=id_komentovaneho)
        try:
            odpoved = self.databaza.vykonaj(dotaz)
            return odpoved.all()[0]
        except:
            return None

    def ziskaj_najnovsiu_relaciu(self, uzivatel: int):
        dotaz = select(Relacia).filter_by(user_id=uzivatel).order_by(desc(Relacia.vytvorene))
        try:
            odpoved = self.databaza.vykonaj(dotaz)
            return odpoved.all()[0].session_id
        except:
            return None

    def ziskaj_paragrafy(self, id_clanku: int):
        paragrafy = []
        try:
            dotaztext = select(Paragraf).filter_by(id_clanku=id_clanku)
            dotazmedium = select(ParagrafMedium).filter_by(id_clanku=id_clanku)
            paragrafy.append(self.databaza.vykonaj(dotaztext).all())
            paragrafy.append(self.databaza.vykonaj(dotazmedium).all())
            return paragrafy
        except:
            return None


if __name__ == '__main__':
    Databaza().vytvor_databazu()

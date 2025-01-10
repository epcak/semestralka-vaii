import spravaprihlasenie
import spravcadatabaze
import bcrypt
from sqlalchemy import update, delete

from spravaprihlasenie import vyhladavac
from spravcadatabaze import Uzivatel

from sqlalchemy.orm import declarative_base, sessionmaker



class Konto:
    def __init__(self):
        self.meno = ''
        self.email = ''
        self.db_id = None

    def vytvorenie_konta(self, meno: str, email: str, heslo: str) -> int:
        pass

    def nacitanie_db_id(self, db_id: int) -> bool:
        pass

    def nacitanie_meno(self, meno: str) -> bool:
        pass

    def nacitanie_email(self, email: str) -> bool:
        pass

    def kontrola_heslo(self, heslo: str) -> bool:
        if self.db_id is not None:
            spravaprihlasenie.KontrolaHesla().kontrola_hesla(db_id=self.db_id, heslo=heslo)
        return False

    def ziskanie_zoznamu_clankov(self):
        return list()

    def ziskanie_zoznamu_blogov(self):
        return list()

    def ziskanie_zoznamu_for(self):
        return list()

    def ziskanie_zoznamu_navodov(self):
        return list()

    def zmena_hesla(self, aktualne: str, nove: str) -> bool:
        if self.db_id is None:
            return False
        if not spravaprihlasenie.KontrolaHesla().kontrola_hesla(db_id=self.db_id, heslo=aktualne):
            return False
        db = spravaprihlasenie.db
        novoheslo = bcrypt.hashpw(nove.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with db.dbsession() as relacia:
            uzivatel = relacia.get(spravcadatabaze.Uzivatel, self.db_id)
            uzivatel.heslo = novoheslo
            relacia.commit()
        return True

    def zmena_emailu(self, email: str) -> bool:
        uzivatel = spravaprihlasenie.vyhladavac.ziskaj_uzivatela(email=email)
        if uzivatel is not None:
            return False
        with spravaprihlasenie.db.dbsession() as relacia:
            uziv = relacia.get(spravcadatabaze.Uzivatel, self.db_id)
            uziv.email = email
            relacia.commit()
        return True

    def zmena_mena(self, meno: str) -> bool:
        uzivatel = spravaprihlasenie.vyhladavac.ziskaj_uzivatela(meno=meno)
        if uzivatel is not None:
            return False
        with spravaprihlasenie.db.dbsession() as relacia:
            uziv = relacia.get(spravcadatabaze.Uzivatel, self.db_id)
            uziv.meno = meno
            relacia.commit()
        return True

    def odstranenie_uctu(self, heslo: str):
        db = spravaprihlasenie.db
        if self.db_id is None:
            return False
        if not spravaprihlasenie.KontrolaHesla().kontrola_hesla(db_id=self.db_id, heslo=heslo):
            return False
        db.odstran_uzivatela(self.db_id)

        self.meno = ''
        self.email = ''
        self.db_id = None
        return True

    def nacitaj_z_relacie(self, sid: int):
        vyhladavac = spravaprihlasenie.vyhladavac
        user_id = vyhladavac.ziskaj_info_session(sid=sid).user_id
        uzivatel = vyhladavac.ziskaj_uzivatela(user_id=user_id)
        self.db_id = user_id
        self.meno = uzivatel.meno
        self.email = uzivatel.email


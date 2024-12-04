import spravaprihlasenie
import spravcadatabaze
import bcrypt
from sqlalchemy import update, delete
from spravcadatabaze import Uzivatel



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
        dotaz = update(Uzivatel).values({"heslo": novoheslo}).where(Uzivatel.user_id == self.db_id)
        db.uprav(dotaz)
        return True

    def zmena_emailu(self, email: str) -> bool:
        return True

    def zmena_mena(self, meno: str) -> bool:
        return True

    def odstranenie_uctu(self, heslo: str) -> bool:
        db = spravaprihlasenie.db
        vyhladavac = spravaprihlasenie.vyhladavac
        if self.db_id is None:
            return False
        if not spravaprihlasenie.KontrolaHesla().kontrola_hesla(db_id=self.db_id, heslo=heslo):
            return False
        db.uprav(delete(spravcadatabaze.Uzivatel).where(spravcadatabaze.Uzivatel.user_id ==self.db_id))

        self.meno = ''
        self.email = ''
        self.db_id = None
        return True

    def nacitaj_z_relacie(self, sid: int):
        db = spravaprihlasenie.db
        vyhladavac = spravaprihlasenie.vyhladavac
        user_id = vyhladavac.ziskaj_info_session(sid=sid).user_id
        uzivatel = vyhladavac.ziskaj_uzivatela(user_id=user_id)
        self.db_id = user_id
        self.meno = uzivatel.meno
        self.email = uzivatel.email


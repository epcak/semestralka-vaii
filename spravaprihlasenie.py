import spravcadatabaze
import datetime
from sqlalchemy import select
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

db = None
vyhladavac = None

def prirad_db(databaza: spravcadatabaze.Databaza):
    global db, vyhladavac
    db = databaza
    vyhladavac = spravcadatabaze.VyhladavacDB(db)


class Registracia:
    def __init__(self):
        self.user_id = -1

    def registracia(self, udaje: dict) -> str:
        global vyhladavac
        if vyhladavac.ziskaj_uzivatela(meno=udaje["meno"]) is not None:
            return "Užívateľ už existuje"
        elif vyhladavac.ziskaj_uzivatela(email=udaje["email"]) is not None:
            return "Email už používa iný účet"
        else:
            if self.registrovanie_konta(udaje):
                return ""
            else:
                return "Nastala chyba"

    def registrovanie_konta(self, udaje: dict) -> bool:
        global db, vyhladavac
        na_pridanie = [spravcadatabaze.Uzivatel(meno=udaje["meno"], email=udaje["email"], heslo=udaje["heslo"], rola=0)]
        db.pridaj_do_databazy(na_pridanie)
        try:
            self.user_id = vyhladavac.ziskaj_uzivatela(meno=udaje["meno"])
            return True
        except:
            return False

    def ziskanie_session_id(self) -> int:
        rel = Relacia()
        rel.vytvor_novu(self.user_id)
        return rel.ziskaj_session_id()


class Prihlasenie:
    def __init__(self):
        pass

    def prihlasenie(self, udaje: dict) -> bool:
        pass

    def ziskanie_session_id(self) -> int:
        pass


class KontrolaHesla:
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt

    def kontrola_hesla(self, db_id: int, heslo: str) -> bool:
        global vyhladavac
        return self.bcrypt.checkpw(heslo, vyhladavac.ziskaj_heslo(db_id))


class Relacia:
    def __init__(self):
        self.sid = -1

    def __init__(self, sid: int):
        self.sid = sid

    def ziskaj_session_id(self) -> int:
        return self.sid

    def vytvor_novu(self, uzivatel: int, neexiprovat = False):
        import spravcadatabaze
        na_pridanie = []
        vytvorene = datetime.datetime.now()
        if neexiprovat:
            na_pridanie.append(spravcadatabaze.Relacia(user_id=uzivatel, vytvorene=vytvorene, expires=(datetime.datetime.now() + datetime.timedelta(days=30))))
        else:
            na_pridanie.append(spravcadatabaze.Relacia(user_id=uzivatel, vytvorene=vytvorene))
        global db, vyhladavac
        db.pridaj_do_databazy(na_pridanie)
        self.sid = vyhladavac.ziskaj_najnovsiu_relaciu(uzivatel)


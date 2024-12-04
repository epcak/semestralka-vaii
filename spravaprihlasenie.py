import spravcadatabaze
import datetime
import bcrypt
from sqlalchemy import select
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

db = spravcadatabaze.Databaza()
db.otvor_databazu()
vyhladavac = spravcadatabaze.VyhladavacDB(db)




class Registracia:
    def __init__(self, bcrypt):
        self.user_id = -1
        self.bcrypt = bcrypt

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
        na_pridanie = [spravcadatabaze.Uzivatel(meno=udaje["meno"], email=udaje["email"], heslo=self.bcrypt.hashpw(bytes(udaje["heslo"], encodings="utf-8"), self.bcrypt.genslat()), rola=0)]
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
        self.user_id = -1

    def prihlasenie(self, udaje: dict) -> bool:
        global vyhladavac
        uzivatel = vyhladavac.ziskaj_uzivatela(meno=udaje["meno"])
        if uzivatel is None:
            uzivatel = vyhladavac.ziskaj_uzivatela(email=udaje["meno"])
        if uzivatel is None:
            return False
        self.user_id = uzivatel.user_id
        return KontrolaHesla().kontrola_hesla(uzivatel, udaje["heslo"])


    def ziskanie_session_id(self) -> int:
        rel = Relacia()
        rel.vytvor_novu(self.user_id)
        return rel.ziskaj_session_id()


class KontrolaHesla:
    def __init__(self):
        pass

    def kontrola_hesla(self, db_id: int, heslo: str) -> bool:
        global vyhladavac
        return bcrypt.checkpw(bytes(heslo, encoding="utf-8"), bcrypt.hashpw(bytes(heslo, encoding="utf-8"), bcrypt.gensalt()))


class Relacia:
    def __init__(self, sid = -1):
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


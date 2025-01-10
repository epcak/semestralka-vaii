import spravcadatabaze
import datetime
import bcrypt
from sqlalchemy import select
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

db = spravcadatabaze.Databaza()
db.otvor_databazu()
vyhladavac = spravcadatabaze.VyhladavacDB(db)
generator_id = spravcadatabaze.GeneratorID(db)


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
                return "Nastala chyba pri zadavani udajov do databazy"

    def registrovanie_konta(self, udaje: dict) -> bool:
        global db, vyhladavac
        na_pridanie = spravcadatabaze.Uzivatel(user_id=generator_id.pouzivatelske_id() ,meno=udaje["meno"], email=udaje["email"], heslo=(bcrypt.hashpw(str(udaje["heslo"]).encode('utf-8'), bcrypt.gensalt())).decode('utf-8'), rola=0)
        db.pridaj_jedne_objekt(na_pridanie)
        try:
            self.user_id = vyhladavac.ziskaj_uzivatela(meno=udaje["meno"]).user_id
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
        return KontrolaHesla().kontrola_hesla(uzivatel.user_id, udaje["heslo"])


    def ziskanie_session_id(self) -> int:
        rel = Relacia()
        rel.vytvor_novu(self.user_id)
        return rel.ziskaj_session_id()


class KontrolaHesla:
    def __init__(self):
        pass

    def kontrola_hesla(self, db_id: int, heslo: str) -> bool:
        global vyhladavac
        hashnute = vyhladavac.ziskaj_heslo(db_id)
        return bcrypt.checkpw(heslo.encode('utf-8'), hashnute.encode('utf-8'))


class Relacia:
    def __init__(self, sid = -1):
        self.sid = sid

    def ziskaj_session_id(self) -> int:
        return self.sid

    def vytvor_novu(self, uzivatel: int, neexiprovat = False):
        global db, vyhladavac
        vytvorene = datetime.datetime.now()
        if neexiprovat:
            db.pridaj_jedne_objekt(spravcadatabaze.Relacia(session_id=generator_id.relacne_id(), user_id=uzivatel, vytvorene=vytvorene, expires=(datetime.datetime.now() + datetime.timedelta(days=30))))
        else:
            rel = spravcadatabaze.Relacia(session_id=generator_id.relacne_id(), user_id=uzivatel, vytvorene=vytvorene)
            db.pridaj_jedne_objekt(rel)
        self.sid = vyhladavac.ziskaj_najnovsiu_relaciu(uzivatel)


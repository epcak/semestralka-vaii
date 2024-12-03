import spravcadatabaze

class Registracia:
    def __init__(self):
        pass

    def registracia(self, udaje: dict) -> bool:
        pass

    def registrovanie_konta(self, udaje: dict):
        pass

    def ziskanie_session_id(self) -> int:
        pass


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

    def kontrola_hesla(self, databaza: spravcadatabaze.Databaza, db_id: int, heslo: str) -> bool:
         return self.bcrypt.checkpw(heslo, spravcadatabaze.VyhladavacDB(databaza).ziskaj_heslo(db_id))


class Session:
    def __init__(self, sid: int):
        self.sid = sid

    def ziskaj_session_id(self) -> int:
        return self.sid

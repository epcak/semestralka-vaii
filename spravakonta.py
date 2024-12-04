import spravaprihlasenie

class Konto:
    def __init__(self, bcrypt):
        self.bcrypt = bcrypt
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
            spravaprihlasenie.KontrolaHesla(self.bcrypt).kontrola_hesla(db_id=self.db_id, heslo=heslo)
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
        return True

    def zmena_emailu(self, email: str) -> bool:
        return True

    def zmena_mena(self, meno: str) -> bool:
        return True

    def odstranenie_uctu(self, heslo: str) -> bool:
        self.meno = ''
        self.email = ''
        self.db_id = None
        return True

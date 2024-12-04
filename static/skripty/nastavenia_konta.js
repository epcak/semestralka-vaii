function zmenaHesla() {
    if (document.getElementById("nove_heslo").value !== document.getElementById("opakovane_heslo").value){
        return;
    }
    let dotaz = "/zmenahesla?sid="
    dotaz = dotaz.concat(Cookies.get("SessionID"))
    dotaz = dotaz.concat("&heslo=")
    dotaz = dotaz.concat(document.getElementById("aktualne_heslo").value)
    dotaz = dotaz.concat("&nove=")
    dotaz = dotaz.concat(document.getElementById("nove_heslo").value)
    fetch(dotaz, {
        method: 'POST'
    }).then(response => response.json())
    .then(data => {
        if (data.uspesnost === true) {
            window.location.replace("/");
        }
    }).catch(error => console.error(error));
}

function odstranenieUctu() {
    let dotaz = "/odstranitucet?sid="
    dotaz = dotaz.concat(Cookies.get("SessionID"))
    dotaz = dotaz.concat("&heslo=")
    dotaz = dotaz.concat(document.getElementById("heslo_odstranit").value)
    if (window.confirm("Naozaj chceš odstrániť účet?")) {
        fetch(dotaz, {
        method: 'POST'
    }).then(response => response.json())
    .then(data => {
        if (data.uspesnost === true) {
            window.location.replace("/odhlasit");
        }
    }).catch(error => console.error(error));
    }
}

function zmenaUdajov() {
    meno = document.getElementById("uzivatelske_meno").value;
    email = document.getElementById("email").value;
    dlzka = email.length;
    zavinac = email.indexOf("@");
    bodka = email.indexOf(".");
    if (bodka === -1 || zavinac === -1 || zavinac === 0 || bodka < zavinac || (bodka + 1) === dlzka) {
        return;
    }
    let dotaz = "/zmenaudajov?sid="
    dotaz = dotaz.concat(Cookies.get("SessionID"))
    dotaz = dotaz.concat("&meno=")
    dotaz = dotaz.concat(meno)
    dotaz = dotaz.concat("&email=")
    dotaz = dotaz.concat(email)
    fetch(dotaz, {
        method: 'POST'
    }).then(response => response.json())
    .then(data => {
        if (data.uspesnost === true) {
            window.location.replace("/");
        }
    }).catch(error => console.error(error));
}
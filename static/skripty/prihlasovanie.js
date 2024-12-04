function overPrihlasenie() {
    fetch('/prihlas?meno='.concat(document.getElementById("uzivatelske_meno").value).concat('&heslo=').concat(document.getElementById("heslo").value), {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if (data.uspesnost === true) {
            document.cookie = "SessionID=" + data.sid;
            window.location.replace("/");
        } else {
            document.getElementById("chyba").style.visibility = "visible";
        }
    })
    .catch(error => console.error(error));
}

function overRegistraciu() {
    if (document.getElementById("heslo").value !== document.getElementById("opakovane_heslo").value) {
        document.getElementById("chyba").innerHTML = "Hesla sa musia rovnat";
        return;
    }
    email = document.getElementById("email").value;
    dlzka = email.length;
    zavinac = email.indexOf("@");
    bodka = email.indexOf(".");
    if (bodka === -1 || zavinac === -1 || zavinac === 0 || bodka < zavinac || (bodka + 1) === dlzka) {
        document.getElementById("chyba").innerHTML = "Nespravny format emailu";
        return;
    }
    let dotaz = "/registruj?meno="
    dotaz = dotaz.concat(document.getElementById("uzivatelske_meno").value)
    dotaz = dotaz.concat("&email=")
    dotaz = dotaz.concat(document.getElementById("email").value)
    dotaz = dotaz.concat("&heslo=")
    dotaz = dotaz.concat(document.getElementById("heslo").value)
    fetch(dotaz, {
        method: 'POST'
    }).then(response => response.json())
    .then(data => {
        if (data.uspesnost === true) {
            document.cookie = "SessionID=" + data.sid;
            window.location.replace("/");
        } else {
            document.getElementById("chyba").innerHTML = data.chyba;
        }
    }).catch(error => console.error(error));
}
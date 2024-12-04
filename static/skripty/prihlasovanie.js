function overPrihlasenie() {
    fetch('/prihlas?meno=test&heslo=test', {
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

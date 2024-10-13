let otvorene_menu = false;

function burgerNavigaciaTlacitko() {
    let items = document.getElementsByClassName('skryte_v_menu');
    let hlavicka = document.getElementsByTagName("header");
    for (let i = 0; i < items.length; i++) {
        if (otvorene_menu) {
            items[i].style.display = "";
            hlavicka[0].style.borderRadius = "";
        } else {
            items[i].style.display = "block";
            hlavicka[0].style.borderRadius = "28px 28px 0 0";
        }
    }
    otvorene_menu = !otvorene_menu;
}
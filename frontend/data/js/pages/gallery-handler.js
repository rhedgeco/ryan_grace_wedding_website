M.AutoInit();

function left_pad(string) {
    let zeroes = "000";
    return zeroes.substring(0, zeroes.length - string.length) + string;
}

function populate_gallery(_callback) {
    let imageCount = 50;
    let req = new XMLHttpRequest();
    req.open('GET', 'data/images/gallery/html/image.html');
    req.onload = function () {
        let gallery = document.getElementById('gallery');
        gallery.innerHTML = "";
        for (let i = 1; i <= imageCount; i++) {
            let pad = left_pad('' + i);
            gallery.innerHTML += req.responseText.replace(
                '[img]',
                'data/images/gallery/images/full/' + pad + 'rgengage.jpg'
            );
        }
        _callback();
    };
    req.send();
}

function control_gallery() {
    let gallery = document.querySelector('#gallery');
    gallery.querySelectorAll('.gallery-item').forEach(function (item) {
        item.addEventListener('click', function () {
            item.classList.toggle('full');
        });
    });
}

populate_gallery(control_gallery);
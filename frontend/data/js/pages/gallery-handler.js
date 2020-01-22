function left_pad(string) {
    let zeroes = "000";
    return zeroes.substring(0, zeroes.length - string.length) + string;
}

function populate_gallery(_callback) {
    let imageCount = 50;
    let req = new XMLHttpRequest();
    req.open('GET','data/images/gallery/html/image.html');
    req.onload = function () {
        let gallery = document.getElementById('gallery');
        gallery.innerHTML = "";
        for (let i = 1; i <= imageCount; i++)
        {
            gallery.innerHTML += req.responseText.replace(
                '[full-img]',
                'data/images/gallery/images/full/'+left_pad(''+i)+'rgengage.jpg'
            );
        }
        _callback();
    };
    req.send();
}

function control_gallery() {
    var gallery = document.querySelector('#gallery');
    var getVal = function (elem, style) {
        return parseInt(window.getComputedStyle(elem).getPropertyValue(style));
    };
    var getHeight = function (item) {
        return item.querySelector('.content').getBoundingClientRect().height;
    };
    var resizeAll = function () {
        var altura = getVal(gallery, 'grid-auto-rows');
        var gap = getVal(gallery, 'grid-row-gap');
        gallery.querySelectorAll('.gallery-item').forEach(function (item) {
            var el = item;
            el.style.gridRowEnd = "span " + Math.ceil((getHeight(item) + gap) / (altura + gap));
        });
    };
    gallery.querySelectorAll('img').forEach(function (item) {
        item.classList.add('byebye');
        if (item.complete) {
            console.log(item.src);
        } else {
            item.addEventListener('load', function () {
                var altura = getVal(gallery, 'grid-auto-rows');
                var gap = getVal(gallery, 'grid-row-gap');
                var gitem = item.parentElement.parentElement;
                gitem.style.gridRowEnd = "span " + Math.ceil((getHeight(gitem) + gap) / (altura + gap));
                item.classList.remove('byebye');
            });
        }
    });
    window.addEventListener('resize', resizeAll);
    gallery.querySelectorAll('.gallery-item').forEach(function (item) {
        item.addEventListener('click', function () {
            item.classList.toggle('full');
        });
    });
}

control_gallery();
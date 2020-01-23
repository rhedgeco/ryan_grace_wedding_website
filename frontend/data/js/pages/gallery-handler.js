M.AutoInit();

let current_page = 1;
let max_pages = 1;

function refresh_page_num() {
    let req = new XMLHttpRequest();
    req.open('GET', 'api/gallery_info');
    req.onload = function () {
        try {
            json = JSON.parse(req.responseText);
            max_pages = json['page_count'];
        } catch (e) {
            max_pages = 1;
            M.toast({html: '<span class="red-text">ERROR COMMUNICATING WITH GALLERY SERVER</span>'})
        }
        $('.page-num').each(function (i, obj) {
            obj.innerText = '' + current_page + ' / ' + max_pages;
        });
        $('.prev-btn').each(function (i, obj) {
            if(current_page === 1) {if(!obj.classList.contains('disabled')) {obj.classList.add('disabled')}}
            else {obj.classList.remove('disabled')}
        })
        $('.next-btn').each(function (i, obj) {
            if(current_page === max_pages) {if(!obj.classList.contains('disabled')) {obj.classList.add('disabled')}}
            else {obj.classList.remove('disabled')}
        })
    };
    req.send();
}

function get_gallery_html(page, _callback) {
    let req = new XMLHttpRequest();
    req.open('GET', 'api/gallery_html_images?images_per_page=10&page_number=' + page);
    req.onload = function () {
        let gallery = document.getElementById('gallery');
        gallery.innerHTML = req.responseText;
        _callback();
        refresh_page_num();
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

function next_page() {
    if (current_page < max_pages) {
        current_page++;
        get_gallery_html(current_page, control_gallery);
    }
}

function prev_page() {
    if (current_page > 1) {
        current_page--;
        get_gallery_html(current_page, control_gallery);
    }
}

get_gallery_html(current_page, control_gallery);
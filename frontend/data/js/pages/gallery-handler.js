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
            if (current_page === 1) {
                if (!obj.classList.contains('disabled')) {
                    obj.classList.add('disabled')
                }
            } else {
                obj.classList.remove('disabled')
            }
        });
        $('.next-btn').each(function (i, obj) {
            if (current_page === max_pages) {
                if (!obj.classList.contains('disabled')) {
                    obj.classList.add('disabled')
                }
            } else {
                obj.classList.remove('disabled')
            }
        });
    };
    req.send();
}

function get_gallery_html() {
    update_current_page();
    let req = new XMLHttpRequest();
    req.open('GET', 'api/gallery_html_images?page_number=' + current_page);
    req.onload = function () {
        let gallery = document.getElementById('gallery');
        gallery.innerHTML = req.responseText;
        $("#loader").hide();
        // control_gallery();
        refresh_page_num();
        load_full_images();
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

function update_current_page() {
    current_page = getUrlParam('page', 1);
}

function next_page() {
    if (current_page < max_pages) {
        $("#loader").show();
        document.getElementById("gallery").innerHTML = "";
        current_page++;
        refresh_page_num();
        history.pushState(null, '', '?page=' + current_page);
        get_gallery_html();
    }
}

function prev_page() {
    if (current_page > 1) {
        $("#loader").show();
        document.getElementById("gallery").innerHTML = "";
        current_page--;
        refresh_page_num();
        history.pushState(null, '', '?page=' + current_page);
        get_gallery_html();
    }
}

function load_full_images() {
    $('.preview').each(function () {
        let image = $(this);
        let download = new Image();
        download.onload = function () {
            image.attr('src',this.src);
            image.addClass('full-view');
            image.removeClass('preview');
            let galleryItem = image.parent().parent().parent();
            galleryItem.click( function () {
                galleryItem.toggleClass('full');
            });
        };
        download.src = image.attr('data-src');
    })
}

window.onpopstate = function (e) {
    $("#loader").show();
    document.getElementById("gallery").innerHTML = "";
    current_page = getUrlParam('page', 1);
    update_current_page();
    get_gallery_html();
};

get_gallery_html();
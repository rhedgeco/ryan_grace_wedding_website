M.AutoInit();

let current_page = 1;
let max_pages = 1;

function refresh_page_num() {
    $("#loader").show();
    document.getElementById("gallery").innerHTML = "";
    let req = new XMLHttpRequest();
    req.open('GET', 'api/gallery_info');
    req.onload = function () {
        try {
            json = JSON.parse(req.responseText);
            max_pages = json['page_count'];
            update_current_page();
            get_gallery_html();
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
    let req = new XMLHttpRequest();
    req.open('GET', 'api/gallery_html_images?page_number=' + current_page);
    req.onload = function () {
        let gallery = document.getElementById('gallery');
        gallery.innerHTML = req.responseText;
        $("#loader").hide();
        load_full_images();
    };
    req.send();
}

function update_current_page() {
    current_page = Math.min(Math.max(0, parseInt(getUrlParam('page', 1))), max_pages);
}

function next_page() {
    if (current_page < max_pages) {
        current_page++;
        history.pushState(null, '', '?page=' + current_page);
        refresh_page_num();
    }
}

function prev_page() {
    if (current_page > 1) {
        current_page--;
        history.pushState(null, '', '?page=' + current_page);
        refresh_page_num();
    }
}

function load_full_images() {
    $('.preview').each(function () {
        let image = $(this);
        let download = new Image();
        download.onload = function () {
            image.attr('src', this.src);
            image.addClass('full-view');
            image.removeClass('preview');
            let galleryItem = image.parent().parent().parent();
            galleryItem.click(function () {
                galleryItem.toggleClass('full');
            });
        };
        download.src = image.attr('data-src');
    })
}

window.onpopstate = function (e) {
    refresh_page_num();
};

refresh_page_num();
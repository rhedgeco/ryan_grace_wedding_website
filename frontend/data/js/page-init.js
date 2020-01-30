M.AutoInit();

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function getUrlParam(parameter, defaultvalue) {
    let params = new URLSearchParams(window.location.search);
    if (!params.has(parameter)) return defaultvalue;
    return params.get(parameter);
}

function show_admin_items(admin_id) {
    $('.admin-visibility').each(function () {
        $(this).addClass('admin-show');
    });
    $('#admin_login').html(admin_id);
}

function detect_admin() {
    let req = new XMLHttpRequest();
    req.open('GET', 'api/admins?token=' + getCookie('token'));
    req.onload = function () {
        if (req.status === 200) {
            show_admin_items(this.responseText);
        }
    };
    req.send();
}

$(document).ready(function () {
    detect_admin();
});

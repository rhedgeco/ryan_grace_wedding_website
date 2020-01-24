M.AutoInit();

function login_admin() {
    let admin_id = $('#admin_id').val();
    let password = $('#password').val();

    let req = new XMLHttpRequest();
    let form = new FormData();
    form.append('admin_id', admin_id);
    form.append('password', password);
    req.open('GET','api/auth');
    req.onload = function () {
        if(req.status === 200) {
            document.cookie = 'authToken='+this.responseText;
            window.location.href = 'home.html';
        } else {M.toast({html: 'ERROR : ' + req.responseText})}
    };
    req.send(form);
}

function register_admin() {
    let admin_id = $('#admin_id').val();
    let password = $('#password').val();
    let add_code = $('#add_code').val();

    let req = new XMLHttpRequest();
    let form = new FormData();
    form.append('admin_id', admin_id);
    form.append('password', password);
    form.append('add_code', add_code);
    req.open('POST','api/admins');
    req.onload = function () {
        if(req.status === 200) {
            window.location.href = 'admin-login.html';
        } else {M.toast({html: 'ERROR : ' + req.responseText})}
    };
    req.send(form);
}

// Validate confirm password field
$('#pass_conf').bind('input', function () {
    var to_confirm = $(this);
    var to_equal = $('#password');

    if (to_confirm.val() !== to_equal.val())
        this.setCustomValidity('Passwords must match.');
    else
        this.setCustomValidity('');
});
M.AutoInit();

function register_admin() {
    let admin_id = $('#admin_id').val();
    let password = $('#password').val();
    let add_code = $('#add_code').val();

    let req = new XMLHttpRequest();
    req.open('POST','api/admins?admin_id='+admin_id+'&password='+password+'&add_code='+add_code);
    req.onload = function () {
        if(req.status === 200) {
            window.location.href = 'admin-login.html';
        } else {M.toast({html: 'ERROR : ' + req.responseText})}
    };
    req.send();
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
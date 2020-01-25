M.AutoInit();

function login_admin() {
    let admin_id = $('#admin_id').val();
    let password = $('#password').val();

    let req = new XMLHttpRequest();
    req.open('GET','api/auth');
    req.setRequestHeader("Authorization", "Basic " + btoa(admin_id + ":" + password));
    req.onload = function () {
        if(req.status === 200) {
            token = this.responseText;
            setCookie('token',token,1);
            window.location.href = 'home.html';
        } else {M.toast({html: 'ERROR : ' + req.responseText})}
    };
    req.send('admin_id=test&password=test');
}

function register_admin() {
    let admin_id = $('#admin_id').val();
    let password = $('#password').val();
    let add_code = $('#add_code').val();

    let req = new XMLHttpRequest();
    let form = new FormData();
    form.append('add_code', add_code);
    req.open('POST','api/admins');
    req.setRequestHeader("Authorization", "Basic " + btoa(admin_id + ":" + password));
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
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}
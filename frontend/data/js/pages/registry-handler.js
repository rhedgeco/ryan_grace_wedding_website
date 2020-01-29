function populate_registry() {
    let req = new XMLHttpRequest();
    req.open('GET', 'api/myregistry_scraper');
    req.onload = function () {
        if (req.status === 200) {
            $('#registry-message').remove();
            $('#registry-preloader').remove();
            let $holder = $('#registry-holder');
            $holder.append(req.responseText);
        } else (M.toast({html: 'Error retrieving registry.'}))
    };
    req.send();
}

$(document).ready(function () {
    populate_registry();
});
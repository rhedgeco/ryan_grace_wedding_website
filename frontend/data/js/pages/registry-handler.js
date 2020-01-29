function populate_registry() {
    let req = new XMLHttpRequest();
    req.open('GET', 'api/myregistry_scraper');
    req.onload = function () {
        $('#registry-message').remove();
        $('#registry-preloader').remove();
        let $holder = $('#registry-holder');
        if (req.status === 200) {
            $holder.append(req.responseText);
        } else {
            $holder.after('<br>ERROR<br>' +
                'There was a problem populating registry data<br>' +
                'from MyRegistry servers.<br>' +
                'Try to accessing it directly ' +
                '<a href="https://www.myregistry.com/wedding-registry/ryan-hedgecock-and-grace-perlman-campbell-ca/2280168">here</a>.');
            $holder.remove();
        }
    };
    req.send();
}

$(document).ready(function () {
    populate_registry();
});
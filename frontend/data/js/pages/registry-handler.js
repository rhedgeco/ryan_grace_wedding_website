function alert_title() {
    let req = new XMLHttpRequest();
    req.open('GET', 'api/myregistry_scraper');
    req.onload = function () {
        if (req.status === 200) {
            let items = JSON.parse(req.responseText);
            let $holder = $('#registry-holder');
            for(let item of items['titles']) {
                $holder.append('<h5>' + item + '</h5>');
            }
        } else (M.toast({html: 'Error retrieving registry.'}))
    };
    req.send();
}
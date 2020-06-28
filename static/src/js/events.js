let eventsFrom = document.querySelector(".events_form");

if (eventsFrom) {
    // format phone on keypress
    document.getElementById('id_name').focus();
    document.getElementById('id_phone_contact').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '' + x[1] + '-' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // trix wysiwyg editor prevent file upload
    addEventListener("trix-file-accept", function (event) {
        event.preventDefault();
    });

    // google places autocomplete
    var input = document.getElementById('id_location');
    var options = {
        componentRestrictions: { country: 'us' }
    };
    google.maps.event.addDomListener(input, 'keydown', function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
        }
    });
    autocomplete = new google.maps.places.Autocomplete(input, options);
}

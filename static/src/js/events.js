let eventsFrom = document.querySelector(".events_form");

if (eventsFrom) {
    // var placesAutocomplete = places({
    //     appId: 'plM3ZWFPSCRI',
    //     apiKey: 'c6f53472cf6a8edc5fe8bf7f06018d65',
    //     container: document.querySelector('#id_location'),
    //     countries: 'us',
    // });

    // placesAutocomplete.on('change', function resultSelected(e) {
    //     console.log(e.suggestion);
    // document.querySelector('#id_location').value =
    //     `${e.suggestion.county} ${e.suggestion.city} ${e.suggestion.administrative}`
    // document.querySelector('#id_suburb').value = `${e.suggestion.suburb}`
    // document.querySelector('#id_city').value = `${e.suggestion.city}`
    // document.querySelector('#id_state').value = `${e.suggestion.administrative}`
    // });

    document.getElementById('id_name').focus();
    document.getElementById('id_phone_contact').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '' + x[1] + '-' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // document.querySelector(".form-field--description").addEventListener("click", function () {
    //     document.querySelector("trix-editor").focus();
    // });

    addEventListener("trix-file-accept", function (event) {
        event.preventDefault();
    });
}

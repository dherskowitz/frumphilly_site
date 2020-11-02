let form = document.querySelector(".form");

if (form && document.getElementById("id_location")) {
    // trix wysiwyg editor prevent file upload
    addEventListener("trix-file-accept", function (event) {
        event.preventDefault();
    });

    // google places autocomplete
    var input = document.getElementById("id_location");
    var city = document.getElementById("id_city");
    var state = document.getElementById("id_state");
    var zipcode = document.getElementById("id_zipcode");
    var location_type = document.getElementById("id_location_type");
    var options = {
        types: ["address"],
        componentRestrictions: {
            country: "us",
        },
    };
    const autocomplete = new google.maps.places.Autocomplete(input, options);
    google.maps.event.addDomListener(input, "keydown", function (event) {
        if (event.keyCode === 13) {
            event.preventDefault();
        }
    });

    google.maps.event.addListener(autocomplete, "place_changed", () => {
        // console.log(autocomplete.getPlace());
        let place = autocomplete.getPlace();

        city.value = place.vicinity;
        location_type.value = place.types[0];
        state.value = place.address_components.find((element) =>
            element.types.includes("administrative_area_level_1")
        ).short_name;
        zipcode.value = place.address_components.find((element) =>
            element.types.includes("postal_code")
        ).long_name;
    });
}

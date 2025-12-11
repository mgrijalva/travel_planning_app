
async function initAutocomplete() {
    if (!window.google || !google.maps || !google.maps.importLibrary) {
    console.error('Google Maps loader not available');
    return;
    }
    await google.maps.importLibrary("places");

    const input = document.getElementById("address");
    if (!input) return;

    const autocomplete = new google.maps.places.Autocomplete(input, { types: [] });
    autocomplete.setFields(["formatted_address", "geometry", "name"]);

    autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    if (!place || !place.geometry) return;
    const latEl = document.getElementById("address-lat");
    const lngEl = document.getElementById("address-lng");
    if (latEl) latEl.value = String(place.geometry.location.lat());
    if (lngEl) lngEl.value = String(place.geometry.location.lng());
    if (place.formatted_address) input.value = place.formatted_address;
    });
}

initAutocomplete();
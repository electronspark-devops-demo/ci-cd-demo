document.addEventListener("DOMContentLoaded", function(event) {
    var alertBanner = document.getElementById("alertBanner");
    if (alertBanner) {
        alertBanner.classList.remove("hidden");
        setTimeout(function() {
            alertBanner.classList.add("hidden");
        }, 5000);
    }
});

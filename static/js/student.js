// Send student location to server
function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            fetch("/update_location", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude
                })
            });
            console.log("Location sent:", position.coords.latitude, position.coords.longitude);
        }, err => {
            alert("Location access denied. Please allow GPS.");
        });
    } else {
        alert("Geolocation is not supported by your browser.");
    }
}

// Update location every 10 seconds
setInterval(sendLocation, 10000);
sendLocation(); // initial call

// Initialize Leaflet map
var map = L.map('map').setView([20.5937, 78.9629], 5); // Center on India
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var markers = {}; // Store markers by student mobile number

function updateLocations() {
    fetch("/student_locations")
        .then(res => res.json())
        .then(data => {
            data.forEach(student => {
                var id = student.mobile;
                var latlng = [student.lat, student.lng];

                if (markers[id]) {
                    // Update existing marker
                    markers[id].setLatLng(latlng);
                } else {
                    // Create new marker
                    markers[id] = L.marker(latlng).addTo(map)
                        .bindPopup(student.name + " - " + student.mobile);
                }
            });

            // Fit map to all markers
            if (data.length > 0) {
                var group = new L.featureGroup(Object.values(markers));
                map.fitBounds(group.getBounds().pad(0.2));
            }
        });
}

// Update every 5 seconds
setInterval(updateLocations, 5000);
updateLocations(); // Initial load

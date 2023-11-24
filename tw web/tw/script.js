// script.js
document.addEventListener('DOMContentLoaded', function() {
    const map = L.map('map').setView([25.0330, 121.5654], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    fetch('data.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                
                const totalCounts=item.v6_recur+item.v6_open+item.odns+item.dnssec+item.doe;

                const popupContent = `
                    <div class="popup-content">
                        <p><b>v6 Recur:</b> ${item.v6_recur}</p>
                        <p><b>v6 Open:</b> ${item.v6_open}</p>
                        <p><b>ODNS:</b> ${item.odns}</p>
                        <p><b>DNSSEC:</b> ${item.dnssec}</p>
                        <p><b>DOE:</b> ${item.doe}</p>
                        <button onclick="window.open('details.html?lat=${encodeURIComponent(item.lat)}&lng=${encodeURIComponent(item.lng)}&v6_recur=${encodeURIComponent(item.v6_recur)}&v6_open=${encodeURIComponent(item.v6_open)}&odns=${encodeURIComponent(item.odns)}&dnssec=${encodeURIComponent(item.dnssec)}&doe=${encodeURIComponent(item.doe)}', '_blank')" class="details-btn">详情</button>
                    </div>
                `;

                const color = getColorForTotalCounts(totalCounts);

                const marker = L.circleMarker([item.lat, item.lng], {
                    color: color,
                    fillColor: color,
                    fillOpacity: 1,
                    radius: 5
                }).addTo(map);

                marker.bindPopup(popupContent);
            });
        });
    
});
function getColorForTotalCounts(totalCounts) {
    if (totalCounts > 10000) {
        return 'red';
    } else if (totalCounts > 5000) {
        return 'orange';
    } else if (totalCounts > 1000) {
        return 'yellow';
    } else {
        return 'green';
    }
}
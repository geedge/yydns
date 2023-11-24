window.onload = function() {
    const urlParams = new URLSearchParams(window.location.search);
    const lat = urlParams.get('lat');
    const lng = urlParams.get('lng');
    const v6_recur = urlParams.get('v6_recur');
    const v6_open = urlParams.get('v6_open');
    const dnssec = urlParams.get('dnssec');
    const doe = urlParams.get('doe');
    const odns = urlParams.get('odns');
    const fileName = `${lat}_${lng}.json`;

    displayStatistics(lat, lng, v6_recur, v6_open, dnssec, doe, odns);
    fetchDetails(fileName);
};



function fetchDetails(fileName) {
    fetch(fileName)
        .then(response => response.json())
        .then(data => displayDetails(data))
        .catch(error => console.error('Error loading data:', error));
}


function displayDetails(data) {
    const detailsCard = document.getElementById('details-card');
    let detailsHtml = `<h2><i class="fas fa-list"></i>Details</h2>`;

    Object.keys(data).forEach(key => {
        detailsHtml += `
            <h3 class="toggle-section" onclick="toggleSection('${key}')">${key.toUpperCase()}</h3>
            <table id="table-${key}" class="collapsed">`;

        data[key].forEach(item => {
            detailsHtml += `<tr>
                <td>${item.ip}</td>
                <td>${item.owner}</td>
                <td>${item.isp}</td>
                <!-- 更多列数据 -->
            </tr>`;
        });

        detailsHtml += `</table>`;
    });

    detailsCard.innerHTML = detailsHtml;
}

function toggleSection(key) {
    const table = document.getElementById(`table-${key}`);
    table.classList.toggle('collapsed');
}
function displayStatistics(lat, lng, v6_recur, v6_open, dnssec, doe, odns) {
    const statisticsCard = document.getElementById('statistics-card');
    statisticsCard.innerHTML = `
        <div class="stats-row">
            <div class="stats-item"><i class="fas fa-map-marker-alt"></i><b>Latitude:</b> ${lat}</div>
            <div class="stats-item"><i class="fas fa-map-marker-alt"></i><b>Longitude:</b> ${lng}</div>
            <div class="stats-item"><i class="fas fa-network-wired"></i><b>V6 Recur:</b> ${v6_recur}</div>
            <div class="stats-item"><i class="fas fa-network-wired"></i><b>V6 Open:</b> ${v6_open}</div>
        </div>
        <div class="stats-row">
            <div class="stats-item"><i class="fas fa-lock"></i><b>DNSSEC:</b> ${dnssec}</div>
            <div class="stats-item"><i class="fas fa-bolt"></i><b>DOE:</b> ${doe}</div>
            <div class="stats-item"><i class="fas fa-server"></i><b>ODNS:</b> ${odns}</div>
        </div>
    `;
}
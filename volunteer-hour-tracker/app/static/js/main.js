// app/static/js/main.js
document.addEventListener("DOMContentLoaded", function() {
    fetchVolunteerData();

    const form = document.getElementById("volunteer-form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        addVolunteerHours();
    });
});

function fetchVolunteerData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById("volunteer-table-body");
            tableBody.innerHTML = "";
            data.forEach(volunteer => {
                const row = document.createElement("tr");
                row.innerHTML = `<td>${volunteer.name}</td><td>${volunteer.hours}</td>`;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching volunteer data:', error));
}

function addVolunteerHours() {
    const nameInput = document.getElementById("volunteer-name");
    const hoursInput = document.getElementById("volunteer-hours");

    const volunteerData = {
        name: nameInput.value,
        hours: parseInt(hoursInput.value)
    };

    fetch('/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(volunteerData)
    })
    .then(response => {
        if (response.ok) {
            fetchVolunteerData();
            nameInput.value = '';
            hoursInput.value = '';
        } else {
            console.error('Error adding volunteer hours:', response.statusText);
        }
    })
    .catch(error => console.error('Error:', error));
}
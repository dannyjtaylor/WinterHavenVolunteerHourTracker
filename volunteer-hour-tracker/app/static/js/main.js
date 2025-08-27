// app/static/js/main.js
document.addEventListener("DOMContentLoaded", function() {
    loadVolunteers();

    const form = document.getElementById("add-volunteer-form");
    form.addEventListener("submit", function(event) {
        event.preventDefault();
        addVolunteerHours();
    });
});

// Fetch and display volunteer data
async function loadVolunteers() {
    const response = await fetch('/data');
    const data = await response.json();
    const tbody = document.querySelector('#volunteer-table tbody');
    tbody.innerHTML = '';
    data.forEach(volunteer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${volunteer.name}</td>
            <td>${volunteer.hours}</td>
        `;
        tbody.appendChild(row);
    });
}

// Handle form submission to add hours
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
            loadVolunteers();
            nameInput.value = '';
            hoursInput.value = '';
        } else {
            console.error('Error adding volunteer hours:', response.statusText);
        }
    })
    .catch(error => console.error('Error:', error));
}
request_teams();

function request_teams() {
    var senddata = {
        data: 'request teams',
    };

    console.log('JSON data to be sent:', JSON.stringify(senddata));

    fetch('https://79.171.148.163/api', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(senddata)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('Response from server:', data);

        if (data.status === 'Retrieved team list') {
            console.log('200 OK team list recieved.');
            
            const teamsContent = document.getElementById('teams-content');
            teamsContent.innerHTML = '';

            data.team_list.forEach((team, index) => {
                const teamDiv = document.createElement('div');
                teamDiv.id = `team-${index + 1}`;
                teamDiv.style.borderBottom = '2px solid black';
                teamDiv.style.paddingBottom = '10px';

                const teamLabel = document.createElement('label');
                teamLabel.id = `team-${index + 1}-title`;
                teamLabel.textContent = team.uddannelseNavn;

                const teamCheckbox = document.createElement('input');
                teamCheckbox.type = 'checkbox';
                teamCheckbox.id = `teams-checkbox-${index + 1}`;
                teamCheckbox.name = 'teams-checked';
                teamCheckbox.style.marginTop = '10px';

                teamDiv.appendChild(teamLabel);
                teamDiv.appendChild(teamCheckbox);

                teamsContent.appendChild(teamDiv);
            });
        } else {
            console.error('Error:', data.status);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = '/login';
    });
}
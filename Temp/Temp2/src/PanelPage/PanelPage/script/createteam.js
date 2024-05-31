document.addEventListener('DOMContentLoaded', function() {
    // Create Team
    const createClickable = document.getElementById('create_team');
    const createOpen = document.getElementById('create_open');
    const closeBtnCreate = document.getElementById('close_btn_create');

    createClickable.addEventListener('click', function() {
        createOpen.style.display = 'block';
    });

    closeBtnCreate.addEventListener('click', function() {
        createOpen.style.display = 'none';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('create-submit-btn').addEventListener('click', createTeam);
});

function createTeam() {
    // Hent værdierne fra inputfelterne
    var name = document.getElementById('inputbox_team_name').value;
    var meet = document.getElementById('inputbox_team_meet').value;

    const confirmationText = document.querySelector("#confirmation-field");

    // Tjek om de er tomme inden vi sender dataen til serveren
    if (name.trim() === '') {
        document.getElementById('inputbox_team_name').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'hold navn' og 'mødetidspunkt' kasserne.";

    } else {
        document.getElementById('inputbox_team_name').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (meet.trim() === '') {
        document.getElementById('inputbox_team_meet').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'hold navn' og 'mødetidspunkt' kasserne.";
    } else {
        document.getElementById('inputbox_team_meet').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (name.trim() === '' || meet.trim() === '') {
        console.log('[!] Inputboxes are empty, aborting...');
        return;
    }

    var senddata = {
        data: 'create team request',
        team_name: name,
        team_meet: meet
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
        return response.json();
    })
    .then(data => {
        if (data.status === 'Create Team: Success') {
            document.getElementById('confirmation-field').classList.remove('error');
            confirmationText.textContent = "Uddannelsesholdet er oprettet.";

        } else {
            console.log('520 Unknown; Unknown error occurred');
            document.getElementById('confirmation-field').classList.add('error');
            confirmationText.textContent = "En ukendt fejl skete under oprettelsen af uddannelsesholdet.";
            
            throw new Error("HTTP error; 520 Unknown; Unknown error occurred");
        }
    })
    .catch(error => {
        // Håndterer fejl her
        console.error('Error:', error);
    });
}

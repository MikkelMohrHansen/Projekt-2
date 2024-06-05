document.addEventListener('DOMContentLoaded', function() {
    // Create Team
    const createClickable = document.getElementById('create_room');
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
    // Hent værdierne fra inputfeltet
    var name = document.getElementById('inputbox_room_name').value;

    const confirmationText = document.querySelector("#confirmation-field");

    // Tjek om de er tomme inden vi sender dataen til serveren
    if (name.trim() === '') {
        document.getElementById('inputbox_room_name').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'lokale navn' kassen.";

    } else {
        document.getElementById('inputbox_room_name').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (name.trim() === '') {
        console.log('[!] Inputboxes are empty, aborting...');
        return;
    }

    var senddata = {
        data: 'create room request',
        room_name: name,
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
        if (data.status === 'Create Room: Success') {
            document.getElementById('confirmation-field').classList.remove('error');
            confirmationText.textContent = "Lokalet er oprettet.";

        } else {
            console.log('520 Unknown; Unknown error occurred');
            document.getElementById('confirmation-field').classList.add('error');
            confirmationText.textContent = "En ukendt fejl skete under oprettelsen af lokalet.";
            
            throw new Error("HTTP error; 520 Unknown; Unknown error occurred");
        }
    })
    .catch(error => {
        // Håndterer fejl her
        console.error('Error:', error);
    });
}

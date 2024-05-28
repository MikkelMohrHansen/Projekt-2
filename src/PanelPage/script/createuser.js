document.addEventListener('DOMContentLoaded', function() {
    // Create User
    const createClickable = document.getElementById('create_user');
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
    document.getElementById('create-submit-btn').addEventListener('click', createUser);
});

function createUser() {
    // Hent værdierne fra inputfelterne
    var email = document.getElementById('inputbox_new_email').value;
    var password = document.getElementById('inputbox_new_kodeord').value;

    const confirmationText = document.querySelector("#confirmation-field");

    // Tjek om de er tomme inden vi sender dataen til serveren
    if (email.trim() === '') {
        document.getElementById('inputbox_new_email').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'email' og 'kodeord' kasserne.";

    } else {
        document.getElementById('inputbox_new_email').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (password.trim() === '') {
        document.getElementById('inputbox_new_kodeord').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'email' og 'kodeord' kasserne.";
    } else {
        document.getElementById('inputbox_new_kodeord').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (email.trim() === '' || password.trim() === '') {
        console.log('[!] Inputboxes are empty, aborting...');
        return;
    }

    var senddata = {
        data: 'create user request',
        user: email,
        pass: password
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
        if (data.status === 'Create User: Success') {
            document.getElementById('confirmation-field').classList.remove('error');
            confirmationText.textContent = "Brugeren er oprettet.";

        } else {
            console.log('520 Unknown; Unknown error occurred');
            document.getElementById('confirmation-field').classList.add('error');
            confirmationText.textContent = "En ukendt fejl skete under oprettelsen af brugeren.";
            
            throw new Error("HTTP error; 520 Unknown; Unknown error occurred");
        }
    })
    .catch(error => {
        // Håndterer fejl her
        console.error('Error:', error);
    });
}

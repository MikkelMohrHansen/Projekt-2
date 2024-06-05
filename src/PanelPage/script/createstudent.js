document.addEventListener('DOMContentLoaded', function() {
    // Create Team
    const createClickable = document.getElementById('create_student');
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
    document.getElementById('create-submit-btn').addEventListener('click', createStudent);
});

function createStudent() {
    // Hent værdierne fra inputfelterne
    var s_name = document.getElementById('inputbox_student_name').value;
    var s_team = document.getElementById('inputbox_student_team').value;
    var s_date = document.getElementById('inputbox_student_starttime').value;
    var s_enddate = document.getElementById('inputbox_student_endtime').value;

    const confirmationText = document.querySelector("#confirmation-field");

    // Tjek om de er tomme inden vi sender dataen til serveren
    if (s_name.trim() === '') {
        document.getElementById('inputbox_student_name').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'studerende navn', 'Uddannelse', 'Opstartsdato' og 'Slutdato'kasserne.";

    } else {
        document.getElementById('inputbox_student_name').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (s_team.trim() === '') {
        document.getElementById('inputbox_student_team').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'studerende navn', 'Uddannelse', 'Opstartsdato' og 'Slutdato'kasserne.";
    } else {
        document.getElementById('inputbox_student_team').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (s_date.trim() === '') {
        document.getElementById('inputbox_student_starttime').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'studerende navn', 'Uddannelse', 'Opstartsdato' og 'Slutdato'kasserne.";
    } else {
        document.getElementById('inputbox_student_starttime').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (s_enddate.trim() === '') {
        document.getElementById('inputbox_student_endtime').classList.add('error');
        document.getElementById('confirmation-field').classList.add('error');
        confirmationText.textContent = "Venligst udfyld 'studerende navn', 'Uddannelse', 'Opstartsdato' og 'Slutdato'kasserne.";
    } else {
        document.getElementById('inputbox_student_endtime').classList.remove('error');
        document.getElementById('confirmation-field').classList.remove('error');
        confirmationText.textContent = "";
    }

    if (s_name.trim() === '' || s_team.trim() === '' || s_date.trim() === '' || s_enddate.trim() === '' ) {
        console.log('[!] Inputboxes are empty, aborting...');
        return;
    }

    var senddata = {
        data: 'create student request',
        student_name: s_name,
        student_team: s_team,
        student_start: s_date,
        student_end: s_enddate
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
        if (data.status === 'Create student: Success') {
            document.getElementById('confirmation-field').classList.remove('error');
            confirmationText.textContent = "Den studerende er oprettet.";

        } else {
            console.log('520 Unknown; Unknown error occurred');
            document.getElementById('confirmation-field').classList.add('error');
            confirmationText.textContent = "En ukendt fejl skete under oprettelsen af den studerende.";
            
            throw new Error("HTTP error; 520 Unknown; Unknown error occurred");
        }
    })
    .catch(error => {
        // Håndterer fejl her
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('submit-btn').addEventListener('click', sendData);
});

function sendData() {
    // Hent værdierne fra inputfelterne
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    
    const responseStatusText = document.querySelector("#response-status");

    // Tjek om de er tomme inden vi sender dataen til serveren
    if (email.trim() === '') {
        document.getElementById('email').classList.add('error');
        responseStatusText.textContent = "Please fill out 'Email' and 'Password' boxes";

    } else {
        document.getElementById('email').classList.remove('error');
        responseStatusText.textContent = "";
    }

    if (password.trim() === '') {
        document.getElementById('password').classList.add('error');
        const responseStatusText = document.querySelector("#response-status");
        responseStatusText.textContent = "Please fill out 'Email' and 'Password' boxes";
    } else {
        document.getElementById('password').classList.remove('error');
        responseStatusText.textContent = "";
    }

    if (email.trim() === '' || password.trim() === '') {
        console.log('[!] Inputboxes are empty, aborting...');
        return;
    }

    var senddata = {
        data: 'login',
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
        const responseStatusText = document.querySelector("#response-status");

        if (data.status === 'Login: Credentials accepted') {
            console.log('200 OK; login authenticated');
            window.location.href = '/dashboard';
        } else if (data.status === 'Error: Invalid credentials') {
            document.getElementById('inputbox_deviceid').classList.add('error');
            document.getElementById('inputbox_password').classList.add('error');

            responseStatusText.textContent = "You have entered an invalid username or password";

            throw new Error("HTTP error; 401 Unauthorized; Invalid credentials");
        } else {
            console.log('520 Unknown; Unknown error occurred');
            responseStatusText.textContent = "An unknown error occured. Please fill out the 'contact us' form for assistance";
            
            throw new Error("HTTP error; 520 Unknown; Unknown error occurred");
        }
    })
    .catch(error => {
        // Håndterer fejl her
        console.error('Error:', error);
    });
}

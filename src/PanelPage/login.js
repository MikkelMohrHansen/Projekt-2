document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    var formData = {
        email: email,
        password: password
    };

    console.log(JSON.stringify(formData));  // Log the JSON string to the console
});
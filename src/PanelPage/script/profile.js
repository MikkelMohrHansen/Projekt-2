function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

document.addEventListener('DOMContentLoaded', function() {
    const studentId = getQueryParam('id');
    
    var senddata = {
        data: 'profile',
        id: studentId
    };

    if (studentId) {
        fetch('https://79.171.148.163/api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(senddata)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('name').textContent = data.navn;
            document.getElementById('school-team').textContent = data.uddannelseNavn;

            console.log("Recieved student average:", data);

            document.getElementById('check-in-percentage-text').textContent = data.attendance;
            
            if (data.checked_in_today == 1) {
                document.getElementsByClassName("check-in-mark")[0].src = "img/check-mark.png";
                document.getElementById('check-in-timestamp').textContent = data.checked_in_today_timestamp
            }
            else {
                document.getElementsByClassName("check-in-mark")[0].src = "img/x-mark.png";
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('name').textContent = 'Student ID not found';
    }
});
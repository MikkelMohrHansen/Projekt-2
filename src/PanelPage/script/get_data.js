setInterval(getData(), 40000);

function getData() {

    const studentId = getQueryParam('id');

    var senddata = {
        data: 'session get data',
        id: studentId
    };

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

        const StudentData = data.student_data;

        try {
            // 'student' i URL
            if (window.location.href.indexOf("student") > -1) {
                // Grab recording data for activity graph
                const event = new CustomEvent('updateGraph', { detail: { student_id: studentId, student_data: StudentData } });
                document.dispatchEvent(event);
            }

        } catch (error) {
            console.error('Error parsing student info:', error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

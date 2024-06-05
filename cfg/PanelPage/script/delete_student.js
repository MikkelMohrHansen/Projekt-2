document.getElementById('delete-student-submit-btn').addEventListener('click', function() {
    const checkedBoxes = document.querySelectorAll('input[name="student-checked"]:checked');
    const studentsToDelete = [];

    checkedBoxes.forEach(checkbox => {
        const studentDivId = checkbox.id.replace('student-checkbox-', 'student-');
        const studentLabel = document.getElementById(`${studentDivId}-title`);
        studentsToDelete.push(studentLabel.textContent);
    });

    if (studentsToDelete.length > 0) {
        var senddata = {
            data: 'delete students',
            students: studentsToDelete
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

            if (data.status === 'Students deleted') {
                console.log('Selected students have been deleted.');
                checkedBoxes.forEach(checkbox => {
                    const studentDiv = document.getElementById(checkbox.id.replace('student-checkbox-', 'student-'));
                    studentDiv.remove();
                });
            } else {
                console.error('Error:', data.status);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        console.log('No students selected for deletion.');
    }
});

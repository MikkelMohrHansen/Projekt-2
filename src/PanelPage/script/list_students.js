request_student();

function request_student() {
    var senddata = {
        data: 'request students',
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

        if (data.status === 'Retrieved student list') {
            console.log('200 OK student list recieved.');
            
            const studentContent = document.getElementById('student-content');
            studentContent.innerHTML = '';

            data.student_list.forEach((student, index) => {
                const studentDiv = document.createElement('div');
                studentDiv.id = `student-${index + 1}`;
                studentDiv.style.borderBottom = '2px solid black';
                studentDiv.style.paddingBottom = '10px';

                const studentLabel = document.createElement('label');
                studentLabel.id = `student-${index + 1}-title`;
                studentLabel.textContent = student.navn;

                const studentCheckbox = document.createElement('input');
                studentCheckbox.type = 'checkbox';
                studentCheckbox.id = `student-checkbox-${index + 1}`;
                studentCheckbox.name = 'student-checked';
                studentCheckbox.style.marginTop = '10px';

                const studentID = document.createElement('p');
                studentID.id = `student-${index + 1}-studentID`;
                studentID.className = `student-info`;
                studentID.textContent = student.studentID;

                const studentTeam = document.createElement('p');
                studentTeam.id = `student-${index + 1}-team`;
                studentTeam.className = `student-info`;
                studentTeam.textContent = student.uddannelseNavn;

                const studentStartdate = document.createElement('p');
                studentStartdate.id = `student-${index + 1}-startdate`;
                studentStartdate.className = `student-info`;
                studentStartdate.textContent = student.opstartsDato;


                studentDiv.appendChild(studentLabel);
                studentDiv.appendChild(studentCheckbox);
                studentDiv.appendChild(studentID);
                studentDiv.appendChild(studentTeam);
                studentDiv.appendChild(studentStartdate);

                studentContent.appendChild(studentDiv);
            });
        } else {
            console.error('Error:', data.status);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
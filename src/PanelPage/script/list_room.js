request_rooms();

function request_rooms() {
    var senddata = {
        data: 'request rooms',
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

        if (data.status === 'Retrieved room list') {
            console.log('200 OK team list recieved.');
            
            const roomsContent = document.getElementById('room-content');
            roomsContent.innerHTML = '';

            data.room_list.forEach((room, index) => {
                const roomDiv = document.createElement('div');
                roomDiv.id = `room-${index + 1}`;
                roomDiv.style.borderBottom = '2px solid black';
                roomDiv.style.paddingBottom = '10px';

                const roomLabel = document.createElement('label');
                roomLabel.id = `room-${index + 1}-title`;
                roomLabel.textContent = room.lokaleNavn;

                const roomCheckbox = document.createElement('input');
                roomCheckbox.type = 'checkbox';
                roomCheckbox.id = `room-checkbox-${index + 1}`;
                roomCheckbox.name = 'room-checked';
                roomCheckbox.style.marginTop = '10px';

                const lokaleID = document.createElement('p');
                lokaleID.id = `room-${index + 1}-lokaleID`;
                lokaleID.className = `lokale-info`;
                lokaleID.textContent = student.lokaleID;

                roomDiv.appendChild(roomLabel);
                roomDiv.appendChild(roomCheckbox);
                roomDiv.appendChild(lokaleID);

                roomsContent.appendChild(roomDiv);
            });
        } else {
            console.error('Error:', data.status);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
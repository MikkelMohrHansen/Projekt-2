document.getElementById('delete-room-submit-btn').addEventListener('click', function() {
    const checkedBoxes = document.querySelectorAll('input[name="room-checked"]:checked');
    const roomsToDelete = [];

    checkedBoxes.forEach(checkbox => {
        const roomDivId = checkbox.id.replace('room-checkbox-', 'room-');
        const roomLabel = document.getElementById(`${roomDivId}-title`);
        roomsToDelete.push(roomLabel.textContent);
    });

    if (roomsToDelete.length > 0) {
        var senddata = {
            data: 'delete rooms',
            rooms: roomsToDelete
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

            if (data.status === 'Rooms deleted') {
                console.log('Selected rooms have been deleted.');
                checkedBoxes.forEach(checkbox => {
                    const roomDiv = document.getElementById(checkbox.id.replace('room-checkbox-', 'room-'));
                    roomDiv.remove();
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

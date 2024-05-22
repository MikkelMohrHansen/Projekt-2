document.getElementById('inputbox_searchtimelogger').addEventListener('input', function() {
    const query = this.value;

    if (query.length > 0) {
        var senddata = {
            data: 'search',
            search: query
        };
        
        fetch('https://79.171.148.163/api', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(senddata)
        })
        .then(response => response.json())
        .then(data => {
            const resultsContainer = document.getElementById('search-results');
            resultsContainer.innerHTML = '';

            data.forEach(student => {
                const div = document.createElement('div');
                div.textContent = student.navn;
                div.addEventListener('click', () => {
                    console.log('Student ID:', student.studentID);
                    window.location.href = `student.html?id=${student.studentID}`;
                });
                resultsContainer.appendChild(div);
            });
        })
        .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('search-results').innerHTML = '';
    }
});

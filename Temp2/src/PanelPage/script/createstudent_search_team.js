document.getElementById('inputbox_student_team').addEventListener('input', function() {
    const query = this.value;

    if (query.length > 0) {
        var senddata = {
            data: 'search uddannelse',
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
            const resultsContainer = document.getElementById('search-results-uddannelse');
            resultsContainer.innerHTML = '';

            data.forEach(uddannelse => {
                const div = document.createElement('div');
                div.textContent = uddannelse.uddannelseNavn;
                div.addEventListener('click', () => {
                    document.getElementById('inputbox_student_team').value = uddannelse.uddannelseNavn;
                    resultsContainer.innerHTML = '';
                });
                resultsContainer.appendChild(div);
            });
        })
        .catch(error => console.error('Error:', error));
    } else {
        document.getElementById('search-results-uddannelse').innerHTML = '';
    }
});
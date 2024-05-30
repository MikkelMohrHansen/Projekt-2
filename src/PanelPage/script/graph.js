// Data til grafen
var data = {
    labels: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"],
    datasets: [] 
};

// Indstillinger for grafen
var options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        x: {
            title: {
                display: true,
                text: 'Timer'
            },
            beginAtZero: true
        },
        y: {
            title: {
                display: true,
                text: 'Fremmødeprocent'
            },
            beginAtZero: true
        }
    }
};

// Hent canvas og opret grafen
var ctx = document.getElementById('activity-chart').getContext('2d');
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: options
});

// Random int generator vi bruger til RGB randomizer
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener('updateGraph', function (event) {
    // Get existing datasets
    var datasets = myLineChart.data.datasets || [];

    // Opdater dataset med det modtaget info
    const { student_id, student_data } = event.detail;
    
    const randomRed = getRandomInt(0, 255);
    const randomGreen = getRandomInt(0, 255);
    const randomBlue = getRandomInt(0, 255);

    datasets.push({
        label: student_id,
        fill: false,
        borderColor: `rgb(${randomRed}, ${randomGreen}, ${randomBlue})`,
        data: student_data || []
    });

    myLineChart.data.datasets = datasets;

    myLineChart.update();
});

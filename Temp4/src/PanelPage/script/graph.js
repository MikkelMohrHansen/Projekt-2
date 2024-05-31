// Data til grafen (1=kommet, 0=ikke kommet)
var months = ["JAN", "FEB", "MAR", "APR", "MAJ", "JUN", "JUL", "AUG", "SEP", "OKT", "NOV", "DEC"];
var attendance = new Array(months.length).fill(0); // Initialize attendance array with zeros for all months

// Beregn månedlig gennemsnitlig check-in procentdel for hver måned
var monthlyAverages = attendance.map(month => 0); // Initialize monthly averages array with zeros for all months

// Function to update attendance based on check-in data
function updateAttendance(checkInData) {
    checkInData.forEach(entry => {
        const date = new Date(entry.checkIn);
        const monthIndex = date.getMonth(); // Get month index (0-11)
        attendance[monthIndex] = 1; // Mark check-in for this month
    });

    // Recalculate monthly averages
    monthlyAverages = attendance.map((month, index) => {
        const totalDays = new Date(new Date().getFullYear(), index + 1, 0).getDate(); // Get total days in month
        const attendedDays = month;
        return (attendedDays / totalDays) * 100;
    });
}

// Function to filter data for a specific month
function filterDataForMonth(monthIndex) {
    return attendance[monthIndex];
}

// Indstillinger for grafen
var options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
        y: {
            beginAtZero: true,
            max: 100,
            title: {
                display: true,
                text: 'Procent (%)'
            }
        },
        x: {
            title: {
                display: true,
                text: 'Måneder'
            }
        }
    }
};

// Hent canvas og opret grafen
var ctx = document.getElementById('myLineChart').getContext('2d');
var myLineChart = new Chart(ctx, {
    type: 'line',
    data: data,
    options: options
});

// Random int generator vi bruger til RGB randomizer
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

document.addEventListener('updateGraph', function(event) {
    const { student_data } = event.detail;

    // Update attendance based on received student data
    updateAttendance(student_data);

    // Update the data object and then call myLineChart.update() to refresh the chart
});

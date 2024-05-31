document.addEventListener('DOMContentLoaded', (event) => {
    const ctx = document.getElementById('activity-chart').getContext('2d');
    const myLineChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ["JAN", "FEB", "MAR", "APR", "MAJ", "JUN", "JUL", "AUG", "SEP", "OKT", "NOV", "DEC"],
            datasets: [{
                label: 'Attendance Percentage',
                data: [],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                fill: true,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            maintainAspectRatio: false, // Allow chart to adjust to its container size
            responsive: true, // Make the chart responsive
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw.toFixed(2) + '%';
                        }
                    }
                }
            }
        }
    });

    document.addEventListener('updateGraph', function(event) {
        console.log('Received event:', event);
        const { student_id, student_data } = event.detail;

        if (!student_data) {
            console.error('Invalid check-in data format:', student_data);
            return;
        }

        // Process the student_data to update the graph
        updateAttendance(student_data, myLineChart);
    });

    function updateAttendance(checkInData, chart) {
        console.log('Processing check-in data:', checkInData);

        if (!Array.isArray(checkInData)) {
            console.error('Invalid check-in data format:', checkInData);
            return;
        }

        // Initialize attendance array with 0s for each month
        let attendance = new Array(12).fill(0);
        let daysInMonth = new Array(12).fill(0);

        // Update attendance based on checkInData
        checkInData.forEach(checkIn => {
            let checkInDate = new Date(checkIn.checkIn);
            let monthIndex = checkInDate.getMonth();
            attendance[monthIndex] += 1;
            daysInMonth[monthIndex] = Math.max(daysInMonth[monthIndex], checkInDate.getDate());
        });

        // Calculate attendance percentage
        let attendancePercentage = attendance.map((count, index) => {
            return daysInMonth[index] > 0 ? (count / daysInMonth[index]) * 100 : 0;
        });

        console.log('Attendance percentage:', attendancePercentage);

        // Update chart data
        chart.data.datasets[0].data = attendancePercentage;
        chart.update();
    }
});


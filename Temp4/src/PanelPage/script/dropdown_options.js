document.addEventListener('DOMContentLoaded', function () {
    var hold = document.getElementById('teams');
    var studerende = document.getElementById('students');

    hold.addEventListener('click', function () {
        window.location.href = './teams.html';
    });

    studerende.addEventListener('click', function () {
        window.location.href = './students.html';
    });
});
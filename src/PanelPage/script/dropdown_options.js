document.addEventListener('DOMContentLoaded', function () {
    var hold = document.getElementById('teams');
    var studerende = document.getElementById('students');
    var lokaler = document.getElementById('rooms');

    hold.addEventListener('click', function () {
        window.location.href = './teams.html';
    });

    studerende.addEventListener('click', function () {
        window.location.href = './students.html';
    });

    lokaler.addEventListener('click', function () {
        window.location.href = './rooms.html';
    });
});
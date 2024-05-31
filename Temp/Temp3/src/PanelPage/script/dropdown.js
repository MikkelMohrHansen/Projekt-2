document.addEventListener('DOMContentLoaded', function () {
    var dropdownBtn = document.getElementById('dropdown_btn');
    var dropdownOptions = document.getElementById('options');

    dropdownBtn.addEventListener('click', function () {
        dropdownOptions.classList.toggle('active');
    });
});
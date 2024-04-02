document.addEventListener('DOMContentLoaded', function() {
    let deleteButtons = document.querySelectorAll('.delete-button');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(event) {
            event.preventDefault();
            if (confirm('Are you sure you want to delete this user?')) {
                let form = button.parentElement;
                form.submit();
            }
        });
    });
});

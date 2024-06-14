
document.addEventListener('DOMContentLoaded', function () {

    // Setting volume reduced at loading of the page 
    var audioElement = document.getElementById('audio-example');
    if (audioElement) {
        audioElement.volume = 0.2;
    }

    // Handling playlist items modals

    const toggles = document.querySelectorAll('.nav-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('change', function () {
            // Unchecking all other checkboxes
            toggles.forEach(otherToggle => {
                if (otherToggle !== this) {
                    otherToggle.checked = false;
                    const otherLabel = otherToggle.nextElementSibling;
                    const otherArticle = otherLabel.nextElementSibling;
                    otherLabel.style.color = 'antiquewhite';
                    otherArticle.classList.remove('show');
                }
            });

            // Handling the current checkbox
            const label = this.nextElementSibling;
            const article = label.nextElementSibling;
            if (this.checked) {
                label.style.color = 'red';
                article.classList.add('show');
            } else {
                label.style.color = 'antiquewhite';
                article.classList.remove('show');
            }
        });
    });
});
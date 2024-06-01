
document.addEventListener('DOMContentLoaded', function() {

    // Setting volume reduced at loading of the page 
    var audioElement = document.getElementById('audio-example');
    audioElement.volume = 0.2;

    // Handling playlist items modals
    const toggles = document.querySelectorAll('.nav-toggle');

    toggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            // Unchecking all other checkboxes
            toggles.forEach(otherToggle => {
                if (otherToggle !== this) {
                    otherToggle.checked = false;
                    const otherLabel = otherToggle.nextElementSibling;
                    const otherArticle = otherLabel.nextElementSibling;
                    otherLabel.style.color = 'antiquewhite';
                    otherArticle.style.opacity = '0';
                    otherArticle.style.maxHeight = '0';
                }
            });

            // Handling the current checkbox
            const label = this.nextElementSibling;
            const article = label.nextElementSibling;
            if (this.checked) {
                label.style.color = 'red';
                article.style.opacity = '1';
                article.style.maxHeight = '100dvh';
            } else {
                label.style.color = 'antiquewhite';
                article.style.opacity = '0';
                article.style.maxHeight = '0';
            }
        });
    });
});




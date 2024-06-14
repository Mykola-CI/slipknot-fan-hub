
document.addEventListener('DOMContentLoaded', function () {

    // Setting volume reduced at loading of the page 
    const allAudios = document.querySelectorAll('audio');
    allAudios.forEach(audio => {
        audio.volume = 0.2;
    });

    // Handling playlist items modals

    const toggles = document.querySelectorAll('.nav-toggle');
    

    toggles.forEach(toggle => {
        toggle.addEventListener('change', function () {

            // Stop all audio elements when playlist item is closed or new item opened
            allAudios.forEach(audio => {
                audio.pause();
                audio.currentTime = 0;
            });

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
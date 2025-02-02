window.onload = function () {
    // Check if it's the user's first time
    if (!localStorage.getItem('visited')) {
        // If it's the first visit, show the splash screen
        setTimeout(function () {
            // Display the loader after the text animation finishes
            document.querySelector('.loader-container').style.display = 'block';
        }, 2000); // Delay for text animation

        // After 5 seconds, fade-out splash screen and display home page text
        setTimeout(function () {
            // Fade out splash screen
            document.getElementById('splash-screen').style.opacity = 0;

            // After the fade-out completes, hide splash screen and show home page
            setTimeout(function () {
                document.getElementById('splash-screen').style.display = 'none';
                document.getElementById('home-page').style.display = 'block';

                // Fade-in effect for home page text
                setTimeout(function () {
                    document.getElementById('home-page').style.opacity = 1;
                }, 10); // Small delay to trigger the opacity change
            }, 1000); // Wait for the fade-out animation to finish
        }, 5000); // 5-second delay before starting the transition

        // Mark the user as having visited
        localStorage.setItem('visited', 'true');
    } else {
        // If the user has visited before, skip the splash screen and show the home page
        document.getElementById('splash-screen').style.display = 'none';
        document.getElementById('home-page').style.opacity = '1';
    }
};
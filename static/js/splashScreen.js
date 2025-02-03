window.onload = () => {
    // Check if it's the user's first time
    if (!localStorage.getItem('visited')) {
        setTimeout(() => {
            document.querySelector('.loader-container').style.display = 'block';
        }, 2000);

        setTimeout(() => {
            document.getElementById('splash-screen').style.opacity = 0;

            setTimeout(() => {
                document.getElementById('splash-screen').style.display = 'none';
                document.getElementById('home-page').style.display = 'block';

                setTimeout(() => {
                    document.getElementById('home-page').style.opacity = 1;
                }, 10);
            }, 1000);
        }, 5000);
        localStorage.setItem('visited', 'true');
    } else {
        document.getElementById('splash-screen').style.display = 'none';
        document.getElementById('home-page').style.opacity = '1';
    }
};
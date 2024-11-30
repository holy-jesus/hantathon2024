() => {
    const images = document.querySelectorAll('img');
    for (const img of images) {
        if (!img.hasAttribute('alt')) {
            return false;
        }
    }
    return true;
};

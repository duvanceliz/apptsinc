
document.addEventListener('DOMContentLoaded', function() {
    const scrollBox = document.getElementById('container-dropzone');
    let scale = 1;

    document.addEventListener('wheel', function(event) {
        if (event.ctrlKey) {
            event.preventDefault();
            if (event.deltaY < 0) {
                scale += 0.1;
            } else {
                scale -= 0.1;
                if (scale < 0.1) {
                    scale = 0.1;
                }
            }
            scrollBox.style.transform = `scale(${scale})`;
        }
    });

    scrollBox.addEventListener('wheel', function(event) {
        if (event.ctrlKey) {
            event.preventDefault();
        }
    });
});
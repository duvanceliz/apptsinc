function centerScroll() {
    const container = document.getElementById('parent-container-dropzone');
    const content = container.firstElementChild;

    const centerX = (content.offsetWidth - container.clientWidth) / 2;
    const centerY = (content.offsetHeight - container.clientHeight) / 2;

    container.scrollLeft = centerX;
    container.scrollTop = centerY;
}

// Ejecutar la función al cargar la página
window.addEventListener('load', centerScroll);
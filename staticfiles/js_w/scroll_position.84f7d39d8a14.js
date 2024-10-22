

// Guardar la posición de desplazamiento antes de recargar la página
window.addEventListener('beforeunload', function() {
    localStorage.setItem('scrollPosition', window.scrollY);
});

// Restaurar la posición de desplazamiento al cargar la página
window.addEventListener('load', function() {
    let scrollPosition = localStorage.getItem('scrollPosition');
    if (scrollPosition) {
        window.scrollTo(0, scrollPosition);
    }
    
});

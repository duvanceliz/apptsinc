function toggleSubfolders(button) {
    // Obtener la siguiente etiqueta <ul> que contiene las subcarpetas
    var subfolderList = button.parentElement.querySelector('ul');

    if (subfolderList) {
    if (subfolderList.style.display === "none") {
        subfolderList.style.display = "block";
        button.innerHTML = `<i class="bi bi-caret-down-fill"></i>`;  // Cambiar el texto del botón para mostrar que se puede colapsar
    } else {
        subfolderList.style.display = "none";
        button.innerHTML = `<i class="bi bi-caret-right-fill"></i>`; // Cambiar el texto del botón para mostrar que se puede expandir
    }
}
}
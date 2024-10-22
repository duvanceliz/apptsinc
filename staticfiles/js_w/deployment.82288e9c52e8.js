
document.addEventListener("DOMContentLoaded", function () {
    var items = tree.querySelectorAll('ul');
    const navTree = document.getElementById("nav-tree")

    items.forEach(item => {

        var state = localStorage.getItem(`${item.dataset.id}`);

        item.style.display = state
       
        
    });

    navTree.style.display = localStorage.getItem("navtree")

});


    function toggleSubfolders(button) {
    // Obtener la siguiente etiqueta <ul> que contiene las subcarpetas
    var subfolderList = button.parentElement.querySelector('ul');
    if (subfolderList) {
        if (subfolderList.style.display === "none") {
            subfolderList.style.display = "block";
            localStorage.setItem(`${subfolderList.dataset.id}`,'block')
            
            // localStorage.setItem('folderColor',subfolderList.style.background)
        button.innerHTML = `<button class="btn btn-light btn-sm" ><i class="bi bi-folder2-open"></i></button>`;  // Cambiar el texto del botón para mostrar que se puede colapsar
    } else {
        subfolderList.style.display = "none";
        
        localStorage.setItem(`${subfolderList.dataset.id}`,'none')
        button.innerHTML = `<button class="btn btn-light btn-sm"><i class="bi bi-folder"></i></button>`; // Cambiar el texto del botón para mostrar que se puede expandir
    }
}
}

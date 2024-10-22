

// document.addEventListener("DOMContentLoaded", function() {
//     document.getElementById("loading-overlay").style.display = "flex";
// });
// window.addEventListener("load", function() {
//     document.getElementById("loading-overlay").style.display = "none";
// });

document.addEventListener("DOMContentLoaded", function() {
    var overlay = document.getElementById("loading-overlay");

    document.querySelectorAll("#loader").forEach(function(link) {
        link.addEventListener("click", function(event) {
            
            overlay.style.display = "flex"; // Mostrar la superposición con el spinner
          
        });
    });

    window.addEventListener("load", function(event) {
        overlay.style.display = "none";
    });
 
    
});

// var loadingInterval = setInterval(function() {
//     if (document.readyState === "loading") {
//         console.log("La página está cargando...");
//         // Aquí puedes mostrar un spinner o actualizar una barra de progreso
//         overlay.style.display = "flex";
//     } else {
//         clearInterval(loadingInterval); // Detén el intervalo cuando termine de cargar
//         overlay.style.display = "none";
//         console.log("Carga completa");
//     }
// }, 100); // Intervalo de verificación cada 100ms

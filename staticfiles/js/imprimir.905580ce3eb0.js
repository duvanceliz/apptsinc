

function printDropzoneContent() {
    // Obtiene el contenido de la dropzone
    const dropzone = document.getElementById('outer-dropzone');
    const svgContent = dropzone.innerHTML;

    // Crea una nueva ventana o iframe
    const printWindow = window.open('', '_blank');
    printWindow.document.open();
    printWindow.document.write(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Print SVG</title>
             <style>
            .iframe {
        
                    background-color: #21242b;
                    /* border: 2px dashed rgb(148, 146, 146); */
                    border-radius: 4px;
                    margin: 0;
                    padding: 10px;
                    width: 1000px;
                    height: 1000px;
                    transition: background-color 0.3s;
                    background: 
                    linear-gradient(to right, #6060607b 1px, transparent 1px),
                    linear-gradient(to bottom, #6060607b 1px, transparent 1px);
                    background-size: 20px 20px;
                    border: 1px solid #6c6c6c;
                    padding: 20px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    /* transform: translate(50%,50%); */
                    user-select: none;

            }
            </style>
        </head>
        <body>
             <div class="iframe">
               ${
                svgContent
               }
             <div>
        </body>
        </html>
    `);
    printWindow.document.close();

    // Espera a que el contenido se cargue completamente antes de imprimir
    // printWindow.onload = function() {
    //     printWindow.print();
    //     printWindow.close();
    // };
}
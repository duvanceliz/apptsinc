

function verificar() {

    let resultado = window.confirm('Estas seguro de borrar el proyecto?');
    if (resultado === true) {
        return true
    } else {
        return false
    }

}


function confirm_delete_folder() {

    let resultado = window.confirm('Estás seguro de borrar la carpeta?, esta accción eliminará todo los archivos que contenga');
    if (resultado === true) {
        return true
    } else {
        return false
    }

}

function confirm_delete_file() {

    let resultado = window.confirm('¿Estás seguro de borrar el proyecto?');
    if (resultado === true) {
        return true
    } else {
        return false
    }

}
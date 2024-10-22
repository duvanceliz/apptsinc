function confirm_delete_folder() {

    let resultado = window.confirm('Estás seguro de borrar la carpeta?');
    if (resultado === true) {
        return true
    } else {
        return false
    }

}


function verificar() {

    let resultado = window.confirm('Estas seguro de borrar el proyecto?');
    if (resultado === true) {
        return true
    } else {
        return false
    }

}
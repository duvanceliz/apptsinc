const btntotal = document.getElementById('btntotal')
const dashboard_id = document.getElementById('dashboard-id').value


function abrirVentana() {
    window.open(
        `http://localhost:8000/totalproducts/?id=${dashboard_id}`, 
        '_blank',
        'width=800,height=400,top=100,left=100'
    );
}

btntotal.addEventListener('click',e=>{

    abrirVentana();
})


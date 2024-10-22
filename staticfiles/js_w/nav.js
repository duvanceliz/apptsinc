document.addEventListener("DOMContentLoaded", function () {
    var tree = document.getElementById('tree');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    


    function save_to_database(items){
        var order = [];
        items.forEach((item,index)=>{
            var parent = item.parentElement.closest('li');
            order.push({
                id: item.dataset.id,
                parent: parent ? parent.dataset.id : null,  // Captura el ID del padre
                order: index  // Index de la posición
            });
        })

        axios.post('/update_tree_order/', {
            order: order
        }, {
            headers: {
                'X-CSRFToken': csrfToken
            }
        })
        .then(response => {
            console.log('Orden actualizado:', response.data);
        })
        .catch(error => {
            console.error('Error al actualizar el orden:', error);
        });
        

    }
    // Inicializa Sortable en la raíz del árbol
    new Sortable(tree, {
        group: 'nested', // Permite el anidamiento
        animation: 150,
        fallbackOnBody: true,
        swapThreshold: 0.65,
        // Recorre todos los elementos anidados
        onEnd: function (evt) {
            
            var items = tree.querySelectorAll('li');

           save_to_database(items)

            // var itemEl = evt.item; // Elemento arrastrado
            // console.log('Orden cambiado: ' + itemEl.dataset.id);
            // Aquí puedes hacer una llamada a tu backend para actualizar el orden
        },
        onMove: function (evt, originalEvent) {
            evt.dragged.style.backgroundColor = '#f0f0f0';
        }
    });

    // Inicializa Sortable en los subelementos
    var nestedLists = tree.querySelectorAll('ul');
    nestedLists.forEach(function (nestedList) {
        new Sortable(nestedList, {
            group: 'nested',
            animation: 150,
            fallbackOnBody: true,
            swapThreshold: 0.65,
            onEnd: function (evt) {
                var items = tree.querySelectorAll('li');
                save_to_database(items)
            }
        });
    });
});




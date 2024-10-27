document.addEventListener("DOMContentLoaded", function () {
    var table1 = document.getElementById('table-1');
    var table2 = document.getElementById('table-2');
    var table3 = document.getElementById('table-3');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    function post(url, data, csrfToken) {
        axios
        .post(url, data, {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        })
        .then(function (response) {
          // document.getElementById('mensaje').innerText = response.data.mensaje;
          console.log(response.data.mensaje);
                
            })
            .catch(function (error) {
              // document.getElementById('mensaje').innerText = 'Error: ' + error.response.data.mensaje;
              console.log(error.response.data.mensaje);
            });
        }
    
    new Sortable(table1, {
        group: 'shared', // set both lists to same group
        animation: 150,
        onAdd: function (evt) {
        
            const data = {
                task_id:evt.item.dataset.id,
                container:'container1'
            }
            console.log(data)
            post("/save_order_container_task/",data,csrfToken)
            
        }
    });
    
    new Sortable(table2, {
        group: 'shared',
        animation: 150,
        onAdd: function (evt) {
           
            const data = {
                task_id:evt.item.dataset.id,
                container:'container2'
            }
            console.log(data)
            post("/save_order_container_task/",data,csrfToken)
          
        }
    });

    new Sortable(table3, {
        group: 'shared',
        animation: 150,
        onAdd: function (evt) {
           
            const data = {
                task_id:evt.item.dataset.id,
                container:'container3'
            }
            console.log(data)
            post("/save_order_container_task/",data,csrfToken)
           
        }
    });

});

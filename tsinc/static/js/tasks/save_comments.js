
const comment = document.getElementById("comment")
const btnModal = document.querySelectorAll("#btn-modal")
const btnCommentSave = document.getElementById("btn-comment-save")
const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const eventState = {
    btn: null,
  };



function post(url, data, csrfToken) {
    axios
    .post(url, data, {
      headers: {
        "X-CSRFToken": csrfToken,
      },
    })
    .then(function (response) {
      // document.getElementById('mensaje').innerText = response.data.mensaje;
      console.log(response.data.status);
      const notificacion = document.getElementById("notificacion");
      const mensajeNotificacion = document.getElementById("mensajeNotificacion");

      if (response.data.status) {
          // Mostrar mensaje de éxito
          mensajeNotificacion.textContent = '¡Formulario enviado con éxito!';
          notificacion.style.backgroundColor = '#28a745'; // Verde
          mostrarNotificacion();
      } else {
          // Mostrar mensaje de error
          mensajeNotificacion.textContent = 'Hubo un problema al enviar el formulario.';
          notificacion.style.backgroundColor = '#dc3545'; // Rojo
          mostrarNotificacion();
      }
      
            
        })
        .catch(function (error) {
          // document.getElementById('mensaje').innerText = 'Error: ' + error.response.data.mensaje;
          
            // Mostrar mensaje de error si hay un fallo en la solicitud
            if(error){
              const notificacion = document.getElementById("notificacion");
            const mensajeNotificacion = document.getElementById("mensajeNotificacion");
            mensajeNotificacion.textContent = 'Ocurrió un error al enviar el formulario.';
            notificacion.style.backgroundColor = '#dc3545'; // Rojo
            mostrarNotificacion();
            console.error("Error:", error);

            }
            
        });
    }


btnModal.forEach((btn)=>{
    btn.addEventListener("click",(item)=>{

        eventState.btn = btn
        
    })
} )

btnCommentSave.addEventListener("click",(e)=>{
    

    const data= {
        task_id:eventState.btn.dataset.task_id,
        message:comment.value 
    }

    if (!comment.value){

        data.message = null
       
    }

    post("/comment/save/",data,csrfToken)
    
})

function mostrarNotificacion() {
  const notificacion = document.getElementById("notificacion");
  notificacion.style.display = 'block'; // Mostrar el div
  setTimeout(() => {
      notificacion.style.display = 'none'; // Ocultar después de 3 segundos
  }, 3000);
}







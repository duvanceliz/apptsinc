
const btnModalTwo = document.querySelectorAll("#btn-modal-two")
const btnSendFile = document.getElementById("btn-send-file")
const csrfTokenTwo = document.querySelector('[name=csrfmiddlewaretoken]').value;
const fileInput = document.getElementById('fileInput');
const eventStateTwo = {
    btn: null,
  };


function post2(url, data, csrfToken) {
    axios
    .post(url, data, {
      headers: {
        'Content-Type': 'multipart/form-data',
        "X-CSRFToken": csrfToken,
      },
    })
    .then(function (response) {
      // document.getElementById('mensaje').innerText = response.data.mensaje;
      console.log(response.data.message);
      const alert = document.getElementById("alert-notification");
      const alertMessage = document.getElementById("alert-message");

      if (response.data.message) {
          // Mostrar mensaje de éxito
          alertMessage.textContent = '¡Formulario enviado con éxito!';
          alert.style.backgroundColor = '#28a745'; // Verde
          showAlert();
      } else {
          // Mostrar mensaje de error
          alertMessage.textContent = 'Hubo un problema al enviar el formulario.';
          alert.style.backgroundColor = '#dc3545'; // Rojo
          showAlert();
      }
      
            
        })
        .catch(function (error) {
          // document.getElementById('mensaje').innerText = 'Error: ' + error.response.data.mensaje;
          
            // Mostrar mensaje de error si hay un fallo en la solicitud
            const alert = document.getElementById("alert-notification");
            const alertMessage = document.getElementById("alert-message");
            alertMessage.textContent = 'Ocurrió un error al enviar el formulario.';
            alert.style.backgroundColor = '#dc3545'; // Rojo
            showAlert();
            console.error("Error:", error);
        });
    }


    
btnModalTwo.forEach((btn)=>{
    btn.addEventListener("click",(item)=>{

        eventStateTwo.btn = btn   
    })
} )


btnSendFile.addEventListener("click",(e)=>{
    
    // Crear el objeto FormData
    const file = fileInput.files[0];
    
    // Crear el objeto FormData
    const data = new FormData();
    data.append('file', file); // 'file' es la clave que usará Django para identificar el archivo
    
    // Si necesitas agregar información adicional
    data.append('task_id', eventStateTwo.btn.dataset.task_id);


    post2("/upload_task_file/",data,csrfTokenTwo)
    
})

function showAlert() {
  const alert = document.getElementById("alert-notification");
  alert.style.display = 'block'; // Mostrar el div
  setTimeout(() => {
      alert.style.display = 'none'; // Ocultar después de 3 segundos
  }, 3000);
}






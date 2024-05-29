const btnsave = document.querySelector("#save");
const csrfToken = document.querySelector("#form > input");
const form = document.getElementById("form");
const dash_id = document.getElementById("dashboard_id").value;


form.addEventListener("submit", (e) => {
  e.preventDefault();
  const listItem = [];
  const listLabel = [];
  const todositem = document.querySelectorAll("div.dropzone > img");
  const todoslabel = document.querySelectorAll("div.dropzone > input");
  todositem.forEach((todo) => {
    const obj = {};
    obj.pk = todo.getAttribute("pk");
    obj.id_code = todo.getAttribute("id_code");
    obj.x = todo.getAttribute("data-x");
    obj.y = todo.getAttribute("data-y");
    obj.zindex = todo.style.zIndex;
    obj.width = todo.style.width;
    obj.height = todo.style.height;
    listItem.push(obj);
  });
  todoslabel.forEach((todo) => {
    
    const obj = {};
    obj.id_code = todo.getAttribute("id_code");
    obj.x = todo.getAttribute("data-x");
    obj.y = todo.getAttribute("data-y");
    obj.value = todo.value;
    obj.width = todo.style.width;
    obj.height = todo.style.height;
    obj.zindex = todo.style.zIndex;
    listLabel.push(obj);
  });

  axios
    .post(
      "/saveitems/",
      {
        dashboard_id: dash_id,
        values: listItem,
        labels: listLabel
      },
      {
        headers: {
          "X-CSRFToken": csrfToken.value,
        },
      }
    )
    .then(function (response) {
      // document.getElementById('mensaje').innerText = response.data.mensaje;
      console.log(response.data.mensaje);
    })
    .catch(function (error) {
      // document.getElementById('mensaje').innerText = 'Error: ' + error.response.data.mensaje;
      console.log(error.response.data.mensaje);
    });
});

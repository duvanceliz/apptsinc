const car = document.getElementById("car");
const btn_save = document.getElementById("btn-save");
const csrfToken = document.querySelector("#form > input").value;
const ids = [];



function post(url, data, csrfToken) {
  axios
  .post(url, data, {
    headers: {
      "X-CSRFToken": csrfToken,
    },
  })
  .then(function (response) {
    // document.getElementById('mensaje').innerText = response.data.mensaje;
    // console.log(response.data.mensaje);
          const alert_n = document.querySelector(".notification-save")
          alert_n.classList.toggle("visible");

          setTimeout(() => {
           alert_n.classList.remove("visible");
           alert_n.classList.add("fade-out");
          }, 2000);
          setTimeout(() => {
           alert_n.classList.remove("fade-out");
          }, 2000);

      })
      .catch(function (error) {
        // document.getElementById('mensaje').innerText = 'Error: ' + error.response.data.mensaje;
        console.log(error.response.data.mensaje);
      });
  }

for (let tr of car.getElementsByTagName("tr")) {
  // Itera a través de los td dentro de cada tr
  for (let th of tr.getElementsByTagName("th")) {
    // Obtiene el texto dentro de cada td
    //  console.log(th.textContent);
    ids.push(parseInt(th.textContent));
  }
}


btn_save.addEventListener("click", (e) => {
    const products = [];
  for (id of ids) {
    const obj = {};
    const quantity = document.getElementById(`quantity${id}`);
    const price = document.getElementById(`price${id}`);
    obj.id = id;
    obj.quantity = quantity.value;
    obj.price = price.value;
    products.push(obj);
  }

  post("/savecar/",{values:products},csrfToken)
});

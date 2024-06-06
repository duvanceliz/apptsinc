const eventState = {
  target: null,
};

const eventState2 = {
  target: null,
};

const eventStateTable = {
  target: null,
};
const btndelete = document.getElementById("delete");
const form2 = document.getElementById("form2");
const btnon = document.getElementById("on");
const btnunder = document.getElementById("under");
const btnclone = document.getElementById("clone");
const alertdiv = document.getElementById("alert");
const btnlabel = document.getElementById("btnlabel");
const btnsave = document.querySelector("#save");
const csrfToken = document.querySelector("#form > input").value;
const form = document.getElementById("form");
const dash_id = document.getElementById("dashboard_id").value;
const btnInventory = document.getElementById("btnInventory");
const results = document.getElementById("results");
// const linkProduct = document.getElementById("link-product");
const formSearch = document.getElementById("form-search");
const dropzone = document.getElementById("outer-dropzone");
const todo = document.querySelectorAll(
  "div.dropzone > img, div.dropzone > input"
);

// Función para guardar la posición de un elemento
function savePosition(itemId, x, y) {
    const positions = JSON.parse(localStorage.getItem("itemPositions")) || {};
    positions[itemId] = { x: x, y: y };
    localStorage.setItem("itemPositions", JSON.stringify(positions));
}

//*************************************************** */
// HACE UNA PETICION POST AL SERVIDOR
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

//*************************************************** */
// FUNCION PARA GENERAR UN CODIGO ALEATORIO
function generateCode(length) {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}
//*************************************************** */

//************************************************** */
// FUNCION QUE CAMBIA EL Z-INDEX
function changeZindex(btn) {
  if (btn.id == "on") {
    eventState2.target.style.zIndex = "10";
  }
  if (btn.id == "under") {
    eventState2.target.style.zIndex = "0";
  }
}
//************************************************** */

//************************************************** */
//FUNCION LIMPIA LA SELECCION DE TODOS LOS ELEMENTOS
function clean(todo) {
  todo.forEach((item) => {
    item.style.backgroundColor = "rgba(0, 0, 0, 0)";
  });
}
//************************************************** */

// SI LA DROPZONE ES CLICKEADA LIMPIA LA SELECCION
//DESACTIVA TODOD LOS BOTONES SUPERIORES Y EL PANEL DERECHO
dropzone.addEventListener("click", (e) => {
  if (e.target.id == "outer-dropzone") {
    const todo = document.querySelectorAll(
      "div.dropzone > img, div.dropzone > input"
    );
    
    console.log('click zona')
    clean(todo);
    panel.innerHTML = ``;
    btnon.disabled = true;
    btnunder.disabled = true;
    btndelete.disabled = true;
    btnclone.disabled = true;

  }
});

//************************************************** */

//*************************************************** */

// LINKEA LOS PRODUCTO A CADA ITEM DE LA DAHSBOARD
// linkProduct.addEventListener("click", (e) => {
//   if (eventState2.target.getAttribute("pk")) {
//     eventState2.target.setAttribute("product_id", eventStateTable.target.id);
//     console.log(eventState2.target);
//     console.log(eventStateTable.target);
//   }
// });

//*************************************************** */

//*************************************************** */

// HACE UNA BUSQUEDA DE LOS PRODUCTOS EN EL INVENTARIO
formSearch.addEventListener("submit", (e) => {
  e.preventDefault();

  const inputSearch = document.getElementById("input-search").value;
  axios
    .post(
      "/productsearch/",
      {
        search: inputSearch,
      },
      {
        headers: {
          "X-CSRFToken": csrfToken,
        },
      }
    )
    .then(function (response) {
      console.log(response.data);
      results.innerHTML = ``;
      response.data.forEach((obj) => {
        results.innerHTML += `
            <tr id="${obj.id}">
              <th scope="row">${obj.id}</th>
              <td>${obj.product_name}</td>
              <td>${obj.model}</td>
              <td>${obj.brand}</td>
              <td>${obj.sale_price}</td>
              </tr>
        `;
      });
      const interactItemTable = document.querySelectorAll("#results > tr");
      interactItemTable.forEach((row) => {
        row.addEventListener("click", (e) => {
          interactItemTable.forEach((row) => {
            row.style = "";
          });
          eventStateTable.target = row;
          row.style.border = "2px solid white";
        });
      });
    })
    .catch(function (error) {
      // document.getElementById('mensaje').innerText = 'Error: ' + error.response.data.mensaje;
      console.log(error.response.data.mensaje);
    });
});

//*************************************************** */

//*************************************************** */
// ENVIA TODO LOS ITEMS AL SERVIDOR Y LOS GUARDA EN LA BASE DE DATOS
form.addEventListener("submit", (e) => {
  e.preventDefault();
  
  clean(todo)
  btnsave.disabled = true;
  alertdiv.hidden = true;
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
    obj.product_id = todo.getAttribute("product_id");
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

  //"/saveitems/"
  const data = {
    dashboard_id: dash_id,
    values: listItem,
    labels: listLabel,
  };

  post("/saveitems/", data, csrfToken);
});
//*************************************************** */

//*************************************************** */

//BOTON LABEL: AGREGA UN NUEVO LABEL A LA DASHBOARD

btnlabel.addEventListener("click", (e) => {

clean(todo)
  let newInput = document.createElement("input");
  newInput.style.width = "100px";
  newInput.style.height = "40px";
  newInput.style.textAlign = "center";
  newInput.style.zIndex = "0";
  newInput.setAttribute("id_code", generateCode(4));
  newInput.style.backgroundColor = "rgba(0, 0, 0, 0)";
  newInput.style.color = "white";
  newInput.style.border = "1px solid white";
  newInput.className = "drag-drop";
  dropzone.appendChild(newInput);
});

//*************************************************** */

//*************************************************** */

// BONTON ENCIMA: CAMBIA EL Z-INDEX DE UN ITEM SELECIONADO
btnon.addEventListener("click", (e) => {
  changeZindex(btnon);
});

//*************************************************** */

//*************************************************** */
//BOTON DEBAJO: CAMBIA EL Z-INDEX DE UN ITEM SELECIONADO
btnunder.addEventListener("click", (e) => {
  changeZindex(btnunder);
});

//*************************************************** */

//*************************************************** */
//BOTON CLONAR: CLONA UN ITEM SELECCIONADO
btnclone.addEventListener("click", (e) => {
  // console.log(eventState2.target)
  clean(todo)
  const clone = eventState2.target.cloneNode(true);

  clone.setAttribute("id_code", generateCode(4));
  clone.style.transform = "translate(-16.3754px, -19.729px)";
  clone.setAttribute("data-x", "-16.3754");
  clone.setAttribute("data-y", "-19.729");
  clone.style.backgroundColor = "rgba(0, 0, 0, 0)";
  dropzone.appendChild(clone);
  //   // clone.style.width = "auto";
  //   clone.style.zIndex = "0";
  //
  //
});
//*************************************************** */

//*************************************************** */

// BORRA UN ITEM SELECCIONADO DE LA BASE DE DATO
form2.addEventListener("submit", (e) => {
  e.preventDefault();
  const csrfToken = document.querySelector("#form2 > input").value;
  const item = eventState2.target;

  const data = {
    id_code: item.getAttribute("id_code"),
  };
  post("/deleteitem/", data, csrfToken);
  item.remove();
});
//*************************************************** */

//*************************************************** */
// LE AGREGA UN EVENTO DE ESCUCHA DARGSTART A CADA ITEM DEL PANEL Y LE PASA EL TARGET AL OBJ EVENTSTATE
const items = document.querySelectorAll("#item").forEach((item) => {
  item.addEventListener("dragstart", (e) => {
    eventState.target = e.target;
  });
});

//*************************************************** */

//*************************************************** */
// UNA VEZ ARRASTRADO Y SOLTADO DENTRO DE LA ZONA EL ITEM ES CLONADO.
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
});

dropzone.addEventListener("drop", (e) => {
  if (eventState.target.id == "item") {
    const clone = eventState.target.cloneNode(true);
    clone.classList.add("drag-drop");
    clone.removeAttribute("id");
    // clone.style.width = "auto";
    clone.style.zIndex = "0";
    clone.setAttribute("id_code", generateCode(4));
    dropzone.appendChild(clone);
  }
});
//*************************************************** */

//*************************************************** */
// FUNCION PARA MOVER CADA ITEM DENTRO DE LA ZONA
function dragMoveListener(event) {
  var target = event.target;

  // keep the dragged position in the data-x/data-y attributes
  var x = (parseFloat(target.getAttribute("data-x")) || 0) + event.dx;
  var y = (parseFloat(target.getAttribute("data-y")) || 0) + event.dy;

  // translate the element
  target.style.transform = "translate(" + x + "px, " + y + "px)";

  // update the posiion attributes
  target.setAttribute("data-x", x);
  target.setAttribute("data-y", y);
}
//*************************************************** */

//*************************************************** */
// AGREGA UNA ITERACCION DE CLICK A TODOS LOS ITEMS DENTRO DE LA ZONA
//DESACTIVA TODO LOS BOTONES
//AGREGA EL PANEL DERECHO CON LA INFORMACION
//AGREGA SELECCION

interact(".drag-drop")
  .on("tap", function (event) {
    // event.currentTarget.classList.toggle("switch-bg");
    console.log("click al objeto");

    clean(todo);

    btnon.disabled = false;
    btnunder.disabled = false;
    btndelete.disabled = false;
    btnclone.disabled = false;
    btnInventory.disabled = false;
    eventState2.target = event.target;
    btnsave.disabled = false

    panel.innerHTML = `
      
      <input class="form-control form-control-sm bg-dark text-white" type="text" disabled value=" Item: ${event.target.getAttribute(
        "id_code"
      )}" aria-label=".form-control-sm example">
      <input class="form-control form-control-sm bg-dark text-white" type="text" disabled value=" x: ${event.target.getAttribute(
        "data-x"
      )}" aria-label=".form-control-sm example">
      <input class="form-control form-control-sm  bg-dark text-white
      bg-dark text-white" type="text" disabled value=" y: ${event.target.getAttribute(
        "data-y"
      )}" aria-label=".form-control-sm example">
      <input class="form-control form-control-sm  bg-dark text-white
      bg-dark text-white" type="text" disabled value=" Ancho: ${
        event.target.style.width
      }" aria-label=".form-control-sm example">
      <input class="form-control form-control-sm  bg-dark text-white
      bg-dark text-white" type="text" disabled value=" Alto: ${
        event.target.style.height
      }" aria-label=".form-control-sm example">
      <input class="form-control form-control-sm  bg-dark text-white
      bg-dark text-white" type="text" disabled value=" zindex: ${
        event.target.style.zIndex
      }" aria-label=".form-control-sm example">
      `;

    event.target.style.backgroundColor = "rgba(70, 157, 186, 0.4)";
    event.target.style.borderRadius = "4px";

    event.preventDefault();
  })
  .on("doubletap", function (event) {
    // event.currentTarget.classList.toggle("large");
    // event.currentTarget.classList.remove("rotate");

    // event.target.remove();

    event.preventDefault();
  })
  .on("hold", function (event) {
    // event.currentTarget.classList.toggle("rotate");
    // event.currentTarget.classList.remove("large");
  });
//*************************************************** */

//*************************************************** */
// AGREGA INTERACION A LA ZONA Y A REACCION A LOS EVENTOS QUE GENERA CADA ITEM

interact(".dropzone").dropzone({
  // only accept elements matching this CSS selector
  // Require a 75% element overlap for a drop to be possible
  overlap: 0.75,

  // listen for drop related events:

  ondropactivate: function (event) {
    // cuando se activa el evento o mientras se mueve el objeto
  },
  ondragenter: function (event) {
    // cuando el evento esta dentro de la zona o el obejeto esta dentro de la zona sin soltar
    var draggableElement = event.relatedTarget; // este se le aplica al objeto
    var dropzoneElement = event.target; // este le aplica a la zona

    // console.log("dentro de zona");
  },
  ondropdeactivate: function (event) {
    var draggableElement = event.relatedTarget; // este se le aplica al objeto
    var dropzoneElement = event.target; // este le aplica a la zona
    alertdiv.hidden = false;
    btnsave.disabled = false;
    console.log("dejo de moverse");
    // const itemId = event.target;
    // console.log(itemId)
    // const x = event.clientX; // Obtén la nueva posición X
    // const y = event.clientY; // Obtén la nueva posición Y
    // savePosition(elementId, x, y);
  },
  ondrop: function (event) {
    // cuando el objeto es soltado dentro de la zona
    //       event.relatedTarget.textContent = 'Dropped'
  },
});
//*************************************************** */

//*************************************************** */
// AGREGA INTERACCION DE ARRASTRE PARA TODOS LOS ITEM DENTRO DE LA ZONA
// TAMBIEM DE REDIMENSIONAMIENDO PERO ESTAN DESACTIVADO
interact(".drag-drop")
  .resizable({
    // resize from all edges and corners
    edges: { left: false, right: false, bottom: false, top: false },

    listeners: {
      move(event) {
        var target = event.target;
        var x = parseFloat(target.getAttribute("data-x")) || 0;
        var y = parseFloat(target.getAttribute("data-y")) || 0;

        // update the element's style
        target.style.width = event.rect.width + "px";
        target.style.height = event.rect.height + "px";

        // translate when resizing from top or left edges
        x += event.deltaRect.left;
        y += event.deltaRect.top;

        target.style.transform = "translate(" + x + "px," + y + "px)";

        target.setAttribute("data-x", x);
        target.setAttribute("data-y", y);
        target.textContent =
          Math.round(event.rect.width) +
          "\u00D7" +
          Math.round(event.rect.height);
      },
    },
    modifiers: [
      // keep the edges inside the parent
      interact.modifiers.restrictEdges({
        outer: "parent",
      }),

      // minimum size
      interact.modifiers.restrictSize({
        min: { width: 50, height: 20 },
      }),
    ],

    inertia: true,
  })
  .draggable({
    listeners: {
      move: window.dragMoveListener,
      end(event) {
        const itemId = event.target.getAttribute('id_code');
        const x = event.target.getAttribute('data-x'); // Obtén la nueva posición X
        const y = event.target.getAttribute('data-y'); // Obtén la nueva posición Y
        savePosition(itemId, x, y);
      },
    },
    inertia: false,
    modifiers: [
      interact.modifiers.restrictRect({
        restriction: "parent",
        endOnly: false,
      }),
      interact.modifiers.snap({
        targets: [interact.snappers.grid({ x: 2.5, y: 2.5 })],
        range: Infinity,
        relativePoints: [{ x: 1, y: 1 }],
      }),
    ],
  });

window.dragMoveListener = dragMoveListener;
//*************************************************** */

function loadPositions(){
    const positions = JSON.parse(localStorage.getItem('itemPositions')) || {};

    for (const itemId in positions) {
        const item = document.querySelector(`[id_code="${itemId}"]`);
           
        if (item) {
            const pos = positions[itemId];
            item.style.transform = `translate(${pos.x}px,${pos.y}px)`
            item.setAttribute('data-x',pos.x)
            item.setAttribute('data-y',pos.y)
            // item.style.left = pos.x + 'px';
            // item.style.top = pos.y + 'px';
        }
    }
}

window.onload = loadPositions;
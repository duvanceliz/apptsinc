const eventState = {
  target: null,
};

const eventState2 = {
  target: null,
};
const btndelete = document.getElementById("delete");
const form2 = document.getElementById("form2");
const btnon = document.getElementById("on");
const btnunder = document.getElementById("under");
const btnclone = document.getElementById("clone");



btnon.addEventListener("click", (e) => {
  changeZindex(btnon);
});

btnunder.addEventListener("click", (e) => {
  changeZindex(btnunder);
});

btnclone.addEventListener('click',e=>{

  // console.log(eventState2.target)
  const clone = eventState2.target.cloneNode(true);

  
  clone.setAttribute("id_code", generateCode(4));
  clone.style.transform = 'translate(-16.3754px, -19.729px)'
  clone.setAttribute('data-x',"-16.3754")
  clone.setAttribute('data-y',"-19.729")
  dropzone.appendChild(clone);
  //   // clone.style.width = "auto";
  //   clone.style.zIndex = "0";
  //   
  //   
})


function changeZindex(btn) {
  if (btn.id == "on") {
    eventState2.target.style.zIndex = "10";
  }
  if (btn.id == "under") {
    eventState2.target.style.zIndex = "0";
  }
}

function deleteItem(id_code) {
  const csrfToken = document.querySelector("#form2 > input").value;
  axios
    .post(
      "/deleteitem/",
      {
        id_code: id_code,
      },
      {
        headers: {
          "X-CSRFToken": csrfToken,
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
}

//********************************************************* */

form2.addEventListener("submit", (e) => {
  e.preventDefault();

  const item = eventState2.target;
  item.remove();
  deleteItem(eventState2.target.getAttribute("id_code"));
});

//******************************************************************** */

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

//************************************************************************* */

const dropzone = document.getElementById("outer-dropzone");
const items = document.querySelectorAll("#item").forEach((item) => {
  item.addEventListener("dragstart", (e) => {
    eventState.target = e.target;
  });
});

//********************************************************************** */
dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
});
dropzone.addEventListener("drop", (e) => {
  if (eventState.target.id == "item") {
    const clone = eventState.target.cloneNode(true);
    clone.classList.add("drag-drop");
    clone.removeAttribute("id");
    clone.removeAttribute("id");
    // clone.style.width = "auto";
    clone.style.zIndex = "0";
    clone.setAttribute("id_code", generateCode(4));
    dropzone.appendChild(clone);
  }
});

//***************************************************************************** */

// interact(".drag-drop").draggable({
//   inertia: false,
//   modifiers: [
//     interact.modifiers.restrictRect({
//       restriction: "parent",
//       endOnly: false,
//     }),
//     interact.modifiers.snap({
//       targets: [interact.snappers.grid({ x: 10, y: 10 })],
//       range: Infinity,
//       relativePoints: [{ x: 10, y: 10 }],
//     }),
//   ],
//   autoScroll: true,
//   // dragMoveListener from the dragging demo above
//   listeners: { move: dragMoveListener },
// });

//****************************************************************************************A */

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

interact(".drag-drop")
  .on("tap", function (event) {
    // event.currentTarget.classList.toggle("switch-bg");
    console.log("click al objeto");
    const btndelete = document.getElementById("delete");

    btnon.disabled = false;
    btnunder.disabled = false;
    btndelete.disabled = false;
    btnclone.disabled = false;
    eventState2.target = event.target;

    panel.innerHTML = `
    
    <input class="form-control form-control-sm" type="text" disabled value=" Item: ${event.target.getAttribute(
      "id_code"
    )}" aria-label=".form-control-sm example">
    <input class="form-control form-control-sm" type="text" disabled value=" x: ${event.target.getAttribute(
      "data-x"
    )}" aria-label=".form-control-sm example">
    <input class="form-control form-control-sm" type="text" disabled value=" y: ${event.target.getAttribute(
      "data-y"
    )}" aria-label=".form-control-sm example">
    <input class="form-control form-control-sm" type="text" disabled value=" Ancho: ${
      event.target.style.width
    }" aria-label=".form-control-sm example">
    <input class="form-control form-control-sm" type="text" disabled value=" Alto: ${
      event.target.style.height
    }" aria-label=".form-control-sm example">
    <input class="form-control form-control-sm" type="text" disabled value=" zindex: ${
      event.target.style.zIndex
    }" aria-label=".form-control-sm example">
    `;

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

// this function is used later in the resizing and gesture demos

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
    // console.log("dejo de moverse");
  },
  ondrop: function (event) {
    // cuando el objeto es soltado dentro de la zona
    //       event.relatedTarget.textContent = 'Dropped'
  },
});

interact(".drag-drop")
  .resizable({
    // resize from all edges and corners
    edges: { left: true, right: true, bottom: true, top: true },

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
        min: { width: 50, height: 50 },
      }),
    ],

    inertia: true,
  })
  .draggable({
    listeners: { move: window.dragMoveListener },
    inertia: false,
    modifiers: [
      interact.modifiers.restrictRect({
        restriction: "parent",
        endOnly: false,
      }),
      interact.modifiers.snap({
        targets: [interact.snappers.grid({ x: 10, y: 10 })],
        range: Infinity,
        relativePoints: [{ x: 5, y: 5 }],
      }),
    ],
  });

window.dragMoveListener = dragMoveListener;

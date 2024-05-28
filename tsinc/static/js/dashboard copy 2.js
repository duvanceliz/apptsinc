const dropzone = document.getElementById("outer-dropzone");
// Crear el nuevo div
// let x = 163
// let y = 157
// let nuevoDiv = document.createElement('div');
// // nuevoDiv.innerHTML = 'Este es el nuevo div';
// nuevoDiv.className ='drag drag-drop'
// nuevoDiv.id = 'item'
// nuevoDiv.style.transform = "translate(" + x + "px, " + y + "px)";
// // nuevoDiv.style.border = '1px solid red'; // Agregar estilo para visualizarlo mejor
// nuevoDiv.setAttribute("data-x", x);
// nuevoDiv.setAttribute("data-y", y);
// // Seleccionar el div contenedor
// // Insertar el nuevo div dentro del contenedor
// dropzone.appendChild(nuevoDiv);

var elementSelected = null;
//***************************************************************** */
function addobj() {
  moveItem(elementSelected, dropzone);
}

function moveItem(elementSelected, destination) {
  elementSelected.classList.remove("selected");
  const clone = elementSelected.cloneNode(true);
  clone.classList.add("drag-drop");
  destination.appendChild(clone);
}

interact("#item").draggable({
  listeners: {
    start(event) {
      //Crear un clon del elemento arrastrable
      const clone = event.target.cloneNode(true);
      clone.style.position = "absolute";
      // clone.style.pointerEvents = 'none';
      document.body.appendChild(clone);
      event.interactable.clonedElement = clone;
      //  moveItem(clone,dropzone)
    },
    move(event) {
      // Mover el clon con el cursor
      const clone = event.interactable.clonedElement;
      const target = event.target
      // console.log(event.target)
      // console.log(clone)
      // keep the dragged position in the data-x/data-y attributes
      var x = (parseFloat(target.getAttribute("data-x")) || 0) + event.dx;
      var y = (parseFloat(target.getAttribute("data-y")) || 0) + event.dy;

      // translate the element
      target.style.transform = "translate(" + x + "px, " + y + "px)";

      // update the posiion attributes
      target.setAttribute("data-x", x);
      target.setAttribute("data-y", y);
    },
    end(event) {
      // Eliminar el clon al soltar

      const clone = event.interactable.clonedElement;

      if (clone) {
        clone.remove();
        event.interactable.clonedElement = null;
      }
    },
  },
});

//******************************************************************* */
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
    console.log("dentro de zona");
  },
  ondropdeactivate: function (event) {
    var draggableElement = event.relatedTarget; // este se le aplica al objeto
    var dropzoneElement = event.target; // este le aplica a la zona
  },
  ondrop: function (event) {
    // cuando el objeto es soltado dentro de la zona
    //       event.relatedTarget.textContent = 'Dropped'

    console.log("soltado");
  },
});

//********************************************************************************** */

// interact(".drag-drop")
//   .on("tap", function (event) {
//     // event.currentTarget.classList.toggle("switch-bg");
//     console.log("click al objeto");
//     var panel = document.getElementById("panel");

//     panel.innerHTML = `<input class="form-control form-control-sm" type="text" value=" Item ${event.target.innerText}" aria-label=".form-control-sm example">`;

//     event.preventDefault();
//   })
//   .on("doubletap", function (event) {
//     // event.currentTarget.classList.toggle("large");
//     // event.currentTarget.classList.remove("rotate");

//     event.target.remove();

//     event.preventDefault();
//   })
//   .on("hold", function (event) {
//     // event.currentTarget.classList.toggle("rotate");
//     // event.currentTarget.classList.remove("large");
//   });

//********************************************************************* */

// interact("#item")
//   .on("tap", function (event) {
//     // event.currentTarget.classList.toggle("switch-bg");
//     items = document.querySelectorAll("#availableItems div");

//     items.forEach((item) => {
//       item.classList.remove("selected");
//     });

//     elementSelected = event.target;
//     elementSelected.classList.add("selected");

//     event.preventDefault();
//   })
//   .on("doubletap", function (event) {
//     // event.currentTarget.classList.toggle("large");
//     // event.currentTarget.classList.remove("rotate");
//     console.log("doble click al obj");
//     event.preventDefault();
//   })
//   .on("hold", function (event) {
//     // event.currentTarget.classList.toggle("rotate");
//     // event.currentTarget.classList.remove("large");
//   });

//************************************************************************************ */

interact(".drag-drop").draggable({
  inertia: false,
  modifiers: [
    interact.modifiers.restrictRect({
      restriction: "parent",
      endOnly: false,
    }),
    interact.modifiers.snap({
      targets: [interact.snappers.grid({ x: 10, y: 10 })],
      range: Infinity,
      relativePoints: [{ x: 0, y: 0 }],
    }),
  ],
  autoScroll: true,
  // dragMoveListener from the dragging demo above
  listeners: { move: dragMoveListener },
});

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

// this function is used later in the resizing and gesture demos
window.dragMoveListener = dragMoveListener;

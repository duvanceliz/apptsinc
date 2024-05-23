var count = 0;
const drag = document.getElementById("drag");
const drag2 = document.getElementById("drag2");
const dropzone = document.getElementById("outer-dropzone");

function addobj() {
  const clone = drag.cloneNode(true);
  clone.classList.add("drag-drop");
  dropzone.appendChild(clone);
}

function addobj2() {

  
  const clone = drag2.cloneNode(true);
  clone.classList.add("drag-drop");
  dropzone.appendChild(clone);

}


interact(".dropzone").dropzone({
  // only accept elements matching this CSS selector
  // accept: '#drag',
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

    // function areDivsAdjacent(div1, div2) {
    //   const rect1 = div1.getBoundingClientRect();
    //   const rect2 = div2.getBoundingClientRect();
    
    //   const horizontalAdjacent = rect1.right === rect2.left || rect1.left === rect2.right;
    
    //   const verticalAdjacent = rect1.bottom === rect2.top || rect1.top === rect2.bottom;
    
    //   return horizontalAdjacent || verticalAdjacent;
    // }
  
    // if (areDivsAdjacent(drag,drag2)) {
    //   console.log("Los div están pegados.");
    // } else {
    //   console.log("Los div no están pegados.");
    // }
    

  },
  ondropdeactivate: function (event) {
    var draggableElement = event.relatedTarget; // este se le aplica al objeto
    var dropzoneElement = event.target; // este le aplica a la zona
      
    //cuando se desactiva el evento o no se mueve el objeto dentro de la zona
    // remove active dropzone feedback
    // event.target.classList.remove('drop-active')
    // event.target.classList.remove('drop-target')
    // console.log("objeto dejo de moverse");

    
    



    //  console.log(draggableElement.getBoundingClientRect())
  
    // function areDivsAdjacent(div1, div2) {
    //   const rect1 = div1.getBoundingClientRect();
    //   const rect2 = div2.getBoundingClientRect();
    
    //   const horizontalAdjacent = rect1.right === rect2.left || rect1.left === rect2.right;
    
    //   const verticalAdjacent = rect1.bottom === rect2.top || rect1.top === rect2.bottom;
    
    //   return horizontalAdjacent || verticalAdjacent;
    // }
  
    // if (areDivsAdjacent(drag,drag2)) {
    //   console.log("Los div están pegados.");
    // } else {
    //   console.log("Los div no están pegados.");
    // }

    
  },
});

interact(".drag-drop")
  .on("tap", function (event) {
    // event.currentTarget.classList.toggle("switch-bg");
    console.log("click al objeto");
    event.preventDefault();
  })
  .on("doubletap", function (event) {
    // event.currentTarget.classList.toggle("large");
    // event.currentTarget.classList.remove("rotate");
    console.log("doble click al obj");
    event.preventDefault();
  })
  .on("hold", function (event) {
    // event.currentTarget.classList.toggle("rotate");
    // event.currentTarget.classList.remove("large");
  });

  interact(".drag")
  .on("tap", function (event) {
    // event.currentTarget.classList.toggle("switch-bg");
    event.target.classList.add('select')
    console.log(event.target);
   
    event.preventDefault();
  })
  .on("doubletap", function (event) {
    // event.currentTarget.classList.toggle("large");
    // event.currentTarget.classList.remove("rotate");
    console.log("doble click al obj");
    event.preventDefault();
  })
  .on("hold", function (event) {
    // event.currentTarget.classList.toggle("rotate");
    // event.currentTarget.classList.remove("large");
  });


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

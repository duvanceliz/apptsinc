
const eventState = {
  target: null
};


function generateCode(length) {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
      result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}


//************************************************************************* */

const dropzone = document.getElementById("outer-dropzone");
const items = document.querySelectorAll('#item').forEach(item =>{
  item.addEventListener('dragstart', e =>{
    eventState.target = e.target

  })
})


//********************************************************************** */
dropzone.addEventListener('dragover', e=>{
 
  e.preventDefault()
})
dropzone.addEventListener('drop', e =>{    
  if(eventState.target.id == 'item'){
    const clone = eventState.target.cloneNode(true)
    clone.classList.add('drag-drop')
    clone.removeAttribute('id')
    clone.setAttribute('id_code',generateCode(4))
    dropzone.appendChild(clone)
  }
    
})

//***************************************************************************** */

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



interact(".drag-drop")
  .on("tap", function (event) {
    // event.currentTarget.classList.toggle("switch-bg");
    console.log("click al objeto");
    var panel = document.getElementById("panel");

    // panel.innerHTML = `<input class="form-control form-control-sm" type="text" value=" Item ${event.target.innerText}" aria-label=".form-control-sm example">`;

    event.preventDefault();
  })
  .on("doubletap", function (event) {
    // event.currentTarget.classList.toggle("large");
    // event.currentTarget.classList.remove("rotate");

    event.target.remove();

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
window.dragMoveListener = dragMoveListener;



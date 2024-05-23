// interact('.dropzone').dropzone({
//     // only accept elements matching this CSS selector
//     accept: '#drag',
//     // Require a 75% element overlap for a drop to be possible
//     overlap: 0.75,
  
//     // listen for drop related events:
  
//     ondropactivate: function (event) { // cuando se activa el evento o mientras se mueve el objeto
//       // add active dropzone feedback
//       event.target.classList.add('drop-active')
//     },
//     ondragenter: function (event) { // cuando el evento esta dentro de la zona o el obejeto esta dentro de la zona sin soltar
//       var draggableElement = event.relatedTarget // este se le aplica al objeto
//       var dropzoneElement = event.target // este le aplica a la zona
  
//       // feedback the possibility of a drop
//       dropzoneElement.classList.add('drop-target') // zona cambia a azul
//       draggableElement.classList.add('can-drop') // objeto cambia a verde
//       draggableElement.textContent = 'Dragged in' //
//     },
//     ondragleave: function (event) { // cuando cuando el objeto esta fuera de la zona
//       // remove the drop feedback style
//       event.target.classList.remove('drop-target')
//       event.relatedTarget.classList.remove('can-drop')
//       event.relatedTarget.textContent = 'Dragged out'
//     },
//     ondrop: function (event) { // cuando el objeto es soltado dentro de la zona
//       event.relatedTarget.textContent = 'Dropped'
//     },
//     ondropdeactivate: function (event) {//cuando se desactiva el evento o no se mueve el objeto dentro de la zona
//       // remove active dropzone feedback
//     event.target.classList.remove('drop-active')
//     event.target.classList.remove('drop-target')
//     }
//   })

// *************************************************************************

  
  interact('.drag')
    .draggable({
      inertia: false,
      modifiers: [
        interact.modifiers.restrictRect({
          restriction: 'parent',
          endOnly: false
        })
      ],
      autoScroll: false,
      // dragMoveListener from the dragging demo above
      listeners: { move: dragMoveListener }
    })


function dragMoveListener (event) {
  var target = event.target

  // keep the dragged position in the data-x/data-y attributes
  var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
  var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy

  // translate the element
  target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'

  // update the posiion attributes
  target.setAttribute('data-x', x)
  target.setAttribute('data-y', y)
}

// this function is used later in the resizing and gesture demos
window.dragMoveListener = dragMoveListener
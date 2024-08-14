const btnrm = document.getElementById("btnrm")
const btnor = document.getElementById("btnor")
const re_form = document.getElementById("remission-form")
const or_form = document.getElementById("order-form")


btnrm.addEventListener('click',e=>{
    re_form.hidden = false
    or_form.hidden = true
})

btnor.addEventListener('click',e=>{
    re_form.hidden = true
    or_form.hidden = false
})
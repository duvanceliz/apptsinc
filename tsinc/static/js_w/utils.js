const btnHiddenFolder = document.getElementById("btn-hidden-folder")
const formSaveFolder = document.getElementById("form-save-folder")
const btnHiddenDeleteFolder = document.getElementById("btn-hidden-delete-folder")
const tree = document.getElementById("tree")
const btnOpenCloseNav = document.getElementById("btn-open-close-nav")
const  navTree = document.getElementById("nav-tree")


btnOpenCloseNav.addEventListener('click',(e)=>{
    

    if ( navTree.style.display == "none"){
        navTree.style.display = "block"
        localStorage.setItem("navtree","block")
    }else{
        navTree.style.display = "none"
        localStorage.setItem("navtree","none")
    }
})

btnHiddenFolder.addEventListener('click',(e)=>{
    

    if ( formSaveFolder.style.display == "none"){
        formSaveFolder.style.display = "block"
    }else{
        formSaveFolder.style.display = "none"
    }
})

btnHiddenDeleteFolder.addEventListener('click',(e)=>{

    const links = tree.querySelectorAll("a")

    links.forEach((link)=>{
        if(link.id){
           
           if(link.style.display === "none"){
            link.style.display = "inline-block"
           }else{
            link.style.display = "none"
           }
        }
    })


   
})
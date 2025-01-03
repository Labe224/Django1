let menu=document.getElementById("sub_menu")
let menu_btn=document.getElementById("menu_btn")
menu_btn.onclick=affiche
function affiche(){
    menu.classList.toggle('affiche')
    let classes =menu.className
    i=classes.indexOf('affiche')
    if (i!=-1){
       document.body.style.overflow='hidden'
    } else{
        document.body.style.overflow=''
    }
    
}

function clique(params) {
    params.style.color='red'
}
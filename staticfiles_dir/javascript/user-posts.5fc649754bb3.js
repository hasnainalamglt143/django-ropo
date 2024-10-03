
document.addEventListener("DOMContentLoaded",()=>{


let updateBtns=document.querySelectorAll(".update_post");
let deleteBtns=document.querySelectorAll(".delete_post");

function deletePost(id) {
    let allowed = confirm("Are you sure you want to delete this post?");
    if (allowed) {
        window.location.href = `/delete-post/${id}/`;
    }
  
}

function update_Post(id) {
    
        window.location.href = `/update-post/${id}/`;
    
}
updateBtns.forEach((updateBtn,i)=>{
    updateBtn.addEventListener("click",(e)=>{
        update_Post(e.target.dataset.id)
    
    })
})

deleteBtns.forEach((deleteBtn,i)=>{
    deleteBtn.addEventListener("click",(e)=>{
        deletePost(e.target.dataset.id)
    
    })
})
//respnsiveness

const menue_icon=document.getElementById("menu-bar")
const menue=document.getElementById("menu")
console.log(menue,menue_icon)
menue_icon.addEventListener("click",()=>{
    menue.classList.toggle("hidden")

})



},false);
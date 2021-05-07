
function () {
   var addCart = document.getElementById("add-cart");
   addCart.addEventListener("click",display);
}

function display(){
  console.log("quantity");
  document.getElementById("counter").textContent=document.getElementById("quantity").textContent;
}

  
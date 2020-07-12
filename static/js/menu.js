function closeNav(){
  document.getElementById("sidenav").style.width = "0";
};

function openNav(){
  document.getElementById("sidenav").style.width = "250px";
};

document.addEventListener('mousedown', function(e){
  var sidebar = document.getElementById("sidenav");
  if (sidebar.style.width == "250px"){
    if (!sidebar.contains(e.target)){
      closeNav();
    }
  }
});

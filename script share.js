// script.js


function addShakeAnimation(button) {
  button.style.animation = "shake 0.5s";
  setTimeout(() => {
    button.style.animation = "";
  }, 500);
}


function changeTextColor(button) {
  button.style.color = "blue"; 
}


document.querySelectorAll('.btn').forEach(item => {
  item.addEventListener('click', event => {
    
    item.classList.toggle('active');

    
    if (item.classList.contains('active')) {
      item.style.transition = "transform 0.5s ease, background-color 0.5s ease";
      item.style.transform = "scale(1.2)";
      item.style.backgroundColor = "#ff7f50"; 
      addShakeAnimation(item); 
      changeTextColor(item); 
    } else {
      item.style.transition = "transform 0.5s ease, background-color 0.5s ease";
      item.style.transform = "scale(1)";
      item.style.backgroundColor = "initial";     }
  });
});

document.addEventListener("DOMContentLoaded", function() {
  var buttons = document.querySelectorAll('.pBtn');
  var userPoint = parseInt(document.getElementById("userPoints").value);
  buttons.forEach(function(button) {
      button.addEventListener('click', function() {

          var buttonId = this.getAttribute('id');
          var pInput = "p_" + buttonId;
          var pInputElement = document.getElementById(pInput);
          var pInt = parseInt(pInputElement.value);
          var intID = parseInt(buttonId);
          if (pInt > userPoint) {
            alert("אין לך מספיק נקודות");
          } else {
            alert("הרכישה בוצעה בהתחלה");
            window.location.href = "http://127.0.0.1:8000/website/updatepoints/" + intID;
          }



      });
  });
});
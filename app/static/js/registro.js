function validateForm() {
    var name = document.forms["form-signin"]["txtFullname"].value;
    var email = document.forms["form-signin"]["txtEmail"].value;
    var password = document.forms["form-signin"]["txtPassword"].value;
  
    if (name == "") {
      alert("Nombre y Apellido debe ser completado");
      return false;
    }
    if (email == "") {
      alert("Correo Electrónico debe ser completado");
      return false;
    }
    if (password == "") {
      alert("Contraseña debe ser completada");
      return false;
    }
  }
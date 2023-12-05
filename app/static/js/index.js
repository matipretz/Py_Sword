document.querySelector('.form-control').addEventListener('submit', function (e) {
    e.preventDefault();
    // Evitar que el formulario se envíe automáticamente

    // Obtener los valores de los campos de entrada
    let email = document.getElementById('exampleInputEmail1').value;
    let password = document.getElementById('exampleInputPassword1').value;

    // Validar si los campos están completos  

    if (email.trim() === '' || password.trim() === '') {
        alert('Por favor complete todos los campos');
        return;
    }
    // Validar el formato del correo electrónico  
    let emailFormat = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailFormat.test(email)) {
        alert('Por favor ingrese un correo electrónico válido');
        return;
    }
    // Si todas las validaciones pasan, puedes enviar el formulario  

    this.submit();
});

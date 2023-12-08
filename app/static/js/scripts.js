function switchPassword() {
    const contrasenaInput = document.getElementById('contrasena');
    const tipoInput = contrasenaInput.type === 'password' ? 'text' : 'password';
    contrasenaInput.type = tipoInput;
    const toggleBtn = document.getElementById('toggleBtn');
    toggleBtn.textContent = tipoInput === 'password' ? 'Mostrar' : 'Ocultar';
}

function generarContrasena() {
    const longitud = document.getElementById('longitud').value;
    const contrasenaInput = document.getElementById('contrasena');
    const contrasenaGenerada = generarContrasenaAleatoria(longitud);
    contrasenaInput.value = contrasenaGenerada;
}

function generarContrasenaAleatoria(longitud) {
    const caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_=+";
    let contrasena = '';
    for (let i = 0; i < longitud; i++) {
        const caracter = caracteres[Math.floor(Math.random() * caracteres.length)];
        contrasena += caracter;
    }
    return contrasena;
}

document.getElementById('longitud').addEventListener('input', function () {
    document.getElementById('valorLongitud').innerText = this.value;
});

function togglePassword(button) {
    const contrasenaInput = button.parentNode.previousElementSibling.querySelector('.contrasena-fila');
    const tipoInput = contrasenaInput.type === 'password' ? 'text' : 'password';
    contrasenaInput.type = tipoInput;

    // Habilita o deshabilita el botón de copiar según el estado del campo de contraseña
    const copyButton = button.parentNode.querySelector('.copy-btn');
    copyButton.disabled = tipoInput === 'password';
}

function copyToClipboard(button) {
    const contrasenaInput = button.parentNode.previousElementSibling.querySelector('.contrasena-fila');

    // Selecciona el texto en el campo de contraseña
    contrasenaInput.select();
    contrasenaInput.setSelectionRange(0, 99999); // Para dispositivos móviles

    // Copia el texto al portapapeles
    document.execCommand('copy');

    // Deselecciona el texto para evitar confusiones visuales
    window.getSelection().removeAllRanges();
}
function deleteRow(button) {
    var id = button.getAttribute("data-id");

    // Mostrar un mensaje de confirmación
    var confirmacion = confirm("¿Estás seguro de que quieres borrar esta contraseña?");

    if (confirmacion) {
        fetch(`/borrar/${id}`, {
            method: 'DELETE',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('No se pudo borrar la fila');
                }
                return response.json();
            })
            .then(data => {
                alert(data.mensaje);
                location.reload();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    } else {
        // El usuario ha cancelado, no hacemos nada
    }
}
function habilitarEdicion(id) {
    // Redirigir a la página de edición con el ID de la contraseña
    window.location.href = `/editar/${id}`;
}

function abrirModal(id) {
    var modal = document.getElementById('editarModal');
    var iframe = document.getElementById('editarFrame');
    iframe.src = `/editar/${id}`;
    modal.style.display = 'block';
}

function cerrarModal() {
    var modal = document.getElementById('editarModal');
    modal.style.display = 'none';
}

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
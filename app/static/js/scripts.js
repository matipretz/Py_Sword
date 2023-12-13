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

function cerrarModal() {
    history.back();
}

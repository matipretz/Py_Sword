function togglePassword() {
    const contrasenaInput = document.getElementById('contrasena');
    const tipoInput = contrasenaInput.type === 'password' ? 'text' : 'password';
    contrasenaInput.type = tipoInput;
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

function guardarCambios(id) {
    var nuevo_servicio = document.getElementById("nuevo_servicio").value;
    var nuevo_usuario = document.getElementById("nuevo_usuario").value;
    var nueva_contrasena = document.getElementById("nueva_contrasena").value;

    fetch(`/editar/${id}`, {
        method: 'PUT',  
        headers: {
            'Content-Type': 'text/html; charset=utf-8',  
        },
        body: JSON.stringify({
            nuevo_servicio: nuevo_servicio,
            nuevo_usuario: nuevo_usuario,
            nueva_contrasena: nueva_contrasena,
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`No se pudieron guardar los cambios. ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        alert(data.mensaje);
        location.reload();
        cerrarModal();  
    })
    .catch(error => {
        console.error('Error al guardar los cambios:', error.message);
    });
}



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
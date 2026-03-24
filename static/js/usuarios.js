function abrirModal() {
    document.getElementById('user-nombre').value   = '';
    document.getElementById('user-password').value = '';
    document.getElementById('user-rol').value      = 'cajero';
    document.getElementById('modal').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal').classList.add('hidden');
}

async function guardar() {
    const nombre   = document.getElementById('user-nombre').value.trim();
    const password = document.getElementById('user-password').value.trim();
    const rol      = document.getElementById('user-rol').value;

    if (!nombre || !password) {
        Swal.fire({ icon: 'warning', title: 'Campos incompletos', text: 'Completá nombre y contraseña.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
        return;
    }

    try {
        const res  = await fetch('/usuarios/crear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre, password, rol })
        });
        const data = await res.json();
        if (data.ok) { cerrarModal(); location.reload(); }
        else Swal.fire({ icon: 'error', title: 'Error', text: data.msg || 'No se pudo crear el usuario.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo conectar con el servidor.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

async function eliminar(id, nombre) {
    const result = await Swal.fire({
        title: '¿Eliminar usuario?',
        text: `"${nombre}" será eliminado permanentemente.`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#ef4444',
        cancelButtonColor: '#475569',
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        background: '#1e293b',
        color: '#f1f5f9'
    });

    if (!result.isConfirmed) return;

    try {
        const res  = await fetch(`/usuarios/eliminar/${id}`, { method: 'POST' });
        const data = await res.json();
        if (data.ok) location.reload();
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo eliminar el usuario.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('modal').addEventListener('click', e => {
        if (e.target === document.getElementById('modal')) cerrarModal();
    });
});
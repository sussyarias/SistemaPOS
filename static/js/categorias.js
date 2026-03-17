async function guardar() {
    const nombre = document.getElementById('cat-nombre').value.trim();

    if (!nombre) {
        Swal.fire({ icon: 'warning', title: 'Campo vacío', text: 'Escribí el nombre de la categoría.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
        return;
    }

    try {
        const res  = await fetch('/categorias/crear', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre })
        });
        const data = await res.json();
        if (data.ok) location.reload();
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo guardar la categoría.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

async function eliminar(id, nombre) {
    const result = await Swal.fire({
        title: '¿Eliminar categoría?',
        text: `"${nombre}" será eliminada. Los productos asociados quedarán sin categoría.`,
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
        const res  = await fetch(`/categorias/eliminar/${id}`, { method: 'POST' });
        const data = await res.json();
        if (data.ok) location.reload();
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo eliminar la categoría.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('modal').addEventListener('click', e => {
        if (e.target === document.getElementById('modal'))
            document.getElementById('modal').classList.add('hidden');
    });

    document.getElementById('cat-nombre').addEventListener('keydown', e => {
        if (e.key === 'Enter') guardar();
    });
});
function abrirModal() {
    document.getElementById('modal-titulo').textContent = 'Nuevo producto';
    document.getElementById('prod-id').value = '';
    document.getElementById('prod-nombre').value = '';
    document.getElementById('prod-precio').value = '';
    document.getElementById('prod-stock').value = '';
    document.getElementById('prod-stock-min').value = '5';
    document.getElementById('prod-cat').value = '';
    document.getElementById('modal').classList.remove('hidden');
}

function abrirEditar(btn) {
    document.getElementById('modal-titulo').textContent = 'Editar producto';
    document.getElementById('prod-id').value = btn.dataset.id;
    document.getElementById('prod-nombre').value = btn.dataset.nombre;
    document.getElementById('prod-precio').value = btn.dataset.precio;
    document.getElementById('prod-stock').value = btn.dataset.stock;
    document.getElementById('prod-stock-min').value = btn.dataset.stockMin;
    document.getElementById('prod-cat').value = btn.dataset.cat || '';
    document.getElementById('modal').classList.remove('hidden');
}

function cerrarModal() {
    document.getElementById('modal').classList.add('hidden');
}

async function guardar() {
    const id = document.getElementById('prod-id').value;
    const nombre = document.getElementById('prod-nombre').value.trim();
    const precio = parseFloat(document.getElementById('prod-precio').value);
    const stock = parseInt(document.getElementById('prod-stock').value);
    const stockMin = parseInt(document.getElementById('prod-stock-min').value);
    const catId = document.getElementById('prod-cat').value || null;

    if (!nombre || isNaN(precio) || isNaN(stock)) {
        Swal.fire({ icon: 'warning', title: 'Campos incompletos', text: 'Completá todos los campos obligatorios.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
        return;
    }

    const url = id ? `/inventario/editar/${id}` : '/inventario/crear';
    const body = { nombre, precio, stock, stock_minimo: stockMin, categoria_id: catId };

    try {
        const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const data = await res.json();
        if (data.ok) {
            cerrarModal();
            location.reload();
        }
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo guardar el producto.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

async function eliminar(id, nombre) {
    const confirm = await Swal.fire({
        title: '¿Eliminar producto?',
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

    if (!confirm.isConfirmed) return;

    try {
        const res  = await fetch(`/inventario/eliminar/${id}`, { method: 'POST' });
        const data = await res.json();
        if (data.ok) location.reload();
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo eliminar el producto.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

function filtrar() {
    const q   = document.getElementById('buscar').value.toLowerCase();
    const cat = document.getElementById('filtro-cat').value;
    document.querySelectorAll('.producto-row').forEach(row => {
        const nombre = row.dataset.nombre;
        const catRow = row.dataset.cat;
        const visible = nombre.includes(q) && (cat === '' || catRow === cat);
        row.style.display = visible ? '' : 'none';
    });
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('buscar').addEventListener('input', filtrar);
    document.getElementById('filtro-cat').addEventListener('change', filtrar);
    document.getElementById('modal').addEventListener('click', e => {
        if (e.target === document.getElementById('modal')) cerrarModal();
    });
});
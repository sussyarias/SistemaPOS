async function verDetalle(facturaId) {
    try {
        const res  = await fetch(`/historial/detalle/${facturaId}`);
        const data = await res.json();

        document.getElementById('modal-titulo').textContent = `Factura #${String(facturaId).padStart(5, '0')}`;
        document.getElementById('modal-contenido').innerHTML = data.items.map(item => `
            <div class="flex justify-between py-1.5 border-b border-slate-800">
                <span>${item.descripcion} x${item.cantidad}</span>
                <span class="text-indigo-400">₡${Number(item.cantidad * item.precio).toLocaleString('es-CR')}</span>
            </div>
        `).join('');

        document.getElementById('modal').classList.remove('hidden');
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo cargar el detalle.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('modal').addEventListener('click', e => {
        if (e.target === document.getElementById('modal'))
            document.getElementById('modal').classList.add('hidden');
    });
});
let carrito = [];

function agregarAlCarrito(el) {
    const id = parseInt(el.dataset.id);
    const nombre = el.dataset.nombre;
    const precio = parseFloat(el.dataset.precio);
    const stock = parseInt(el.dataset.stock);

    const existente = carrito.find(i => i.id === id);
    if (existente) {
        if (existente.cant >= stock) {
            Swal.fire({ icon: 'warning', title: 'Sin stock', text: 'No hay más unidades disponibles.', confirmButtonColor: '#6366f1' });
            return;
        }
        existente.cant++;
    } else {
        if (stock <= 0) {
            Swal.fire({ icon: 'warning', title: 'Sin stock', text: 'Este producto no tiene stock disponible.', confirmButtonColor: '#6366f1' });
            return;
        }
        carrito.push({ id, nombre, precio, cant: 1, stock });
    }
    renderCarrito();
}

function renderCarrito() {
    const cont = document.getElementById('carrito-items');

    if (carrito.length === 0) {
        cont.innerHTML = '<p class="text-slate-500 text-sm text-center mt-8">El carrito está vacío</p>';
        actualizarTotales();
        return;
    }

    cont.innerHTML = carrito.map((item, i) => `
        <div class="bg-slate-800 rounded-xl p-3 flex items-start gap-2">
            <div class="flex-1">
                <p class="text-white text-sm font-medium">${item.nombre}</p>
                <p class="text-indigo-400 text-sm">₡${fmt(item.precio)}</p>
            </div>
            <div class="flex items-center gap-2">
                <button onclick="cambiarCant(${i}, -1)" class="w-6 h-6 bg-slate-700 hover:bg-slate-600 rounded-lg text-white text-xs">−</button>
                <span class="text-white text-sm w-5 text-center">${item.cant}</span>
                <button onclick="cambiarCant(${i}, 1)" class="w-6 h-6 bg-slate-700 hover:bg-slate-600 rounded-lg text-white text-xs">+</button>
                <button onclick="quitarItem(${i})" class="w-6 h-6 bg-red-900/40 hover:bg-red-900 rounded-lg text-red-400 text-xs ml-1">✕</button>
            </div>
        </div>
    `).join('');

    actualizarTotales();
}

function cambiarCant(i, delta) {
    carrito[i].cant += delta;
    if (carrito[i].cant <= 0) carrito.splice(i, 1);
    else if (carrito[i].cant > carrito[i].stock) carrito[i].cant = carrito[i].stock;
    renderCarrito();
}

function quitarItem(i) {
    carrito.splice(i, 1);
    renderCarrito();
}

function limpiarCarrito() {
    if (carrito.length === 0) return;
    Swal.fire({
        title: '¿Limpiar carrito?',
        text: 'Se eliminarán todos los productos.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#6366f1',
        cancelButtonColor: '#475569',
        confirmButtonText: 'Sí, limpiar',
        cancelButtonText: 'Cancelar',
        background: '#1e293b',
        color: '#f1f5f9'
    }).then(result => {
        if (result.isConfirmed) {
            carrito = [];
            renderCarrito();
        }
    });
}

function actualizarTotales() {
    const subtotal = carrito.reduce((s, i) => s + i.cant * i.precio, 0);
    const descuento = parseFloat(document.getElementById('descuento').value) || 0;
    const base = Math.max(subtotal - descuento, 0);
    const iva = Math.round(base * 0.13);
    const total = base + iva;

    document.getElementById('lbl-subtotal').textContent = '₡' + fmt(subtotal);
    document.getElementById('lbl-descuento').textContent = '-₡' + fmt(descuento);
    document.getElementById('lbl-iva').textContent = '₡' + fmt(iva);
    document.getElementById('lbl-total').textContent = '₡' + fmt(total);

    const rowDesc = document.getElementById('row-descuento');
    rowDesc.style.display = descuento > 0 ? 'flex' : 'none';
}

async function cobrar() {
    if (carrito.length === 0) {
        Swal.fire({ icon: 'warning', title: 'Carrito vacío', text: 'Agregá productos antes de cobrar.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
        return;
    }

    const subtotal = carrito.reduce((s, i) => s + i.cant * i.precio, 0);
    const descuento = parseFloat(document.getElementById('descuento').value) || 0;
    const base = Math.max(subtotal - descuento, 0);
    const iva = Math.round(base * 0.13);
    const total = base + iva;

    const confirm = await Swal.fire({
        title: '¿Confirmar factura?',
        html: `
            <div style="text-align:left; color:#94a3b8; font-size:14px; line-height:2">
                <div style="display:flex; justify-content:space-between"><span>Subtotal</span><span>₡${fmt(subtotal)}</span></div>
                ${descuento > 0 ? `<div style="display:flex; justify-content:space-between; color:#f87171"><span>Descuento</span><span>-₡${fmt(descuento)}</span></div>` : ''}
                <div style="display:flex; justify-content:space-between"><span>IVA 13%</span><span>₡${fmt(iva)}</span></div>
                <div style="display:flex; justify-content:space-between; color:#fff; font-weight:bold; font-size:16px; border-top:1px solid #334155; margin-top:6px; padding-top:6px">
                    <span>Total</span><span style="color:#818cf8">₡${fmt(total)}</span>
                </div>
            </div>`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#6366f1',
        cancelButtonColor: '#475569',
        confirmButtonText: 'Cobrar e imprimir',
        cancelButtonText: 'Cancelar',
        background: '#1e293b',
        color: '#f1f5f9'
    });

    if (!confirm.isConfirmed) return;

    const items = carrito.map(i => ({ id: i.id, desc: i.nombre, cant: i.cant, precio: i.precio }));

    try {
        const res = await fetch('/pos/facturar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items, descuento })
        });
        const data = await res.json();
        if (data.ok) {
            await Swal.fire({
                icon: 'success',
                title: '¡Factura impresa!',
                text: `Factura #${String(data.factura_id).padStart(5, '0')} generada correctamente.`,
                confirmButtonColor: '#6366f1',
                background: '#1e293b',
                color: '#f1f5f9'
            });
            carrito = [];
            renderCarrito();
            location.reload();
        } else {
            Swal.fire({ icon: 'error', title: 'Error', text: 'No se pudo procesar la factura.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
        }
    } catch(e) {
        Swal.fire({ icon: 'error', title: 'Error de conexión', text: 'No se pudo conectar con el servidor.', confirmButtonColor: '#6366f1', background: '#1e293b', color: '#f1f5f9' });
    }
}

function filtrar() {
    const q = document.getElementById('buscar').value.toLowerCase();
    const cat = document.getElementById('filtro-cat').value;
    document.querySelectorAll('.producto-card').forEach(card => {
        const nombre = card.dataset.nombre.toLowerCase();
        const catCard = card.dataset.cat;
        const visible = nombre.includes(q) && (cat === '' || catCard === cat);
        card.style.display = visible ? '' : 'none';
    });
}

function fmt(n) {
    return Math.round(n).toLocaleString('es-CR');
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('buscar').addEventListener('input', filtrar);
    document.getElementById('filtro-cat').addEventListener('change', filtrar);
    document.getElementById('descuento').addEventListener('input', actualizarTotales);
});
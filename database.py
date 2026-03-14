import psycopg2
from psycopg2.extras import RealDictCursor
from config import DB_CONFIG

def get_con():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)

def init_db():
    """Verifica que la conexión funcione correctamente."""
    try:
        con = get_con()
        con.close()
        return True
    except Exception as e:
        return str(e)

def login(nombre, password):
    con = get_con()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, rol FROM usuarios WHERE nombre=%s AND password=%s", (nombre, password))
    row = cur.fetchone()
    con.close()
    return dict(row) if row else None

def get_usuarios():
    con = get_con()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, rol FROM usuarios ORDER BY nombre")
    rows = cur.fetchall()
    con.close()
    return [dict(r) for r in rows]

def crear_usuario(nombre, password, rol):
    con = get_con()
    cur = con.cursor()
    cur.execute("INSERT INTO usuarios(nombre, password, rol) VALUES(%s, %s, %s)", (nombre, password, rol))
    con.commit()
    con.close()

def eliminar_usuario(user_id):
    con = get_con()
    cur = con.cursor()
    cur.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
    con.commit()
    con.close()

def get_categorias():
    con = get_con()
    cur = con.cursor()
    cur.execute("SELECT id, nombre FROM categorias ORDER BY nombre")
    rows = cur.fetchall()
    con.close()
    return [dict(r) for r in rows]

def crear_categoria(nombre):
    con = get_con()
    cur = con.cursor()
    cur.execute("INSERT INTO categorias(nombre) VALUES(%s)", (nombre,))
    con.commit()
    con.close()

def eliminar_categoria(cat_id):
    con = get_con()
    cur = con.cursor()
    cur.execute("DELETE FROM categorias WHERE id=%s", (cat_id,))
    con.commit()
    con.close()

def get_productos(buscar='', categoria_id=None):
    con = get_con()
    cur = con.cursor()
    if categoria_id:
        cur.execute("""
            SELECT p.id, p.nombre, p.precio, p.stock, p.stock_minimo, c.nombre AS categoria
            FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE LOWER(p.nombre) LIKE %s AND p.categoria_id = %s
            ORDER BY p.nombre
        """, ('%' + buscar.lower() + '%', categoria_id))
    else:
        cur.execute("""
            SELECT p.id, p.nombre, p.precio, p.stock, p.stock_minimo, c.nombre AS categoria
            FROM productos p LEFT JOIN categorias c ON p.categoria_id = c.id
            WHERE LOWER(p.nombre) LIKE %s
            ORDER BY p.nombre
        """, ('%' + buscar.lower() + '%',))
    rows = cur.fetchall()
    con.close()
    return [dict(r) for r in rows]

def crear_producto(nombre, precio, stock, stock_minimo, categoria_id):
    con = get_con()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO productos(nombre, precio, stock, stock_minimo, categoria_id)
        VALUES(%s, %s, %s, %s, %s)
    """, (nombre, precio, stock, stock_minimo, categoria_id))
    con.commit()
    con.close()

def editar_producto(prod_id, nombre, precio, stock, stock_minimo, categoria_id):
    con = get_con()
    cur = con.cursor()
    cur.execute("""
        UPDATE productos SET nombre=%s, precio=%s, stock=%s, stock_minimo=%s, categoria_id=%s
        WHERE id=%s
    """, (nombre, precio, stock, stock_minimo, categoria_id, prod_id))
    con.commit()
    con.close()

def eliminar_producto(prod_id):
    con = get_con()
    cur = con.cursor()
    cur.execute("DELETE FROM productos WHERE id=%s", (prod_id,))
    con.commit()
    con.close()

def get_productos_stock_bajo():
    con = get_con()
    cur = con.cursor()
    cur.execute("SELECT id, nombre, stock, stock_minimo FROM productos WHERE stock <= stock_minimo ORDER BY stock")
    rows = cur.fetchall()
    con.close()
    return [dict(r) for r in rows]

def descontar_stock(prod_id, cantidad):
    con = get_con()
    cur = con.cursor()
    cur.execute("UPDATE productos SET stock = stock - %s WHERE id=%s", (cantidad, prod_id))
    con.commit()
    con.close()

def crear_factura(cajero, items, subtotal, descuento, iva, total):
    con = get_con()
    cur = con.cursor()
    cur.execute("""
        INSERT INTO facturas(cajero, subtotal, descuento, iva, total)
        VALUES(%s, %s, %s, %s, %s) RETURNING id
    """, (cajero, subtotal, descuento, iva, total))
    factura_id = cur.fetchone()['id']
    for item in items:
        cur.execute("""
            INSERT INTO factura_items(factura_id, producto_id, descripcion, cantidad, precio)
            VALUES(%s, %s, %s, %s, %s)
        """, (factura_id, item['id'], item['desc'], item['cant'], item['precio']))
        descontar_stock(item['id'], item['cant'])
    con.commit()
    con.close()
    return factura_id

def get_historial(limit=50):
    con = get_con()
    cur = con.cursor()
    cur.execute("""
        SELECT id, fecha, cajero, subtotal, descuento, iva, total
        FROM facturas ORDER BY fecha DESC LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    con.close()
    return [dict(r) for r in rows]

def get_factura_items(factura_id):
    con = get_con()
    cur = con.cursor()
    cur.execute("""
        SELECT descripcion, cantidad, precio
        FROM factura_items WHERE factura_id=%s
    """, (factura_id,))
    rows = cur.fetchall()
    con.close()
    return [dict(r) for r in rows]

def get_reporte_hoy():
    con = get_con()
    cur = con.cursor()
    cur.execute("""
        SELECT COUNT(*) AS total_facturas,
               COALESCE(SUM(subtotal), 0) AS subtotal,
               COALESCE(SUM(descuento), 0) AS descuentos,
               COALESCE(SUM(iva), 0) AS iva,
               COALESCE(SUM(total), 0) AS total
        FROM facturas
        WHERE DATE(fecha) = CURRENT_DATE
    """)
    resumen = dict(cur.fetchone())
    cur.execute("""
        SELECT cajero, COUNT(*) AS facturas, COALESCE(SUM(total), 0) AS total
        FROM facturas
        WHERE DATE(fecha) = CURRENT_DATE
        GROUP BY cajero ORDER BY total DESC
    """)
    por_cajero = [dict(r) for r in cur.fetchall()]
    cur.execute("""
        SELECT fi.descripcion, SUM(fi.cantidad) AS unidades, SUM(fi.cantidad * fi.precio) AS total
        FROM factura_items fi
        JOIN facturas f ON fi.factura_id = f.id
        WHERE DATE(f.fecha) = CURRENT_DATE
        GROUP BY fi.descripcion ORDER BY unidades DESC LIMIT 10
    """)
    top_productos = [dict(r) for r in cur.fetchall()]
    con.close()
    return {'resumen': resumen, 'por_cajero': por_cajero, 'top_productos': top_productos}
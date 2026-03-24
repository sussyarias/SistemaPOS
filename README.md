# SistemaPOS
Sistema POS (Point of Sale) desarrollado en Python con gestión de inventario, facturación térmica y soporte multi-caja vía PostgreSQL.

El objetivo de este proyecto es construir un sistema de punto de venta sencillo que ajuste el stock automáticamente al momento de facturar, con soporte para impresión térmica directa.

## Features
- Login con múltiples usuarios y roles (admin / cajero)
- Punto de venta con carrito y descuentos
- Inventario con control de stock, alertas y códigos de producto
- Historial de facturas con detalle por factura
- Reporte de ventas del día
- Gestión de usuarios y categorías
- Impresión térmica directa ESC/POS (impresora AON PR-100)

## Tecnologías
- Python 3.13
- Flask
- PostgreSQL
- HTML + Tailwind CSS
- win32print (impresión térmica)

## Estructura del proyecto
```
SistemaPOS/
├── app.py              #Servidor Flask
├── config.py           #Configuración del negocio y BD
├── database.py         #Conexión y consultas PostgreSQL
├── printer.py          #Impresión ESC/POS
├── requirements.txt
├── BD/
│   └── pos_db.sql      #Script de creación de tablas
├── routes/
│   ├── auth.py
│   ├── pos.py
│   ├── inventario.py
│   ├── reportes.py
│   └── usuarios.py
├── views/              #Templates HTML con Tailwind CSS
└── static/             #CSS y JS
```

## Instalación
### 1. Clona el repositorio
```bash
git clone https://github.com/sussyarias/SistemaPOS.git
cd SistemaPOS
```

### 2. Crea un entorno virtual
```bash
python -m venv venv
```

### 3. Activa el entorno virtual
```bash
.\venv\Scripts\Activate.ps1
```

### 4. Instala las dependencias
```bash
pip install -r requirements.txt
```

### 5. Configura la base de datos
Edita `config.py` con los datos de tu servidor PostgreSQL:

```python
DB_CONFIG = {
    'host':     'localhost',
    'port':     5432,
    'database': 'pos_db',
    'user':     'postgres',
    'password': 'tu_password',
}
```

Luego crea las tablas usando el archivo `BD/pos_db.sql` en pgAdmin.

### 6. Corre la aplicación
```bash
python app.py
```

Abre el navegador en `http://localhost:5000`

## Usuarios por defecto
| Usuario | Contraseña |   Rol  |
|---------|------------|--------|
| Admin   |    1234    | admin  |
| Cajero1 |    0000    | cajero |

## Autora
Sussy Arias
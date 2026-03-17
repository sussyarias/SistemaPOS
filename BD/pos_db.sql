--Pegar en tu base de datos Postgres :)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    rol VARCHAR(20) DEFAULT 'cajero'
);

CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    precio NUMERIC(10,2) NOT NULL,
    stock INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 5,
    categoria_id INTEGER REFERENCES categorias(id)
);

CREATE TABLE facturas (
    id SERIAL PRIMARY KEY,
    fecha TIMESTAMP DEFAULT NOW(),
    cajero VARCHAR(100) NOT NULL,
    subtotal NUMERIC(10,2),
    descuento NUMERIC(10,2) DEFAULT 0,
    iva NUMERIC(10,2),
    total NUMERIC(10,2)
);

CREATE TABLE factura_items (
    id SERIAL PRIMARY KEY,
    factura_id INTEGER REFERENCES facturas(id),
    producto_id INTEGER REFERENCES productos(id),
    descripcion VARCHAR(150),
    cantidad INTEGER,
    precio NUMERIC(10,2)
);

-- Datos iniciales para pruebas :D
INSERT INTO usuarios(nombre, password, rol) VALUES ('Admin', '1234', 'admin');
INSERT INTO usuarios(nombre, password, rol) VALUES ('Cajero1', '0000', 'cajero');

INSERT INTO categorias(nombre) VALUES ('Bebidas'), ('Comidas'), ('Postres'), ('Otros');

INSERT INTO productos(nombre, precio, stock, stock_minimo, categoria_id) VALUES
('Cafe Americano', 1500, 20, 5, 1),
('Pan con queso', 1500, 15, 5, 2),
('Jugo natural', 2200, 10, 3, 1);
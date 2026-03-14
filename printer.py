import win32print
from config import EMPRESA, IMPRESORA, ANCHO_TICKET

ESC = chr(27)
GS  = chr(29)

INIT      = ESC + chr(64)
CUT       = GS  + chr(86) + chr(1)
CENTER    = ESC + chr(97) + chr(1)
LEFT      = ESC + chr(97) + chr(0)
BOLD_ON   = ESC + chr(69) + chr(1)
BOLD_OFF  = ESC + chr(69) + chr(0)
BIG_ON    = GS  + chr(33) + chr(17)
BIG_OFF   = GS  + chr(33) + chr(0)
LF        = '\n'

def lc(izq, der, ancho=None):
    if ancho is None:
        ancho = ANCHO_TICKET
    espacios = ancho - len(str(izq)) - len(str(der))
    if espacios < 1:
        espacios = 1
    return str(izq) + ' ' * espacios + str(der) + '\r\n'

def sep(ancho=None):
    if ancho is None:
        ancho = ANCHO_TICKET
    return '-' * ancho + '\r\n'

def centrar(texto, ancho=None):
    if ancho is None:
        ancho = ANCHO_TICKET
    return str(texto).center(ancho) + '\r\n'

def construir_ticket(factura_id, cajero, items, subtotal, descuento, iva, total, fecha):
    t = ''
    t += INIT
    t += CENTER + BOLD_ON + BIG_ON
    t += EMPRESA['nombre'] + LF
    t += BIG_OFF + BOLD_OFF
    t += centrar('Tel: ' + EMPRESA['telefono'])
    t += centrar(EMPRESA['direccion'])
    t += LEFT
    t += sep()
    t += lc('Factura #:', str(factura_id).zfill(5))
    t += lc('Fecha:', fecha)
    t += lc('Cajero:', cajero)
    t += sep()
    t += BOLD_ON + lc('PRODUCTO', 'TOTAL') + BOLD_OFF
    t += sep()

    for item in items:
        total_linea = item['cant'] * item['precio']
        desc  = item['desc'] + ' x' + str(item['cant'])
        monto = 'C' + f"{int(total_linea):,}"
        if len(desc) > ANCHO_TICKET - len(monto) - 1:
            desc = desc[:ANCHO_TICKET - len(monto) - 2]
        t += lc(desc, monto)

    t += sep()
    t += lc('Subtotal:', 'C' + f"{int(subtotal):,}")
    if descuento > 0:
        t += lc('Descuento:', '-C' + f"{int(descuento):,}")
    t += lc('IVA 13%:', 'C' + f"{int(iva):,}")
    t += BOLD_ON
    t += lc('TOTAL:', 'C' + f"{int(total):,}")
    t += BOLD_OFF
    t += sep()
    t += CENTER
    t += 'Gracias por su compra!' + LF
    t += '**** **** **** ****' + LF
    t += LF + LF + LF
    t += CUT
    return t

def imprimir(ticket_str):
    try:
        hp = win32print.OpenPrinter(IMPRESORA)
        win32print.StartDocPrinter(hp, 1, ('Factura', None, 'RAW'))
        win32print.StartPagePrinter(hp)
        win32print.WritePrinter(hp, ticket_str.encode('ascii', errors='replace'))
        win32print.EndPagePrinter(hp)
        win32print.EndDocPrinter(hp)
        win32print.ClosePrinter(hp)
        return True
    except Exception as e:
        return str(e)

def imprimir_factura(factura_id, cajero, items, subtotal, descuento, iva, total, fecha):
    ticket = construir_ticket(factura_id, cajero, items, subtotal, descuento, iva, total, fecha)
    return imprimir(ticket)

def imprimir_prueba():
    items = [
        {'desc': 'Cafe Americano', 'cant': 1, 'precio': 1500},
        {'desc': 'Pan con queso',  'cant': 2, 'precio': 1500},
    ]
    return imprimir_factura(
        factura_id = 1,
        cajero     = 'Admin',
        items      = items,
        subtotal   = 4500,
        descuento  = 0,
        iva        = 585,
        total      = 5085,
        fecha      = '13/03/2026 17:00'
    )

if __name__ == '__main__':
    resultado = imprimir_prueba()
    if resultado is True:
        print('Ticket de prueba impreso correctamente.')
    else:
        print('Error:', resultado)

import csv
import json
from datetime import datetime
from collections import defaultdict


#EXTRACT: leer datos
def extraer_ventas(ruta_csv):
    """Lee el CSV y devuelve una lista de diccionarios (datos crudos)."""
    with open(ruta_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


# TRANSFORM: limpiar y calcular
def transformar_ventas(ventas_raw):
    """Limpia datos sucios y calcula totales. Devuelve (limpias, errores)."""
    limpias = []
    errores = []

    for i, venta in enumerate(ventas_raw):
        try:
            # Validar producto no vacío
            if not venta.get("producto", "").strip():
                raise ValueError("Producto vacío")

            # Convertir cantidad (default 1 si vacío)
            cantidad_raw = venta.get("cantidad", "").strip()
            cantidad = int(cantidad_raw) if cantidad_raw else 1

            # Convertir precio
            precio = float(venta["precio_unitario"])

            # Calcular total
            total = cantidad * precio

            # Registro limpio
            limpias.append({
                "fecha": venta["fecha"],
                "producto": venta["producto"].strip(),
                "categoria": venta["categoria"].strip(),
                "cantidad": cantidad,
                "precio_unitario": precio,
                "total": round(total, 2),
                "cliente": venta["cliente"].strip(),
            })
        except (ValueError, TypeError) as e:
            errores.append({
                "fila": i + 2,  # +2 por header y 0-index
                "error": str(e),
                "datos": dict(venta),
            })

    return limpias, errores


# ANALYZE: generar métricas
def generar_resumen(ventas_limpias):
    """Genera el resumen ejecutivo a partir de datos limpios."""
    if not ventas_limpias:
        return {"error": "No hay datos válidos"}

    # Métricas generales
    total_facturado = sum(v["total"] for v in ventas_limpias)
    num_transacciones = len(ventas_limpias)
    ticket_medio = total_facturado / num_transacciones

    # Por categoría
    por_categoria = defaultdict(lambda: {"total": 0, "transacciones": 0})
    for v in ventas_limpias:
        cat = v["categoria"]
        por_categoria[cat]["total"] += v["total"]
        por_categoria[cat]["transacciones"] += 1

    # Top productos
    productos_total = defaultdict(float)
    for v in ventas_limpias:
        productos_total[v["producto"]] += v["total"]

    top_productos = sorted(productos_total.items(), key=lambda x: x[1], reverse=True)[:3]

    # Clientes únicos
    clientes = set(v["cliente"] for v in ventas_limpias)

    return {
        "fecha_reporte": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_facturado": round(total_facturado, 2),
        "num_transacciones": num_transacciones,
        "ticket_medio": round(ticket_medio, 2),
        "clientes_unicos": len(clientes),
        "por_categoria": dict(por_categoria),
        "top_3_productos": [
            {"producto": p, "total": round(t, 2)} for p, t in top_productos
        ],
    }


# LOAD: escribir resultados
def guardar_resultado(resumen, errores, ruta_salida, ruta_errores):
    """Escribe el resumen y los errores en archivos JSON."""
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resumen, f, indent=2, ensure_ascii=False)

    if errores:
        with open(ruta_errores, "w", encoding="utf-8") as f:
            json.dump(errores, f, indent=2, ensure_ascii=False)
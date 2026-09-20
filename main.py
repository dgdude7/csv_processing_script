import pipeline_ventas
def main():
    """Punto de entrada del pipeline."""
    print("=" * 50)
    print("  PIPELINE DE VENTAS DIARIAS")
    print("=" * 50)

    # Configuración
    ruta_entrada = "data/ventas_dia.csv"
    ruta_salida = "data/resumen_dia.json"
    ruta_errores = "data/errores_dia.json"

    # 1. EXTRACT
    print("\n[1/4] Extrayendo datos...")
    ventas_raw = pipeline_ventas.extraer_ventas(ruta_entrada)
    print(f"      Leídos: {len(ventas_raw)} registros")

    # 2. TRANSFORM
    print("[2/4] Limpiando y transformando...")
    ventas_limpias, errores = pipeline_ventas.transformar_ventas(ventas_raw)
    tasa_exito = len(ventas_limpias) / len(ventas_raw) * 100
    print(f"      Válidos: {len(ventas_limpias)} ({tasa_exito:.0f}%)")
    print(f"      Errores: {len(errores)}")

    # 3. ANALYZE
    print("[3/4] Generando resumen ejecutivo...")
    resumen = pipeline_ventas.generar_resumen(ventas_limpias)
    print(f"      Total facturado: {resumen['total_facturado']}€")

    # 4. LOAD
    print("[4/4] Guardando resultados...")
    pipeline_ventas.guardar_resultado(resumen, errores, ruta_salida, ruta_errores)
    print(f"      Resumen: {ruta_salida}")
    if errores:
        print(f"      Errores: {ruta_errores}")

    # Reporte final
    print("\n" + "=" * 50)
    print("  RESUMEN EJECUTIVO")
    print("=" * 50)
    print(f"  Facturación total: {resumen['total_facturado']}€")
    print(f"  Ticket medio:      {resumen['ticket_medio']}€")
    print(f"  Transacciones:     {resumen['num_transacciones']}")
    print(f"  Clientes únicos:   {resumen['clientes_unicos']}")
    print(f"\n  Top 3 productos:")
    for item in resumen["top_3_productos"]:
        print(f"    • {item['producto']}: {item['total']}€")
    print("=" * 50)


if __name__ == "__main__":
    main()
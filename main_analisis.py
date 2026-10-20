import pandas as pd
from utils_telecom import limpiar_y_validar_datos, evaluar_estadisticas_latencia, persistir_modelo_joblib

def ejecutar_pipeline_analitico():
    print("--- INICIANDO PIPELINE ANALÍTICO MODULAR ---")
    
    # 1. Simulación o carga de datos operacionales de RedConecta
    data_operacional = pd.DataFrame({
        "region": ["Metropolitana", "Norte", "Sur", "Centro", "Metropolitana", "Sur"] * 20,
        "tipo_servicio": ["Móvil", "Internet Hogar", "Corporativo", "Móvil", "Internet Hogar", "Corporativo"] * 20,
        "latencia_ms": [28.5, 45.2, 18.9, 65.4, 32.1, 48.0] * 20,
        "tiempo_resolucion_min": [25.0, 55.5, 15.0, 85.2, 30.0, 45.0] * 20,
        "incidencias": [2, 5, 1, 8, 3, 4] * 20,
        "tickets_soporte": [3, 6, 2, 9, 4, 5] * 20
    })
    
    # 2. Aplicar módulo de limpieza y validación
    df_procesado = limpiar_y_validar_datos(data_operacional)
    print(f" Registros procesados y validados: {len(df_procesado)}")
    
    # 3. Aplicar módulo de evaluación estadística (SciPy / NumPy)
    metricas_latencia = evaluar_estadisticas_latencia(df_procesado, "latencia_ms")
    print("\n Métricas Estadísticas de Latencia (ms):")
    for k, v in metricas_latencia.items():
        print(f"   - {k}: {v}")
        
    # 4. Persistir resultados con Joblib
    persistir_modelo_joblib(metricas_latencia, "metricas_latencia_red.pkl")
    print("\n Pipeline completado con éxito.")

if __name__ == "__main__":
    ejecutar_pipeline_analitico()
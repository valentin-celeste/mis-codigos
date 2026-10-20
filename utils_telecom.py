import numpy as np
import pandas as pd
import scipy.stats as stats
import joblib
import os

def limpiar_y_validar_datos(df):
    """
    Limpia valores nulos críticos y valida rangos lógicos operacionales 
    utilizando NumPy y Pandas.
    """
    df_clean = df.copy()
    
    # Imputación de nulos numéricos críticos con la mediana
    cols_numericas = ["latencia_ms", "tiempo_resolucion_min", "incidencias", "tickets_soporte"]
    for col in cols_numericas:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
            
    # Filtrar valores negativos lógicamente imposibles
    df_clean = df_clean[(df_clean["latencia_ms"] >= 0) & (df_clean["tiempo_resolucion_min"] >= 0)]
    
    return df_clean

def evaluar_estadisticas_latencia(df, columna="latencia_ms"):
    """
    Realiza cálculos estadísticos avanzados utilizando SciPy y NumPy 
    para evaluar el comportamiento de la red.
    """
    datos = df[columna].dropna().values
    
    # Estadísticos descriptivos con NumPy
    media = np.mean(datos)
    mediana = np.median(datos)
    percentil_95 = np.percentile(datos, 95)
    desv_est = np.std(datos, ddof=1)
    
    # Prueba de normalidad de Shapiro-Wilk con SciPy (muestreo si excede 5000 registros)
    sample_data = datos[:5000] if len(datos) > 5000 else datos
    shapiro_stat, p_value = stats.shapiro(sample_data)
    
    resultados = {
        "media": round(media, 2),
        "mediana": round(mediana, 2),
        "percentil_95": round(percentil_95, 2),
        "desv_estandar": round(desv_est, 2),
        "shapiro_stat": round(shapiro_stat, 4),
        "p_value": round(p_value, 5)
    }
    return resultados

def persistir_modelo_joblib(objeto_analitico, nombre_archivo="artefacto_operacional.pkl"):
    """
    Serializa y guarda modelos o estructuras de datos procesadas usando Joblib.
    """
    os.makedirs("modelos", exist_ok=True)
    ruta = os.path.join("modelos", nombre_archivo)
    joblib.dump(objeto_analitico, ruta)
    print(f" Artefacto guardado exitosamente en: {ruta}")
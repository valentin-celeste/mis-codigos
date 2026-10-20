import pandas as pd
import numpy as np
from scipy import stats
import joblib
import os

def cargar_y_evaluar_datos(file_path):
    """Carga el dataset oficial y realiza el diagnóstico de calidad de datos."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    df = pd.read_excel(file_path)
    
    print("--- EVALUACIÓN DE CALIDAD DE DATOS (DATA QUALITY) ---")
    print(f"Total de Registros: {len(df)}")
    print(f"Valores Nulos por Columna:\n{df.isnull().sum()}\n")
    
    # Detección de outliers en Latencia mediante Z-score con SciPy
    z_scores_latencia = stats.zscore(df['latencia_ms'])
    outliers_latencia = df[np.abs(z_scores_latencia) > 3]
    print(f"Outliers detectados en Latencia (Z-Score > 3): {len(outliers_latencia)}")
    
    return df

def generar_archivos_por_area(df, output_dir='outputs'):
    """Genera y exporta los archivos requeridos para Soporte Técnico y CX."""
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Área de Soporte Técnico
    cols_soporte = [
        'fecha_registro', 'region', 'tipo_servicio', 
        'incidencias_reportadas', 'tickets_soporte', 'tiempo_resolucion_hr'
    ]
    df_soporte = df[cols_soporte].copy()
    path_soporte = os.path.join(output_dir, 'reporte_soporte_tecnico.csv')
    df_soporte.to_csv(path_soporte, index=False)
    
    # 2. Área de Experiencia de Clientes (CX)
    cols_cx = [
        'fecha_registro', 'tipo_servicio', 
        'clientes_afectados', 'latencia_ms', 'cumplimiento_sla'
    ]
    df_cx = df[cols_cx].copy()
    path_cx = os.path.join(output_dir, 'reporte_experiencia_clientes.csv')
    df_cx.to_csv(path_cx, index=False)
    
    print("--- ARCHIVOS GENERADOS EXITOSAMENTE ---")
    print(f"1. Soporte Técnico: {path_soporte}")
    print(f"2. Experiencia de Clientes: {path_cx}\n")

def serializar_pipeline_joblib(df, model_dir='models'):
    """Serializa la estructura de datos procesada para su reuso continuo."""
    os.makedirs(model_dir, exist_ok=True)
    pipeline_data = {
        'resumen_region': df.groupby('region')[['incidencias_reportadas', 'tiempo_resolucion_hr']].mean().to_dict(),
        'sla_cumplimiento': df['cumplimiento_sla'].value_counts(normalize=True).to_dict()
    }
    model_path = os.path.join(model_dir, 'pipeline_telecom_v1.pkl')
    joblib.dump(pipeline_data, model_path)
    print(f"Pipeline serializado con Joblib en: {model_path}")

if __name__ == "__main__":
    DATASET_PATH = "dataset_set_D_telecomunicaciones.xlsx"
    df_telecom = cargar_y_evaluar_datos(DATASET_PATH)
    generar_archivos_por_area(df_telecom)
    serializar_pipeline_joblib(df_telecom)
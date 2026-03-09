import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def process_fraud_detection(df):
    """
    Recibe un DataFrame, entrena un modelo rápido de detección 
    de anomalías y devuelve el DataFrame con los resultados.
    """
    # 1. Limpieza rápida: Eliminamos 'Time' y 'Class' (si existe) para el entrenamiento
    features = df.drop(['Time'], axis=1)
    if 'Class' in features.columns:
        features = features.drop(['Class'], axis=1)

    # 2. Escalar los datos (importante para modelos de detección)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features)

    # 3. Modelo: Isolation Forest
    # contamination=0.01 significa que marcamos el 1% como sospechoso
    model = IsolationForest(contamination=0.01, random_state=42, n_jobs=-1)
    
    # Predecir: 1 es normal, -1 es anomalía
    df['anomaly_score'] = model.fit_predict(scaled_data)
    df['is_fraud'] = df['anomaly_score'].map({1: 0, -1: 1})
    
    return df
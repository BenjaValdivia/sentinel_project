import pandas as pd
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

def process_fraud_detection(df):
    """
    Recibe un DataFrame, entrena un modelo rápido de detección 
    de anomalías y devuelve el DataFrame con los resultados.
    """
    # 1. Limpieza rápida: Eliminamos columnas que no sirven para el entrenamiento
    features = df.drop(['Time'], axis=1, errors='ignore')
    if 'Class' in features.columns:
        features = features.drop(['Class'], axis=1)

    # --- BLINDAJE ANTI-CRASHES ---
    # Ignoramos automáticamente cualquier columna de texto (como patentes o códigos de maquinaria)
    # y nos quedamos solo con las columnas numéricas que el algoritmo puede entender.
    features = features.select_dtypes(include=['number'])

    # --- OPTIMIZACIÓN DE MEMORIA ---
    # Convertir a float32 reduce el consumo de RAM a la mitad
    features = features.astype('float32')

    # 2. Escalar los datos (Crucial para Isolation Forest)
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(features)

    # 3. Modelo: Isolation Forest
    # contamination=0.01 marca el 1% de los datos como sospechosos
    # n_jobs=-1 usa todos los núcleos de tu procesador para terminar más rápido
    model = IsolationForest(contamination=0.01, random_state=42, n_jobs=-1)
    
    # 4. Predecir: 1 es normal, -1 es anomalía
    df['anomaly_score'] = model.fit_predict(scaled_data)
    
    # Mapeamos los resultados para que sea más fácil leerlos (1 = Fraude/Anomalía, 0 = Normal)
    df['is_fraud'] = df['anomaly_score'].map({1: 0, -1: 1})
    
    return df
# 🛡️ Sentinel AI: Plataforma de Detección de Fraude Local

Sentinel AI es un dashboard interactivo construido con Python y Streamlit diseñado para la detección de anomalías y fraudes en transacciones financieras. 

La principal ventaja de este sistema es su **enfoque en la privacidad**: todo el procesamiento de Machine Learning y análisis de datos se ejecuta de forma 100% local en la memoria RAM del equipo, sin enviar información sensible a la nube o servidores de terceros.

## ✨ Características Principales

* **Procesamiento Local Seguro:** Carga de archivos CSV pesados y ejecución del modelo en entorno local.
* **Inteligencia Artificial Integrada:** Utiliza el algoritmo `Isolation Forest` de Scikit-Learn para detectar comportamientos transaccionales que se desvían de la norma estadística (Outliers).
* **Métricas en Tiempo Real:** Cálculo dinámico de transacciones, capital en riesgo y ticket promedio.
* **Visualización Avanzada (Optimizada):** * Mapa de Desviaciones (Scatter plot con navegación fluida).
  * Distribución de Capital (Boxplot con escala logarítmica ajustada).
* **Módulo de Inspección Prioritaria:** Panel interactivo para aislar, auditar y simular el bloqueo de las transacciones más críticas.
* **Exportación de Datos:** Generación de reportes limpios en formato CSV con las banderas de fraude integradas.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.x
* **Frontend / Dashboard:** [Streamlit](https://streamlit.io/)
* **Análisis de Datos:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (`IsolationForest`, `StandardScaler`)
* **Visualización:** Plotly Express

## 🚀 Instalación y Ejecución

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local (instrucciones para Windows PowerShell):

### 1. Clonar el repositorio
```powershell
git clone [https://github.com/TU_USUARIO/sentinel_project.git](https://github.com/TU_USUARIO/sentinel_project.git)
cd sentinel_project

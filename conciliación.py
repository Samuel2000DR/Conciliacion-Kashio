import streamlit as st
import pandas as pd
import os

def find_uploaded_files():
    files = os.listdir()
    eecc_file = next((f for f in files if "ultimos_movimientos" in f.lower()), None)
    metabase_file = next((f for f in files if "procesopago" in f.lower()), None)
    return eecc_file, metabase_file

def main():
    st.title("Análisis de DSN y Extornos")
    
    eecc_file, metabase_file = find_uploaded_files()
    
    if not eecc_file or not metabase_file:
        st.warning("No se encontraron los archivos necesarios. Asegúrate de haber subido los archivos con los nombres correctos.")
        return
    
    st.success(f"Archivo EECC detectado: {eecc_file}")
    st.success(f"Archivo Metabase detectado: {metabase_file}")
    
    # Cargar datos
    data_eecc = pd.read_excel(eecc_file)
    data_metabase = pd.read_excel(metabase_file)
    
    # Definir índices de las columnas a comparar
    criteria_column_index_eecc = 7  # Columna 8 (basado en 0)
    criteria_column_index_metabase = 26  # Columna 27 (basado en 0)
    
    if criteria_column_index_eecc >= len(data_eecc.columns) or criteria_column_index_metabase >= len(data_metabase.columns):
        st.error("Las columnas de comparación no existen en los archivos.")
        return
    
    criteria_column_eecc = data_eecc.columns[criteria_column_index_eecc]
    criteria_column_metabase = data_metabase.columns[criteria_column_index_metabase]
    
    # Encontrar DSN que están en EECC pero no en Metabase
    dsns_not_in_metabase = data_eecc[~data_eecc[criteria_column_eecc].isin(data_metabase[criteria_column_metabase])]
    
    st.subheader(f"DSN Encontrados (Pagos en EECC no ubicados en core de Kashio): {len(dsns_not_in_metabase)}")
    st.dataframe(dsns_not_in_metabase)
    
    # Guardar resultado
    output_file = "DSN_encontrados.xlsx"
    dsns_not_in_metabase.to_excel(output_file, index=False)
    
    # Descargar archivo
    with open(output_file, "rb") as file:
        st.download_button(
            label="Descargar archivo de DSN encontrados",
            data=file,
            file_name=output_file,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()

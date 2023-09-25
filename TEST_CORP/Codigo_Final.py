
# Import the libraries
import pandas as pd  # Used for data manipulation and analysis, particularly with structured data.
import time  # Used for measuring time or introducing delays in code.
import os  # Used for interacting with the operating system, like file and directory manipulation.
import re  # Used for pattern matching and manipulating strings based on regular expressions.
import datetime


def procesar_archivos_en_directorio(ruta_directorio):
    """
    Procesa archivos Excel dentro de una ruta dada que comienzan con "Base_" seguido de un número.
    
    Args:
    - ruta_directorio (str): Ruta al directorio que contiene los archivos a procesar.
    
    Returns:
    - DataFrame: Un conjunto de datos concatenado con el contenido de todos los archivos procesados.
    """
    # Lista todos los archivos en el directorio
    lista_archivos = os.listdir(ruta_directorio)
    print(lista_archivos)
    
    # Inicializa una lista vacía para almacenar DataFrames individuales
    lista_dataframes = []

    # Expresión regular para identificar archivos que siguen el patrón "Base_" seguido de un número
    patron = r'^Base_\d+'

    for nombre_archivo in lista_archivos:
        if re.match(patron, nombre_archivo):
            print(nombre_archivo)
            
            # Leer el archivo Excel principal, omitiendo las primeras 4 filas y usando 2 filas como encabezado
            df_principal = pd.read_excel(os.path.join(ruta_directorio, nombre_archivo), skiprows=4, header=[0, 1])
            
            # Leer las primeras 3 filas del mismo archivo para capturar información adicional
            df_info_adicional = pd.read_excel(os.path.join(ruta_directorio, nombre_archivo), nrows=3)

            # Extraer el número del nombre del archivo
            numero_archivo = re.search(r'(\d+)', nombre_archivo).group(1)
            df_principal['Nombre del Proceso'] = f"proceso {numero_archivo}"
            
            # Capturar información adicional y añadirla al DataFrame principal
            for i in range(3):
                df_principal[df_info_adicional.iloc[i, 0]] = df_info_adicional.iloc[i, 1]

            # Agregar información de metadatos
            df_principal['RECORD_SOURCE'] = nombre_archivo
            fecha_formateada = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            df_principal['LOAD_DATE'] = fecha_formateada
            
            # Agregar DataFrame procesado a la lista
            lista_dataframes.append(df_principal)
        else:
            print(f"No es base a usar {nombre_archivo}")

    # Concatena todos los DataFrames en uno solo
    dataset_final = pd.concat(lista_dataframes)
    
    return dataset_final

start_time = time.time()

# Uso del código:
ruta = 'Prueba reto'
Base_Total = procesar_archivos_en_directorio(ruta)
Base_permanencia = pd.read_excel(os.path.join(ruta, "Base_permanencia.xlsx"))
pd.set_option('display.max_columns', 78) 





# Cleaning up the column names
cleaned_columns = []
for col in Base_Total.columns:
    # Check if the second level of the multi-index is a string and contains "Unnamed:"
    if isinstance(col[1], str) and ("Unnamed:" in col[1] or col[1] == "" or col[1] is None):
        cleaned_columns.append(col[0])
    else:
        cleaned_columns.append(col)

Base_Total.columns = cleaned_columns




new_columns = []
for col in Base_Total.columns:
    if isinstance(col, tuple):
        new_col = '_'.join(col)
    else:
        new_col = col
    new_columns.append(new_col)

Base_Total.columns = new_columns




Base_Total.columns = Base_Total.columns.str.replace('\n', ' ')






# Lista de competencias que quieres revisar
competencias = ["Calidad del trabajo", 
                "Desarrollo de relaciones", 
                "Escrupulosidad/Minuciosidad", 
                "Flexibilidad y Adaptabilidad", 
                "Orden y la calidad", 
                "Orientación al Logro", 
                "Pensamiento Analítico", 
                "Resolución de problemas", 
                "Tesón y disciplina", 
                "Trabajo en equipo"]

# Categorías de las competencias a verificar
categorias = ["_Valor", "_Esperado", "_Brecha", "_Cumplimiento"]

# Construye una máscara para filtrar las filas
mask = True
for competencia in competencias:
    for categoria in categorias:
        columna = f"{competencia}{categoria}"
        mask &= Base_Total[columna].notna()

# Elimina las filas usando la máscara inversa (con ~)
Base_Total.drop(Base_Total[~mask].index, inplace=True)





Base_Total["Fecha de Finalización de Proceso (Zona horaria GMT 0)"] = Base_Total["Fecha de Finalización de Proceso (Zona horaria GMT 0)"].fillna(Base_Total["Fecha de Ingreso a Proceso (Zona horaria GMT 0)"])


# Ordena el DataFrame por 'Fecha de Finalización de Proceso (Zona horaria GMT 0)' de manera descendente
Base_Total = Base_Total.sort_values(by='Fecha de Finalización de Proceso (Zona horaria GMT 0)', ascending=False)

# Elimina duplicados por 'No. Identificación' y se queda con el primer registro (el más reciente debido al ordenamiento previo)
Base_Total = Base_Total.drop_duplicates(subset='No. Identificación', keep='first')





current_datetime = datetime.datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M")  # Formatea la fecha y hora actual
Base_Total['PROCESS_DATA'] = formatted_datetime
# Obtener el nombre de usuario de Windows
windows_username = os.getlogin()

# Establecer el valor de la columna CREATION_USER
Base_Total['CREATION_USER'] = windows_username


Base_Total["No. Identificación"]=Base_Total["No. Identificación"].str.replace(' ', '', regex=True)
Base_permanencia["No. Identificación"]=Base_permanencia["No. Identificación"].str.replace(' ', '', regex=True)
Base_Total=pd.merge(Base_Total,Base_permanencia,how='inner',on='No. Identificación')




Base_Total = Base_Total.sort_values(by=["Nombre del Proceso",'Ranking'], ascending=True)



Base_Total.to_excel("Modelo_base_consolidado.xlsx",index=False)



end_time = time.time()

print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos.")
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import statsmodels.api as sm


# Importar los datos de precios de la acción
df = pd.read_csv("C:/Users/Rayzek/Documents/PROYECTOS/DATASETS/ACCIONES/AMZN.csv")
df.head()

# Set date as the index of the DataFrame
df=df.set_index('Date')

# Select only data from dates before the quarantine period
start_date = '2000-01-03'
end_date = '2020-03-22'
df = df.loc[start_date:end_date]
df=df.reset_index()


import seaborn as sns
# Seleccionar las características que se utilizarán para predecir el precio
# Convertir la columna de fecha a variables dummies
df_dummies = pd.get_dummies(df['Date'])

# Unir la matriz de variables dummies con los datos originales
df = pd.concat([df, df_dummies], axis=1)
df


# Seleccionar la variable objetivo, en este caso el precio de cierre
y = df['Close']

X = df.drop("Close",axis=1)

# Añadir una columna constante para representar el término independiente en la regresión
X = sm.add_constant(X)



# Dividir los datos en un conjunto de entrenamiento y un conjunto de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Entrenar un modelo de regresión lineal utilizando la librería statsmodels
regression_model = sm.OLS(y_train, X_train)
regression_results = regression_model.fit()

# Realizar predicciones en el conjunto de prueba
y_pred = regression_results.predict(X_test)

# Calcular el error estándar de las predicciones
std_error = regression_results.mse_resid**0.5

# Calcular el Standard Error Band
se_band = 2 * std_error

# Crear un DataFrame con los resultados
results = pd.DataFrame({'y_test': y_test, 'y_pred': y_pred})

# Añadir la banda de error estándar a los resultados
results['lower_band'] = results['y_pred'] - se_band
results['upper_band'] = results['y_pred'] + se_band

# Graficar los resultados usando seaborn
sns.lineplot(data=results, x=results.index, y='y_test', label='Precio real')
sns.lineplot(data=results, x=results.index, y='y_pred', label='Precio predecido')
sns.lineplot(data=results, x=results.index, y='lower_band', label='Banda inferior', linestyle='--')
sns.lineplot(data=results, x=results.index, y='upper_band', label='Banda superior', linestyle='--')

# Mostrar la gráfica
plt.show()

# Calcular el error absoluto medio
mae = mean_absolute_error(y_test, y_pred)
print("El error absoluto medio es:", mae)

#multicolinealidad EVITARLA
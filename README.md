# Recolección de Datos ADC con Rapsberry Pi
Este proyecto recoge datos analógicos de varios canales utilizando el módulo ADC ADS1256 conectado a un Raspberry Pi. Los datos recopilados se guardan en un archivo CSV para su posterior análisis. El script ofrece opciones para configurar la tasa de muestreo, los canales a medir y la duración de la recolección de datos. También proporciona un gráfico referente al comportamiento de la onda recibida por el geófono, indicando peak máximo, mínimo y promedio de datos.

## Requisitos

- Raspberry Pi (cualquier modelo con soporte GPIO)
- Módulo ADC ADS1256
- Python 3
- Biblioteca ADS1256
- Biblioteca RPi.GPIO

## Configuración

1. **Conecta el módulo ADS1256 al Raspberry Pi** siguiendo las instrucciones del fabricante.

2. **Instala las bibliotecas de Python necesarias** si no están ya instaladas:
    ```bash
    sudo apt-get update
    sudo apt-get install python-pip
    sudo pip install RPi.GPIO
    sudo pip install spidev
    ```

3. **Descarga la biblioteca ADS1256** desde su [repositorio](https://github.com/AhumadaFranco/ADS1256testGeofono.git).

4. **Clona este repositorio** en tu Raspberry Pi:
    ```bash
    git clone https://github.com/AhumadaFranco/ADS1256testGeofono.git
    cd ADS1256testGeofono/PYtest
    ```

## Uso

1. **Ejecuta el script** para comenzar a recopilar datos:
    ```bash
    sudo python test5.py
    ```

2. **El script te pedirá las siguientes configuraciones:**
   - **Tasa de Muestreo (SPS):** Puedes elegir entre 50 SPS, 60 SPS, 100 SPS, 200 SPS o 500 SPS, 1000 SPS o 2000 SPS.
   - **Canales a Medir:** Ingresa los canales que deseas medir (por ejemplo, 0,1,2). Si no se ingresan canales, se usarán por defecto los canales 0 a 7.
   - **Duración:** Ingresa el tiempo en segundos para la recolección de datos (por ejemplo, 60 para 60 segundos).

  - **Visualización de Datos en Tiempo Real:** Puedes elegir mostrar los datos en tiempo real en la pantalla. Para no retrasar la medición, es decir, que se mantenga el total de muestras en el tiempo establecido por usuario (SPS x duración de muestreo), se visualiza en pantalla la adquisición de datos cada 100 muestras. Esta carencia de retraso en la recolección de datos en un tiempo establecido se da a la perfección cuando funciona un sólo canal. Por otro lado, cabe destacar que es posible que exista un cierto retraso en la toma de muestras, cuando se exije sensar 2 canales o más, debido al aumento de SPS, en dónde se cumple evidentemente la relación entre SPS y duración de muestreo.

3. **El script recopilará datos** según tus configuraciones y los guardará en un archivo CSV.

4. **Los datos recopilados se guardan en un archivo CSV** con un nombre especificado por ti o generado por el script. El archivo CSV tendrá un formato similar a este:
    ```
    T (s), Canal 0 (V), Canal 1 (V), Canal 2 (V)...
    0.000001, value0_0, value0_1, value0_2, ...
    0.000002, value1_0, value1_1, value1_2, ...
    ...
    ```

5. **Después de completar la recolección de datos**, el script mostrará el tiempo total que tomó la recolección y el número total de muestras recopiladas.

## Explicación del Script
El script `test5.py` realiza los siguientes pasos:

1. **Inicialización:** El script inicializa el módulo ADC ADS1256 conectado al Raspberry Pi. Luego solicita al usuario varias configuraciones, incluyendo los canales a medir, la ganancia de trabajo del ADC, la tasa de muestreo y la duración de la medición.

2. **Recolección de Datos:** El script recopila datos de los canales seleccionados, convirtiendo los valores crudos del ADC en valores de voltaje. Periódicamente guarda los datos recopilados en un archivo CSV, asegurando que los datos no se pierdan durante sesiones largas de medición.

3. **Salida:** Los datos recopilados se guardan en un archivo CSV, que se puede analizar posteriormente. Además, se exporta un archivo PNG con un gráfico que evidencia la onda entregada por el geófono, indicando valores relevantes como peaks máximo, mínimo y promedio. Al final de la medición, el script muestra la duración total y el número de muestras recolectadas.

## **Cambios Realizados**


### **Modificaciones en test5.py:**

- **Interfaz de Usuario Mejorada:** El script solicita al usuario que además de ingresar los canales a medir, lo que produce una mayor flexibilidad de análisis de los datos obtenidos, también se integran nuevas opciones a la interfaz, tales como elegir la ganancia (relacionada al PGA del ADC) con que trabaja el ADS1256 y manejar el tiempo de muestreo en segundos, no minutos. Cabe destacar que para la selección de la ganancia, se recomienda considerar el contexto de los parámetros que se emplean para lograr la recolección de los enviado por el geófono, debido a que se está trabajando en Single Mode (0 a 5 V), por lo tanto al estar la señal del geófono desplazada este valor de ganancia genera la lectura adecuada del geófono por parte del ADC (se puede aumentar el valor de ganancia pero considerando una probable saturación en la señal).
  
-  **Aumento de Samples Per Second (SPS):** Se gestiona un incremento desde los 600 SPS experimentales hasta los 2000 SPS, de tal forma que pueda obtener una lectura más cercana al comportamiento real del geófono.
  
- **Exportación de CSV:** Se automatiza el nombre del archivo CSV de tal forma que el documento exportado posee la estructura "geofono_multicanal_{usuario}SPS_AAAAMMDD_hhmmss.csv".
Por ejemplo: geofono_multicanal_2000SPS_20250403_165359.csv

- **Exportación de gráfico:** Se integra la visualización y exportación de un gráfico de onda que evidencia el comportamiento del geófono (clampeado). De esta forma se ejecuta una herramienta gráfica para analizar en primera instancia ruidos, picos de valores, etc.

## Manejo de Errores

El script incluye un bloque try-except para manejar cualquier excepción que pueda ocurrir durante la ejecución. Si ocurre un error, limpia los pines GPIO y muestra el mensaje de error.

## Ejemplo de Salida
Start time (hh:mm:ss.ss): 16:53:44.637
End time (hh:mm:ss.ss): 16:53:59.638
Samples: 30000 @ 2000 sps in 15 sec.


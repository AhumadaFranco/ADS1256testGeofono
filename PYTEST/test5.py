
import RPi.GPIO as GPIO
import ADS1256
import time
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Inicialización del ADC
adc = ADS1256.ADS1256()
adc.ADS1256_init()

# Selección de canales múltiples
print("¿Qué canales desea muestrear? (separados por coma, ej: 0,1,2): ")
entrada = input("Canales (0–7): ")
canales = [int(c.strip()) for c in entrada.split(',') if c.strip().isdigit() and 0 <= int(c.strip()) <= 7]

# Selección de ganancia (PGA)
print("Ganancias disponibles: 1, 2, 4, 8, 16, 32, 64")
gain_map = {1: 0, 2: 1, 4: 2, 8: 3, 16: 4, 32: 5, 64: 6}
ganancia = int(input("Selecciona la ganancia deseada: "))
adc.gain = gain_map.get(ganancia, 0)

# Selección de SPS y duración
print("SPS disponibles: 50, 60, 100, 200, 500, 1000, 2000")
sps = int(input("Ingresa SPS: "))
duracion = float(input("Duración del muestreo (segundos): "))
muestras_totales = int(sps * duracion)

print(f"*** Iniciando adquisición: {muestras_totales} muestras a {sps} SPS en canales {canales} ***")

# Preparación
datos = {canal: [] for canal in canales}
tiempo_lista = []
intervalo = 1.0 / sps

for i in range(muestras_totales):
    if i == 0:
        start_clock = datetime.now()  # hora real
        start_time = time.perf_counter()
    t_actual = time.perf_counter() - start_time
    tiempo_lista.append(round(t_actual, 6))

    valores = adc.ADS1256_GetSelectedChannels(canales)
    for idx, canal in enumerate(canales):
        voltaje = valores[idx] * 5.0 / 0x7FFFFF
        datos[canal].append(round(voltaje, 6))

    if i % 100 == 0:
        texto = f"🔹 Muestra {i} | Tiempo: {t_actual:.3f} s | " + " | ".join(
            [f"Canal {canal}: {datos[canal][-1]:.6f} V" for canal in canales]
        )
        print(texto)

    tiempo_siguiente = start_time + (i + 1) * intervalo
    while time.perf_counter() < tiempo_siguiente:
        pass

print("*** Adquisición finalizada ***")
end_clock = datetime.now()
elapsed = end_clock - start_clock
print(f"Start time (hh:mm:ss.ss): {start_clock.strftime('%H:%M:%S.%f')[:-3]}")
print(f"End time (hh:mm:ss.ss): {end_clock.strftime('%H:%M:%S.%f')[:-3]}")
print(f"Samples: {muestras_totales} @ {sps} sps in {int(duracion)} sec.")

# Exportar CSV
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"geofono_multicanal_{sps}SPS_{timestamp}.csv"

with open(csv_filename, "w", newline="") as f:
    writer = csv.writer(f)
    encabezados = ["Tiempo (s)"] + [f"Canal {c} (V)" for c in canales]
    writer.writerow(encabezados)

    for i in range(muestras_totales):
        fila = [tiempo_lista[i]] + [datos[c][i] for c in canales]
        writer.writerow(fila)

print(f"✅ CSV exportado: {csv_filename}")

# Crear gráfico con subplots
fig, axs = plt.subplots(len(canales), 1, figsize=(14, 4 * len(canales)), sharex=True)
if len(canales) == 1:
    axs = [axs]

for idx, canal in enumerate(canales):
    voltajes = datos[canal]
    tiempos = tiempo_lista
    v_max = max(voltajes)
    v_min = min(voltajes)
    v_prom = sum(voltajes) / len(voltajes)

    axs[idx].plot(tiempos, voltajes, label=f"Canal {canal}", linewidth=1)
    axs[idx].axhline(y=v_prom, color='blue', linestyle='--', label=f"Prom: {v_prom:.3f} V")
    axs[idx].plot(tiempos[voltajes.index(v_max)], v_max, 'go', label=f"Max: {v_max:.3f} V")
    axs[idx].plot(tiempos[voltajes.index(v_min)], v_min, 'ro', label=f"Min: {v_min:.3f} V")
    axs[idx].legend(loc='upper right')
    axs[idx].set_ylabel("Voltaje (V)")
    axs[idx].grid(True)
    axs[idx].set_title(f"Canal {canal}")

axs[-1].set_xlabel("Tiempo (s)")
plt.suptitle(f"Geófono Multicanal | {sps} SPS | Ganancia {ganancia}x", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
png_filename = csv_filename.replace(".csv", ".png")
plt.savefig(png_filename)
print(f"🖼️ Gráfico exportado: {png_filename}")
plt.show()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        GPIO.cleanup()
        print(f"\nProgram terminated due to {{e}}")
        exit()
    finally:
        GPIO.cleanup()

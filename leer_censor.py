import csv
import serial
import time

# Configuración del puerto serial
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

# Pide información inicial
edificio = input("¿En qué edificio se encuentra?: \n 1.R\n 2.P\n 3.C\n 4.A\n 5.D\n").lower()
locacion = input("¿En qué locación está (Salón, Hall o Pasillo)? \n 1.S\n 2.H\n 3.P\n ").lower()
num_datos = int(input("¿Cuántos datos desea tomar)?: "))

# Nombre del archivo CSV
nombre_archivo = 'datos_arduino.csv'

try:
    with open(nombre_archivo, 'x', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Edificio', 'Locación', 'Promedio'])  # Encabezados
except FileExistsError:
    pass


def guardar_promedios(edificio, locacion, num_promedios):
    with open(nombre_archivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        datos_tomados = 0  # Contador de promedios calculados
        try:
            while datos_tomados < num_datos:

                if arduino.in_waiting > 0:
                    data = arduino.readline().decode('utf-8').strip()
                    try:
                        float(data)

                        print(f"Valor recibido: {data}")
                    except ValueError:
                        print(f"Error de lectura: {data}")
                    print(f"Promedio de los últimos 10 segundos: {data}")
                    writer.writerow([edificio, locacion, data])  # Guarda el promedio en el archivo
                    datos_tomados += 1

        except KeyboardInterrupt:
            print("Programa terminado")
        finally:
            arduino.close()


# Ejecuta la función para leer y guardar los promedios
guardar_promedios(edificio, locacion, num_datos)
print(f"Promedios guardados en {nombre_archivo}")

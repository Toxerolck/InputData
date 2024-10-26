import csv
import serial
import time

# Configuración del puerto serial
arduino = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

# Pide información inicial
edificio = input("¿En qué edificio se encuentra?: \n 1.R\n 2.P\n 3.C\n 4.A\n 5.D\n").lower()
locacion = input("¿En qué locación está (Salón, Hall o Pasillo)? \n 1.S\n 2.H\n 3.P\n ").lower()
num_promedios = int(input("¿Cuántos promedios desea tomar (cada promedio se basa en 10 segundos de datos)?: "))

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
        promedios_tomados = 0  # Contador de promedios calculados

        try:
            while promedios_tomados < num_promedios:
                start_time = time.time()
                datos = []

                # Recolecta datos durante 10 segundos
                while time.time() - start_time < 10:
                    if arduino.in_waiting > 0:
                        data = arduino.readline().decode('utf-8').strip()
                        try:
                            dato = float(data)
                            datos.append(dato)
                            print(f"Valor recibido: {dato}")  # Muestra el valor en la consola
                        except ValueError:
                            print(f"Error de lectura: {data}")

                # Calcula y guarda el promedio si se acumularon datos
                if datos:
                    promedio = sum(datos) / len(datos)
                    print(f"Promedio de los últimos 10 segundos: {promedio}")
                    writer.writerow([edificio, locacion, promedio])  # Guarda el promedio en el archivo
                    promedios_tomados += 1  # Incrementa el contador de promedios tomados

        except KeyboardInterrupt:
            print("Programa terminado")
        finally:
            arduino.close()


# Ejecuta la función para leer y guardar los promedios
guardar_promedios(edificio, locacion, num_promedios)
print(f"Promedios guardados en {nombre_archivo}")

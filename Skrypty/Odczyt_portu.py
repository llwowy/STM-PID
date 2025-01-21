import serial
import matplotlib.pyplot as plt
from time import sleep, strftime
import keyboard
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker

plt.ion()

# Konfiguracja portu szeregowego
hSerial = serial.Serial('COM3', 115200, timeout=1, parity=serial.PARITY_NONE)

# Wysłanie komend do mikroprocesora
hSerial.write(b'print_on;')
sleep(0.5)
set_point = 40
hSerial.write(b'set_point=38;')
sleep(0.5)
hSerial.write(b'freq=1;')
sleep(0.5)
hSerial.write(b'select_controller=1;')
sleep(0.5)

# Tworzenie pliku do zapisywania danych
timestr = strftime("%Y%m%d-%H%M%S")
hFile = open(f"data_temperature_{timestr}.txt", "a")

# Inicjalizacja danych do wykresu
temperature_samples = []
set_temperature_samples = []
encoder_samples = []
t = []
t_value = 0

# Resetowanie bufora wejściowego
hSerial.reset_input_buffer()
hSerial.flush()

while True:
    text = hSerial.readline().decode('utf-8').strip()
    try:
        # Oczekiwany format: "Temperatura: X.XX \t Set temp: X.XX \t Encoder: X"
        if text.startswith("Temperatura:"):
            parts = text.split('\t')
            temperature = float(parts[0].split(':')[1].strip())
            set_temp = float(parts[1].split(':')[1].strip())


            # Dodanie danych do list
            temperature_samples.append(temperature)
            set_temperature_samples.append(set_temp)

            t.append(t_value)
            t_value += 1

            # Zapis danych do pliku
            hFile.write(f"{temperature},{set_temp}\n")

            # Rysowanie wykresu
            plt.clf()
            plt.plot(t, temperature_samples, '.', label="Temperature", markersize=5)
            plt.plot(t, set_temperature_samples, '-', label="Set Temperature", linewidth=1)
            plt.title(f"Temperature Logger")
            plt.xlabel("Time (s)")
            plt.ylabel("Temperature (°C)")
            #plt.ylim(15, 60)
            plt.grid()
            plt.legend()
            plt.show()
            plt.pause(0.1)



    except (ValueError, IndexError):
        print(f"Invalid data: {text}")

    # Sprawdzenie, czy klawisz "q" został naciśnięty
    if keyboard.is_pressed("q"):
        print("Exiting...")
        break
    if keyboard.is_pressed("c"):
        plt.clf()


# Zamknięcie portu szeregowego i pliku
hSerial.close()
hFile.close()

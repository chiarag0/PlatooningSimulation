import csv
import math


def generate_sensor_positions(vehicles):
    # Trova la posizione minima lungo l'asse x tra tutti i veicoli
    min_x_pos = vehicles[-1].states[0].position

    # Calcola la distanza totale percorsa dal convoglio
    tot_dist_traveled = vehicles[0].states[-1].position - min_x_pos

    # Calcola il numero di sensori adeguato
    num_sensors = math.ceil(tot_dist_traveled / 100)

    # Calcola l'incremento per la posizione x di ogni sensore
    x_inc = tot_dist_traveled / num_sensors

    # Inizializza la lista di posizioni dei sensori
    sensor_positions = []

    # Genera le posizioni dei sensori
    for i in range(num_sensors):
        x = min_x_pos + i * x_inc
        y = 0
        z = 2.5
        x_rotation = 0
        y_rotation = 0
        z_rotation = 0
        sensor_positions.append((x, y, z, x_rotation, y_rotation, z_rotation, "None"))

    return sensor_positions


def write_sensor_positions_to_csv(sensor_positions, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["x", "y", "z", "x_rotation", "y_rotation", "z_rotation", "None"])
        csv_writer.writerows(sensor_positions)




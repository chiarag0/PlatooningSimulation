import numpy as np

from sensor_positions_generator import generate_sensor_positions, write_sensor_positions_to_csv
from trajectory_data_collector import generate_trajectory_data, write_csv_file

from Controller import Controller
from ControllerState import ControllerState
from Vehicle import Vehicle, MAX_ACCELERATION, MIN_ACCELERATION, MAX_VELOCITY
from VehicleState import VehicleState
import random
import matplotlib.pyplot as plt


def main():
    num_vehicles = 5
    init(num_vehicles)


def init(num_vehicles):
    tau = 0.1  # costante temporale che rappresenta le driveline dynamics
    T = 0.1  # costante temporale che rappresenta il tempo di campionamento
    kp = 0.2  # = 0.2 costante nella legge di controllo di ksi
    kd = 0.7  # = 0.7 ""
    h = 0.7  # time headway

    num_steps = 500
    vehicles = []
    controllers = []

    vehicle_types = generate_vehicle_types(num_vehicles)

    vo_mode = "zero"  # zero, random, equal
    initial_velocities = generate_initial_velocities(num_vehicles, vo_mode)

    input_array = generate_input(num_steps)
    print(input_array)
    plot_input(input_array)

    for i in range(num_vehicles):
        if i == 0:
            controller_states = [ControllerState(input=input_value) for input_value in input_array]
        else:
            controller_states = [ControllerState() for _ in range(num_steps)]  # array di stati per ogni controllore

        controllers.append(Controller(controller_states))

        do = 50
        r = 5
        if i == 0:
            if vehicle_types[i] == "car":
                pos_zero = -4  # lunghezza macchina in metri
            elif vehicle_types[i] == "bus":
                pos_zero = -10  # lunghezza bus in metri
            vehicle_states = [VehicleState(0, initial_velocities[i], 0, pos_zero)]
        else:
            if vehicle_types[i] == "car":
                pos_zero = pos_zero - do - 4
            elif vehicle_types[i] == "bus":
                pos_zero = pos_zero - do - 10
            vehicle_states = [VehicleState(do, initial_velocities[i], 0, pos_zero)]

        vehicles.append(Vehicle(vehicle_types[i], vehicle_states, controllers[i], False))
        # print("controller numero ", i, " : ", controllers[i].states)
        # print("veicolo numero ", i, " : ", vehicles[i].states)

    vehicles[0].first = True

    for k in range(1, num_steps):  # il primo stato (k=0) è già stato inizializzato
        # print("CAMPIONAMENTO NUMERO ", k, " : ")
        for i in range(num_vehicles):
            if i != 0:
                vehicles[i].controller.states[k - 1].error = vehicles[i].get_error(h, k, r)
            vehicles[i].controller.update_state(controllers[i - 1], T, kp, kd, h, k, i)
            vehicles[i].update_state(vehicles[i - 1], T, tau, k)

            # print("Veicolo num", i, " : ")
            # vehicles[i].controller.print_state(k)
            # vehicles[i].print_state()
            # print("\n")
        # print("--------------------\n")

    # print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

    for j in range(num_vehicles):  # CICLO DI STAMPE
        print("\n")
        print("Veicolo num", j, " ---------")
        for k in range(num_steps):
            # for k in range(10):
            if k < 10 or k % 100 == 0:
                # if k % 10 == 0:
                print("STEP NUM ", k)
                print("Input: ", vehicles[j].controller.states[k].input, " ksi: ", vehicles[j].controller.states[k].ksi,
                      " error: ", vehicles[j].controller.states[k].error)
                print("distance: ", vehicles[j].states[k].distance, ", velocity: ", vehicles[j].states[k].velocity,
                      ", acceleration: ", vehicles[j].states[k].acceleration, ", position: ",
                      vehicles[j].states[k].position)

    print("--------------------\n")

    plot_vehicle_positions(vehicles)
    plot_vehicle_distances(vehicles)

    trajectory_data = generate_trajectory_data(vehicles, num_steps)
    write_csv_file(trajectory_data, "trajectory_data.csv")
    sensor_positions = generate_sensor_positions(vehicles)
    write_sensor_positions_to_csv(sensor_positions, "sensor_positions.csv")


def generate_vehicle_types(
        num_vehicles):  # generatore di tipi di veicoli con il triplo di probabilità di macchine rispetto a bus
    car_probability = 3
    bus_probability = 1

    # calcolo delle probabilità relative
    total_probability = car_probability + bus_probability
    car_weight = car_probability / total_probability
    bus_weight = bus_probability / total_probability

    # generazione dell'array di tipi di veicolo
    vehicle_types = random.choices(["car", "bus"], weights=[car_weight, bus_weight], k=num_vehicles)

    print(vehicle_types)

    return vehicle_types


def plot_input(input_array):
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(input_array)), input_array, marker='o', linestyle='-')
    plt.title('Acceleration Profile')
    plt.xlabel('Time Steps')
    plt.ylabel('Acceleration')
    plt.grid(True)
    plt.show()


# visualizzazione continua
def plot_vehicle_positions(vehicles):
    time_steps = len(vehicles[0].states)
    num_vehicles = len(vehicles)

    for i in range(num_vehicles):
        positions = [vehicles[i].states[t].position for t in range(time_steps)]
        plt.plot(range(time_steps), positions, label=f"Vehicle {i}")

    plt.xlabel("Time in ds")
    plt.ylabel("Position in m")
    plt.legend()
    plt.show()


def plot_vehicle_distances(vehicles):
    time_steps = len(vehicles[0].states)
    num_vehicles = len(vehicles)

    for i in range(num_vehicles):
        distances = [vehicles[i].states[t].distance for t in range(time_steps)]
        plt.plot(range(time_steps), distances, label=f"Vehicle {i}")

    plt.xlabel("Time in ds")
    plt.ylabel("Distance in m")
    plt.legend()
    plt.show()



def generate_input(num_steps):
    num_waves = 5  # numero di onde quadre
    wave_length = num_steps // num_waves

    # Crea un array con valori casuali compresi tra -2 e 2
    input_array = np.random.uniform(-MIN_ACCELERATION, MAX_ACCELERATION, num_steps)

    # Genera le onde quadre
    zero_index = np.random.randint(0, num_waves) * wave_length
    for i in range(0, num_steps, wave_length):
        # Sceglie casualmente l'altezza dell'onda quadra
        if i == zero_index:
            height = -2
        else:
            if i == 0:  # Controllo per il primo intervallo
                height = np.random.uniform(0, MAX_ACCELERATION)  # Altezza non negativa
            else:
                height = np.random.uniform(MIN_ACCELERATION, MAX_ACCELERATION)
        # Assegna l'altezza ad ogni elemento dell'onda quadra
        input_array[i:i + wave_length] = height

    return input_array


# def plot_velocity(vehicles):
#     time_steps = len(vehicles[0].states)  # Assuming all vehicles have the same number of states
#     num_vehicles = len(vehicles)
#
#     plt.figure(figsize=(10, 6))
#
#     for i in range(num_vehicles):
#         velocities = [vehicles[i].states[t].velocity for t in range(time_steps)]
#         plt.plot(range(time_steps), velocities, label=f"Vehicle {i}")
#
#     plt.xlabel('Time Steps')
#     plt.ylabel('Velocity')
#     plt.title('Velocity of Vehicles')
#     plt.legend()
#     plt.grid(True)
#     plt.show()


def generate_initial_velocities(num_vehicles, mode):
    if mode == "zero":
        initial_velocities = [0] * num_vehicles
    elif mode == "random":
        initial_velocities = [random.uniform(0, MAX_VELOCITY) for _ in range(num_vehicles)]
    elif mode == "equal":
        constant_velocity = 16.67
        initial_velocities = [constant_velocity] * num_vehicles
    else:
        raise ValueError("Invalid mode. Please choose from 'zero', 'random', or 'equal'.")

    print(initial_velocities)
    return initial_velocities


if __name__ == "__main__":
    main()

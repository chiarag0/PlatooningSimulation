from Controller import Controller
from ControllerState import ControllerState
from Vehicle import Vehicle
from VehicleState import VehicleState
import random


def main():
    num_vehicles = 5
    vo = 16.67  # 60 km/h = 16.67 m/s
    init(num_vehicles, vo)


def init(num_vehicles, vo):
    tau = 0.1  # costante temporale che rappresenta le driveline dynamics
    T = 0.1  # costante temporale che rappresenta il tempo di campionamento
    kp = 0.2  # costante nella legge di controllo di ksi
    kd = 0.7  # ""
    h = 0.5  # time headway

    vehicles = []
    controllers = []

    vehicle_types = generate_vehicle_types(num_vehicles)

    for i in range(num_vehicles):
        controller_states = [ControllerState(0, 0, 0)]  # Lista di stati per ogni controllore
        controllers.append(Controller(controller_states))

        do = (vo * 3.6 / 10) ** 2  # iniziamo con una distanza di sicurezza tra i veicoli
        if i == 0:
            if vehicle_types[i] == "car":
                pos_zero = -4  # lunghezza macchina in metri
            elif vehicle_types[i] == "bus":
                pos_zero = -10  # lunghezza bus in metri
            vehicle_states = [VehicleState(0, vo, 0, pos_zero)]
        else:
            if vehicle_types[i] == "car":
                pos_zero = pos_zero - do - 4
            elif vehicle_types[i] == "bus":
                pos_zero = pos_zero - do - 10
            vehicle_states = [VehicleState(do, vo, 0, pos_zero)]

        vehicles.append(Vehicle("car", vehicle_states, controllers[i], False))
        print("controller numero ", i, " : ", controllers[i].states)
        print("veicolo numero ", i, " : ", vehicles[i].states)
    vehicles[0].first = True

    for k in range(0, 1000):  # esempio numero di campionamenti
        print("CAMPIONAMENTO NUMERO ", k, " : ")
        for i in range(num_vehicles):
            if i != 0:
                vehicles[i].controller.states[-1].error = vehicles[i].get_error(h)
            vehicles[i].controller.update_state(controllers[i - 1], T, kp, kd, h)
            vehicles[i].update_state(vehicles[i - 1], T, tau)

            #print("Veicolo num", i, " : ")
            #vehicles[i].controller.print_state()
            #vehicles[i].print_state()
            #print("\n")
        #print("--------------------\n")

    print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")

    for j in range(num_vehicles):  # CICLO DI STAMPE
        print("\n")
        print("Veicolo num", j, " ---------")
        for k in range(1000):
            if k % 100 == 0:
                print("STEP NUM ", k)
                print("Input: ", vehicles[j].controller.states[k].input, " ksi: ", vehicles[j].controller.states[k].ksi," error: ", vehicles[j].controller.states[k].error)
                print("distance: ", vehicles[j].states[k].distance, ", velocity: ", vehicles[j].states[k].velocity,
                    ", acceleration: ", vehicles[j].states[k].acceleration, ", position: ",
                    vehicles[j].states[k].position)

    print("--------------------\n")


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


if __name__ == "__main__":
    main()

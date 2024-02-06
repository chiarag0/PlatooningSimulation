from Controller import Controller
from ControllerState import ControllerState
from Vehicle import Vehicle
from VehicleState import VehicleState


def main():
    num_vehicles = 5
    init(num_vehicles)


def init(num_vehicles):
    tau = 0.1  # costante temporale che rappresenta le driveline dynamics
    T = 0.1  # costante temporale che rappresenta il tempo di campionamento
    kp = 0.2  # costante nella legge di controllo di ksi
    kd = 0.7  # ""
    h = 0.7  # time headway

    vehicles = []
    controllers = []
    vehicle_states = [VehicleState(0, 16.67, 0) for _ in range(num_vehicles)]  # Vo = 60 km/h #TODO calcolare dist con posiziz e lunghezze
    controller_states = [ControllerState(0, 0) for _ in range(num_vehicles)]  # Lista di stati per ogni controllore

    for i in range(num_vehicles):
        controllers.append(Controller(controller_states[i]))
        vehicles.append(Vehicle("car", vehicle_states, controllers[i], False))
    vehicles[0].first = True


    # for k in range(0, 1000):  # esempio numero di campionamenti
    for i in range(num_vehicles):
        vehicles[i].controller.update_state(controllers[i-1], T, kp, kd, h)

        vehicles[i].update_state(vehicles[i - 1], T, tau)
        vehicles[i].print_state()


if __name__ == "__main__":
    main()

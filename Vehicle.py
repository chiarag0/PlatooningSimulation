from VehicleState import VehicleState

MAX_VELOCITY = 38.89  # m/s  = 140 km/h
MAX_ACCELERATION = 9.8  # m/s^2
MIN_ACCELERATION = -9.8


class Vehicle:
    def __init__(self, type, vehicle_states, controller, first):
        self.type = type
        self.states = vehicle_states
        self.controller = controller
        self.first = first

    def get_error(self, h, k,r):
        ref_dist = r + h * self.states[k - 1].velocity  # r è una costante = distanza min tra 2 veicoli, ad es 5 m
        error = self.states[k - 1].distance - ref_dist
        return error

    def update_state(self, prec, T, tau, k):  # prec è il veicolo precedente
        new_state = VehicleState(0, 0, 0, 0)
        if self.first:
            new_state.distance = 0
            new_state.position = self.states[-1].position + T * self.states[-1].velocity
        elif not self.first:
            new_state.distance = self.states[-1].distance + T * (prec.states[-1].velocity - self.states[-1].velocity)
            new_state.position = prec.states[-1].position - new_state.distance - self.length()

        new_velocity = self.states[-1].velocity + T * self.states[-1].acceleration

        if new_velocity < 0:
            new_state.velocity = 0
        elif new_velocity >= MAX_VELOCITY:
            new_state.velocity = MAX_VELOCITY
        elif new_velocity < 0:
            new_state.velocity = 0
        else:
            new_state.velocity = new_velocity

        new_acceleration = self.states[-1].acceleration + T / tau * (
                self.controller.states[k - 1].input - self.states[-1].acceleration)
        if new_acceleration > MAX_ACCELERATION:
            new_state.acceleration = MAX_ACCELERATION
        elif new_acceleration < MIN_ACCELERATION:
            new_state.acceleration = MIN_ACCELERATION
        else:
            new_state.acceleration = new_acceleration

        self.states.append(new_state)

    def print_state(self):
        print("distance: ", self.states[-1].distance, ", velocity: ", self.states[-1].velocity, ", acceleration: ",
              self.states[-1].acceleration, ", position: ", self.states[-1].position)

    def length(self):
        if self.type == "car":
            return 4  # metri
        elif self.type == "bus":
            return 10  # metri



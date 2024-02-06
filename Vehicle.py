from VehicleState import VehicleState


class Vehicle:
    def __init__(self, type, vehicle_states, controller, first):
        self.type = type
        self.states = vehicle_states
        self.controller = controller
        self.first = first
  
    def update_state(self, prec, T, tau):  # prec è il veicolo precedente
        new_state = VehicleState(0, 0, 0)
        if not self.first:
            new_state.distance = self.states[-1].distance + T * (prec.states[-1].velocity - self.states[-1].velocity)
        print(T)
        new_state.velocity = self.states[-1].velocity + T * self.states[-1].acceleration
        new_state.acceleration = self.states[-1].acceleration + T / tau * (self.controller.states[-1].input - self.states[-1].acceleration)
        self.states.append(new_state)

    def print_state(self):
        print(self.states[-1].distance, self.states[-2].distance)
from ControllerState import ControllerState


class Controller:
    def __init__(self, controller_states=[]):
        self.states = controller_states

    def update_state(self, prec, T, kp, kd, h):  # GLI 1 SONO GLI e; prec è il veicolo precedente

        new_state = ControllerState()
        new_state.ksi = kp * 1 + kd * 1 / T + prec.states[-1].input
        new_state.input = self.states[-1].input + T / h * (self.states[-1].ksi - self.states[-1].input)

        self.states.append(new_state)

    def print_state(self):
        print("input: ", self.states[-1].input, "ksi: ", self.states[-1].ksi)

from ControllerState import ControllerState


class Controller:
    def __init__(self, controller_states=[]):
        self.states = controller_states

    def update_state(self, prec, T, kp, kd, h):  # prec è il veicolo precedente
        if len(self.states) == 1:
            self.states[-1].ksi = kp * self.states[-1].error + kd * self.states[-1].error / T + prec.states[-1].input
        else:
            self.states[-1].ksi = kp * self.states[-1].error + kd * (self.states[-1].error - self.states[-2].error) / T + prec.states[-1].input

        new_state = ControllerState()
        new_state.input = self.states[-1].input + T / h * (self.states[-1].ksi - self.states[-1].input)

        self.states.append(new_state)

    def print_state(self):
        print("input: ", self.states[-1].input, "ksi: ", self.states[-1].ksi)
        print("error: ", self.states[-1].error)

from ControllerState import ControllerState


class Controller:
    def __init__(self, controller_states=[]):
        self.states = controller_states

    def update_state(self, prec, T, kp, kd, h, k, i):  # prec è il veicolo precedente
        if k == 1:
            self.states[k-1].ksi = kp * self.states[k-1].error + kd * self.states[k-1].error / T + prec.states[k-1].input
        else:
            self.states[k-1].ksi = kp * self.states[k-1].error + kd * (
                        self.states[k-1].error - self.states[k-2].error) / T + prec.states[k-1].input
        if i != 0:
            self.states[k].input = self.states[k-1].input + T / h * (self.states[k-1].ksi - self.states[k-1].input)


    def print_state(self,k):
        print("input: ", self.states[k].input, "ksi: ", self.states[k].ksi)
        print("error: ", self.states[k].error)

from Module_Base import Module

class Thruster_Power(Module):
    def __init__ (self, CG, ThrusterFL):
        self.CG = CG
        self.ThrusterFL = ThrusterFL

    def run(self):
        print("running")

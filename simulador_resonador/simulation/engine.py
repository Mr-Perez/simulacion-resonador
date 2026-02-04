class SimulationEngine:
    def __init__(self):
        self.patients = ["Paciente 1", "Paciente 2", "Paciente 3"]
        self.stages = [
            "Sala de Espera",
            "Vestidor",
            "Resonador",
            "Salida"
        ]

        self.current_patient = 0
        self.current_stage = 0
        self.time = 0

        self.study_type = "RM Cerebro"

    def advance(self):
        self.time += self.stage_duration()

        self.current_stage += 1
        if self.current_stage >= len(self.stages):
            self.current_stage = 0
            self.current_patient += 1

            if self.current_patient >= len(self.patients):
                self.current_patient = 0
                self.time = 0

    def stage_duration(self):
        durations = {
            "Sala de Espera": 5,
            "Vestidor": 10,
            "Resonador": 25,
            "Salida": 3
        }
        return durations[self.stages[self.current_stage]]

    def get_state(self):
        return {
            "patient": self.patients[self.current_patient],
            "stage": self.stages[self.current_stage],
            "study": self.study_type,
            "time": self.time
        }


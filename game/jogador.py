class Jogador:

    def __init__(self):

        self.pontos = 60
        self.turnos = 0
        self.combo = 0
        self.tentativas_restantes = 180
        self.multiplicador = (
            1 + self.combo * 0.4
        )
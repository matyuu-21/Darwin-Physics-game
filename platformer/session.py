import settings

class Session:
    def __init__(self):
        self.score = 0
        self.coins = 0

        self.double_score_timer = 0
        self.elapsed_time = 0

    def add_score(self, points):

        if self.double_score_timer > 0:
            points *= 2

        self.score += points

    def add_coin(self, amount=1):
        self.coins += amount
        self.add_score(amount * settings.coin_score)

    def update(self, dt):
        self.double_score_timer = max(
            0, self.double_score_timer - dt
        )
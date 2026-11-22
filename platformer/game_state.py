class GameState:
    def __init__(self):
        self.current_state = "playing"

    def change_state(self, new_state):
        self.current_state = new_state

    def is_playing(self):
        return self.current_state == "playing"

    def is_game_over(self):
        return self.current_state == "game_over"

    def is_paused(self):
        return self.current_state == "paused"
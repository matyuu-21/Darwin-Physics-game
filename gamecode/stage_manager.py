class StageManager: #tracks the stage and scores for the progression update im gonna do
    def __init__(self):
        self.stages = [
            {
                "name": "Stage 1",
                "boss": "boss_1",
                "boss_score": 2000,
                "background": "assets/skybg.png",
                "boss_sprite": "assets/boss1.png"
            },
            {
                "name": "Stage_2",
                "boss": "boss_2",
                "boss_score": 6000,
                "background": "assets/skybg2.png",
                "boss_sprite": "assets/boss2.png"
            },
            {
                "name": "Stage_3",
                "boss": "boss_3",
                "boss_score": 10000, 
                "background": "assets/skybg2.png",
                "boss_sprite": "assets/boss3.png"
            }
        ]

        self.current_stage_index = 0
        self.boss_started = False
        self.game_completed = False

    def get_current_stage(self):
        return self.stages[self.current_stage_index]

    def check_boss_trigger(self, score):
        current_stage = self.get_current_stage()

        if score >= current_stage["boss_score"] and not self.boss_started: 
            self.boss_started = True
            return True

        return False

    def complete_boss(self):
        if self.current_stage_index >= len(self.stages) - 1:
            self.game_completed = True
            return "game_complete"

        self.current_stage_index += 1
        self.boss_started = False

        return "next_stage"

    def reset(self):
        self.current_stage_index = 0
        self.boss_started = False
        self.game_completed = False
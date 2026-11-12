class StageManager: #tracks the stage and scores for the progression update im gonna do
    def __init__(self):
        self.worlds = [
            {"name": "EARTH", "subtitle": "The School", "gravity_scale": 1, "available": True},
             {"name": "MOON",  "subtitle": "Lunar Station", "gravity_scale": 0.5, "available": False},
              {"name": "Jupiter", "subtitle": "Gas Giant", "gravity_scale": 1.4, "available": False}
        ]
        self.stages = [
            {
                "name": "Classroom 1",
                "world": "EARTH",
                "planet": "EARTH",
                "available": True,
                "gravity_scale": 1.0,
                "boss": "boss_1",
                "boss_score": 100, #2000 if done testing
                "background": "assets/skybg.png",
                "boss_sprite": "assets/boss1.png",
                "unlocked": True
                
            },
            {
                "name": "Classroom 2",
                "world": "EARTH",
                "planet": "EARTH",
                "available": True,
                "gravity_scale": 1.0,
                "boss": "boss_2",
                "boss_score": 200, #6000 if done testing
                "background": "assets/skybg2.png",
                "boss_sprite": "assets/boss2.png",
                "unlocked": False
            },
            {
                "name": "Classroom 3",
                "world": "EARTH",
                "planet": "EARTH",
                "available": True,
                "gravity_scale": 1.0,
                "boss": "boss_3",
                "boss_score": 300, #10000 if done testing
                "background": "assets/skybg2.png",
                "boss_sprite": "assets/boss3.png",
                "unlocked": False
            }
            
        ]

        self.current_stage_index = 0
        self.boss_started = False
        self.game_completed = False

    def get_current_stage(self):
        return self.stages[self.current_stage_index]

    def get_worlds(self):
        return self.worlds

    def get_world_stage(self, world_name):
        stages = [
            (index, stage)
            for index, stage in enumerate(self.stages)
            if stage["world"] == world_name
        ]

        if stages:
            return stages

        world = next(world for world in self.worlds if world["name"] == world_name)
        return [
            (None, {
                "name": f"{world_name.title()} Stage {stage_number}",
                "planet": world_name,
                "gravity_scale": world["gravity_scale"],
                "available": False
            })
            for stage_number in range(1, 4)
        ]

    def select_stage(self, stage_index):
        if 0 <= stage_index < len(self.stages):
            self.current_stage_index = stage_index
            self.boss_started = False
            self.game_completed = False
        return False

    def get_stage_start_score(self):
        if self.current_stage_index == 0:
            return 0
        return self.stages[self.current_stage_index - 1]["boss_score"]
    
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

        next_stage_index = self.current_stage_index + 1
        self.stages[next_stage_index]["unlocked"] = True

        self.current_stage_index = next_stage_index
        self.boss_started = False

        return "next_stage"

    def reset(self):
        self.current_stage_index = 0
        self.boss_started = False
        self.game_completed = False
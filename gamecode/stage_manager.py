import random

class StageManager:
    
    def __init__(self):
        
        self.worlds = [
            {
                "name": "Earth",
                "subtitle": "The School",
                "gravity_scale": 1,
                "available": True,
            },
            {
                "name": "Moon",
                "subtitle": "Lunar Station",
                "gravity_scale": 0.5,
                "available": False,
            },
            {
                "name": "Jupiter",
                "subtitle": "Gas Giant",
                "gravity_scale": 1.5,
                "available": False,
            },
        ]

        self.stages = [
            {
                "name": "Classrooms",
                "world": "Earth",
                "planet": "Earth",
                "available": True,
                "unlocked": True,
                "gravity_scale": 1,
                "background": "assets/skybg.png",
                "start_score": 0,
                "bosses": [
                    {
                        "boss": "boss_1",
                        "boss_sprite": "assets/boss1.png",
                        "background": "assets/classroom1.png",
                    },
                    {
                        "boss": "boss_2",
                        "boss_sprite": "assets/boss2.png",
                        "background": "assets/classroom2.png",
                    },
                    {
                        "boss": "boss_3",
                        "boss_sprite": "assets/boss3.png",
                        "background": "assets/classroom3.png",
                    },
                ],
            },
            {
                "name": "City",
                "world": "Earth",
                "planet": "Earth",
                "available": False,
                "unlocked": False,
                "gravity_scale": 1,
                "background": "assets/skybg2.png",
                "start_score": 1000,
                "bosses": [],
            },
            {
                "name": "Space Station",
                "world": "Earth",
                "planet": "Earth",
                "available": False,
                "unlocked": False,
                "gravity_scale": 1,
                "background": "assets/skybg3.png",
                "start_score": 2000,  # change maybe soon w others
                "bosses": [],
            },
        ]

        self.reset()

    def get_current_stage(self):
        return self.stages[self.current_stage_index]

    def get_world(self):
        return self.worlds

    def get_world_stage(self, world_name):

        stages = [
            (index, stage)
            for index, stage in enumerate(self.stages)
            if stage["world"].lower() == world_name.lower()
        ]

        if stages:
            return stages

        world = next(
            world for world in self.worlds
            if world["name"].lower() == world_name.lower()
        )

        return [
            (None, {
                "name": f"{world_name.title()} Stage {number}",
                "planet": world_name,
                "gravity_scale": world["gravity_scale"],
                "available": False,
                "unlocked": False,
            })
            for number in range(1, 4)
        ]

    def select_stage(self, stage_index):

        if 0 <= stage_index < len(self.stages):

            if self.stages[stage_index]["unlocked"]:

                self.current_stage_index = stage_index
                self.boss_started = False
                self.game_completed = False
                self.defeated_bosses = []
                self.spawn_check_timer = 0
                self.boss_cooldown = 0

                return True

        return False

    def get_stage_start_score(self):
        return self.get_current_stage().get("start_score", 0)

    def get_available_bosses(self):
        current_stage = self.get_current_stage()
        return [
            boss_data
            for boss_data in current_stage["bosses"]
            if boss_data["boss"] not in self.defeated_bosses
        ]

    def check_boss_trigger(self, score, dt):

        if self.boss_started or self.game_completed:
            return False

        if self.boss_cooldown > 0:
            self.boss_cooldown -= dt
            return False
        if not self.get_available_bosses():
            return False

        if score < 100:
            return False

        self.spawn_check_timer += dt

        if self.spawn_check_timer < self.spawn_check_interval:
            return False

        self.spawn_check_timer = 0

        if score < 200:
            chance = 0.05
        elif score < 300:
            chance = 0.15
        elif score < 400:
            chance = 0.30
        else:
            chance = 0.45

        if random.random() < chance:
            self.boss_started = True
            return True

        return False

    def choose_boss(self, score):

        available_bosses = self.get_available_bosses()

        if not available_bosses:
            return None

        if score < 200:
            weights = {
                "boss_1": 60,
                "boss_2": 30,
                "boss_3": 10,
            }
        elif score < 400:
            weights = {
                "boss_1": 35,
                "boss_2": 35,
                "boss_3": 30,
            }
        else:
            weights = {
                "boss_1": 20,
                "boss_2": 35,
                "boss_3": 45,
            }

        available_weights = [
            weights[boss_data["boss"]]
            for boss_data in available_bosses
        ]

        return random.choices(
            available_bosses,
            weights=available_weights,
            k=1,
        )[0]

    def complete_boss(self, boss_type):

        if boss_type and boss_type not in self.defeated_bosses:
            self.defeated_bosses.append(boss_type)

        self.boss_started = False
        self.boss_cooldown = 10

        if self.get_available_bosses():
            return "boss_defeated"

        next_stage_index = self.current_stage_index + 1

        if next_stage_index < len(self.stages):

            self.stages[next_stage_index]["unlocked"] = True
            self.stages[next_stage_index]["available"] = True

            self.current_stage_index = next_stage_index
            self.spawn_check_timer = 0

            return "next_stage"

        self.game_completed = True
        return "game_complete"

    def reset(self):

        self.current_stage_index = 0
        self.defeated_bosses = []
        self.boss_started = False
        self.game_completed = False

        self.spawn_check_timer = 0
        self.spawn_check_interval = 5
        self.boss_cooldown = 0
    
    
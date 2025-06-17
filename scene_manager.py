import pygame
from UI.character_select import CharacterSelectScene
from UI.start_scene import StartScene
from UI.intro_scene import IntroScene
from UI.story_scene import StoryScene
from UI.event_scene import EventScene
from UI.set_scene import SetScene
from character import Bubu, Yier, Mitao, Huihui
from UI.components.first_scene import FirstScene
from UI.main_scene import MainScene
from UI.rank_scene import RankScene
from UI.diary_scene import DiaryScene
from UI.sound_control_scene import SoundControlScene
from UI.end_scene import EndScene
from UI.feedback_scene import FeedbackScene

# scene_manager.py
class SceneManager:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.player = None
        self.scene_map = {
            "FIRST": self.first_scene,
            "START": self.start_scene,
            "CHARACTER_SELECT": self.character_select,
            "MAIN": self.main_game_loop,
            "STORY": self.story_and_event,
            "SETTING": self.setting_scene,
            "SOUND_CONTROL":  self.sound_control_scene,
            "SHOW_INTRO": self.intro_scene,
            "RANK": self.rank_scene,
            "END": self.end_scene,
            "FEEDBACK": self.feedback_scene,
            "RESTART": self.restart_game,
            "QUIT": self.quit_game,
            "DIARY": self.diary_scene
        }

    def run(self):
        print("SceneManager 開始跑了")
        next_scene = "FIRST"
        while self.running and next_scene:
            handler = self.scene_map.get(next_scene)
            if handler:
                next_scene = handler()
            else:
                print(f"未知場景：{next_scene}")
                self.running = False

    # --- 各個場景 ---
    def first_scene(self):
        scene = FirstScene(self.screen)
        result = scene.run()
        return {
            "START": "START",
            "QUIT": "QUIT"
        }.get(result, "FIRST")

    def start_scene(self):
        scene = StartScene(self.screen)
        result = scene.run()
        return {
            "START": "CHARACTER_SELECT",
            "SHOW_INTRO": "SHOW_INTRO",
            "SOUND_CONTROL": "SOUND_CONTROL",
            "QUIT": "QUIT"
        }.get(result, "START")
    
    def intro_scene(self):
        scene = IntroScene(self.screen)
        scene.run()
        return "START"

    def character_select(self):
        scene = CharacterSelectScene(self.screen)
        selected = scene.run()
        if selected == "布布 Bubu":
            self.player = Bubu()
        elif selected == "一二 Yier":
            self.player = Yier()
        elif selected == "蜜桃 Mitao":
            self.player = Mitao()
        elif selected == "灰灰 Huihui":
            self.player = Huihui()
        else:
            return "START"
        return "MAIN"
    
    def sound_control_scene(self):
        SoundControlScene(self.screen).run()
        return "START" if self.player is None else "SETTING"

    def main_game_loop(self):
        if self.player.week_number >= 16:
            return "END"

        scene = MainScene(self.screen, self.player)
        result = scene.run()

        return {
            "Next Story": "STORY",
            "SETTING": "SETTING",
            "Quit": "QUIT",
            "DIARY": "DIARY",
        }.get(result, "MAIN")

    def story_and_event(self):
        self.player.week_number += 1
        self.player.week_data = self.player.all_weeks_data[f"week_{self.player.week_number}"]
        StoryScene(self.screen, self.player).run()
        EventScene(self.screen, self.player).run()
        return "MAIN"

    def setting_scene(self):
        set_scene = SetScene(self.screen)
        result = set_scene.run()
        return {
            "BACK": "MAIN",
            "RESTART": "RESTART",
            "SOuND_CONTROL": "SOUND_CONTROL",
            "QUIT": "QUIT"
        }.get(result, "MAIN")
    
    def diary_scene(self):
        print("進入日記場景")
        scene = DiaryScene(self.screen, self.player)
        result = scene.run()
        return "MAIN" if result == "BACK" else result

    def end_scene(self):
        self.player.calculate_GPA()
        scene = EndScene(self.screen, self.player)
        result = scene.run()
        return {
            "SHOW_RANK": "RANK",
            "RESTART": "RESTART",
            "FEEDBACK": "FEEDBACK",
            "Exit": "QUIT"
        }.get(result, "END")


    def rank_scene(self):
        scene = RankScene(self.screen, self.player)
        scene.run()
        return "END"
    
    def feedback_scene(self):
        FeedbackScene(self.screen, self.player).run()
        return "END"

    def restart_game(self):
        self.player = None
        return "START"

    def quit_game(self):
        self.running = False
        return  "QUIT"

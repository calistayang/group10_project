import pygame
import math
import random
from UI.components.base_scene import BaseScene


'''Example usage:
    
    options1 = ["超可愛學姐\n帥潮學長", "看起來是系邊\n有點宅宅的學長", "超搞笑的系核\n第一次見面\n就表演倒立走路", "卷哥卷姐", "被放生了"]

    wheel = LuckyWheelScene(screen, options1)
    result = wheel.run()
    print(f"轉盤結果: {result}")

'''

class LuckyWheelScene(BaseScene):
    def __init__(self, screen, options):
        super().__init__(screen)
        self.options = options
        self.wheel_radius = 300
        self.center = (self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)
        self.angle = 0
        self.spin_speed = 0
        self.is_spinning = False
        self.font = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 48)
        
        

        
        self.font_desc = pygame.font.Font("resource/font/JasonHandwriting3-Regular.ttf", 28)
        self.background = pygame.image.load("resource/image/background_intro.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, self.screen.get_size())
        self.background.set_alpha(100)

        self.button_radius = 80
        self.result_text = None
        self.glow_phase = 0

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dx = event.pos[0] - self.center[0]
            dy = event.pos[1] - self.center[1]
            if dx * dx + dy * dy <= self.button_radius * self.button_radius and not self.is_spinning:
                self.audio.play_sound("resource/music/sound_effect/menu_hover.mp3")
                self.start_spin()

    def start_spin(self):
        self.is_spinning = True
        self.spin_speed = random.uniform(25, 30)
        self.target_angle = None
        self.result_text = None
        self.audio.play_sound("resource/music/sound_effect/luckywheel.mp3")

    def update(self):
        if self.is_spinning:
            self.angle += self.spin_speed
            
            self.spin_speed *= 0.98
            if self.spin_speed < 0.5:
                self.spin_speed = 0
                self.is_spinning = False
                self.calculate_result()


    def calculate_result(self):
        n = len(self.options)
        degrees_per_segment = 360 / n
        corrected_angle = (360 - self.angle % 360) % 360
        index = int(corrected_angle // degrees_per_segment) % n
        self.result_text = self.options[index-1]  # Adjust for zero-based index

    def draw(self):
        
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))

        n = len(self.options)
        degrees_per_segment = 360 / n

        # Glow effect
        glow_color = (255, 255, 100, int(128 + 127 * math.sin(self.glow_phase)))
        glow_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, glow_color, self.center, self.wheel_radius + 10)
        self.screen.blit(glow_surface, (0, 0))

        for i in range(n):
            start_angle_deg = self.angle + i * degrees_per_segment
            end_angle_deg = self.angle + (i + 1) * degrees_per_segment

            start_angle = math.radians(start_angle_deg)
            end_angle = math.radians(end_angle_deg)
            mid_angle = math.radians((start_angle_deg + end_angle_deg) / 2)

            color = (200 + i * 20 % 55, 100 + i * 30 % 155, 150 + i * 40 % 105)

            # Use filled arc via polygon method
            points = [self.center]
            for step in range(10):
                angle = start_angle + (end_angle - start_angle) * (step / 9)
                x = self.center[0] + self.wheel_radius * math.cos(angle)
                y = self.center[1] + self.wheel_radius * math.sin(angle)
                points.append((x, y))

            pygame.draw.polygon(self.screen, color, points)

            # Draw text
            tx = self.center[0] + (self.wheel_radius * 0.6) * math.cos(mid_angle)
            ty = self.center[1] + (self.wheel_radius * 0.6) * math.sin(mid_angle)
            text_surface = self.font_desc.render(self.options[i], True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(tx, ty))
            self.screen.blit(text_surface, text_rect)

        # Draw wheel outline
        pygame.draw.circle(self.screen, (0, 0, 0), self.center, self.wheel_radius, 4)

        # Draw center button as circle
        pygame.draw.circle(self.screen, (250, 100, 100), self.center, self.button_radius)
        button_text = self.font.render("抽獎", True, (255, 255, 255))
        text_rect = button_text.get_rect(center=self.center)
        self.screen.blit(button_text, text_rect)

        # Draw blinking pointer (triangle)
        pointer_alpha = 255  # 固定不閃爍
        pointer_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        pointer = [
            (self.center[0], self.center[1] - self.button_radius  - 30),
            (self.center[0] - 15, self.center[1] - self.button_radius +10),
            (self.center[0] + 15, self.center[1] - self.button_radius +10)
        ]
        pygame.draw.polygon(pointer_surface, (250, 100, 100, pointer_alpha), pointer)
        self.screen.blit(pointer_surface, (0, 0))


        if self.result_text:
            result_surface = self.font_desc.render(f"抽中：\n{self.result_text}", True, (0, 0, 0))
            self.screen.blit(result_surface, (950 , 600))
    
    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.flip()
            clock.tick(self.FPS)
            # 若已經有結果，停留一段時間後自動結束
            if self.result_text:
                pygame.time.wait(3000)
                self.running = False
        return self.result_text
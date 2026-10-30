import pygame

import pyengine.game_object
import pyengine.ui
import pyengine.camera

class Game(pyengine.game_object.GameObject):
    _main = None

    def __init__(self, window):
        if Game._main is not None:
            raise Exception("Game instance already exists. Only one instance is allowed.")
        Game._main = self

        self.window = window

        self.scene: pyengine.game_object.GameObject = None
        self.running = True
        self.target_fps = 60
        self.fps = self.target_fps
        self.delta_time = 00.1 / self.target_fps

        self.clock = pygame.time.Clock()

        self.camera = None
        self.camera = pyengine.camera.Camera()

        self.mouse_down = False
        self._was_mouse_down = False
        self.just_mouse_down = False
        self.just_mouse_up = False

        self.key_just_pressed = None
        self.key_just_released = None
        self.keys_pressed = {}

        self._debug_queue = []
        self._debug_open = False

        self._events = []
    
    def _update(self):
        self.clock.tick(self.target_fps)
        self.fps = self.clock.get_fps()
        self.delta_time = self.clock.get_time() * 0.001

        # Keypresses
        self.mouse_down = pygame.mouse.get_pressed(3)[0]
        self.just_mouse_down = not self._was_mouse_down and self.mouse_down
        self.just_mouse_up = not self.mouse_down and self._was_mouse_down

        self.keys_pressed = pygame.key.get_pressed()
        self.key_just_pressed = None
        self.key_just_released = None

        self._debug_queue.clear()
        
        self._events = pygame.event.get()
        for event in self._events:
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self.key_just_pressed = event.key
                if event.key == pygame.K_F3:
                    self._debug_open = not self._debug_open
            elif event.type == pygame.KEYUP:
                self.key_just_released = event.key
            
        self.update()
        self.camera.update()
        if self.scene is not None:
            self.scene.update()
        
        self._was_mouse_down = self.mouse_down

    def _render(self):
        self.window.fill((0, 0, 0))
        if self.scene is not None:
            self.scene.render()
        else:
            pyengine.ui.text("No scene loaded", (10, 10))
        self.render()

        if self._debug_open:
            r = pyengine.ui.text(f"{round(self.fps)}fps (target {self.target_fps})", (10, 10), size=20, background=(0, 0, 0))
            r = pyengine.ui.text(f"Delta: {round(self.delta_time, 3)}s", (10, r.bottom + 2), size=20, background=(0, 0, 0))
            r = pyengine.ui.text(f"Scene: {self.scene.__class__.__name__}" if self.scene else "No scene loaded", (10, r.bottom + 2), size=20, background=(0, 0, 0))
            r = pyengine.ui.text(f"Camera (position): {int(self.camera.position.x)},{int(self.camera.position.y)}", (10, r.bottom + 2), size=20, background=(0, 0, 0))
            r.bottom += 10
            for text in self._debug_queue:
                r = pyengine.ui.text(text, (10, r.bottom + 2), size=20, background=(0, 0, 0))
        
        pygame.display.update()
    
    def debug(self, *texts):
        texts = [str(text) for text in texts]
        self._debug_queue.extend(texts)
    
    def set_scene(self, scene_class, *args, **kwargs):
        self.scene = scene_class(*args, **kwargs)

    def run(self):
        while self.running:           
            self._update()
            self._render()

    def main() -> 'Game':
        return Game._main

    def get_events(self):
        return self._events
        
import pygame
import math
import pymunk
import pymunk.pygame_util

from pyengine.game_object import GameObject

from src.objects.skeleton import Bone
from src.util.creatures import create_human

PHYSICS_DT = 1/ 120


class MainScene(GameObject):
    def __init__(self):
        super().__init__()

        self.space: pymunk.Space = None

        self.physics_init()

        self.mouse_joint = None
        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    
    def physics_init(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.space.damping = 0.99
        self.space.sleep_time_threshold = 0.5

        # Floor
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(
            floor_body,
            (-10000, 700),
            (10000, 700),
            5
        )
        floor_shape.friction = 0.8
        self.space.add(floor_body, floor_shape)

        human = create_human(self.space)
        self.bones = human.get_skeleton()

    def update(self):
        for event in self.game.get_events():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                p = pymunk.pygame_util.from_pygame(pos, self.window)

                hit = self.space.point_query_nearest(p, 5, pymunk.ShapeFilter())
                if hit and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                    self.mouse_body.position = p
                    self.mouse_joint = pymunk.PivotJoint(self.mouse_body, hit.shape.body, (0,0), hit.shape.body.world_to_local(p))
                    self.mouse_joint.max_force = 50000
                    self.mouse_joint.error_bias = (1 - 0.15) ** 60
                    self.space.add(self.mouse_joint)

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.mouse_joint:
                    self.space.remove(self.mouse_joint)
                    self.mouse_joint = None
        
        if self.mouse_joint:
            pos = pygame.mouse.get_pos()
            self.mouse_body.position = pymunk.pygame_util.from_pygame(pos, self.window)


        for _ in range(2):
            self.space.step(PHYSICS_DT)

        self.game.debug("Bodies: " + str(len(self.space.bodies)))

    def render(self):
        draw_options = pymunk.pygame_util.DrawOptions(self.game.window)
        self.space.debug_draw(draw_options)

        # Draw muscles
        for bone in self.bones:
            for muscle in bone.muscles:
                self.draw_muscle(muscle)
    
    def draw_muscle(self, muscle: pymunk.DampedSpring):
        a = muscle.a.local_to_world(muscle.anchor_a)
        b = muscle.b.local_to_world(muscle.anchor_b)

        # Contraction ratio
        current_length = (b - a).length
        contraction_ratio = (muscle.rest_length - current_length) / muscle.rest_length

        # Draw
        thickness = 2 + 4 * abs(contraction_ratio)
        color = (
            int(255 * max(0, contraction_ratio)),
            0,
            int(255 * max(0, contraction_ratio))
        )
        self.camera.line(color, a, b, int(thickness))

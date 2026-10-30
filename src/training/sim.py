import torch
import pymunk
from src.util.creatures import create_human


class WalkingSim:
    max_steps = 500

    def __init__(self):
        self.space = pymunk.Space()
        self.space.gravity = (0, 900)
        self.space.iterations = 20
        self.space.damping = 0.99

        self.creature = None
        self.bones = []
        self.muscles = []

        self.floor_y = 700
        self._create_world()

        self._starting_position = self.bones[0].body.position
        self._starting_x = float(self.bones[0].body.position.x)
        self._previous_x = self._starting_x
        self._rest_lengths = [muscle.rest_length for muscle in self.muscles]
        self.steps = 0
    
    def reset(self):
        self.__init__()
        return self.get_observation()

    def step(self, action):
        self.steps += 1
        for muscle, rest_length, value in zip(
            self.muscles,
            self._rest_lengths,
            action,
        ):
            contraction = max(-1.0, min(1.0, float(value)))
            muscle.rest_length = rest_length * (1.0 - 0.25 * contraction)

        self.space.step(1 / 60)

        obs = self.get_observation()
        done = self.is_done()
        reward = self.compute_reward(action, done)

        return obs, reward, done

    def get_observation(self):
        obs = []
        for bone in self.bones:
            obs.append(bone.body.angle)
            obs.append(bone.body.angular_velocity / 20.0)
        root = self.bones[0]  # Root bone
        obs.append((root.body.position.y - self.floor_y) / 100.0)
        obs.append(root.body.velocity.y / 300.0)
        obs.append(root.body.velocity.x / 300.0)
        obs.append((self.bones[2].body.position.y - self.floor_y) / 100.0)
        obs.append((self.bones[4].body.position.y - self.floor_y) / 100.0)
        obs.append((self.bones[2].body.position.x - root.body.position.x) / 100.0)
        obs.append((self.bones[4].body.position.x - root.body.position.x) / 100.0)
        obs.append(self.bones[2].body.velocity.x / 300.0)
        obs.append(self.bones[4].body.velocity.x / 300.0)

        return torch.tensor(obs, dtype=torch.float32)

    def compute_reward(self, action, done):
        root = self.bones[0].body
        progress = (root.position.x - self._previous_x) / 20.0
        self._previous_x = float(root.position.x)

        posture_penalty = max(0.0, root.position.y - 620.0) / 100.0
        effort = 0.0005 * sum(float(value) ** 2 for value in action)

        reward = (
            progress
            + 0.002
            - 0.01 * posture_penalty
            - effort
        )

        if done:
            reward -= 2.0

        return float(reward)

    def foot_contact(self):
        left_foot_y = self.bones[2].body.position.y
        right_foot_y = self.bones[4].body.position.y
        return (
            left_foot_y >= self.floor_y - 30
            or right_foot_y >= self.floor_y - 30
        )

    def is_done(self):
        root = self.bones[0].body
        fallen = (
            root.position.y > self.floor_y - 20
            or abs(root.angle) > 2.5
        )
        return fallen or self.steps >= self.max_steps
    
    def _create_world(self):
        # Floor
        floor_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        floor_shape = pymunk.Segment(
            floor_body,
            (-10000, self.floor_y),
            (10000, self.floor_y),
            5
        )
        floor_shape.friction = 0.8
        floor_shape.elasticity = 0.0
        self.space.add(floor_body, floor_shape)

        self.creature = create_human(self.space, pos=(100, 560))
        self.bones = self.creature.get_skeleton()
        self.muscles = self.creature.get_muscles()
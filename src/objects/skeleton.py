import pygame
import math
import pymunk
import pymunk.pygame_util

from src.util.joints import create_bone, create_joint, create_muscle
from pyengine.game_object import GameObject


class Bone:
    def __init__(self, space, rect, friction=0.6, collision_filter=None):
        self.space = space
        self.rect = rect

        b = create_bone((rect[0], rect[1]), rect[2], rect[3])
        self.body = b[0]
        self.shape = b[1]

        self.shape.friction = friction

        if collision_filter is not None:
            self.shape.filter = pymunk.ShapeFilter(group=collision_filter)

        self.space.add(self.body, self.shape)

        self.children = []
        self.muscles = []
    
    def connect_to(self, other, anchor1, anchor2, min_angle=None, max_angle=None):
        """
        Connect two bones
        
        :param other: Connecting joint
        :param anchor1: Local position of joint on "self" - original joint
        :param anchor2: Local position of joint on "other" - connecting joint
        """
        joint = create_joint(self.body, other.body, anchor1, anchor2)
        self.children.append(other)

        if min_angle is not None and max_angle is not None:
            rot_limit = pymunk.RotaryLimitJoint(self.body, other.body, math.radians(min_angle), math.radians(max_angle))
            self.space.add(rot_limit)

        self.space.add(joint)
        return other

    def add_muscle(self, other, anchor1=(0, 0), anchor2=(0, 0)):
        muscle = create_muscle(self.body, other.body, anchor1, anchor2)
        self.muscles.append(muscle)
        self.space.add(muscle)
    
    def get_skeleton(self):
        skeleton = []
        skeleton.append(self)
        for child in self.children:
            skeleton.extend(child.get_skeleton())
        return skeleton

    def get_muscles(self):
        muscles = self.muscles.copy()
        for child in self.children:
            muscles.extend(child.get_muscles())
        return muscles

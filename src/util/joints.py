import pygame
import pymunk
import pymunk.pygame_util


def create_bone(position, length=100, thickness=20):
    mass = 1
    moment = pymunk.moment_for_box(mass, (length, thickness))
    body = pymunk.Body(mass, moment)
    body.position = position

    shape = pymunk.Poly.create_box(body, (length, thickness))
    shape.elasticity = 0.05
    shape.friction = 0.7

    return body, shape


def create_joint(bone1, bone2, anchor1, anchor2):
    joint = pymunk.PinJoint(bone1, bone2, anchor1, anchor2)
    joint.max_force = 50000
    joint.max_bias = 1000
    return joint

def create_muscle(bone1, bone2, anchor1=(0, 0), anchor2=(0, 0)):
    a = bone1.local_to_world(anchor1)
    b = bone2.local_to_world(anchor2)
    distance = (b - a).length

    spring = pymunk.DampedSpring(
        bone1,
        bone2,
        anchor1,
        anchor2,
        rest_length=distance,
        stiffness=300,
        damping=25
    )
    return spring

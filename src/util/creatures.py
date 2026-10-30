from src.objects.skeleton import Bone


# human = Bone(self.space, (500, 500), collision_filter=1)
# skeleton.connect_to(Bone(self.space, (600, 500), collision_filter=1), (50, 0), (-50, 0)) \
#         .connect_to(Bone(self.space, (700, 500), collision_filter=1), (50, 0), (-50, 0))


# skeleton.body.angular_velocity = 30


"""def create_human(space, thickness=10, pos=(500, 500)):
    c = 1  # Collision filter ID (so none of the bones collide)

    hip_width = 50
    quad_length = 40
    shin_length = 35

    back = Bone(space, (pos[0], pos[1], thickness, 100), collision_filter=c)  # Root bone
    hip = back.connect_to(Bone(space, (pos[0], pos[1]+50, hip_width, thickness), collision_filter=c), (0, 50), (0, 0), -30, 30)
    
    # LEFT LEG
    left_quad = Bone(space, (pos[0]-hip.rect[2]/2, hip.rect[1]+hip_width/2, thickness, quad_length), collision_filter=c)
    # left_shin = Bone(space, ())

    # left_quad.connect_to(left_shin)
    # hip.connect_to(left_quad)

        # .connect_to(Bone(space, (pos[0]-hip.rect[2]/2, hip.rect[1]+hip_width/2)))
    # hip.connect_to(Bone(space, (pos[0]+hip.rect[2]/2, hip.rect[1]+hip_width/2, thickness, quad_length), collision_filter=c),
                #    (hip_width/2, 0), (0, -quad_length/2))  # RIght leg
    

    return back"""

def create_human(space, thickness=10, pos=(500, 500)):
    c = 1  # Collision filter ID (so none of the bones collide)

    hip_width = 75
    quad_length = 40
    shin_length = 35

    hip = Bone(space, (pos[0], pos[1]+50, hip_width, thickness), collision_filter=c)

    # --- LEFT LEG ---
    left_thigh = Bone(
        space,
        (pos[0]-hip_width/2, hip.rect[1]+quad_length/2, thickness, quad_length),
        collision_filter=c
    )
    hip.connect_to(left_thigh, (-hip_width/2, 0), (0, -quad_length/2),
                   min_angle=-120, max_angle=20)

    left_shin = Bone(
        space,
        (left_thigh.rect[0], left_thigh.rect[1] + quad_length / 2 + shin_length / 2,
         thickness, shin_length),
        collision_filter=c
    )
    left_thigh.connect_to(left_shin, (0, quad_length/2), (0, -shin_length/2),
                          min_angle=0, max_angle=150)

    # --- RIGHT LEG ---
    right_thigh = Bone(
        space,
        (pos[0]+hip_width/2, hip.rect[1]+quad_length/2, thickness, quad_length),
        collision_filter=c
    )
    hip.connect_to(right_thigh, (hip_width/2, 0), (0, -quad_length/2),
                   min_angle=-120, max_angle=20)

    right_shin = Bone(
        space,
        (right_thigh.rect[0], right_thigh.rect[1] + quad_length / 2 + shin_length / 2,
         thickness, shin_length),
        collision_filter=c
    )
    right_thigh.connect_to(right_shin, (0, quad_length/2), (0, -shin_length/2),
                           min_angle=0, max_angle=150)


    # Muscles
    hip.add_muscle(left_thigh, (-20, 0), (0, -15))
    hip.add_muscle(right_thigh, (20, 0), (0, -15))
    left_thigh.add_muscle(left_shin, (5, 10), (-5, -10))
    right_thigh.add_muscle(right_shin, (-5, 10), (5, -10))

    return hip

import bpy
import random
import math
from math import radians
from ast import literal_eval
import mathutils
 
rig = bpy.context.scene.objects['Thomas_rig'] 
 
 
l_arm_11 = rig.pose.bones['L.arm'] 
r_arm_12 = rig.pose.bones['R.arm'] 

l_brush_15 = rig.pose.bones['L.arm_elbow']
r_brush_16 = rig.pose.bones['R.arm_elbow']


l_leg_23 = rig.pose.bones['L.Leg']
r_leg_24 = rig.pose.bones['L.Leg.001']

l_foot_27 = rig.pose.bones['FootCtrl.L.001']
r_foot_28 = rig.pose.bones['FootCtrl.L.002']

#bpy.context.scene.frame_set(0)
 
#bone.rotation_euler = (0, 0, 0)
#bone2.rotation_quaternion = (1, 0, 0, 0)
#bone.keyframe_insert('rotation_euler', index=-1)
#bone2.keyframe_insert('rotation_quaternion', index=-1)
bpy.context.scene.frame_set(10)
 
#bone.rotation_euler = (radians(120), 10, 15)
#bone2.rotation_quaternion = (1, 1, 0, 1)
#bone2.rotation_quaternion = (1, 1, 1, 1)
#bone.keyframe_insert('rotation_euler', index=-1)
#bone2.keyframe_insert('rotation_quaternion', index=-1)
 
#bpy.context.scene.render.filepath = "/Users/klochkovanton/Desktop/render.mp4" 
#bpy.ops.render.render(animation=True, write_still=True)
obj = {0: l_arm_11, 1:r_arm_12, 2:l_brush_15, 3: r_brush_16, 4: l_leg_23, 5: r_leg_24, 6: l_foot_27, 7: r_foot_28}

l = [11, 12, 15, 16, 23, 24, 27, 28]
d = {11: (440, 494), 12: (331, 484), 15: (515, 623), 16: (247, 638), 23: (420, 661), 24: (355, 661), 27: (434, 929), 28: (350, 934)}

x = 0
y = 0
frame_num = 0
with open("/home/anvar/Documents/boneExper.txt") as file:
    for line in file:
        d = literal_eval(line)
        for i in range(len(l)):
            bpy.context.scene.frame_set(frame_num)
            try:
                x = d[l[i]][0]
            except KeyError:
                pass
            
            try:
                y = d[l[i]][1]
            except KeyError:
                pass
            alpha = math.asin(y / math.sqrt(x ** 2 + y ** 2))
            #beta = math.asin(x / math.sqrt(x ** 2 + y ** 2))
            #alpha = random.randint(-180, 180)
            beta = random.randint(-90, 90)
            gamma = random.randint(-90, 90)
            vec = mathutils.Euler( (math.radians(beta), math.radians(gamma), math.radians(alpha)), 'XYZ') 
            obj[i].rotation_quaternion = vec.to_quaternion()
            obj[i].keyframe_insert('rotation_quaternion', index=-1)
        frame_num += 20
                            
#bpy.context.scene.render.filepath = "/home/anvar/Documents/render.mp4"
#bpy.ops.render.render(animation=True, write_still=True)


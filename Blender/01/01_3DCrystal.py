import bpy
import math

# ===== 清空场景 =====
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ===== 材质创建函数 =====
def create_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.diffuse_color = (*color, 1)  # RGBA
    return mat

# 球体（节点）材质
mat_sphere = create_material("SphereMaterial", (1.0, 0.75, 0.0))  # 橙黄色
# 圆柱体（连接棒）材质
mat_cylinder = create_material("CylinderMaterial", (0.5, 0.85, 1.0))  # 淡蓝色

# ===== 创建一个单元格（球 + 三根棒） =====
def create_unit():
    # 球体
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.15, location=(0, 0, 0))
    sphere = bpy.context.active_object
    sphere.data.materials.append(mat_sphere)

    rods = []
    # 三个方向的连接棒
    for axis in [(1, 0, 0), (0, 1, 0), (0, 0, 1)]:
        bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=0.05, depth=1.0, location=(0, 0, 0))
        rod = bpy.context.active_object
        rod.data.materials.append(mat_cylinder)

        # 平移棒到正确位置
        rod.location = [axis[i] * 0.5 for i in range(3)]
        if axis == (1, 0, 0):
            rod.rotation_euler = (0, math.radians(90), 0)
        elif axis == (0, 1, 0):
            rod.rotation_euler = (math.radians(90), 0, 0)

        rods.append(rod)

    # 合并为一个单元
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select_set(True)
    for rod in rods:
        rod.select_set(True)
    bpy.context.view_layer.objects.active = sphere
    bpy.ops.object.join()

    return sphere

# ===== 生成晶格 =====
size = 5  # 晶格的点数（立方体边长有多少节点）
spacing = 1.0  # 节点间距
unit = create_unit()

objects = []
for x in range(size):
    for y in range(size):
        for z in range(size):
            obj = unit.copy()
            obj.location = (x * spacing, y * spacing, z * spacing)
            bpy.context.collection.objects.link(obj)
            objects.append(obj)

# 删除原始单元模板
bpy.data.objects.remove(unit, do_unlink=True)

# ===== 计算模型中心点 =====
min_x = min(obj.location.x for obj in objects)
max_x = max(obj.location.x for obj in objects)
min_y = min(obj.location.y for obj in objects)
max_y = max(obj.location.y for obj in objects)
min_z = min(obj.location.z for obj in objects)
max_z = max(obj.location.z for obj in objects)

center_x = (min_x + max_x) / 2
center_y = (min_y + max_y) / 2
center_z = (min_z + max_z) / 2
max_dimension = max(max_x - min_x, max_y - min_y, max_z - min_z)

# ===== 添加相机（自动对准模型中心） =====
cam_distance = max_dimension * 2.5  # 相机距离
bpy.ops.object.camera_add(location=(center_x + cam_distance, center_y - cam_distance, center_z + cam_distance / 2))
camera = bpy.context.active_object
bpy.context.scene.camera = camera

# 让相机看向模型中心
direction = (center_x - camera.location.x,
             center_y - camera.location.y,
             center_z - camera.location.z)
rot_y = math.atan2(-direction[2], math.sqrt(direction[0]**2 + direction[1]**2))
rot_z = math.atan2(direction[1], direction[0])
camera.rotation_euler = (rot_y, 0, rot_z)

# ===== 添加灯光 =====
bpy.ops.object.light_add(type='AREA', location=(center_x, center_y, max_z + cam_distance))
light = bpy.context.active_object
light.data.energy = 3000
light.data.size = max_dimension * 1.5

# ===== 设置背景颜色 =====
bpy.context.scene.world.color = (0.1, 0.15, 0.25)

print("3D 晶格模型 + 自动对准相机 已完成！")

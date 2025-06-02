import bpy
import math
from mathutils import Vector

def clear_scene():
    # Clear existing objects from the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_material(name, color, metallic=0.0, roughness=0.5):
    # Create a new material with the specified properties
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    nodes = material.node_tree.nodes

    # Clear default nodes
    nodes.clear()

    # Create Principled BSDF node
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    principled.inputs['Base Color'].default_value = color
    principled.inputs['Metallic'].default_value = metallic
    principled.inputs['Roughness'].default_value = roughness

    # Create Material Output node
    material_output = nodes.new('ShaderNodeOutputMaterial')

    # Link nodes
    material.node_tree.links.new(principled.outputs['BSDF'], material_output.inputs['Surface'])

    return material

def create_manual_page(width=8.5, height=11, thickness=0.01):
    # Create a single manual page
    bpy.ops.mesh.primitive_plane_add(size=1)
    page = bpy.context.active_object

    # Scale to correct dimensions
    page.scale = (width, height, 1)
    page.scale.z = thickness

    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Add subdivision surface modifier for better edge quality
    subsurf = page.modifiers.new(name='Subdivision', type='SUBSURF')
    subsurf.levels = 2

    return page

def create_manual_cover(width=8.5, height=11, thickness=0.02):
    # Create the manual cover
    cover = create_manual_page(width, height, thickness)

    # Create cover material
    cover_material = create_material("CoverMaterial", (0.1, 0.1, 0.1, 1.0), metallic=0.1, roughness=0.3)
    cover.data.materials.append(cover_material)

    return cover

def create_manual_spine(width=8.5, height=11, thickness=0.02, num_pages=20):
    # Create the manual spine
    bpy.ops.mesh.primitive_cube_add()
    spine = bpy.context.active_object

    # Calculate spine width based on number of pages
    spine_width = num_pages * 0.01 # 0.01 units per page

    # Scale to correct dimensions
    spine.scale = (spine_width, height, thickness)

    # Apply scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

    # Create spine material
    spine_material = create_material("SpineMaterial", (0.2, 0.2, 0.2, 1.0), metallic=0.1, roughness=0.3)
    spine.data.materials.append(spine_material)

    return spine
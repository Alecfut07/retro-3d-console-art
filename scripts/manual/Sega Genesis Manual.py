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
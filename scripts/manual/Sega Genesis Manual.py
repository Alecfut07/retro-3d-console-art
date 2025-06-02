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

def create_manual(num_pages=20):
    # Create a complete manual with specified number of pages
    clear_scene()

    # Manual dimensions
    width = 8.5
    height = 11
    page_thickness = 0.01
    cover_thickness = 0.02

    # Create front cover
    front_cover = create_manual_cover(width, height, cover_thickness)
    front_cover.location = (0, 0, 0)

    # Create pages
    pages = []
    for i in range(num_pages):
        page = create_manual_page(width, height, page_thickness)
        # Offset each page slightly
        page.location = (0, 0 (i + 1) * page_thickness)
        pages.append(page)

        # Create page material
        page_material = create_material(f"PageMaterial_{i}", (0.95, 0.95, 0.95, 1.0), metallic=0.0, roughness=0.8)
        page.data.materials.append(page_material)

    # Create back cover
    back_cover = create_manual_cover(width, height, cover_thickness)
    back_cover.location = (0, 0, (num_pages + 1) * page_thickness)

    # Create spine
    spine = create_manual_spine(width, height, cover_thickness, num_pages)
    spine.location = (-width / 2 - spine.scale.x / 2, 0, (num_pages + 1) * page_thickness / 2)

    # Parent all objects to front cover for easier manipulation
    for page in pages:
        page.parent = front_cover
    back_cover.parent = front_cover
    spine.parent = front_cover

    # Add empty object for rotation pivot
    bpy.ops.object.empty_add(type='PLAIN_AXES')
    pivot = bpy.context.active_object
    pivot.location = (-width / 2, 0, 0)
    front_cover.parent = pivot
    return front_cover, pages, back_cover, spine, pivot

def setup_export_settings():
    # Setup export settings for Android compatibility
    # Set up render engine for better preview
    bpy.context.scene.render.engine = 'CYCLES'

    # Set up world background
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs['Color'].default_value = (0.1, 0.1, 0.1, 1.0)
    bg.inputs['Strength'].default_value = 1.0

def main():
    # Create the manual
    front_cover, pages, back_cover, spine, pivot = create_manual(num_pages=20)

    # Setup export settings
    setup_export_settings()

    # Add camera and light for preview
    bpy.ops.object.camera_add(location=(0, -20, 10), rotation=(math.radians(60), 0, 0))
    camera = bpy.context.active_object
    bpy.context.scene.camera = camera
    
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    light = bpy.context.active_object
    light.data.energy = 5.0

if __name__ == "__main__":
    main()
import bpy
import math

def clear_scene():
    # Delete all objects in the scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def create_main_body():
    # Create the main console body
    bpy.ops.mesh.primitive_cube_add(size=1)
    main_body = bpy.context.active_object
    main_body.name = "Genesis_Main_Body"

    # Set dimensions (in meters)
    main_body.scale.x = 0.32 # Width
    main_body.scale.y = 0.20 # Depth
    main_body.scale.z = 0.07 # Height

    # Apply scale
    bpy.ops.object.transform_apply(scale=True)

    # Add bevel for rounded edges
    bpy.ops.object.modifier_add(type='BEVEL')
    main_body.modifiers["Bevel"].width = 0.005
    main_body.modifiers["Bevel"].segments = 3

    return main_body

def create_materials():
    # Create basic material
    mat = bpy.data.materials.new(name="Genesis_Black")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Set material to black
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)

    return mat

def main():
    # Clear existing scene
    clear_scene()

    # Create main body
    main_body = create_main_body()

    # Create and assign material
    mat = create_materials()
    main_body.data.materials.append(mat)

if __name__ == "__main__":
    main()
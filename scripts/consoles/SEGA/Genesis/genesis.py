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

def create_cartridge_slot(main_body):
    # Create the cartridge slot
    bpy.ops.mesh.primitive_cube_add(size=1)
    slot = bpy.context.active_object
    slot.name = "Genesis_Cartridge_Slot"

    # Set dimensions for the slot
    slot.scale.x = 0.12 # Width of the slot
    slot.scale.y = 0.15 # Depth of the slot
    slot.scale.z = 0.02 # Height of the slot

    # Apply scale
    bpy.ops.object.transform_apply(scale=True)

    # Position the slot on top of the main body
    slot.location.x = 0 # Center horizontally
    slot.location.y = 0.1 # Slightly forward on the console
    slot.location.z = 0.045 # On top of the main body

    # Create a boolean modifier to cut the slot 
    bool_mod = main_body.modifiers.new(name="Cartridge_Slot", type='BOOLEAN')
    bool_mod.object = slot
    bool_mod.operation = 'DIFFERENCE'

    # Apply the boolean modifier
    bpy.context.view_layer.objects.active = main_body
    bpy.ops.object.modifier_apply(modifier="Cartridge_Slot")

    # Delete the slot object
    bpy.data.objects.remove(slot)

    # Add bevel to the slot edges
    bpy.ops.object.modifier_add(type='BEVEL')
    main_body.modifiers["Bevel"].width = 0.002
    main_body.modifiers["Bevel"].segments = 2

def create_cartridge_slot_details(main_body):
    # Create guide rails
    def create_guide_rail(side='left'):
        bpy.ops.mesh.primitive_cube_add(size=1)
        rail = bpy.context.active_object
        rail.name = f"Genesis_Guide_Rail_{side}"

        # Set dimensions for the guide rail
        rail.scale.x = 0.005 # Width
        rail.scale.y = 0.15 # Depth
        rail.scale.z = 0.015 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the rail
        x_pos = 0.055 if side == 'left' else -0.055
        rail.location.x = x_pos
        rail.location.y = 0.1
        rail.location.z = 0.045

        return rail
    
    # Create connector pins
    def create_connector_pins():
        bpy.ops.mesh.primitive_cube_add(size=1)
        pins = bpy.context.active_object
        pins.name = "Genesis_Connector_Pins"

        # Set dimensions for the pins
        pins.scale.x = 0.1 # Width
        pins.scale.y = 0.01 # Depth
        pins.scale.z = 0.01 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the pins
        pins.location.x = 0
        pins.location.y = 0.15
        pins.location.z = 0.045

        return pins
    
    # Create the guide rails
    left_rail = create_guide_rail(side='left')
    right_rail = create_guide_rail(side='right')

    # Create the connector pins
    connector_pins = create_connector_pins()

    # Create materials for the details
    def create_rail_material():
        mat = bpy.data.materials.new(name="Genesis_Rail_Material")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)
        return mat
    
    # Assign materials
    rail_mat = create_rail_material()
    left_rail.data.materials.append(rail_mat)
    right_rail.data.materials.append(rail_mat)
    connector_pins.data.materials.append(rail_mat)

    # Parent all details to main body
    left_rail.parent = main_body
    right_rail.parent = main_body
    connector_pins.parent = main_body

def create_detailed_connector_pins(main_body):
    # Create the base connector block
    bpy.ops.mesh.primitive_cube_add(size=1)
    connector_base = bpy.context.active_object
    connector_base.name = "Genesis_Connector_Base"

    # Set dimensions for the base
    connector_base.scale.x = 0.1 # Width
    connector_base.scale.y = 0.02 # Depth
    connector_base.scale.z = 0.01 # Height

    # Apply scale
    bpy.ops.object.transform_apply(scale=True)

    # Position the base
    connector_base.location.x = 0
    connector_base.location.y = 0.15
    connector_base.location.z = 0.045

    # Create individual pins
    def create_pin(index, total_pins=32):
        bpy.ops.mesh.primitive_cube_add(size=1)
        pin = bpy.context.active_object
        pin.name = f"Genesis_Pin_{index}"

        # Set dimensions for the pin
        pin.scale.x = 0.002 # Width
        pin.scale.y = 0.005 # Depth
        pin.scale.z = 0.008 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Calculate position
        spacing = 0.1 / (total_pins + 1)
        x_pos = -0.05 + (spacing * (index + 1))

        # Position the pin
        pin.location.x = x_pos
        pin.location.y = 0.15
        pin.location.z = 0.045

        return pin
    
    # Create all pins
    pins = []
    for i in range(32): # SEGA Gensesis typically has 32 pins
        pin = create_pin(i)
        pins.append(pin)

    # Create materials
    def create_pin_materials():
        # Base material
        base_mat = bpy.data.materials.new(name="Genesis_Connector_Base_Material")
        base_mat.use_nodes = True
        nodes = base_mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)

        # Pin material
        pin_mat = bpy.data.materials.new(name="Genesis_Pin_Material")
        pin_mat.use_nodes = True
        nodes = pin_mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
        nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2

        return base_mat, pin_mat
    
    # Create and assign materials
    base_mat, pin_mat = create_pin_materials()
    connector_base.data.materials.append(base_mat)

    for pin in pins:
        pin.data.materials.append(pin_mat)
    
    # Parent all objects to main body
    connector_base.parent = main_body
    for pin in pins:
        pin.parent = main_body

    # Group all connector parts
    connector_parts = [connector_base] + pins
    for obj in connector_parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = connector_base
    bpy.ops.object.parent_set(type='OBJECT')

def create_pin_contacts(main_body):
    def create_contact(index, total_contacts=32):
        bpy.ops.mesh.primitive_cube_add(size=1)
        contact = bpy.context.active_object
        contact.name = f"Genesis_Pin_Contact_{index}"

        # Set dimensions for the contact
        contact.scale.x = 0.001 # Width
        contact.scale.y = 0.003 # Depth
        contact.scale.z = 0.006 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Calculate position
        spacing = 0.1 / (total_contacts + 1)
        x_pos = -0.05 + (spacing * (index + 1))

        # Position the contact
        contact.location.x = x_pos
        contact.location.y = 0.155 # Slightly forward of the pins
        contact.location.z = 0.045

        # Create the contact material
        contact_mat = bpy.data.materials.new(name=f"Genesis_Contact_Material_{index}")
        contact_mat.use_nodes = True
        nodes = contact_mat.node_tree.nodes
        links = contact_mat.node_tree.links

        # Clear default nodes
        nodes.clear()

        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        bump = nodes.new('ShaderNodeBump')
        noise = nodes.new('ShaderNodeTexNoise')
        color_ramp = nodes.new('ShaderNodeValToRGB')
        mix_shader = nodes.new('ShaderNodeMixShader')
        emission = nodes.new('ShaderNodeEmission')

        # Set up Noise texture for wear pattern
        noise.inputs['Scale'].default_value = 200.0
        noise.inputs['Detail'].default_value = 2.0
        noise.inputs['Roughness'].default_value = 0.7

        # Set up Color Ramp for wear control
        color_ramp.color_ramp.elements[0].position = 0.4
        color_ramp.color_ramp.elements[0].color = (0.7, 0.7, 0.7, 1) # Worn color
        color_ramp.color_ramp.elements[1].position = 0.6
        color_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1) # Clean color

        # Set up Principled BSDF for clean areas
        principled.inputs["Base Color"].default_value = (0.95, 0.95, 0.95, 1)
        principled.inputs["Metallic"].default_value = 1.0
        principled.inputs["Roughness"].default_value = 0.15

        # Set up Emission for subtle glow in worn areas
        emission.inputs["Color"].default_value = (0.8, 0.8, 0.8, 1)
        emission.inputs["Strength"].default_value = 0.1

        # Set up Bump node
        bump.inputs["Strength"].default_value = 0.02

        # Connect nodes for wear effect
        links.new(noise.outputs["Color"], color_ramp.inputs["Fac"])
        links.new(color_ramp.outputs["Color"], principled.inputs["Base Color"])
        links.new(color_ramp.outputs["Color"], emission.inputs["Color"])

        # Connect nodes for surface detail
        links.new(noise.outputs["Color"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], principled.inputs["Normal"])

        # Mix shader for worn/clean areas
        links.new(principled.outputs["BSDF"], mix_shader.inputs[1])
        links.new(emission.outputs["Emission"], mix_shader.inputs[2])
        links.new(color_ramp.outputs["Color"], mix_shader.inputs["Fac"])

        # Connect to output
        links.new(mix_shader.outputs["Shader"], output.inputs["Surface"])

        # Add the material to the contact
        contact.data.materials.append(contact_mat)

        return contact
    
    # Create contact housing
    def create_contact_housing():
        bpy.ops.mesh.primitive_cube_add(size=1)
        housing = bpy.context.active_object
        housing.name = "Genesis_Contact_Housing"

        # Set dimensions for the housing
        housing.scale.x = 0.102 # Width
        housing.scale.y = 0.004 # Depth
        housing.scale.z = 0.008 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the housing
        housing.location.x = 0
        housing.location.y = 0.155
        housing.location.z = 0.045

        # Create housing material
        housing_mat = bpy.data.materials.new(name="Genesis_Contact_Housing_Material")
        housing_mat.use_nodes = True
        nodes = housing_mat.node_tree.nodes
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.05, 0.05, 0.05, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3

        # Add the material to the housing
        housing.data.materials.append(housing_mat)

        return housing
    
    # Create all contacts
    contacts = []
    for i in range(32): # SEGA Genesis typically has 32 contacts
        contact = create_contact(i)
        contacts.append(contact)

    # Create the housing
    housing = create_contact_housing()

    # Parent all objects to main body
    housing.parent = main_body
    for contact in contacts:
        contact.parent = main_body

    # Group all contact parts
    contact_parts = [housing] + contacts
    for obj in contact_parts:
        obj.select_set(True)
    bpy.context.view_layer.objects.active = housing
    bpy.ops.object.parent_set(type='OBJECT')

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

    # Create cartridge slot
    create_cartridge_slot(main_body)

    # Create cartridge slot details
    create_cartridge_slot_details(main_body)

    # Create detailed connector pins
    create_detailed_connector_pins(main_body)

    # Create pin contacts
    create_pin_contacts(main_body)

    # Create and assign material
    mat = create_materials()
    main_body.data.materials.append(mat)

if __name__ == "__main__":
    main()
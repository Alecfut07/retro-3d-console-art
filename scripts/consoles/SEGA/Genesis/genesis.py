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
    main_body.scale.x = 0.2781 # Width: 10.95 inches (278.1 mm)
    main_body.scale.y = 0.2146 # Depth: 8.45 inches (214.6 mm)
    main_body.scale.z = 0.0572 # Height: 2.25 inches (57.2 mm)

    # Apply scale
    bpy.ops.object.transform_apply(scale=True)

    # Add bevel for rounded edges
    bpy.ops.object.modifier_add(type='BEVEL')
    main_body.modifiers["Bevel"].width = 0.002 # Subtle bevel
    main_body.modifiers["Bevel"].segments = 3

    return main_body

def create_cartridge_slot(main_body):
    # Create the cartridge slot
    bpy.ops.mesh.primitive_cube_add(size=1)
    slot = bpy.context.active_object
    slot.name = "Genesis_Cartridge_Slot"

    # Set dimensions for the slot (in meters)
    slot.scale.x = 0.1143 # Length: 4.5 inches (114.3 mm)
    slot.scale.y = 0.0127 # Depth: 0.5 inches (12.7 mm)
    slot.scale.z = 0.01905 # Width: 0.75 inches (19.05 mm)

    # Apply scale
    bpy.ops.object.transform_apply(scale=True)

    # Position the slot on top of the main body
    slot.location.x = 0 # Center horizontally
    slot.location.y = 0.1073 # Half of depth (214.6/2 mm)
    slot.location.z = 0.0286 # Half of height (57.2/2 mm)

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
    main_body.modifiers["Bevel"].width = 0.001
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

def create_buttons(main_body):
    def create_button(name, position_x, is_power=False):
        # Create the button base
        bpy.ops.mesh.primitive_cube_add(size=1)
        button = bpy.context.active_object
        button.name = f"Genesis_{name}_Button"

        # Set dimensions (in meters)
        button.scale.x = 0.0127 # Width: 0.5 inches (12.7 mm)
        button.scale.y = 0.00635 # Height: 0.25 inches (6.35 mm)
        button.scale.z = 0.002 # Depth: 0.08 inches (2 mm)

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the button
        button.location.x = position_x
        button.location.y = 0.1073 # Half of depth (214.6/2 mm)
        button.location.z = 0.0286 # Half of height (57.2/2 mm)

        # Add bevel for rounded edges
        bpy.ops.object.modifier_add(type='BEVEL')
        bevel_mod = button.modifiers["Bevel"]
        bevel_mod.width = 0.0005
        bevel_mod.segments = 3

        # Create button material
        button_mat = bpy.data.materials.new(name=f"Genesis_{name}_Button_Material")
        button_mat.use_nodes = True
        nodes = button_mat.node_tree.nodes

        # Set up button material
        if is_power:
            # Power button is typically red
            nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.1, 0.1, 1)
        else:
            # Reset button is typically black
            nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)

        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3
        nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.1
        
        # Add the material to the button
        button.data.materials.append(button_mat)
        
        return button
    
    def create_power_led():
        # Create the LED indicator
        bpy.ops.mesh.primitive_cylinder_add(radius=0.002, depth=0.001)
        led = bpy.context.active_object
        led.name = "Genesis_Power_LED"

        # Position the LED
        led.location.x = -0.02 # Left of power button
        led.location.y = 0.1073 # Half of depth (214.6/2 mm)
        led.location.z = 0.0286 # Half of height (57.2/2 mm)

        # Create LED material
        led_mat = bpy.data.materials.new(name="Genesis_Power_LED_Material")
        led_mat.use_nodes = True
        nodes = led_mat.node_tree.nodes
        links = led_mat.node_tree.links

        # Clear default nodes
        nodes.clear()
        
        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        emission = nodes.new('ShaderNodeEmission')
        mix = nodes.new('ShaderNodeMixShader')
        principled = nodes.new('ShaderNodeBsdfPrincipled')

        # Set up emission shader
        emission.inputs["Color"].default_value = (0.8, 0.1, 0.1, 1) # Red color
        emission.inputs["Strength"].default_value = 0.5

        # Set up principled shader
        principled.inputs["Base Color"].default_value = (0.8, 0.1, 0.1, 1)
        principled.inputs["Metallic"].default_value = 0.1
        principled.inputs["Roughness"].default_value = 0.3

        # Connect nodes
        links.new(emission.outputs["Emission"], mix.inputs[1])
        links.new(principled.outputs["BSDF"], mix.inputs[2])
        links.new(mix.outputs["Shader"], output.inputs["Surface"])

        # Set mix factor for emission strength
        mix.inputs["Fac"].default_value = 0.5

        # Add the material to the LED
        led.data.materials.append(led_mat)

        return led
    
    # Create power button (left of cartridge slot)
    power_button = create_button("Power", -0.03, is_power=True)

    # Create reset button (right of cartridge slot)
    reset_button = create_button("Reset", 0.03)

    # Create power LED
    power_led = create_power_led()

    # Parent all buttons to main body
    power_button.parent = main_body
    reset_button.parent = main_body
    power_led.parent = main_body

    return power_button, reset_button, power_led

def create_controller_ports(main_body):
    def create_port_base(name, position_x):
        # Create the port housing
        bpy.ops.mesh.primitive_cube_add(size=1)
        port = bpy.context.active_object
        port.name = f"Genesis_{name}_Port"

         # Set dimensions (in meters)
        port.scale.x = 0.0381 # Width: 1.5 inches (38.1 mm)
        port.scale.y = 0.005 # Depth: 0.2 inches (5 mm)
        port.scale.z = 0.0127 # Height: 0.5 inches (12.7 mm)

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the port
        port.location.x = position_x
        port.location.y = 0.2146 # Front face (214.6 mm depth)
        port.location.z = 0.0286 # Half of height (57.2/2 mm)

        # Create port material
        port_mat = bpy.data.materials.new(name=f"Genesis_{name}_Port_Material")
        port_mat.use_nodes = True
        nodes = port_mat.node_tree.nodes

        # Set up port material (black)
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3

        # Add the material to the port
        port.data.materials.append(port_mat)

        return port
        
    def create_port_shielding(port, position_x):
        bpy.ops.mesh.primitive_cube_add(size=1)
        shield = bpy.context.active_object
        shield.name = f"Genesis_{port.name}_Shielding"

        # Set dimensions for shielding
        shield.scale.x = 0.040 # Slightly wider than port
        shield.scale.y = 0.003 # Thin metal shield
        shield.scale.z = 0.014 # Slightly taller than port

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the shielding
        shield.location.x = position_x
        shield.location.y = 0.2146 + 0.004 # Slightly forward of port
        shield.location.z = 0.0286

        # Create shielding material
        shield_mat = bpy.data.materials.new(name=f"Genesis_{port.name}_Shielding_Material")
        shield_mat.use_nodes = True
        nodes = shield_mat.node_tree.nodes

        # Set up shielding material (metallic)
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.7, 0.7, 0.7, 1)
        nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2

        # Add the material to the shielding
        shield.data.materials.append(shield_mat)
        shield.parent = port
        
        return shield

    def create_port_label(port, position_x):
        bpy.ops.mesh.primitive_plane_add(size=1)
        label = bpy.context.active_object
        label.name = f"Genesis_{port.name}_Label"

        # Set dimensions for label
        label.scale.x = 0.015 # Width
        label.scale.y = 0.005 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the label
        label.location.x = position_x
        label.location.y = 0.2146 + 0.007 # Forward of port
        label.location.z = 0.0286 + 0.008 # Above port

        # Create label material
        label_mat = bpy.data.materials.new(name=f"Genesis_{port.name}_Label_Material")
        label_mat.use_nodes = True
        nodes = label_mat.node_tree.nodes

        # Set up label material (white text)
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (1, 1, 1, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2

        # Add the material to the label
        label.data.materials.append(label_mat)
        label.parent = port

        return label

    def create_9pin_connector(port, position_x):
        # Create the 9-pin connector
        bpy.ops.mesh.primitive_cube_add(size=1)
        connector = bpy.context.active_object
        connector.name = f"Genesis_{port.name}_Connector"
        
        # Set dimensions for connector
        connector.scale.x = 0.035 # Width
        connector.scale.y = 0.004 # Depth
        connector.scale.z = 0.011 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the connector
        connector.location.x = position_x
        connector.location.y = 0.2146 + 0.002 # Slightly forward of port
        connector.location.z = 0.0286

        # Create pins
        pins = []
        pin_positions = [
            (-0.015, 0.005), # Pin 1
            (-0.015, 0), # Pin 2
            (-0.015, -0.005), # Pin 3
            (0, 0.005), # Pin 4
            (0, 0), # Pin 5
            (0, -0.005), # Pin 6
            (0.015, 0.005), # Pin 7
            (0.015, 0), # Pin 8
            (0.015, -0.005) # Pin 9
        ]

        for i, (x, y) in enumerate(pin_positions, 1):
            bpy.ops.mesh.primitive_cylinder_add(radius=0.001, depth=0.003)
            pin = bpy.context.active_object
            pin.name = f"Genesis_{port.name}_Pin_{i}"

            # Position the pin
            pin.location.x = position_x + x
            pin.location.y = 0.2146 + 0.003
            pin.location.z = 0.0286 + y

            # Create pin material
            pin_mat = bpy.data.materials.new(name=f"Genesis_{port.name}_Pin_Material_{i}")
            pin_mat.use_nodes = True
            nodes = pin_mat.node_tree.nodes

            # Set up pin material (metallic)
            nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
            nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
            nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.2

            # Add the material to the pin
            pin.data.materials.append(pin_mat)
            pin.parent = connector
            pins.append(pin)
        
        # Create the connector material
        connector_mat = bpy.data.materials.new(name=f"Genesis_{port.name}_Connector_Material")
        connector_mat.use_nodes = True
        nodes = connector_mat.node_tree.nodes

        # Set up connector material
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3

        # Add the material to the connector
        connector.data.materials.append(connector_mat)
        connector.parent = port

        return connector, pins
    
    def create_dust_cover(port, position_x):
        bpy.ops.mesh.primitive_cube_add(size=1)
        cover = bpy.context.active_object
        cover.name = f"Genesis_{port.name}_Dust_Cover"

        # Set dimensions for cover
        cover.scale.x = 0.039 # Slightly wider than port
        cover.scale.y = 0.002 # Thin cover
        cover.scale.z = 0.013 # Slightly taller than port

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the cover
        cover.location.x = position_x
        cover.location.y = 0.2146 + 0.006 # Forward of port
        cover.location.z = 0.0286

        # Create cover material
        cover_mat = bpy.data.materials.new(name=f"Genesis_{port.name}_Dust_Cover_Material")
        cover_mat.use_nodes = True
        nodes = cover_mat.node_tree.nodes

        # Set up cover material (semi-transparent)
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.1, 0.1, 0.1, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.4
        nodes["Principled BSDF"].inputs["Metallic"].default_value = 0.1

        # Add the material to the cover
        cover.data.materials.append(cover_mat)
        cover.parent = port

        return cover
    
    def create_mounting_brackets(port, position_x):
        brackets = []
        for side in ['left', 'right']:
            bpy.ops.mesh.primitive_cube_add(size=1)
            bracket = bpy.context.active_object
            bracket.name = f"Genesis_{port.name}_Bracket_{side}"

            # Set dimensions for bracket
            bracket.scale.x = 0.002 # Width
            bracket.scale.y = 0.008 # Depth
            bracket.scale.z = 0.0127 # Height

            # Apply scale
            bpy.ops.object.transform_apply(scale=True)

            # Position the bracket
            x_offset = -0.020 if side == 'left' else 0.020
            bracket.location.x = position_x + x_offset
            bracket.location.y = 0.2146
            bracket.location.z = 0.0286

            # Create bracket material
            bracket_mat = bpy.data.materials.new(name=f"Genesis_{port.name}_Bracket_Material_{side}")
            bracket_mat.use_nodes = True
            nodes = bracket_mat.node_tree.nodes

            # Set up bracket material (metallic)
            nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.8, 0.8, 0.8, 1)
            nodes["Principled BSDF"].inputs["Metallic"].default_value = 1.0
            nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3

            # Add the material to the bracket
            bracket.data.materials.append(bracket_mat)
            bracket.parent = port
            brackets.append(bracket)

        return brackets

    # Create recess for ports
    def create_port_recess():
        bpy.ops.mesh.primitive_cube_add(size=1)
        recess = bpy.context.active_object
        recess.name = "Genesis_Controller_Ports_Recess"

        # Set dimensions for recess
        recess.scale.x = 0.085 # Width to cover both ports
        recess.scale.y = 0.008 # Depth
        recess.scale.z = 0.015 # Height

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the recess
        recess.location.x = 0
        recess.location.y = 0.2146 
        recess.location.z = 0.0286

        # Create boolean modifier to cut recess
        bool_mod = main_body.modifiers.new(name="Controller_Ports_Recess", type='BOOLEAN')
        bool_mod.object = recess
        bool_mod.operation = 'DIFFERENCE'

        # Apply the boolean modifier
        bpy.context.view_layer.objects.active = main_body
        bpy.ops.object.modifier_apply(modifier="Controller_Ports_Recess")

        # Delete the recess object
        bpy.data.objects.remove(recess)
    
    # Create both controller ports
    port1 = create_port_base("Controller1", -0.02)
    port2 = create_port_base("Controller2", 0.02)

    # Create 9-pin connectors
    connector1, pins1 = create_9pin_connector(port1, -0.02)
    connector2, pins2 = create_9pin_connector(port2, 0.02)

    # Create dust covers
    cover1 = create_dust_cover(port1, -0.02)
    cover2 = create_dust_cover(port2, 0.02)

    # Create mounting brackets
    brackets1 = create_mounting_brackets(port1, -0.02)
    brackets2 = create_mounting_brackets(port2, 0.02)

    # Create shielding for each port
    shield1 = create_port_shielding(port1, -0.02)
    shield2 = create_port_shielding(port2, 0.02)

    # Create labels for each port
    label1 = create_port_label(port1, -0.02)
    label2 = create_port_label(port2, 0.02)

    # Create the recess
    create_port_recess()

    # Parent ports to main body
    port1.parent = main_body
    port2.parent = main_body

    return port1, port2, pins1, pins2

def create_ventilation_grilles(main_body):
    def create_top_grilles():
        # Create the main grille patern
        bpy.ops.mesh.primitive_cube_add(size=1)
        grille = bpy.context.active_object
        grille.name = "Genesis_Top Grilles"

        # Set dimensions for the grille area
        grille.scale.x = 0.15 # Width of grille area
        grille.scale.y = 0.05 # Depth of grille arae
        grille.scale.z = 0.001 # Very thin for the grille pattern

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the grille
        grille.location.x = 0 # Center horizontally
        grille.location.y = 0.1 # Slightly forward on top
        grille.location.z = 0.0572 # Top surface (57.2 mm height)
        
        # Create grille material
        grille_mat = bpy.data.materials.new(name="Genesis_Grille_Material")
        grille_mat.use_nodes = True
        nodes = grille_mat.node_tree.nodes

        # Set up grille material
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3

        # Add the material to the grille
        grille.data.materials.append(grille_mat)

        # Create the grille pattern using boolean operations
        def create_grille_slots():
            slots = []
            # Create multiple slots for the grille pattern
            for i in range(10): # Number of slots
                bpy.ops.mesh.primitive_cube_add(size=1)
                slot = bpy.context.active_object
                slot.name = f"Genesis_Grille_Slot_{i}"

                # Set dimensions for each slot
                slot.scale.x = 0.002 # Width of slot
                slot.scale.y = 0.05 # Depth of slot
                slot.scale.z = 0.002 # Height of slot

                # Apply scale
                bpy.ops.object.transform_apply(scale=True)

                # Position the slot
                x_pos = -0.075 + (i * 0.015) # Space slots evenly
                slot.location.x = x_pos
                slot.location.y = 0.1
                slot.location.z = 0.0572

                slots.append(slot)

            return slots
        
        # Create the slots
        slots = create_grille_slots()

        # Use boolean operations to create the grille pattern
        for slot in slots:
            bool_mod = grille.modifiers.new(name=f"Grille_Slot_{slot.name}", type='BOOLEAN')
            bool_mod.object = slot
            bool_mod.operation = 'DIFFERENCE'

            # Apply the boolean modifier
            bpy.context.view_layer.objects.active = grille
            bpy.ops.object.modifier_apply(modifier=f"Grille_Slot_{slot.name}")

            # Delete the slot object
            bpy.data.objects.remove(slot)

        return grille
    
    def create_side_grilles(side='left'):
        # Create the main grille pattern for the side
        bpy.ops.mesh.primitive_cube_add(size=1)
        grille = bpy.context.active_object
        grille.name = f"Genesis_{side.capitalize()}_Side_Grilles"

        # Set dimensions for the grille area
        grille.scale.x = 0.001 # Very thin for the grille pattern
        grille.scale.y = 0.05 # Depth of grille area
        grille.scale.z = 0.03 # Height of grille area

        # Apply scale
        bpy.ops.object.transform_apply(scale=True)

        # Position the grille
        x_pos = -0.139 if side == 'left' else 0.139 # Left or right side
        grille.location.x = x_pos
        grille.location.y = 0.1 # Slightly forward
        grille.location.z = 0.0286 # Center vertically

        # Create grille material
        grille_mat = bpy.data.materials.new(name=f"Genesis_{side.capitalize()}_Side_Grille_Material")
        grille_mat.use_nodes = True
        nodes = grille_mat.node_tree.nodes

        # Set up grille material
        nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)
        nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.3
        
        # Add the material to the grille
        grille.data.materials.append(grille_mat)

        # Create the grille pattern using boolean operations
        def create_grille_slots():
            slots = []
            # Create multiple slots for the grille pattern
            for i in range(8): # Number of slots
                bpy.ops.mesh.primitive_cube_add(size=1)
                slot = bpy.context.active_object
                slot.name = f"Genesis_{side.capitalize()}_Side_Grille_Slot_{i}"

                # Set dimensions for each slot
                slot.scale.x = 0.002 # Width of slot
                slot.scale.y = 0.05 # Depth of slot
                slot.scale.z = 0.002 # Height of slot

                # Apply scale
                bpy.ops.object.transform_apply(scale=True)

                # Position the slot
                z_pos = 0.015 + (i * 0.004) # Space slots evenly
                slot.location.x = x_pos
                slot.location.y = 0.1
                slot.location.z = z_pos

                slots.append(slot)

            return slots
        
        # Create the slots
        slots = create_grille_slots()

        # Use boolean operations to create the grille pattern
        for slot in slots:
            bool_mod = grille.modifiers.new(name=f"Grille_Slot_{slot.name}", type='BOOLEAN')
            bool_mod.object = slot
            bool_mod.operation = 'DIFFERENCE'

            # Apply the boolean modifier
            bpy.context.view_layer.objects.active = grille
            bpy.ops.object.modifier_apply(modifier=f"Grille_Slot_{slot.name}")

            # Delete the slot object
            bpy.data.objects.remove(slot)

        return grille
    
    # Create the top grilles
    top_grilles = create_top_grilles()

    # Create the side grilles
    left_side_grilles = create_side_grilles('left')
    right_side_grilles = create_side_grilles('right')

    # Parent all grilles to the main body
    top_grilles.parent = main_body
    left_side_grilles.parent = main_body
    right_side_grilles.parent = main_body

    return top_grilles, left_side_grilles, right_side_grilles

def create_materials():
    # Create basic material
    mat = bpy.data.materials.new(name="Genesis_Black")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # Set material to black
    nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.02, 0.02, 0.02, 1)

    return mat

def join_objects(main_body):
    # Select all objects except the main body
    bpy.ops.object.select_all(action='DESELECT')
    for obj in bpy.data.objects:
        if obj != main_body and obj.parent == main_body:
            obj.select_set(True)

    # Set main body as active object
    main_body.select_set(True)
    bpy.context.view_layer.objects.active = main_body

    # Join all selected objects
    bpy.ops.object.join()

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

    # Create buttons
    power_button, reset_button, power_led = create_buttons(main_body)

    # Create controller ports
    port1, port2, pins1, pins2 = create_controller_ports(main_body)

    # Create ventilation grilles
    top_grilles, left_side_grilles, right_side_grilles = create_ventilation_grilles(main_body)

    # Create and assign material
    mat = create_materials()
    main_body.data.materials.append(mat)

    # Join all objects
    #join_objects(main_body)

if __name__ == "__main__":
    main()
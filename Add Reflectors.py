"""This file acts as the main module for this script."""

import traceback
import adsk.core
import adsk.fusion
from adsk.fusion import FeatureOperations, ExtentDirections, DistanceExtentDefinition, ToEntityExtentDefinition
from adsk.core import ValueInput, Point3D
import math
import os

# Initialize the global variables for the Application and UserInterface objects.
app = adsk.core.Application.get()
ui  = app.userInterface

# Design parameters
#
# All angles in degrees
# All distances in mm
l_num_reflectors = 5
l_reflector_angle = 17
l_reflector_depth = 20
l_start_offset = 30
l_finish_offset = 30

r_num_reflectors = 7
r_reflector_angle = 19
r_reflector_depth = 20
r_start_offset = 30
r_finish_offset = 30


def add_left_absorbers(sketch: adsk.fusion.Sketch, ceiling_body: adsk.fusion.BRepBody):
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    extrudes = root.features.extrudeFeatures

    room_length = design.userParameters.itemByName('room_length').value
    room_width  = design.userParameters.itemByName('room_width').value
    print(f'room_length: {room_length}')

    # Do some geometry to calculate how to build our absorbers
    #
    # Distance this panel goes along the wall
    reflector_length = l_reflector_depth / math.tan(math.radians(l_reflector_angle))
    reflector_span = room_length - l_start_offset - l_finish_offset
    reflector_spacing = reflector_span / l_num_reflectors

    print(f'reflector_length: {reflector_length}')
    print(f'reflector_spacing: {reflector_spacing}')
    print(f'reflector_span: {reflector_span}')

    for i in range(l_num_reflectors):
        p1 = sketch.sketchPoints.add(Point3D.create(0, l_start_offset + i * reflector_spacing, 0))
        p2 = sketch.sketchPoints.add(Point3D.create(l_reflector_depth, l_start_offset + i * reflector_spacing + reflector_length, 0))
        p3 = sketch.sketchPoints.add(Point3D.create(0, l_start_offset + (i + 1) * reflector_spacing, 0))
        reflector_line = sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)
        absorber_line = sketch.sketchCurves.sketchLines.addByTwoPoints(p2, p3)
        # design.computeAll()
        reflector_extrude_input = extrudes.createInput(root.createOpenProfile(reflector_line), FeatureOperations.NewBodyFeatureOperation)
        reflector_extrude_input.isSolid = False
        reflector_extrude_input.setOneSideExtent(ToEntityExtentDefinition.create(ceiling_body, False), ExtentDirections.NegativeExtentDirection)
        reflector_extrusion = root.features.extrudeFeatures.add(reflector_extrude_input)
        reflector_extrusion.bodies.item(0).name= f'l_reflector_{i}'
        absorber_extrude_input = extrudes.createInput(root.createOpenProfile(absorber_line), FeatureOperations.NewBodyFeatureOperation)
        absorber_extrude_input.isSolid = False
        absorber_extrude_input.setOneSideExtent(ToEntityExtentDefinition.create(ceiling_body, False), ExtentDirections.NegativeExtentDirection)
        absorber_extrusion = root.features.extrudeFeatures.add(absorber_extrude_input)
        absorber_extrusion.bodies.item(0).name = f'l_absorber_{i}'
    
    


def add_right_absorbers(sketch: adsk.fusion.Sketch, ceiling_body: adsk.fusion.BRepBody):
    design = adsk.fusion.Design.cast(app.activeProduct)
    root = design.rootComponent
    extrudes = root.features.extrudeFeatures

    room_length = design.userParameters.itemByName('room_length').value
    room_width  = design.userParameters.itemByName('room_width').value
    print(f'room_length: {room_length}')

    # Do some geometry to calculate how to build our absorbers
    #
    # Distance this panel goes along the wall
    reflector_length = r_reflector_depth / math.tan(math.radians(r_reflector_angle))
    reflector_span = room_length - r_start_offset - r_finish_offset
    reflector_spacing = reflector_span / r_num_reflectors

    print(f'reflector_length: {reflector_length}')
    print(f'reflector_spacing: {reflector_spacing}')
    print(f'reflector_span: {reflector_span}')

    for i in range(r_num_reflectors):
        p1 = sketch.sketchPoints.add(Point3D.create(room_width, r_start_offset + i * reflector_spacing, 0))
        p2 = sketch.sketchPoints.add(Point3D.create(room_width - r_reflector_depth, r_start_offset + i * reflector_spacing + reflector_length, 0))
        p3 = sketch.sketchPoints.add(Point3D.create(room_width, r_start_offset + (i + 1) * reflector_spacing, 0))
        reflector_line = sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)
        absorber_line = sketch.sketchCurves.sketchLines.addByTwoPoints(p2, p3)
        # design.computeAll()
        reflector_extrude_input = extrudes.createInput(root.createOpenProfile(reflector_line), FeatureOperations.NewBodyFeatureOperation)
        reflector_extrude_input.isSolid = False
        reflector_extrude_input.setOneSideExtent(ToEntityExtentDefinition.create(ceiling_body, False), ExtentDirections.PositiveExtentDirection)
        reflector_extrusion = root.features.extrudeFeatures.add(reflector_extrude_input)
        reflector_extrusion.bodies.item(0).name= f'r_reflector_{i}'
        absorber_extrude_input = extrudes.createInput(root.createOpenProfile(absorber_line), FeatureOperations.NewBodyFeatureOperation)
        absorber_extrude_input.isSolid = False
        absorber_extrude_input.setOneSideExtent(ToEntityExtentDefinition.create(ceiling_body, False), ExtentDirections.PositiveExtentDirection)
        absorber_extrusion = root.features.extrudeFeatures.add(absorber_extrude_input)
        absorber_extrusion.bodies.item(0).name = f'r_absorber_{i}'
    
    

def run(_context: str):
    """This function is called by Fusion when the script is run."""

    design = adsk.fusion.Design.cast(app.activeProduct)
    if not design:
        ui.messageBox('No active Fusion design', 'No Design')
        return
    try:
        root = design.rootComponent
        floor_sketch = root.sketches.itemByName('Floor')
        l_ceiling = root.bRepBodies.itemByName('Street Arch 1')
        add_left_absorbers(floor_sketch, l_ceiling)
        r_ceiling = root.bRepBodies.itemByName('Hall Arch 1')
        add_right_absorbers(floor_sketch, r_ceiling)

        file_path = os.path.expanduser('~/repos/live_room_models/with_reflectors.3mf')
        opt = design.exportManager.createC3MFExportOptions(root, file_path)
        design.exportManager.execute(opt)

    except:  #pylint:disable=bare-except
        # Write the error message to the TEXT COMMANDS window.
        ui.messageBox(f'Failed:\n{traceback.format_exc()}')

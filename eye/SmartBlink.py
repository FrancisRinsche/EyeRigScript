import maya.cmds as cmds


def createBlendShapes(nameOne, nameTwo, indexMiddleElement):

    middleElement = f"{nameOne}_{indexMiddleElement}"

    # adding the smartBlink and smartBlinkHeight attribute to the upper middle controller
    cmds.select(f"{middleElement}_main_ctrl")
    cmds.addAttr(k=True, ln='SmartBlink', at='float', min=0, max=1, dv=0)
    cmds.addAttr(k=True, ln='SmartBlinkHeight', at='float', min=0, max=1, dv=0.2)

    cmds.select(f"{nameTwo}_{indexMiddleElement}_main_ctrl")
    cmds.addAttr(k=True, ln='SmartBlink', at='float', min=0, max=1, dv=0)

    # duplicating the curves to use as blendshapes
    cmds.duplicate(f"{nameOne}_cubic_crv", name=f"{nameOne}_smartBlink_crv")
    cmds.blendShape(f"{nameOne}_cubic_crv", f"{nameTwo}_cubic_crv", f"{nameOne}_smartBlink_crv", name=f"{nameOne}_smartBlink_blend")

    cmds.connectAttr(f"{middleElement}_main_ctrl.SmartBlinkHeight", f"{nameOne}_smartBlink_blend.{nameOne}_cubic_crv")

    cmds.shadingNode('reverse', au=True, name=f"{nameTwo}_reverse_node")
    cmds.connectAttr(f"{middleElement}_main_ctrl.SmartBlinkHeight", f"{nameTwo}_reverse_node.inputX")
    cmds.connectAttr(f"{nameTwo}_reverse_node.outputX", f"{nameOne}_smartBlink_blend.{nameTwo}_cubic_crv")

    cmds.duplicate(f"{nameOne}_linear_crv", name=f"{nameOne}_Blink_crv")
    cmds.duplicate(f"{nameTwo}_linear_crv", name=f"{nameTwo}_Blink_crv")

    # upperlid
    cmds.setAttr(f"{middleElement}_main_ctrl.SmartBlinkHeight", 1)
    cmds.wire(f"{nameOne}_Blink_crv",  w=f"{nameOne}_smartBlink_crv", name=f"{nameOne}_Blink_crv_BaseWire")
    cmds.setAttr(f"{nameOne}_Blink_crv_BaseWire.scale[0]", 0)
    cmds.blendShape( f"{nameOne}_Blink_crv", f"{nameOne}_linear_crv", name=f"{nameOne}_upBlink_blend")
    cmds.connectAttr(f"{middleElement}_main_ctrl.SmartBlink", f"{nameOne}_upBlink_blend.{nameOne}_Blink_crv")

    # lowerlid
    cmds.setAttr(f"{middleElement}_main_ctrl.SmartBlinkHeight", 0)
    cmds.wire(f"{nameTwo}_Blink_crv",  w=f"{nameOne}_smartBlink_crv", name=f"{nameTwo}_Blink_crv_BaseWire")
    cmds.setAttr(f"{nameTwo}_Blink_crv_BaseWire.scale[0]", 0)
    cmds.blendShape( f"{nameTwo}_Blink_crv", f"{nameTwo}_linear_crv", name=f"{nameTwo}_upBlink_blend")
    cmds.connectAttr(f"{nameTwo}_{indexMiddleElement}_main_ctrl.SmartBlink", f"{nameTwo}_upBlink_blend.{nameTwo}_Blink_crv")

    cmds.setAttr(f"{middleElement}_main_ctrl.SmartBlinkHeight", 0.3)
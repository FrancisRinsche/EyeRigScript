import maya.cmds as cmds


def createBlendShapes(nameOne, nameTwo, indexMiddleElement):
    upperMiddleElement = f"{nameOne}_{indexMiddleElement}"

    # adding the smartBlink and smartBlinkHeight attribute to the upper middle controller
    cmds.select(f"{upperMiddleElement}_main_ctrl")
    cmds.addAttr(k=True, ln='SmartBlink', at='float', min=0, max=1, dv=0)
    cmds.addAttr(k=True, ln='SmartBlinkHeight', at='float', min=0, max=1, dv=0.2)

    # adding the smartBlinkHeight attribute to the lower middle controller
    cmds.select(f"{nameTwo}_{indexMiddleElement}_main_ctrl")
    cmds.addAttr(k=True, ln='SmartBlink', at='float', min=0, max=1, dv=0)

    # duplicating the curves to use as blend shapes for the smart-blink function
    cmds.duplicate(f"{nameOne}_cubic_crv", name=f"{nameOne}_smartBlink_crv")
    blinkBlendShape = f"{nameOne}_smartBlink_crv"
    cmds.blendShape(f"{nameOne}_cubic_crv", f"{nameTwo}_cubic_crv", f"{nameOne}_smartBlink_crv",
                    name=f"{nameOne}_smartBlink_blend")

    # connecting the smart-blink height directly with the blendshape value
    cmds.connectAttr(f"{upperMiddleElement}_main_ctrl.SmartBlinkHeight", f"{nameOne}_smartBlink_blend.{nameOne}_cubic_crv")

    # making the reverse connection to the other input of the blendshape value
    cmds.shadingNode('reverse', au=True, name=f"{nameTwo}_reverse_node")
    cmds.connectAttr(f"{upperMiddleElement}_main_ctrl.SmartBlinkHeight", f"{nameTwo}_reverse_node.inputX")
    cmds.connectAttr(f"{nameTwo}_reverse_node.outputX", f"{nameOne}_smartBlink_blend.{nameTwo}_cubic_crv")

    def connectSmartBlink(name, smartBlinkHeight, blendshapeCrv):
        # duplicating linear curve
        cmds.duplicate(f"{name}_linear_crv", name=f"{name}_Blink_crv")

        cmds.setAttr(f"{upperMiddleElement}_main_ctrl.SmartBlinkHeight", smartBlinkHeight)
        cmds.wire(f"{name}_Blink_crv", w=blendshapeCrv, name=f"{name}_Blink_crv_BaseWire")
        cmds.setAttr(f"{name}_Blink_crv_BaseWire.scale[0]", 0)
        cmds.blendShape(f"{name}_Blink_crv", f"{name}_linear_crv", name=f"{name}_upBlink_blend")
        cmds.connectAttr(f"{name}_{indexMiddleElement}_main_ctrl.SmartBlink", f"{name}_upBlink_blend.{name}_Blink_crv")

    connectSmartBlink(nameOne, 1, blinkBlendShape)
    connectSmartBlink(nameTwo, 0, blinkBlendShape)

    # setting the smartblink height to a default value
    cmds.setAttr(f"{upperMiddleElement}_main_ctrl.SmartBlinkHeight", 0.3)

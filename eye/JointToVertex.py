import maya.cmds as cmds


def createStructure(name, vtx):

    def creatEyeJnts(name, vtx):
        cmds.group(name=f"{name}_grp", em=True)
        cmds.group(name=f"{name}_jnt_grp", em=True)
        for i in range(0, len(vtx)):
            cmds.select(cl=1)
            jnt = cmds.joint(name=f"{name}_{i}_tip_BIND_jnt")
            pos = cmds.xform(vtx[i], q=1, ws=1, t=1)
            cmds.xform(jnt, ws=1, t=pos)
            posC = cmds.xform("center_loc", q=1, ws=1, t=1)
            cmds.select(cl=1)
            jntC = cmds.joint(name=f"{name}_{i}_jnt")
            cmds.xform(jntC, ws=1, t=posC)
            cmds.parent(jnt, jntC)
            cmds.joint(jntC, e=1, oj="xyz", secondaryAxisOrient="yup", ch=1, zso=1)
            cmds.parent(f"{name}_{i}_jnt", f"{name}_jnt_grp")
        #cmds.setAttr(f"{name}_jnt_grp.visibility", 0)
        cmds.parent(f"{name}_jnt_grp", f"{name}_grp")

    def createConstraints(name):
        cmds.group(name=f"{name}_loc_grp", em=True)
        children = cmds.listRelatives(f"{name}_jnt_grp", c=True)
        grndChldrn = cmds.listRelatives(children, c=True)
        for s in range(0, len(grndChldrn)):
            loc = cmds.spaceLocator(name=f"{name}_{s}_loc")[0]
            pos = cmds.xform(grndChldrn[s], q=1, ws=1, t=1)
            cmds.xform(loc, ws=1, t=pos)
            par = cmds.listRelatives(grndChldrn[s], p=1)[0]
            cmds.aimConstraint(loc, par, mo=1, weight=1, aimVector=(1, 0, 0), upVector=(0, 1, 0), worldUpType="object",
                               worldUpObject="up_loc")
            cmds.parent(f"{name}_{s}_loc", f"{name}_loc_grp")
            cmds.scale(0.1, 0.1, 0.1, loc)
        #cmds.setAttr(f"{name}_loc_grp.visibility", 0)
        cmds.parent(f"{name}_loc_grp", f"{name}_grp")

    def createLinCurve(name):
        cmds.group(name=f"{name}_crv_grp", em=True)
        locs = cmds.listRelatives(f"{name}_loc_grp", c=True)
        for s in range(0, len(locs)):
            if s == 0:
                pos = cmds.xform(locs[s], q=1, ws=1, t=1)
                cmds.curve(name=f"{name}_linear_crv", d=1, p=[pos])
                shape = cmds.listRelatives(f"{name}_linear_crv", c=True, shapes=True)
                cmds.rename(shape, f"{name}_linear_crv_shape")
                cmds.parent(f"{name}_linear_crv", f"{name}_crv_grp")
            else:
                pos = cmds.xform(locs[s], q=1, ws=1, t=1)
                cmds.curve(f"{name}_linear_crv", a=True, p=[pos])
        cmds.setAttr(f"{name}_crv_grp.visibility", 0)
        cmds.parent(f"{name}_crv_grp", f"{name}_grp")

    def createLowCurve(name, ctrlAmount=5):
        locs = cmds.listRelatives(f"{name}_loc_grp", c=True)

        # calculate margin between controller
        marginBetweenCtrls = (len(locs) - 1) / (ctrlAmount - 1)

        for s in range(0, ctrlAmount):
            if s == 0:
                pos = cmds.xform(locs[s], q=1, ws=1, t=1)
                cmds.curve(name=f"{name}_cubic_crv", d=3, p=[pos])
                shape = cmds.listRelatives(f"{name}_cubic_crv", c=True, shapes=True)
                cmds.rename(shape, f"{name}_cubic_crv_shape")
                cmds.parent(f"{name}_cubic_crv", f"{name}_crv_grp")
            else:
                indexOfCtrl = int(round(marginBetweenCtrls * s, 0))
                pos = cmds.xform(locs[indexOfCtrl], q=1, ws=1, t=1)
                cmds.curve(f"{name}_cubic_crv", a=True, p=[pos])

    creatEyeJnts(name, vtx)
    createConstraints(name)
    createLinCurve(name)
    createLowCurve(name)

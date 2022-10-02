import maya.cmds as cmds


def createStructure(name, vtx):

    # Property of Marco Giordano
    # the following scripts createEyeJnts and createConstraints are taken from his youtube tutorial, and only slightly altered to fit the rest of the script
    def createEyeJnts(name, vtx):
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
        cmds.parent(f"{name}_loc_grp", f"{name}_grp")

    #  End of Property of Marco Giordano

    def createJnts(name, vtx):
        cmds.group(name=f"{name}_grp", em=True)
        cmds.group(name=f"{name}_jnt_grp", em=True)
        for i in range(0, len(vtx)):
            cmds.select(cl=1)
            jnt = cmds.joint(name=f"{name}_{i}_tip_BIND_jnt")
            pos = cmds.xform(vtx[i], q=1, ws=1, t=1)
            cmds.xform(jnt, ws=1, t=pos)
            #posC = cmds.xform("center_loc", q=1, ws=1, t=1)
            #cmds.select(cl=1)
            #jntC = cmds.joint(name=f"{name}_{i}_jnt")
            #cmds.xform(jntC, ws=1, t=posC)
            #cmds.parent(jnt, jntC)
            #cmds.joint(jntC, e=1, oj="xyz", secondaryAxisOrient="yup", ch=1, zso=1)
            cmds.parent(f"{name}_{i}_tip_BIND_jnt", f"{name}_jnt_grp")
        cmds.parent(f"{name}_jnt_grp", f"{name}_grp")

    def createLinCurve(name):
        cmds.group(name=f"{name}_crv_grp", em=True)
        #locs = cmds.listRelatives(f"{name}_loc_grp", c=True)
        for s in range(0, len(vtx)):
            if s == 0:
                pos = cmds.xform(vtx[s], q=1, ws=1, t=1)
                cmds.curve(name=f"{name}_linear_crv", d=1, p=[pos])
                shape = cmds.listRelatives(f"{name}_linear_crv", c=True, shapes=True)
                cmds.rename(shape, f"{name}_linear_crv_shape")
                cmds.parent(f"{name}_linear_crv", f"{name}_crv_grp")
            else:
                pos = cmds.xform(vtx[s], q=1, ws=1, t=1)
                cmds.curve(f"{name}_linear_crv", a=True, p=[pos])
        cmds.parent(f"{name}_crv_grp", f"{name}_grp")

    def createLowCurve(name, ctrlAmount=5):
        # locs = cmds.listRelatives(f"{name}_loc_grp", c=True)

        # calculate margin between controller
        marginBetweenCtrls = (len(vtx) - 1) / (ctrlAmount - 1)

        for s in range(0, ctrlAmount):
            if s == 0:
                pos = cmds.xform(vtx[s], q=1, ws=1, t=1)
                cmds.curve(name=f"{name}_cubic_crv", d=3, p=[pos])
                shape = cmds.listRelatives(f"{name}_cubic_crv", c=True, shapes=True)
                cmds.rename(shape, f"{name}_cubic_crv_shape")
                cmds.parent(f"{name}_cubic_crv", f"{name}_crv_grp")
            else:
                indexOfCtrl = int(round(marginBetweenCtrls * s, 0))
                pos = cmds.xform(vtx[indexOfCtrl], q=1, ws=1, t=1)
                cmds.curve(f"{name}_cubic_crv", a=True, p=[pos])

    if cmds.checkBox('aimConstraint_checkBox', query=True, v=True):
        createEyeJnts(name, vtx)
        createConstraints(name)
    else:
        createJnts(name, vtx)
    createLinCurve(name)
    createLowCurve(name)

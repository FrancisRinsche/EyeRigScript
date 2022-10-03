import maya.cmds as cmds


def createControlElements(name, ctrlAmount, vtx, previousCreatedCtrls=[]):
    def createWireDeformer(name):
        # create a wire deformer on surface1 using curve1
        cmds.wire(f"{name}_linear_crv", w=f"{name}_cubic_crv", name=f"{name}_cubic_crv_BaseWire")

    def calculateControllerPositions(name, ctrlAmount):
        marginBetweenCtrls = (len(vtx) - 1) / (ctrlAmount - 1)
        ctrlList = []
        for i in range(0, ctrlAmount):
            indexOfRelevantLoc = int(round(marginBetweenCtrls * i, 0))

            posOfRelevantLoc = cmds.xform(vtx[indexOfRelevantLoc], q=1, ws=1, t=1)

            ctrlDict = {
                "name": f"{name}_{i}",
                "pos": posOfRelevantLoc
            }
            ctrlList.append(ctrlDict)

        if len(previousCreatedCtrls) != 0:
            ctrlList[0] = previousCreatedCtrls[0]
            ctrlList[len(ctrlList) - 1] = previousCreatedCtrls[len(previousCreatedCtrls) - 1]

        return ctrlList

    def createControls(ctrlList, name):
        # check if the list is already filled, if not, create all controllers in list
        cmds.group(n=f"{name}_CTRLS_grp", em=True)

        for ctrl in ctrlList:
            ctrlName = ctrl.get("name")
            ctrlPosition = ctrl.get("pos")
            # create controller if the controllerName is the same as the prefix, therefore not creating double controller for the first and last vertex
            if ctrlName.startswith(name):
                # create, group and move the controller to the correct positions
                cmds.circle(n=f"{ctrlName}_ctrl", nr=[0, 0, 1], r=0.1)
                cmds.group(f"{ctrlName}_ctrl", n=f"{ctrlName}_grp")
                cmds.move(ctrlPosition[0], ctrlPosition[1], ctrlPosition[2], f"{ctrlName}_grp")
                cmds.parent(f"{ctrlName}_grp", f"{name}_CTRLS_grp")

                # color the controller
                cmds.setAttr(f"{ctrlName}_ctrl.overrideEnabled", 1)
                cmds.setAttr(f"{ctrlName}_ctrl.overrideColor", 14)  # green

        cmds.parent(f"{name}_CTRLS_grp", f"{name}_grp")
        # define first, middle and last item in the ctrl List
        startElement = ctrlList[0].get("name")
        endElement = ctrlList[len(ctrlList) - 1].get("name")

        indexOfMiddleListElement = int(round(len(ctrlList) / 2 - 1, 0))
        print(indexOfMiddleListElement)
        middleElement = ctrlList[indexOfMiddleListElement]["name"]

        # separating the controller by halfes to constrain them under the main controller
        listFirstHalf = []
        listSecondHalf = []

        for idx, element in enumerate(ctrlList):
            if element.get('name') != startElement and element.get('name') != endElement and element.get('name') != middleElement:
                # adding the names that are not the first, the last or the middle element to the second list
                if idx > indexOfMiddleListElement:
                    listSecondHalf.append(element['name'])
                # adding the rest to the first list
                else:
                    listFirstHalf.append(element['name'])

        # duplicating the middlecontroller
        cmds.duplicate(f"{middleElement}_grp", name=f"{middleElement}_main_grp")
        cmds.rename(f"{middleElement}_main_grp|{middleElement}_ctrl", f"{middleElement}_main_ctrl")
        cmds.scale(1.6, 1.6, 1.6, f"{middleElement}_main_ctrl.cv[0]", f"{middleElement}_main_ctrl.cv[2]",
                   f"{middleElement}_main_ctrl.cv[4]",
                   f"{middleElement}_main_ctrl.cv[6]")

        # Add Attribute to main controller
        cmds.select(f"{middleElement}_main_ctrl")
        cmds.addAttr(k=True, ln='SecondaryCtrls', at='bool', dv=1)

        # parent controller or parent constraint controller, and connect the secondary visibility attribute
        cmds.parent(f"{middleElement}_grp", f"{middleElement}_main_ctrl")
        for element in listFirstHalf:
            cmds.parentConstraint(f"{middleElement}_main_ctrl", f"{startElement}_grp", f"{element}_grp", mo=True)
            cmds.connectAttr(f"{middleElement}_main_ctrl.SecondaryCtrls", f"{element}_grp.visibility")
        for element in listSecondHalf:
            cmds.parentConstraint(f"{middleElement}_main_ctrl", f"{endElement}_grp", f"{element}_grp", mo=True)
            cmds.connectAttr(f"{middleElement}_main_ctrl.SecondaryCtrls", f"{element}_grp.visibility")

        return indexOfMiddleListElement

    def createCtrlJnts(ctrlList, name):
        ctrlJointGroupName = f"{name}_CtrlJnt_grp"
        cmds.group(name=ctrlJointGroupName, em=True)

        # create controller if the controllerName is the same as the prefix, therefore not creating double controller for the first and last vertex
        for ctrl in ctrlList:
            ctrlName = ctrl.get("name")
            if ctrlName.startswith(name):
                ctrlJointName = f"{ctrl.get('name')}_Ctrl_jnt"
                cmds.select(d=True)
                cmds.joint(name=ctrlJointName, a=True, p=ctrl.get("pos"))
                cmds.parent(ctrlJointName, ctrlJointGroupName)

                # create point constraints between ctrl joints and controller
                cmds.pointConstraint(f"{ctrl.get('name')}_ctrl", ctrlJointName, mo=True)

        cmds.parent(f"{name}_CtrlJnt_grp", f"{name}_grp")
        # cmds.setAttr(f"{name}_CtrlJnt_grp.visibility", 0)

    def skinCtrlJointToCurve(ctrlList, name):
        bindJnts = []
        for ctrl in ctrlList:
            bindJnts.append(f"{ctrl.get('name')}_Ctrl_jnt")
        cmds.skinCluster(f"{name}_cubic_crv", bindJnts)

    createWireDeformer(name)
    ctrlList = calculateControllerPositions(name, ctrlAmount)
    indexOfMiddleListElement = createControls(ctrlList, name)
    createCtrlJnts(ctrlList, name)
    skinCtrlJointToCurve(ctrlList, name)

    # giving the ctrl list and the name of the middle element back to the UI for the next use of the script
    # the middle controller of the first use would be needed to add a smartblink height connection to both curves
    return ctrlList, indexOfMiddleListElement

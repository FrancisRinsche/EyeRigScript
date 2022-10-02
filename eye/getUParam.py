from maya import cmds, OpenMaya

# Property of Marco Giordano
# the following scripts are taken from his youtube tutorial, and only slightly altered to fit the rest of the script


def connectLocToCurve(name):
    if cmds.checkBox('aimConstraint_checkBox', query=True, v=True):
        sel = cmds.listRelatives(f"{name}_loc_grp", c=True)
    else:
        sel = cmds.listRelatives(f"{name}_jnt_grp", c=True)

    crv = f"{name}_linear_crv_shape"
    
    for s in sel:
        pos = cmds.xform(s,  q = 1, ws = 1, t = 1)
        u = getUParam(pos, crv)
        name = s.replace("_loc", "_pci")
        pci = cmds.createNode("pointOnCurveInfo", n=name)
        cmds.connectAttr(crv+'.worldSpace', pci + '.inputCurve')
        cmds.setAttr(pci+ '.parameter', u)
        cmds.connectAttr(pci + '.position', s + '.t')


def getUParam( pnt = [], crv = None):

    point = OpenMaya.MPoint(pnt[0],pnt[1],pnt[2])
    curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
    paramUtill=OpenMaya.MScriptUtil()
    paramPtr=paramUtill.asDoublePtr()
    isOnCurve = curveFn.isPointOnCurve(point)
    if isOnCurve == True:
        
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    else :
        point = curveFn.closestPoint(point,paramPtr,0.001,OpenMaya.MSpace.kObject)
        curveFn.getParamAtPoint(point , paramPtr,0.001,OpenMaya.MSpace.kObject )
    
    param = paramUtill.getDouble(paramPtr)  
    return param

def getDagPath( objectName):
    
    if isinstance(objectName, list)==True:
        oNodeList=[]
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode
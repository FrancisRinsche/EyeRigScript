sys.path.append('C:/Users/franc/OneDrive/Scripts/RiggingScript/')
sys.path.append('C:/Users/franc/OneDrive/Scripts/RiggingScript/eye')


import maya.cmds as cmds
from eye import JointToVertex, getUParam, createControls, SmartBlink
import importlib

importlib.reload(JointToVertex)
importlib.reload(getUParam)
importlib.reload(createControls)
importlib.reload(SmartBlink)

upperVerts = []
lowerVerts = []
global aimConstraintBool

dialog = cmds.loadUI(uiFile='C:/Users/Franc/OneDrive/Scripts/RiggingScript/EyeRigScript.ui', v=True)
cmds.showWindow(dialog)


def createMiddleLoc():
    cmds.spaceLocator(n="center_loc")
    cmds.spaceLocator(n="up_loc")


def getUpperVertsList():
    global upperVerts
    upperVerts = cmds.ls(os=True, fl=True)


def getLowerVertsList():
    global lowerVerts
    lowerVerts = cmds.ls(os=True, fl=True)


def runJointToVertex():

    aimConstraintBool = cmds.checkBox('aimConstraint_checkBox', query=True, v=True)

    # upperLid
    prefix = cmds.textField('prefixOne_lineEdit', query=True, text=True)
    if prefix != "":
        JointToVertex.createStructure(prefix, upperVerts)
        getUParam.connectLocToCurve(prefix)

    # LowerLid
    prefixTwo = cmds.textField('prefixTwo_lineEdit', query=True, text=True)
    if prefixTwo != "":
        JointToVertex.createStructure(prefixTwo, lowerVerts)
        getUParam.connectLocToCurve(prefixTwo)


def runWireDeformerScript():
    ctrlAmount = int(cmds.textField("controlAmount_lineEdit", query=True, text=True))

    # upperLid
    prefix = cmds.textField("prefixOne_lineEdit", query=True, text=True)
    createdControls, indexMiddleElement = createControls.createControlElements(prefix, ctrlAmount, upperVerts)

    prefixTwo = cmds.textField("prefixTwo_lineEdit", query=True, text=True)
    if prefixTwo != "":
        # lowerLid
        prefixTwo = cmds.textField("prefixTwo_lineEdit", query=True, text=True)
        createControls.createControlElements(prefixTwo, ctrlAmount, lowerVerts, createdControls)

        # create SmartBlink BlendShapes if the Box is checked
        if cmds.checkBox('smartBlink_checkBox', query=True, v=True):
            SmartBlink.createBlendShapes(prefix, prefixTwo, indexMiddleElement)

    # delete middle locator, as they are not needed anymore
    cmds.delete("center_loc", "up_loc")

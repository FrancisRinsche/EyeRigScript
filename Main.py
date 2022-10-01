sys.path.append('C:/Users/franc/OneDrive/Scripts/RiggingScript/')
sys.path.append('C:/Users/franc/OneDrive/Scripts/RiggingScript/eye')


import maya.cmds as cmds
from eye import JointToVertex, getUParam, createControls, SmartBlink
import importlib

importlib.reload(JointToVertex)
importlib.reload(getUParam)
importlib.reload(createControls)
importlib.reload(SmartBlink)

upperVerts = ["a"]
lowerVerts = []

dialog = cmds.loadUI(uiFile='C:/Users/Franc/OneDrive/Scripts/RiggingScript/RiggingScriptNew_2.ui', v=True)
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
    # upperLid
    prefix = cmds.textField('prefixOne_lineEdit', query=True, text=True)

    print(prefix)
    if prefix != "":
        print("test")
        JointToVertex.createStructure(prefix, upperVerts)
        getUParam.connectLocToCurve(prefix)

    # LowerLid
    prefixTwo = cmds.textField('prefixTwo_lineEdit', query=True, text=True)
    print(prefixTwo)
    if prefixTwo != "":
        JointToVertex.createStructure(prefixTwo, lowerVerts)
        getUParam.connectLocToCurve(prefixTwo)


def runWireDeformerScript():
    print("this works")
    ctrlAmount = int(cmds.textField("controlAmount_lineEdit", query=True, text=True))
    print(ctrlAmount)
    # upperLid
    prefix = cmds.textField("prefixOne_lineEdit", query=True, text=True)
    createdControls, indexMiddleElement = createControls.createControlElements(prefix, ctrlAmount)

    prefixTwo = cmds.textField("prefixTwo_lineEdit", query=True, text=True)
    if prefixTwo != "":
        # lowerLid
        prefixTwo = cmds.textField("prefixTwo_lineEdit", query=True, text=True)
        createControls.createControlElements(prefixTwo, ctrlAmount, createdControls)


        # create BlendShapes
        SmartBlink.createBlendShapes(prefix, prefixTwo, indexMiddleElement)

    cmds.delete("center_loc", "up_loc")

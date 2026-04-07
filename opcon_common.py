import re
import xml.etree.ElementTree as ET


class OpConHeader:
    def __init__(self, event_switch):
        if (event_switch is not None) and ((event_switch < 0)):
            raise ValueError("event_switch must be a positive integer")
        self.event_switch = event_switch

    def event_switch(self, event_switch):
        if (event_switch is not None) and ((event_switch < 0)):
            raise ValueError("event_switch must be a positive integer")
        self.event_switch = event_switch

    def update(self, telegram) -> None:
        tree = ET.fromstring(telegram)
        print(tree)
        node = tree.find("header")
        if self.event_switch and node is not None:
            node.set("eventSwitch", str(self.event_switch))
        return ET.tostring(tree)


def NewOpConHeader(event_switch: int) -> OpConHeader:
    return OpConHeader(event_switch)


class OpConLocation:
    def __init__(
        self,
        lineNo=None,
        statNo=None,
        statIdx=None,
        fuNo=None,
        workPos=None,
        toolPos=None,
        Application=None,
        ProcessName=None,
        ProcessNo=None,
    ):
        if (lineNo is not None) and ((lineNo < 0) or (lineNo > 9999)):
            raise ValueError("lineNo must be between 0 and 9999")
        if (statNo is not None) and ((statNo < 0) or (statNo > 9999)):
            raise ValueError("statNo must be between 0 and 9999")
        if (statIdx is not None) and ((statIdx < 0) or (statIdx > 9999)):
            raise ValueError("statIdx must be between 0 and 9999")
        if (fuNo is not None) and ((fuNo < 1) or (fuNo > 9)):
            raise ValueError("fuNo must be between 1 and 9")
        if (workPos is not None) and ((workPos < 1) or (workPos > 9999)):
            raise ValueError("workPos must be between 1 and 9999")
        if (toolPos is not None) and ((toolPos < 1) or (toolPos > 9999)):
            raise ValueError("toolPos must be between 1 and 9999")

        self._lineNo = lineNo
        self._statNo = statNo
        self._statIdx = statIdx
        self._fuNo = fuNo
        self._workPos = workPos
        self._toolPos = toolPos
        self._application = Application
        self._processName = ProcessName
        self._processNo = ProcessNo

    def lineNo(self, lineNo):
        if (lineNo < 0) or (lineNo > 9999):
            raise ValueError("lineNo must be between 0 and 9999")
        self._lineNo = lineNo

    def statNo(self, statNo):
        if (statNo < 0) or (statNo > 9999):
            raise ValueError("statNo must be between 0 and 9999")
        self._statNo = statNo

    def statIdx(self, statIdx):
        if (statIdx < 0) or (statIdx > 9999):
            raise ValueError("statIdx must be between 0 and 9999")
        self._statIdx = statIdx

    def fuNo(self, fuNo):
        if (fuNo < 1) or (fuNo > 9):
            raise ValueError("fuNo must be between 1 and 9")
        self._fuNo = fuNo

    def workPos(self, workPos):
        if (workPos < 1) or (workPos > 9999):
            raise ValueError("workPos must be between 1 and 9999")
        self._workPos = workPos

    def toolPos(self, toolPos):
        if (toolPos < 1) or (toolPos > 9999):
            raise ValueError("toolPos must be between 1 and 9999")
        self._toolPos = toolPos

    def application(self, application):
        self._application = application

    def processName(self, processName):
        self._processName = processName

    def processNo(self, processNo):
        self._processNo = processNo

    def update(self, telegram) -> None:
        tree = ET.fromstring(telegram)
        node = tree.find("header/location")
        if self._lineNo is not None:
            node.set("lineNo", str(self._lineNo))
        if self._statNo is not None:
            node.set("statNo", str(self._statNo))
        if self._statIdx is not None:
            node.set("statIdx", str(self._statIdx))
        if self._fuNo is not None:
            node.set("fuNo", str(self._fuNo))
        if self._workPos is not None:
            node.set("workPos", str(self._workPos))
        if self._toolPos is not None:
            node.set("toolPos", str(self._toolPos))
        if self._application is not None:
            node.set("application", self._application)
        if self._processName is not None:
            node.set("processName", self._processName)
        if self._processNo is not None:
            node.set("processNo", str(self._processNo))
        return ET.tostring(tree)


def NewOpConLocation(
    locationId=None,
    lineNo=None,
    statNo=None,
    statIdx=None,
    fuNo=None,
    workPos=None,
    toolPos=None,
    application=None,
    processName=None,
    processNo=None,
) -> OpConLocation:
    if locationId is not None:
        location = OpConLocation()
        matches = re.match(r"(\d*)\.(\d*)\.(\d*)\.(\d*)\.(\d*)\.(\d*)", locationId)

        if matches:
            location.lineNo(int(matches.group(1)))
            location.statNo(int(matches.group(2)))
            location.statIdx(int(matches.group(3)))
            location.fuNo(int(matches.group(4)))
            location.workPos(int(matches.group(5)))
            location.toolPos(int(matches.group(6)))
    else:
        location = OpConLocation(
            lineNo=lineNo,
            statNo=statNo,
            statIdx=statIdx,
            fuNo=fuNo,
            workPos=workPos,
            toolPos=toolPos,
        )

    location.application(application)
    location.processName(processName)
    location.processNo(processNo)
    return location

import re
import xml.etree.ElementTree as ET


class OpConHeader:
    def __init__(self, event_switch):
        if (event_switch is not None) and ((event_switch < 0)):
            raise ValueError("event_switch must be a positive integer")
        self._event_switch = event_switch

    @property
    def event_switch(self):
        return self._event_switch

    @event_switch.setter
    def event_switch(self, event_switch):
        if (event_switch is not None) and ((event_switch < 0)):
            raise ValueError("event_switch must be a positive integer")
        self._event_switch = event_switch

    def update(self, telegram) -> bytes:
        tree = ET.fromstring(telegram)
        print(tree)
        node = tree.find("header")
        if self._event_switch and node is not None:
            node.set("eventSwitch", str(self._event_switch))
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

    @property
    def lineNo(self):
        return self._lineNo

    @lineNo.setter
    def lineNo(self, lineNo):
        if (lineNo < 0) or (lineNo > 9999):
            raise ValueError("lineNo must be between 0 and 9999")
        self._lineNo = lineNo

    @property
    def statNo(self):
        return self._statNo

    @statNo.setter
    def statNo(self, statNo):
        if (statNo < 0) or (statNo > 9999):
            raise ValueError("statNo must be between 0 and 9999")
        self._statNo = statNo

    @property
    def statIdx(self):
        return self._statIdx

    @statIdx.setter
    def statIdx(self, statIdx):
        if (statIdx < 0) or (statIdx > 9999):
            raise ValueError("statIdx must be between 0 and 9999")
        self._statIdx = statIdx

    @property
    def fuNo(self):
        return self._fuNo

    @fuNo.setter
    def fuNo(self, fuNo):
        if (fuNo < 1) or (fuNo > 9):
            raise ValueError("fuNo must be between 1 and 9")
        self._fuNo = fuNo

    @property
    def workPos(self):
        return self._workPos

    @workPos.setter
    def workPos(self, workPos):
        if (workPos < 1) or (workPos > 9999):
            raise ValueError("workPos must be between 1 and 9999")
        self._workPos = workPos

    @property
    def toolPos(self):
        return self._toolPos

    @toolPos.setter
    def toolPos(self, toolPos):
        if (toolPos < 1) or (toolPos > 9999):
            raise ValueError("toolPos must be between 1 and 9999")
        self._toolPos = toolPos

    @property
    def application(self):
        return self._application

    @application.setter
    def application(self, application):
        self._application = application

    @property
    def processName(self):
        return self._processName

    @processName.setter
    def processName(self, processName):
        self._processName = processName

    @property
    def processNo(self):
        return self._processNo

    @processNo.setter
    def processNo(self, processNo):
        self._processNo = processNo

    def update(self, telegram) -> bytes:
        tree = ET.fromstring(telegram)
        node = tree.find("header/location")
        if node is None:
            raise ValueError("Telegram does not contain a location node")

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
            location.lineNo = int(matches.group(1))
            location.statNo = int(matches.group(2))
            location.statIdx = int(matches.group(3))
            location.fuNo = int(matches.group(4))
            location.workPos = int(matches.group(5))
            location.toolPos = int(matches.group(6))
    else:
        location = OpConLocation(
            lineNo=lineNo,
            statNo=statNo,
            statIdx=statIdx,
            fuNo=fuNo,
            workPos=workPos,
            toolPos=toolPos,
        )

    location.application = application
    location.processName = processName
    location.processNo = processNo

    return location


class OpConEvent:
    def __init__(self, identifier=None, typeNo=None, typeVar=None):
        self._identifier = identifier
        self._typeNo = typeNo
        self._typeVar = typeVar

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def typeNo(self):
        return self._typeNo

    @typeNo.setter
    def typeNo(self, typeNo):
        self._typeNo = typeNo

    @property
    def typeVar(self):
        return self._typeVar

    @typeVar.setter
    def typeVar(self, typeVar):
        self._typeVar = typeVar

    def update(self, telegram):
        tree = ET.fromstring(telegram)
        event_node = tree.find("event")

        if event_node is None:
            raise ValueError("Telegram does not contain an event node")
        if self._identifier is not None:
            event_node.set("identifier", self._identifier)
        if self._typeNo is not None:
            event_node.set("typeNo", self._typeNo)
        if self._typeVar is not None:
            event_node.set("typeVar", self._typeVar)
        return ET.tostring(tree)


def NewOpConEvent(
    group=None, opConEvent=None, identifier=None, typeNo=None, typeVar=None
) -> OpConEvent:
    event = OpConEvent()
    if opConEvent is not None:
        event.identifier = opConEvent.identifier
        event.typeNo = opConEvent.typeNo
        event.typeVar = opConEvent.typeVar

    if group is not None:
        # TODO: implement the group logic
        pass
    else:
        if identifier is not None:
            event.identifier = identifier
        if typeNo is not None:
            event.typeNo = typeNo
        if typeVar is not None:
            event.typeVar = typeVar
    return event


class OpConResHead:
    VALID_RESULTS = [-1, 0, 1, 2, 12]

    def __init__(
        self,
        result=None,
        typeNo=None,
        typeVar=None,
        workingCode=None,
        nioBits=None,
        machineId=None,
    ):
        self.result = result
        self.workingCode = workingCode
        self.typeNo = typeNo
        self.typeVar = typeVar
        self.nioBits = nioBits
        self.machineId = machineId

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, result):
        if result is not None and result not in self.VALID_RESULTS:
            raise ValueError(f"result must be one of {self.VALID_RESULTS}")
        self._result = result

    @property
    def typeNo(self):
        return self._typeNo

    @typeNo.setter
    def typeNo(self, typeNo):
        self._typeNo = typeNo

    @property
    def typeVar(self):
        return self._typeVar

    @typeVar.setter
    def typeVar(self, typeVar):
        self._typeVar = typeVar

    @property
    def workingCode(self):
        return self._workingCode

    @workingCode.setter
    def workingCode(self, workingCode):
        if workingCode is not None and (workingCode < 0 or workingCode > 15):
            raise ValueError("workingCode must be between 0 and 15")
        self._workingCode = workingCode

    @property
    def nioBits(self):
        return self._nioBits

    @nioBits.setter
    def nioBits(self, nioBits):
        self._nioBits = nioBits

    @property
    def machineId(self):
        return self._machineId

    @machineId.setter
    def machineId(self, machineId):
        self._machineId = machineId

    def update(self, telegram):
        node = ET.fromstring(telegram)
        resHead_node = node.find("body/structs/resHead")

        if resHead_node is None:
            raise ValueError("Telegram does not contain a resHead node")
        if self._result is not None:
            resHead_node.set("result", str(self.result))
        if self._typeNo is not None:
            resHead_node.set("typeNo", str(self.typeNo))
        if self._typeVar is not None:
            resHead_node.set("typeVar", str(self.typeVar))
        if self._workingCode is not None:
            resHead_node.set("workingCode", str(self.workingCode))
        if self._nioBits is not None:
            resHead_node.set("nioBits", str(self.nioBits))
        if self._machineId is not None:
            resHead_node.set("machineId", str(self.machineId))
        return ET.tostring(node)


def NewOpConResHead(
    opConEvent=None,
    result=None,
    typeNo=None,
    typeVar=None,
    workingCode=None,
    nioBits=None,
    machineId=None,
) -> OpConResHead:
    resHead = OpConResHead()
    if opConEvent is not None:
        resHead.typeNo = opConEvent.typeNo
        resHead.typeVar = opConEvent.typeVar
    if result is not None:
        resHead.result = result
    if typeNo is not None:
        resHead.typeNo = typeNo
    if typeVar is not None:
        resHead.typeVar = typeVar
    if workingCode is not None:
        resHead.workingCode = workingCode
    if nioBits is not None:
        resHead.nioBits = nioBits
    if machineId is not None:
        resHead.machineId = machineId
    return resHead


class OpConItem:
    VALID_DATA_TYPES = [2, 3, 4, 5, 7, 8, 11, 14, 16, 17, 18, 19, 20, 21]

    def __init__(self, name=None, value=None, dataType=None):
        self.name = name
        self.value = value
        self.dataType = dataType

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, dataType):
        if dataType is not None and dataType not in self.VALID_DATA_TYPES:
            raise ValueError(f"Invalid dataType: {dataType}")
        self._dataType = dataType

    def update(self, telegram):
        node = ET.fromstring(telegram)
        item_node = node.findall("body/items/item")
        itemsNames = [item.get("name") for item in item_node]

        if self.name is not None and self.name not in itemsNames:
            items_node = node.find("body/items")
            if items_node is None:
                raise ValueError("Telegram does not contain an items node")
            new_item = ET.SubElement(items_node, "item")
            new_item.set("name", str(self.name))
            if self.value is not None:
                new_item.set("value", str(self.value))
            if self.dataType is not None:
                new_item.set("dataType", str(self.dataType))

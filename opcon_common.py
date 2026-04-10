import re
import json
import xml.etree.ElementTree as ET
from opcon_enums import LabelType, OpConTestComparator


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

        attrs = {
            "lineNo": self.lineNo,
            "statNo": self.statNo,
            "statIdx": self.statIdx,
            "fuNo": self.fuNo,
            "workPos": self.workPos,
            "toolPos": self.toolPos,
            "application": self.application,
            "processName": self.processName,
            "processNo": self.processNo,
        }
        for attr_name, value in attrs.items():
            if value is not None:
                node.set(attr_name, str(value))
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

    # TODO: validate if should use __eq__ or ==
    def __eq__(self, other) -> bool:
        if (
            self.name == other.name
            and self.value == other.value
            and self.dataType == other.dataType
        ):
            return True
        return False

    def __str__(self):
        return json.dumps(
            {"name": self.name, "value": self.value, "dataType": self.dataType}
        )


def NewOpConItem(name, value=None, dataType=None) -> OpConItem:
    opconItem = OpConItem()
    opconItem.name = name
    if value is not None:
        opconItem.value = value
    if dataType is not None:
        opconItem.dataType = dataType
    return opconItem


def NewOpConMaterialItems(label, labelType=LabelType.MAT):
    class MaterialItem:
        def __init__(self, valuePrefix, itemName, itemDefaultValue, itemDataType):
            self._valuePrefix = valuePrefix
            self._itemName = itemName
            self._itemDefaultValue = itemDefaultValue
            self._itemDataType = itemDataType

        @property
        def valuePrefix(self):
            return self._valuePrefix

        @property
        def itemName(self):
            return self._itemName

        @property
        def itemDefaultValue(self):
            return self._itemDefaultValue

        @property
        def itemDataType(self):
            return self._itemDataType

    materials = []
    if labelType == LabelType.MAT:
        materials.append(MaterialItem("@1T(.*)@2T", "Component1.Batch1", "", 8))
        materials.append(MaterialItem("@2T(.*)@1Z", "Component1.Batch2", "", 8))
        materials.append(MaterialItem("@20T(.*)@1T", "Component1.BatchCounter", "0", 3))
        materials.append(
            MaterialItem("@14D(.*)@30P", "Component1.ExpirationDate", "", 8)
        )
        materials.append(MaterialItem("@12V(.*)@10V", "Component1.Manufacturer", "", 8))
        materials.append(
            MaterialItem("@10V(.*)@2P", "Component1.ManufacturerLocation", "", 8)
        )
        materials.append(
            MaterialItem("@1P(.*)@31P", "Component1.ManufacturerTypeNo", "", 8)
        )
        materials.append(MaterialItem("@Z(.*)@K", "Component1.MsLevel", "", 8))
        materials.append(MaterialItem("@31P(.*)@12V", "Component1.OrderingNo", "", 8))
        materials.append(MaterialItem("@3S(.*)@Q", "Component1.PackageId", "", 8))
        materials.append(MaterialItem("@20P(.*)@6D", "Component1.PartAddInfo", "", 8))
        materials.append(
            MaterialItem("@6D(.*)@14D", "Component1.ProductionDate", "", 8)
        )
        materials.append(
            MaterialItem("@K(.*)@16K", "Component1.PurchaseOrderNo", "", 8)
        )
        materials.append(
            MaterialItem("@Q(\\d*)\\D*\\d*@20T", "Component1.Quantity", "0.0", 5)
        )
        materials.append(
            MaterialItem("@Q(\\d*)\\D*\\d*@20T", "Component1.QuantityRaw", "0.0", 5)
        )
        materials.append(
            MaterialItem("@Q\\d*(\\D*)\\d*@20T", "Component1.QuantityUnit", "", 8)
        )
        materials.append(
            MaterialItem("@Q\\d*(\\D*)\\d*@20T", "Component1.QuantityUnitRaw", "", 8)
        )
        materials.append(MaterialItem("@30P(.*)@Z", "Component1.RoHS", "", 8))
        materials.append(MaterialItem("@16K(.*)@V", "Component1.ShippingNoteNo", "", 8))
        materials.append(MaterialItem("@1Z(.*)@@", "Component1.SupplierData", "", 8))
        materials.append(MaterialItem("@V(.*)@3S", "Component1.SupplierId", "", 8))
        materials.append(MaterialItem("@P(.*)@1P", "Component1.TypeNo", "", 8))
        materials.append(MaterialItem("@2P(.*)@20P", "Component1.TypeVar", "", 8))
        materials.append(MaterialItem("", "labelFormat", "2", 3))
        materials.append(MaterialItem("@12S(.*)@P", "labelVersion", "2", 3))

    if labelType == LabelType.GTL:
        materials.append(MaterialItem("1T(.*)Q", "Component1.Batch1", "", 8))
        materials.append(MaterialItem("", "Component1.Batch2", "", 8))
        materials.append(MaterialItem("", "Component1.BatchCounter", "0", 3))
        materials.append(MaterialItem("14D(.*)16D", "Component1.ExpirationDate", "", 8))
        materials.append(MaterialItem("12V(.*)1P", "Component1.Manufacturer", "", 8))
        materials.append(MaterialItem("", "Component1.ManufacturerLocation", "", 8))
        materials.append(MaterialItem("1P(.*)33T", "Component1.ManufacturerTypeNo", "", 8))
        materials.append(MaterialItem("", "Component1.MsLevel", "", 8))
        materials.append(MaterialItem("K(.*)4K", "Component1.OrderingNo", "", 8))
        materials.append(MaterialItem("1J(.*)14D", "Component1.PackageId", "", 8))
        materials.append(MaterialItem("23P(.*)30P", "Component1.PartAddInfo", "", 8))
        materials.append(MaterialItem("16D(.*)P", "Component1.ProductionDate", "", 8))
        materials.append(MaterialItem("K(.*)16K", "Component1.PurchaseOrderNo", "", 8))
        materials.append(MaterialItem("Q(.*)3Q", "Component1.Quantity", "0.0", 5))
        materials.append(MaterialItem("Q(.*)3Q", "Component1.QuantityRaw", "0.0", 5))
        materials.append(MaterialItem("3Q(.*)K", "Component1.QuantityUnit", "", 8))
        materials.append(MaterialItem("3Q(.*)K", "Component1.QuantityUnitRaw", "", 8))
        materials.append(MaterialItem("", "Component1.RoHS", "0", 8))
        materials.append(MaterialItem("2K(.*)23P", "Component1.ShippingNoteNo", "", 8))
        materials.append(MaterialItem("1Z(.*)", "Component1.SupplierData", "", 8))
        materials.append(MaterialItem("V(.*)13V", "Component1.SupplierId", "", 8))
        materials.append(MaterialItem("P(.*)2P", "Component1.TypeNo", "", 8))
        materials.append(MaterialItem("2P(.*)1T", "Component1.TypeVar", "", 8))
        materials.append(MaterialItem("", "labelFormat", "2", 3))
        materials.append(MaterialItem("", "labelVersion", "4992", 3))
        materials.append(MaterialItem("13V(.*)7Q", "Component1.SupplierIdDUNS", "", 8))

    for mat in materials:
        m = re.match(mat.valuePrefix, label)
        v = m.group(1) if m else mat.itemDefaultValue
        yield NewOpConItem(name=mat.itemName, value=v, dataType=mat.itemDataType)


class OpConStructArray:
    def __init__(self, name=None, structDef=None, data=None):
        self.name = name
        self.structDef = structDef
        self.data = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def structDef(self):
        return self._structDef

    @structDef.setter
    def structDef(self, structDef):
        self._structDef = structDef

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def update(self, telegram):
        arrayName = self.name
        tree = ET.fromstring(telegram)
        values = tree.find(f"body/structArrays/array[@name='{arrayName}']/values")
        if values is None:
            return

        for structData in self.data:
            for node in values:
                has = True
                for selector, value in structData["selectors"].items():
                    has = has and (node.get(selector) == value)

                if has:
                    for attr, val in structData["attributes"].items():
                        node.set(attr, val)

        return ET.tostring(tree)

    def __eq__(self, other) -> bool:
        if self.name == other.name:
            if self.structDef == other.structDef:
                if self.data == other.data:
                    return True
                return False
            return False
        return False

    def __str__(self):
        return json.dumps(
            {"name": self.name, "structDef": self.structDef, "data": self.data}
        )


def NewOpConStructArray(name):
    structArray = OpConStructArray()
    structArray.name = name
    structArray.data = []
    return structArray


class OpConStructArrayValue:
    def __init__(self, selectors=None, attributes=None):
        self.selectors = selectors
        self.attributes = attributes

    @property
    def selectors(self):
        return self._selectors

    @selectors.setter
    def selectors(self, selectors):
        self._selectors = selectors

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes


def AddOpConStructArrayValue(structArray, selectors, attributes):
    structArrayValues = OpConStructArrayValue()
    structArrayValues.selectors = selectors
    structArrayValues.attributes = attributes
    structArray.data.append(structArrayValues)
    return structArray


def AddOpConStructArrayStructDef(structArray, name, dataType):
    structArrayValues = OpConStructArrayValue()
    structArrayValues.attributes = {"name": name, "dataType": str(dataType)}
    structArray.structDef.append(structArrayValues)
    return structArray


def AddOpConStructArrayResult(structArray, selectors, pos=1, result=1, nioBits=0, identifier=None, targetIdx=1, state=4):
    structArrayValue = OpConStructArrayValue()
    structArrayValue.selectors = selectors
    structArrayValue.attributes = {
        "pos": pos,
        "result": result,
        "nioBits": nioBits,
        "identifier": identifier,
        "targetIdx": targetIdx,
        "state": state
        }

    structArray.data.append(structArrayValue)
    return structArray


def NewOpConResultsStructArray(group):
    results = NewOpConStructArray("results")
    for part in group.parts:
        selectors = {"pos": str(part.pos)}
        AddOpConStructArrayResult(results, selectors=selectors, pos=part.pos, identifier=part.identifier)
    return results


class OpConArray:
    def __init__(self, name=None, dataType=None, data=None):
        self.name = name
        self.dataType = dataType
        self.data = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def dataType(self):
        return self._dataType

    @dataType.setter
    def dataType(self, dataType):
        self._dataType = dataType

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    def update(self, telegram):
        arrayName = self.name
        tree = ET.fromstring(telegram)
        values = tree.find(f"body/{arrayName}")
        valuesSubArray = tree.find(f"body/arrays/array[@name='{arrayName}']")

        if values is None or valuesSubArray is None:
            return

        for value in self.data:
            for node in values:
                has = True
                for selector in value.selectors.keys():
                    has = has and (node.get(selector) == value.selectors[selector])

                if has:
                    data = value
                    for attr in data.attributes.keys():
                        node.set(attr, data.attributes[attr])

        for value in self.data:
            for node in valuesSubArray:
                has = True
                for selector in value.selectors.keys():
                    has = has and (node.get(selector) == value.selectors[selector])

                if has:
                    data = value
                    for attr in data.attributes.keys():
                        node.set(attr, data.attributes[attr])
        return ET.tostring(tree)

    def __eq__(self, other) -> bool:
        if (self.name == other.name) and (self.dataType == other.dataType) and (self.data == other.data):
            return True
        return False

    def __str__(self) -> str:
        return json.dumps(
            {"name": self.name, "dataType": self.dataType, "data": self.data}
        )


class OpConArrayValue:
    def __init__(self, selectors=None, attributes=None):
        self.selectors = selectors
        self.attributes = attributes

    @property
    def selectors(self):
        return self._selectors

    @selectors.setter
    def selectors(self, selectors):
        self._selectors = selectors

    @property
    def attributes(self):
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes


def NewOpConArray(name, dataType):
    opConArray = OpConArray()
    opConArray.name = name
    opConArray.dataType = dataType
    opConArray.data = []
    return opConArray


def AddOpConArrayValue(array, selectors, attributes):
    arrayValue = OpConArrayValue()
    arrayValue.selectors = selectors
    arrayValue.attributes = attributes
    array.data.append(arrayValue)
    return array


class OpConPart:
    def __init__(self, pos=None, identifier=None):
        self.pos = pos
        self.identifier = identifier

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        self._pos = pos

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier


class OpConGroup:
    def __init__(self, identifier=None, parts=None):
        self.identifier = identifier
        self.parts = parts

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        self._identifier = identifier

    @property
    def parts(self):
        return self._parts

    @parts.setter
    def parts(self, parts):
        self._parts = parts


def NewOpConGroups(idetifier, format, start=1, parts=0, count=0):
    for i in range(0, count, 1):
        groupIdentifier = f"{idetifier}{format}".format(0, i + start)
        partsArray = []
        for j in range(0, parts, 1):
            partIdentifier = f"{idetifier}{format}".format(j + 1, i + start)
            partObject = OpConPart((j + 1), partIdentifier)
            partsArray.append(partObject)
        groupObject = OpConGroup(groupIdentifier, partsArray)
        return groupObject


def GetOpConPartsInGroups(groups):
    for group in groups:
        for part in group.parts:
            yield part


def EditOpConTelegram(telegram, eventData=None, header=None,
                      location=None, resHead=None, items=None, structArrays=None, arrays=None):
    if eventData is not None:
        telegram = eventData.update(telegram)

    if header is not None:
        telegram = header.update(telegram)

    if location is not None:
        telegram = location.update(telegram)

    if resHead is not None:
        telegram = resHead.update(telegram)

    if items is not None:
        for item in items:
            telegram = item.update(telegram)

    if structArrays is not None:
        for structArray in structArrays:
            telegram = structArray.update(telegram)

    if arrays is not None:
        for array in arrays:
            telegram = array.update(telegram)

    return telegram


class OpConTestRuleResult:
    def __init__(self, rule=None, value=None, request=None, response=None, ok=None):
        self.rule = rule
        self.value = value
        self.request = request
        self.response = response
        self.ok = ok

    @property
    def rule(self):
        return self._rule

    @rule.setter
    def rule(self, rule):
        self._rule = rule

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def request(self):
        return self._request

    @request.setter
    def request(self, request):
        self._request = request

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response):
        self._response = response

    @property
    def ok(self):
        return self._ok

    @ok.setter
    def ok(self, ok):
        self._ok = ok

    def __str__(self):
        return json.dumps({
            "rule": self.rule,
            "value": self.value,
            "request": self.request,
            "response": self.response,
            "ok": self.ok
        })


class OpConTestRule:
    def __init__(self, xpath=None, negative=None, comparator=None, value=None):
        self.xpath = xpath
        self.negative = negative
        self.comparator = comparator
        self.value = value

    @property
    def xpath(self):
        return self._xpath

    @xpath.setter
    def xpath(self, xpath):
        self._xpath = xpath

    @property
    def negative(self):
        return self._negative

    @negative.setter
    def negative(self, negative):
        self._negative = negative

    @property
    def comparator(self):
        return self._comparator

    @comparator.setter
    def comparator(self, comparator):
        self._comparator = comparator

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def execute(self, request, telegram):
        if (self.xpath is None):
            raise ValueError("xpath must be defined to execute the test rule")

        ok = False
        tree = ET.fromstring(telegram)
        node = tree.find(self.xpath)

        if node is not None:
            if node.text:
                val = node.text
            else:
                # Get inner XML (equivalent to InnerXml)
                val = (node.text or '') + ''.join(ET.tostring(child, encoding='unicode') for child in node)

            if val is None:
                val = ""
            if self.value is None:
                self.value = ""

            if self.comparator == OpConTestComparator.EQ:
                if (val):
                    ok = val == self.value
            elif self.comparator == OpConTestComparator.NEQ:
                if (val):
                    ok = val != self.value
            elif self.comparator == OpConTestComparator.Contains:
                if (val):
                    ok = self.value in val
            elif self.comparator == OpConTestComparator.Absent:
                if (not val):
                    ok = True
            elif self.comparator == OpConTestComparator.Exists:
                if (val):
                    ok = True
            else:
                raise ValueError(f"Unsupported comparator: {self.comparator}")

            rule = OpConTestRuleResult()
            rule.rule = self
            rule.request = request
            rule.response = telegram
            rule.ok = ok
            rule.value = val
            return rule
        else:
            raise ValueError(f"XPath '{self.xpath}' did not match any nodes in the telegram")

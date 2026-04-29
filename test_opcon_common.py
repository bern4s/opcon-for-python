import pytest
import xml.etree.ElementTree as ET
import opcon_common
import json


class TestOpConHeader:
    HEADER_NUMBER = 999

    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpConBasic.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_create_simple_header(self):
        header = opcon_common.NewOpConHeader(self.HEADER_NUMBER)
        assert header.event_switch == self.HEADER_NUMBER

    def test_update_header(self):
        header = opcon_common.NewOpConHeader(self.HEADER_NUMBER)
        updated_telegram = header.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        header_node = parsed_xml.find("header")

        assert header_node is not None
        telegram_event_switch = header_node.get("eventSwitch")
        assert telegram_event_switch == str(self.HEADER_NUMBER)

    def test_invalid_header_event_switch(self):
        with pytest.raises(ValueError, match="event_switch must be a positive integer"):
            opcon_common.NewOpConHeader(-1)


class TestOpConLocation:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpConBasic.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_create_simple_location(self):
        location = opcon_common.NewOpConLocation(
            lineNo=666,
            statNo=9999,
            statIdx=1,
            fuNo=1,
            workPos=1,
            toolPos=1,
            application="PLC",
            processName="Test",
            processNo=0,
        )

        assert location._lineNo == 666
        assert location._statNo == 9999
        assert location._statIdx == 1
        assert location._fuNo == 1
        assert location._workPos == 1
        assert location._toolPos == 1
        assert location._application == "PLC"
        assert location._processName == "Test"
        assert location._processNo == 0

    def test_update_location(self):
        location = opcon_common.NewOpConLocation(
            lineNo=1234,
            statNo=888,
            statIdx=50,
            fuNo=5,
            workPos=6,
            toolPos=8,
            application="Test_App",
            processName="Test_Loc",
            processNo=555,
        )
        updated_telegram = location.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        location_node = parsed_xml.find("header/location")

        assert location_node is not None
        assert location_node.get("lineNo") == "1234"
        assert location_node.get("statNo") == "888"
        assert location_node.get("statIdx") == "50"
        assert location_node.get("fuNo") == "5"
        assert location_node.get("workPos") == "6"
        assert location_node.get("toolPos") == "8"
        assert location_node.get("application") == "Test_App"
        assert location_node.get("processName") == "Test_Loc"
        assert location_node.get("processNo") == "555"

    def test_location_id(self):
        locationId = "666.321.123.5.564.897"
        location = opcon_common.NewOpConLocation(
            locationId=locationId,
            application="Test_App",
            processName="Test_Loc",
            processNo=555,
        )

        assert location._lineNo == 666
        assert location._statNo == 321
        assert location._statIdx == 123
        assert location._fuNo == 5
        assert location._workPos == 564
        assert location._toolPos == 897
        assert location._application == "Test_App"
        assert location._processName == "Test_Loc"
        assert location._processNo == 555

    def test_update_location_id(self):
        locationId = "666.321.123.5.564.897"
        location = opcon_common.NewOpConLocation(
            locationId=locationId,
            application="Test_App",
            processName="Test_Loc",
            processNo=555,
        )
        updated_telegram = location.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        location_node = parsed_xml.find("header/location")

        assert location_node is not None
        assert location_node.get("lineNo") == "666"
        assert location_node.get("statNo") == "321"
        assert location_node.get("statIdx") == "123"
        assert location_node.get("fuNo") == "5"
        assert location_node.get("workPos") == "564"
        assert location_node.get("toolPos") == "897"
        assert location_node.get("application") == "Test_App"
        assert location_node.get("processName") == "Test_Loc"
        assert location_node.get("processNo") == "555"

    def test_invalid_location_fuNo(self):
        with pytest.raises(ValueError, match="fuNo must be between 1 and 9"):
            opcon_common.NewOpConLocation(
                lineNo=1234,
                statNo=888,
                statIdx=50,
                fuNo=10,
                workPos=6,
                toolPos=8,
                application="Test_App",
                processName="Test_Loc",
                processNo=555,
            )


class TestOpConResHead:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_create_simple_res_head(self):
        res_head = opcon_common.NewOpConResHead(
            result=1,
            typeNo=100,
            typeVar="0001",
            workingCode=13,
            nioBits=2,
            machineId="Machine_1",
        )
        assert res_head.result == 1
        assert res_head.typeNo == 100
        assert res_head.typeVar == "0001"
        assert res_head.workingCode == 13
        assert res_head.nioBits == 2
        assert res_head.machineId == "Machine_1"

    def test_update_res_head(self):
        res_head = opcon_common.NewOpConResHead(
            result=12, typeNo=200, typeVar="Test_Res"
        )
        updated_telegram = res_head.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        res_head_node = parsed_xml.find("body/structs/resHead")

        assert res_head_node is not None
        assert res_head_node.get("result") == "12"
        assert res_head_node.get("typeNo") == "200"
        assert res_head_node.get("typeVar") == "Test_Res"

    def test_invalid_result(self):
        with pytest.raises(ValueError, match="result must be one of"):
            o = opcon_common.NewOpConResHead(typeNo=100, typeVar="Test")
            o.result = 888

    def test_invalid_working_code(self):
        with pytest.raises(ValueError, match="workingCode must be between 0 and 15"):
            o = opcon_common.NewOpConResHead(typeNo=100, typeVar="Test")
            o.workingCode = 300

    def test_use_created_res_head(self):
        res_head = opcon_common.NewOpConResHead(
            opConEvent=opcon_common.OpConResHead(typeNo=1234, typeVar="0009"),
            result=1,
            machineId="Machine_99",
        )
        assert res_head.typeNo == 1234
        assert res_head.typeVar == "0009"
        assert res_head.result == 1
        assert res_head.machineId == "Machine_99"


class TestOpConItem:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_opcon_item_str(self):
        packageIdItem = opcon_common.NewOpConItem("Component1.PackageId", 123456489, 16)
        assert packageIdItem.__str__() == json.dumps(
            {
                "name": packageIdItem.name,
                "value": packageIdItem.value,
                "dataType": packageIdItem.dataType,
            }
        )

    def test_opcon_item_equality(self):
        item1 = opcon_common.NewOpConItem("Component1.PackageId", 123456489, 16)
        item2 = opcon_common.NewOpConItem("Component1.PackageId", 123456489, 16)
        item3 = opcon_common.NewOpConItem("Component1.PackageId", 987654321, 16)

        assert item1 == item2
        assert item1 != item3

    def test_opcon_item_update(self):
        VALID_DATA_TYPES = [2, 3, 4, 5, 7, 8, 11, 14, 16, 17, 18, 19, 20, 21]

        for data_type in VALID_DATA_TYPES:
            testItem = opcon_common.NewOpConItem("Test.Item", "TestValue", data_type)
            updatedTelegram = testItem.update(self.telegram)
            updatedTelegram = ET.fromstring(updatedTelegram)
            targetNode = updatedTelegram.find("body/items/item[@name='Test.Item']")
            assert targetNode is not None
            assert targetNode.get("value") == "TestValue"
            assert targetNode.get("dataType") == str(data_type)

    def test_opcon_item_update_no_data_type(self):
        testItem = opcon_common.NewOpConItem("Test.Item", "TestValue")
        updatedTelegram = testItem.update(self.telegram)
        updatedTelegram = ET.fromstring(updatedTelegram)
        targetNode = updatedTelegram.find("body/items/item[@name='Test.Item']")
        assert targetNode is not None
        assert targetNode.get("value") == "TestValue"
        assert targetNode.get("dataType") is None

    def test_opcon_item_update_existing_item(self):
        testItem = opcon_common.NewOpConItem("routeList", "testRouteList", 16)
        updatedTelegram = testItem.update(self.telegram)
        updatedTelegram = ET.fromstring(updatedTelegram)
        numChildItems = len(updatedTelegram.findall("body/items/item"))
        targetNode = updatedTelegram.find("body/items/item[@name='routeList']")
        assert numChildItems == 3
        assert targetNode is not None
        assert targetNode.get("value") == "testRouteList"
        assert targetNode.get("dataType") == "16"

    def test_opcon_item_invalid_data_type(self):
        invlid_data_types = [1, 6, 9, 10]
        for dataType in invlid_data_types:
            with pytest.raises(ValueError, match=f"Invalid dataType: {dataType}"):
                opcon_common.NewOpConItem("Test.Item", "TestValue", dataType)


class TestOpConMaterialItems:
    def test_opcon_material_items_mat_label(self):
        SUPPLIER_ID = "1111122222"
        BATCH_1 = "TestBatch1"
        BATCH_2 = "TestBatch2"
        BATCH_COUNTER = 50
        EXPIRATION_DATE = "20501231"
        MANUFACTURER = "TestManufacturer"
        MANUFACTURER_LOCATION = "AUT-KORNEUBURG"
        MANUFACTURER_TYPE_NO = "123456789"
        MSL_LEVEL = 5
        ORDERING_NO = "987654321"
        PACKAGE_ID = "B555666444"
        PART_ADD_INFO = "TestPartAddInfo"
        PRODUCTION_DATE = "20240101"
        PURCHASE_ORDER_NO = "V465"
        QUANTITY = 100
        QUANTITY_UNIT = "NAR"
        QUANTITY_FLOAT = 500
        ROHS = "Y"
        SHIPPING_NOTE_NO = "SN1234567890"
        SUPPLIER_DATA = "TestSupplierData"
        TYPE_NO = "1234567890"
        TYPE_VAR = "08"
        LABEL_VERSION = "0002"

        items = list(
            opcon_common.NewOpConMaterialItems(
                f"""[)>@06@12S{LABEL_VERSION}@P{TYPE_NO}@1P{MANUFACTURER_TYPE_NO}@31P{ORDERING_NO}@12V{MANUFACTURER}@10V{MANUFACTURER_LOCATION}@2P{TYPE_VAR}@20P{PART_ADD_INFO}@6D{PRODUCTION_DATE}@14D{EXPIRATION_DATE}@30P{ROHS}@Z{MSL_LEVEL}@K{PURCHASE_ORDER_NO}@16K{SHIPPING_NOTE_NO}@V{SUPPLIER_ID}@3S{PACKAGE_ID}@Q{QUANTITY}{QUANTITY_UNIT}{QUANTITY_FLOAT}@20T{BATCH_COUNTER}@1T{BATCH_1}@2T{BATCH_2}@1Z{SUPPLIER_DATA}@@"""
            )
        )

        supplierIdItem = next(
            (item for item in items if item.name == "Component1.SupplierId"), None
        )
        assert supplierIdItem is not None
        assert supplierIdItem.value == SUPPLIER_ID

        batch1Item = next(
            (item for item in items if item.name == "Component1.Batch1"), None
        )
        assert batch1Item is not None
        assert batch1Item.value == BATCH_1

        batch2Item = next(
            (item for item in items if item.name == "Component1.Batch2"), None
        )
        assert batch2Item is not None
        assert batch2Item.value == BATCH_2

        batchCounterItem = next(
            (item for item in items if item.name == "Component1.BatchCounter"), None
        )
        assert batchCounterItem is not None
        assert int(batchCounterItem.value) == BATCH_COUNTER

        expirationDateItem = next(
            (item for item in items if item.name == "Component1.ExpirationDate"), None
        )
        assert expirationDateItem is not None
        assert expirationDateItem.value == EXPIRATION_DATE

        manufacturerItem = next(
            (item for item in items if item.name == "Component1.Manufacturer"), None
        )
        assert manufacturerItem is not None
        assert manufacturerItem.value == MANUFACTURER

        manufacturerLocationItem = next(
            (item for item in items if item.name == "Component1.ManufacturerLocation"),
            None,
        )
        assert manufacturerLocationItem is not None
        assert manufacturerLocationItem.value == MANUFACTURER_LOCATION

        manufacturerTypeNoItem = next(
            (item for item in items if item.name == "Component1.ManufacturerTypeNo"),
            None,
        )
        assert manufacturerTypeNoItem is not None
        assert manufacturerTypeNoItem.value == MANUFACTURER_TYPE_NO

        mslLevelItem = next(
            (item for item in items if item.name == "Component1.MsLevel"), None
        )
        assert mslLevelItem is not None
        assert int(mslLevelItem.value) == MSL_LEVEL

        orderingNoItem = next(
            (item for item in items if item.name == "Component1.OrderingNo"), None
        )
        assert orderingNoItem is not None
        assert orderingNoItem.value == ORDERING_NO

        packageIdItem = next(
            (item for item in items if item.name == "Component1.PackageId"), None
        )
        assert packageIdItem is not None
        assert packageIdItem.value == PACKAGE_ID

        partAddInfoItem = next(
            (item for item in items if item.name == "Component1.PartAddInfo"), None
        )
        assert partAddInfoItem is not None
        assert partAddInfoItem.value == PART_ADD_INFO

        productionDateItem = next(
            (item for item in items if item.name == "Component1.ProductionDate"), None
        )
        assert productionDateItem is not None
        assert productionDateItem.value == PRODUCTION_DATE

        purchaseOrderNoItem = next(
            (item for item in items if item.name == "Component1.PurchaseOrderNo"), None
        )
        assert purchaseOrderNoItem is not None
        assert purchaseOrderNoItem.value == PURCHASE_ORDER_NO

        # FIXME: Update logic to handle the decimal part
        quantityItem = next(
            (item for item in items if item.name == "Component1.Quantity"), None
        )
        assert quantityItem is not None
        assert int(quantityItem.value) == QUANTITY

        quantityUnitItem = next(
            (item for item in items if item.name == "Component1.QuantityUnit"), None
        )
        assert quantityUnitItem is not None
        assert quantityUnitItem.value == QUANTITY_UNIT

        rohsItem = next(
            (item for item in items if item.name == "Component1.RoHS"), None
        )
        assert rohsItem is not None
        assert rohsItem.value == ROHS

        shippingNoteNoItem = next(
            (item for item in items if item.name == "Component1.ShippingNoteNo"), None
        )
        assert shippingNoteNoItem is not None
        assert shippingNoteNoItem.value == SHIPPING_NOTE_NO

        supplierDataItem = next(
            (item for item in items if item.name == "Component1.SupplierData"), None
        )
        assert supplierDataItem is not None
        assert supplierDataItem.value == SUPPLIER_DATA

        typeNoItem = next(
            (item for item in items if item.name == "Component1.TypeNo"), None
        )
        assert typeNoItem is not None
        assert typeNoItem.value == TYPE_NO

        typeVarItem = next(
            (item for item in items if item.name == "Component1.TypeVar"), None
        )
        assert typeVarItem is not None
        assert typeVarItem.value == TYPE_VAR

        labelVersionItem = next(
            (item for item in items if item.name == "labelVersion"), None
        )
        assert labelVersionItem is not None
        assert labelVersionItem.value == LABEL_VERSION

    def test_opcon_material_items_gtl_label(self):
        BATCH_1 = "TestBatch1"
        EXPIRATION_DATE = "20251229"
        MANUFACTURER = "TestManufacturer"
        MANUFACTURER_TYPE_NO = "123456789"
        ORDERING_NO = "987654321"
        PACKAGE_ID = "UNFAS3BRG826000063419"
        PART_ADD_INFO = "TestPartAddInfo"
        PRODUCTION_DATE = "20240101"
        QUANTITY = 129
        QUANTITY_UNIT = "EA"
        SHIPPING_NOTE_NO = "SN1234567890"
        GROSS_WEIGHT_KG = 5.0
        SUPPLIER_ID = "097135674"
        TYPE_NO = "1234567890"
        TYPE_VAR = "08"
        SUPPLIER_ID_DUNS = "097135674"

        items = list(
            opcon_common.NewOpConMaterialItems(
                f"""[)>0612PGTL39K121J{PACKAGE_ID}14D{EXPIRATION_DATE}16D{PRODUCTION_DATE}P{TYPE_NO}2P{TYPE_VAR}1T{BATCH_1}Q{QUANTITY}3Q{QUANTITY_UNIT}K{ORDERING_NO}4K0012SGY202212310115K123V{SUPPLIER_ID}13V{SUPPLIER_ID_DUNS}7Q{GROSS_WEIGHT_KG}2K{SHIPPING_NOTE_NO}23P{PART_ADD_INFO}30PNA12V{MANUFACTURER}1P{MANUFACTURER_TYPE_NO}33TY
                """, labelType=opcon_common.LabelType.GTL
            )
        )

        batch1Item = next(
            (item for item in items if item.name == "Component1.Batch1"), None
        )
        assert batch1Item is not None
        assert batch1Item.value == BATCH_1

        expirationDateItem = next(
            (item for item in items if item.name == "Component1.ExpirationDate"), None
        )
        assert expirationDateItem is not None
        assert expirationDateItem.value == EXPIRATION_DATE

        manufacturerItem = next(
            (item for item in items if item.name == "Component1.Manufacturer"), None
        )
        assert manufacturerItem is not None
        assert manufacturerItem.value == MANUFACTURER

        manufacturerTypeNoItem = next(
            (item for item in items if item.name == "Component1.ManufacturerTypeNo"), None,
        )
        assert manufacturerTypeNoItem is not None
        assert manufacturerTypeNoItem.value == MANUFACTURER_TYPE_NO

        orderingNoItem = next(
            (item for item in items if item.name == "Component1.OrderingNo"), None
        )
        assert orderingNoItem is not None
        assert orderingNoItem.value == ORDERING_NO

        packageIdItem = next(
            (item for item in items if item.name == "Component1.PackageId"), None
        )
        assert packageIdItem is not None
        assert packageIdItem.value == PACKAGE_ID

        partAddInfoItem = next(
            (item for item in items if item.name == "Component1.PartAddInfo"), None
        )
        assert partAddInfoItem is not None
        assert partAddInfoItem.value == PART_ADD_INFO

        productionDateItem = next(
            (item for item in items if item.name == "Component1.ProductionDate"), None
        )
        assert productionDateItem is not None
        assert productionDateItem.value == PRODUCTION_DATE

        quantityItem = next(
            (item for item in items if item.name == "Component1.Quantity"), None
        )
        assert quantityItem is not None
        assert int(quantityItem.value) == QUANTITY

        quantityUnitItem = next(
            (item for item in items if item.name == "Component1.QuantityUnit"), None
        )
        assert quantityUnitItem is not None
        assert quantityUnitItem.value == QUANTITY_UNIT

        shippingNoteNoItem = next(
            (item for item in items if item.name == "Component1.ShippingNoteNo"), None
        )
        assert shippingNoteNoItem is not None
        assert shippingNoteNoItem.value == SHIPPING_NOTE_NO

        grossWeightKgItem = next(
            (item for item in items if item.name == "Component1.GrossWeightKg"), None
        )
        assert grossWeightKgItem is not None
        assert float(grossWeightKgItem.value) == GROSS_WEIGHT_KG

        supplierIdItem = next(
            (item for item in items if item.name == "Component1.SupplierId"), None
        )
        assert supplierIdItem is not None
        assert supplierIdItem.value == SUPPLIER_ID

        typeNoItem = next(
            (item for item in items if item.name == "Component1.TypeNo"), None
        )
        assert typeNoItem is not None
        assert typeNoItem.value == TYPE_NO

        typeVarItem = next(
            (item for item in items if item.name == "Component1.TypeVar"), None
        )
        assert typeVarItem is not None
        assert typeVarItem.value == TYPE_VAR

        supplierIdDunsItem = next(
            (item for item in items if item.name == "Component1.SupplierIdDUNS"), None
        )
        assert supplierIdDunsItem is not None
        assert supplierIdDunsItem.value == SUPPLIER_ID_DUNS

    def test_invalid_label_type(self):
        with pytest.raises(ValueError, match="Invalid labelType"):
            list(
                opcon_common.NewOpConMaterialItems(
                    """[)>@06@12S0002@P1234567890@1P123456789
                    @31P987654321@12VTestManufacturer
                    @10VTestManufacturerLocation@2P08
                    @20PTestPartAddInfo@6D20240101@14D20251231
                    @30PY@Z5@K987654321@16KSN1234567890
                    @V1111122222@3SUNFAS3BRG826000063419
                    @Q100NAR500.0@20T50@1TTestBatch1@2TTestBatch2
                    @1ZTestSupplierData@@""",
                    labelType="InvalidType",  # type: ignore
                )
            )


class TestOpConStructArray:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_opcon_struct_array(self):
        structArray = opcon_common.NewOpConStructArray("TestStructArray")
        assert structArray.name == "TestStructArray"
        assert structArray.data == []
        assert structArray.structDef == []

    def test_opcon_struct_array_update(self):
        struct_array = opcon_common.NewOpConStructArray("results")
        struct_array.data = {
            "selectors": {
                "pos": "1"
                },
            "attributes": {
                "result": "TestResult",
                "nioBits": "100",
                "identifier": "TestIdentifier",
                "targetIdx": "5",
                "state": "TestState"
                },
        }
        updated_telegram = struct_array.update(self.telegram)
        assert updated_telegram is not None

        updated_telegram = ET.fromstring(updated_telegram.decode("utf-8"))
        targetNode = updated_telegram.find("body/structArrays/array[@name='results']/values/item[@pos='1']")

        assert targetNode is not None
        assert targetNode.get("result") == "TestResult"
        assert targetNode.get("nioBits") == "100"
        assert targetNode.get("identifier") == "TestIdentifier"
        assert targetNode.get("targetIdx") == "5"
        assert targetNode.get("state") == "TestState"

    def test_opcon_struct_array_identifier_update(self):
        struct_array = opcon_common.NewOpConStructArray("results")
        struct_array.data = {
            "selectors": {
                "identifier": "PLS1SZxMILx1023"
                },
            "attributes": {
                "pos": "10",
                "result": "TestResult2",
                "nioBits": "200",
                "targetIdx": "15",
                "state": "TestState1"
                },
        }
        updated_telegram = struct_array.update(self.telegram)
        assert updated_telegram is not None

        updated_telegram = ET.fromstring(updated_telegram.decode("utf-8"))
        targetNode = updated_telegram.find(
            "body/structArrays/array[@name='results']/values/item[@identifier='PLS1SZxMILx1023']"
            )

        assert targetNode is not None
        assert targetNode.get("pos") == "10"
        assert targetNode.get("result") == "TestResult2"
        assert targetNode.get("nioBits") == "200"
        assert targetNode.get("targetIdx") == "15"
        assert targetNode.get("state") == "TestState1"

    def test_opcon_struct_array_no_matching_node(self):
        struct_array = opcon_common.NewOpConStructArray("results")
        struct_array.data = {
            "selectors": {
                "pos": "999"
                },
            "attributes": {
                "result": "TestResult3",
                "nioBits": "300",
                "identifier": "TestIdentifier3",
                "targetIdx": "25",
                "state": "TestState3"
                },
        }
        updated_telegram = struct_array.update(self.telegram)
        assert updated_telegram is not None

        updated_telegram = ET.fromstring(updated_telegram.decode("utf-8"))
        targetNode = updated_telegram.find("body/structArrays/array[@name='results']/values/item[@pos='999']")

        assert targetNode is None

    def test_opcon_struct_array_equality(self):
        struct_array1 = opcon_common.NewOpConStructArray("results")
        struct_array1.data = {
            "selectors": {
                "pos": "1"
                },
            "attributes": {
                "result": "TestResult",
                "nioBits": "100",
                "identifier": "TestIdentifier",
                "targetIdx": "5",
                "state": "TestState"
                },
        }

        struct_array2 = opcon_common.NewOpConStructArray("results")
        struct_array2.data = {
            "selectors": {
                "pos": "1"
                },
            "attributes": {
                "result": "TestResult",
                "nioBits": "100",
                "identifier": "TestIdentifier",
                "targetIdx": "5",
                "state": "TestState"
                },
        }

        struct_array3 = opcon_common.NewOpConStructArray("results")

        assert struct_array1 == struct_array2
        assert struct_array1 != struct_array3

class TestOpConStructArrayValue:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_opcon_struct_array_value(self):
        structArray = opcon_common.NewOpConStructArray("TestStructArray")
        opcon_common.AddOpConStructArrayValue(structArray, {"pos": "1"}, {"result": "TestResult"})
        opcon_common.AddOpConStructArrayValue(structArray, {"pos": "1"}, {"identifier": "testIdentifier"})
        
        assert len(structArray.data) == 2
    
    def test_opcon_struct_array_struct_definition(self):
        structArray = opcon_common.NewOpConStructArray("TestStructArray")
        opcon_common.AddOpConStructArrayStructDef(structArray, "a", "8")
        opcon_common.AddOpConStructArrayStructDef(structArray, "b", "3")
        opcon_common.AddOpConStructArrayStructDef(structArray, "c", "2")
        opcon_common.AddOpConStructArrayStructDef(structArray, "d", "8")
        opcon_common.AddOpConStructArrayStructDef(structArray, "e", "8")
        opcon_common.AddOpConStructArrayStructDef(structArray, "f", "8")
        opcon_common.AddOpConStructArrayStructDef(structArray, "g", "8")

        assert len(structArray.structDef) == 7
    
    def test_opcon_struct_array_result(self):
        structArray = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayResult(
            structArray, 
            {"pos": "1"}, 
            pos=10, 
            result=4, 
            nioBits=2, 
            identifier="TestIdentifier", 
            targetIdx=1, 
            state=4
        )

        assert len(structArray.data) == 1
        assert len(structArray.data[0].attributes.items()) == 6
        telegram = structArray.update(self.telegram)
        assert telegram is not None
        print(telegram.decode("utf-8"))

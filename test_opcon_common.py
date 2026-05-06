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
                """,
                labelType=opcon_common.LabelType.GTL,
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
            (item for item in items if item.name == "Component1.ManufacturerTypeNo"),
            None,
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
        opcon_common.AddOpConStructArrayValue(
            struct_array,
            {"pos": "1"},
            {
                "result": "TestResult",
                "nioBits": "100",
                "identifier": "TestIdentifier",
                "targetIdx": "5",
                "state": "TestState",
            },
        )
        updated_telegram = struct_array.update(self.telegram)
        assert updated_telegram is not None

        updated_telegram = ET.fromstring(updated_telegram.decode("utf-8"))
        targetNode = updated_telegram.find(
            "body/structArrays/array[@name='results']/values/item[@pos='1']"
        )

        assert targetNode is not None
        assert targetNode.get("result") == "TestResult"
        assert targetNode.get("nioBits") == "100"
        assert targetNode.get("identifier") == "TestIdentifier"
        assert targetNode.get("targetIdx") == "5"
        assert targetNode.get("state") == "TestState"

    def test_opcon_struct_array_identifier_update(self):
        struct_array = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayValue(
            struct_array,
            {"identifier": "PLS1SZxMILx1023"},
            {
                "pos": "10",
                "result": "TestResult2",
                "nioBits": "200",
                "targetIdx": "15",
                "state": "TestState1",
            },
        )
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
        opcon_common.AddOpConStructArrayValue(
            struct_array,
            {"pos": "999"},
            {
                "result": "TestResult3",
                "nioBits": "300",
                "identifier": "TestIdentifier3",
                "targetIdx": "25",
                "state": "TestState3",
            },
        )
        updated_telegram = struct_array.update(self.telegram)
        assert updated_telegram is not None

        updated_telegram = ET.fromstring(updated_telegram.decode("utf-8"))
        targetNode = updated_telegram.find(
            "body/structArrays/array[@name='results']/values/item[@pos='999']"
        )

        assert targetNode is None

    def test_opcon_struct_array_equality(self):
        struct_array1 = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayValue(
            struct_array1,
            {"pos": "1"},
            {
                "result": "TestResult",
                "nioBits": "100",
                "identifier": "TestIdentifier",
                "targetIdx": "5",
                "state": "TestState",
            },
        )

        struct_array2 = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayValue(
            struct_array2,
            {"pos": "1"},
            {
                "result": "TestResult",
                "nioBits": "100",
                "identifier": "TestIdentifier",
                "targetIdx": "5",
                "state": "TestState",
            },
        )

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
        opcon_common.AddOpConStructArrayValue(
            structArray, {"pos": "1"}, {"result": "TestResult"}
        )
        opcon_common.AddOpConStructArrayValue(
            structArray, {"pos": "1"}, {"identifier": "testIdentifier"}
        )

        assert len(structArray.data) == 2

    def test_opcon_struct_array_struct_definition(self):
        structArray = opcon_common.NewOpConStructArray("TestStructArray")
        opcon_common.AddOpConStructArrayStructDef(structArray, "a", 8)
        opcon_common.AddOpConStructArrayStructDef(structArray, "b", 3)
        opcon_common.AddOpConStructArrayStructDef(structArray, "c", 2)
        opcon_common.AddOpConStructArrayStructDef(structArray, "d", 8)
        opcon_common.AddOpConStructArrayStructDef(structArray, "e", 8)
        opcon_common.AddOpConStructArrayStructDef(structArray, "f", 8)
        opcon_common.AddOpConStructArrayStructDef(structArray, "g", 8)

        assert len(structArray.structDef) == 7

    def test_opcon_struct_array_result(self):
        structArray = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayResult(
            structArray,
            {"pos": "1"},
            pos="10",
            result="1",
            nioBits="2",
            identifier="TestIdentifier",
            targetIdx="1",
            state="4",
        )

        assert len(structArray.data) == 1
        assert len(structArray.data[0].attributes.items()) == 6
        telegram = structArray.update(self.telegram)
        assert telegram is not None

    def test_opcon_struct_array_result_invalid_result(self):
        structArray = opcon_common.NewOpConStructArray("results")
        with pytest.raises(ValueError, match="result must be one of"):
            opcon_common.AddOpConStructArrayResult(
                structArray,
                {"pos": "1"},
                result="999",
            )

    def test_opcon_struct_array_result_invalid_state(self):
        structArray = opcon_common.NewOpConStructArray("results")
        with pytest.raises(ValueError, match="state must be one of"):
            opcon_common.AddOpConStructArrayResult(
                structArray,
                {"pos": "1"},
                state="999",
            )


class TestOpConEvent:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpConBasic.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_create_simple_event(self):
        event = opcon_common.NewOpConEvent(
            identifier="TestIdentifier", typeNo="12345", typeVar="0001"
        )
        assert event.identifier == "TestIdentifier"
        assert event.typeNo == "12345"
        assert event.typeVar == "0001"

    def test_event_update(self):
        event = opcon_common.NewOpConEvent(
            identifier="NewIdentifier", typeNo="99999", typeVar="0005"
        )
        updated_telegram = event.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        event_node = parsed_xml.find("event/partReceived")

        assert event_node is not None
        assert event_node.get("identifier") == "NewIdentifier"
        assert event_node.get("typeNo") == "99999"
        assert event_node.get("typeVar") == "0005"

    def test_event_update_partial(self):
        event = opcon_common.NewOpConEvent(identifier="OnlyIdentifier")
        updated_telegram = event.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        event_node = parsed_xml.find("event/partReceived")

        assert event_node is not None
        assert event_node.get("identifier") == "OnlyIdentifier"

    def test_event_from_existing_event(self):
        original_event = opcon_common.OpConEvent(
            identifier="OriginalId", typeNo="111", typeVar="222"
        )
        new_event = opcon_common.NewOpConEvent(opConEvent=original_event)
        assert new_event.identifier == "OriginalId"
        assert new_event.typeNo == "111"
        assert new_event.typeVar == "222"

    def test_event_from_existing_with_override(self):
        original_event = opcon_common.OpConEvent(
            identifier="OriginalId", typeNo="111", typeVar="222"
        )
        new_event = opcon_common.NewOpConEvent(
            opConEvent=original_event, identifier="OverriddenId"
        )
        assert new_event.identifier == "OverriddenId"
        assert new_event.typeNo == "111"
        assert new_event.typeVar == "222"

    def test_event_update_no_event_node(self):
        telegram_no_event = """<?xml version="1.0"?><root><header/></root>"""
        event = opcon_common.NewOpConEvent(identifier="Test")
        with pytest.raises(ValueError, match="Telegram does not contain an event node"):
            event.update(telegram_no_event)

    def test_event_update_empty_event_node(self):
        telegram_empty_event = """<?xml version="1.0"?><root><event></event></root>"""
        event = opcon_common.NewOpConEvent(identifier="Test")
        with pytest.raises(
            ValueError, match="Telegram event node does not contain any child nodes"
        ):
            event.update(telegram_empty_event)


class TestOpConArray:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        self.telegram_with_array = """<?xml version="1.0" encoding="utf-8"?>
<root>
    <body>
        <testArray>
            <item pos="1" value="val1"/>
            <item pos="2" value="val2"/>
            <item pos="3" value="val3"/>
        </testArray>
        <structArrays>
            <array name="testArray">
                <item pos="1" value="val1"/>
                <item pos="2" value="val2"/>
            </array>
        </structArrays>
        <arrays>
            <array name="simpleArray" dataType="8">
                <item value="item1"/>
                <item value="item2"/>
                <item value="item3"/>
            </array>
        </arrays>
    </body>
</root>"""

    def test_create_array(self):
        array = opcon_common.NewOpConArray("testArray", 8)
        assert array.name == "testArray"
        assert array.dataType == 8
        assert array.data == []

    def test_add_array_value(self):
        array = opcon_common.NewOpConArray("testArray", 8)
        opcon_common.AddOpConArrayValue(array, {"pos": "1"}, {"value": "newValue"})

        assert len(array.data) == 1
        assert array.data[0].selectors == {"pos": "1"}
        assert array.data[0].attributes == {"value": "newValue"}

    def test_array_update(self):
        array = opcon_common.NewOpConArray("testArray", 8)
        opcon_common.AddOpConArrayValue(array, {"pos": "1"}, {"value": "updatedValue"})

        updated_telegram = array.update(self.telegram_with_array)
        assert updated_telegram is not None

        parsed_xml = ET.fromstring(updated_telegram)
        node = parsed_xml.find("body/testArray/item[@pos='1']")
        assert node is not None
        assert node.get("value") == "updatedValue"

    def test_array_equality(self):
        # Test arrays with same name and dataType but no data
        array1 = opcon_common.NewOpConArray("testArray", 8)
        array2 = opcon_common.NewOpConArray("testArray", 8)
        array3 = opcon_common.NewOpConArray("differentArray", 8)

        assert array1 == array2
        assert array1 != array3

    def test_array_inequality_different_datatype(self):
        array1 = opcon_common.NewOpConArray("testArray", 8)
        array2 = opcon_common.NewOpConArray("testArray", 3)
        assert array1 != array2

    def test_array_str(self):
        array = opcon_common.NewOpConArray("testArray", 8)
        str_repr = str(array)
        assert "testArray" in str_repr
        assert "8" in str_repr


class TestOpConArrayValue:
    def test_array_value_creation(self):
        value = opcon_common.OpConArrayValue(
            selectors={"pos": "1"}, attributes={"value": "test"}
        )
        assert value.selectors == {"pos": "1"}
        assert value.attributes == {"value": "test"}


class TestOpConPartAndGroup:
    def test_create_part(self):
        part = opcon_common.OpConPart(pos=1, identifier="TestPart")
        assert part.pos == 1
        assert part.identifier == "TestPart"

    def test_create_group(self):
        parts = [
            opcon_common.OpConPart(pos=1, identifier="Part1"),
            opcon_common.OpConPart(pos=2, identifier="Part2"),
        ]
        group = opcon_common.OpConGroup(identifier="GroupId", parts=parts)
        assert group.identifier == "GroupId"
        assert len(group.parts) == 2

    def test_new_opcon_groups(self):
        groups = list(
            opcon_common.NewOpConGroups(
                identifier="GRP", format="{0}_{1}", start=1, parts=3, count=2
            )
        )

        assert len(groups) == 2
        assert groups[0].identifier == "GRP0_1"
        assert len(groups[0].parts) == 3
        assert groups[0].parts[0].pos == 1
        assert groups[0].parts[0].identifier == "GRP1_1"
        assert groups[1].identifier == "GRP0_2"

    def test_get_opcon_parts_in_groups(self):
        groups = list(
            opcon_common.NewOpConGroups(
                identifier="GRP", format="{0}_{1}", start=1, parts=2, count=2
            )
        )

        parts = list(opcon_common.GetOpConPartsInGroups(groups))
        assert len(parts) == 4

    def test_new_opcon_results_struct_array(self):
        parts = [
            opcon_common.OpConPart(pos="1", identifier="Part1"),
            opcon_common.OpConPart(pos="2", identifier="Part2"),
        ]
        group = opcon_common.OpConGroup(identifier="GroupId", parts=parts)

        results = opcon_common.NewOpConResultsStructArray(group)
        assert results.name == "results"
        assert len(results.data) == 2


class TestEditOpConTelegram:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_edit_telegram_with_header(self):
        header = opcon_common.NewOpConHeader(999)
        result = opcon_common.EditOpConTelegram(self.telegram, header=header)

        parsed_xml = ET.fromstring(result)
        header_node = parsed_xml.find("header")
        assert header_node is not None
        assert header_node.get("eventSwitch") == "999"

    def test_edit_telegram_with_location(self):
        location = opcon_common.NewOpConLocation(lineNo=1234, statNo=5678)
        result = opcon_common.EditOpConTelegram(self.telegram, location=location)

        parsed_xml = ET.fromstring(result)
        loc_node = parsed_xml.find("header/location")
        assert loc_node is not None
        assert loc_node.get("lineNo") == "1234"
        assert loc_node.get("statNo") == "5678"

    def test_edit_telegram_with_event(self):
        event = opcon_common.NewOpConEvent(identifier="NewIdentifier")
        result = opcon_common.EditOpConTelegram(self.telegram, eventData=event)

        parsed_xml = ET.fromstring(result)
        event_node = parsed_xml.find("event/partReceived")
        assert event_node is not None
        assert event_node.get("identifier") == "NewIdentifier"

    def test_edit_telegram_with_res_head(self):
        res_head = opcon_common.NewOpConResHead(result=0, workingCode=5)
        result = opcon_common.EditOpConTelegram(self.telegram, resHead=res_head)

        parsed_xml = ET.fromstring(result)
        res_head_node = parsed_xml.find("body/structs/resHead")
        assert res_head_node is not None
        assert res_head_node.get("result") == "0"
        assert res_head_node.get("workingCode") == "5"

    def test_edit_telegram_with_items(self):
        items = [
            opcon_common.NewOpConItem("TestItem1", "Value1", 8),
            opcon_common.NewOpConItem("TestItem2", "Value2", 3),
        ]
        result = opcon_common.EditOpConTelegram(self.telegram, items=items)

        parsed_xml = ET.fromstring(result)
        item1 = parsed_xml.find("body/items/item[@name='TestItem1']")
        item2 = parsed_xml.find("body/items/item[@name='TestItem2']")
        assert item1 is not None
        assert item1.get("value") == "Value1"
        assert item2 is not None
        assert item2.get("value") == "Value2"

    def test_edit_telegram_with_struct_arrays(self):
        struct_array = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayValue(
            struct_array, {"pos": "1"}, {"result": "0"}
        )

        result = opcon_common.EditOpConTelegram(
            self.telegram, structArrays=[struct_array]
        )

        parsed_xml = ET.fromstring(result)
        node = parsed_xml.find(
            "body/structArrays/array[@name='results']/values/item[@pos='1']"
        )
        assert node is not None
        assert node.get("result") == "0"

    def test_edit_telegram_multiple_updates(self):
        header = opcon_common.NewOpConHeader(888)
        event = opcon_common.NewOpConEvent(identifier="MultiUpdate")
        items = [opcon_common.NewOpConItem("multiItem", "multiValue", 8)]

        result = opcon_common.EditOpConTelegram(
            self.telegram, header=header, eventData=event, items=items
        )

        parsed_xml = ET.fromstring(result)
        header_node = parsed_xml.find("header")
        assert header_node is not None
        assert header_node.get("eventSwitch") == "888"
        event_node = parsed_xml.find("event/partReceived")
        assert event_node is not None
        assert event_node.get("identifier") == "MultiUpdate"
        item_node = parsed_xml.find("body/items/item[@name='multiItem']")
        assert item_node is not None
        assert item_node.get("value") == "multiValue"


class TestOpConTestRule:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpConResponse_1.xml", "r")
        self.response_telegram = f.read()
        f.close()

    def test_create_test_rule_eq(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="/root/event/result/@returnCode", value="-2", eq=True
        )
        assert rule.xpath == "/root/event/result/@returnCode"
        assert rule.value == "-2"
        assert rule.comparator == opcon_common.OpConTestComparator.EQ
        assert rule.negative is False

    def test_create_test_rule_neq(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="/root/event/result/@returnCode", value="0", neq=True
        )
        assert rule.comparator == opcon_common.OpConTestComparator.NEQ

    def test_create_test_rule_contains(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="/root/event/result", value="warning", contains=True
        )
        assert rule.comparator == opcon_common.OpConTestComparator.Contains

    def test_create_test_rule_absent(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="/root/nonexistent", value="", absent=True
        )
        assert rule.comparator == opcon_common.OpConTestComparator.Absent

    def test_create_test_rule_exists(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="/root/event/result", value="", exists=True
        )
        assert rule.comparator == opcon_common.OpConTestComparator.Exists

    def test_create_test_rule_negative(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="/root/event/result/@returnCode", value="-2", negative=True, eq=True
        )
        assert rule.negative is True

    def test_create_test_rule_no_comparator(self):
        with pytest.raises(
            ValueError, match="At least one comparator must be specified"
        ):
            opcon_common.NewOpConTestRule(xpath="/root/event/result", value="test")

    def test_execute_rule_eq_pass(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="MES detected a warning.", eq=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is True
        assert result.value == "MES detected a warning."

    def test_execute_rule_eq_fail(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="wrong value", eq=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is False

    def test_execute_rule_neq_pass(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="wrong value", neq=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is True

    def test_execute_rule_contains_pass(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="warning", contains=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is True

    def test_execute_rule_contains_fail(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="not present", contains=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is False

    def test_execute_rule_absent_pass(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="nonexistent/path", value="", absent=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is True

    def test_execute_rule_absent_fail(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="", absent=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is False

    def test_execute_rule_exists_pass(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="", exists=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is True

    def test_execute_rule_exists_fail(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="nonexistent/path", value="", exists=True
        )
        result = rule.execute("request", self.response_telegram)
        assert result.ok is False

    def test_execute_rule_no_xpath(self):
        rule = opcon_common.OpConTestRule()
        rule.comparator = opcon_common.OpConTestComparator.EQ
        rule.value = "test"
        with pytest.raises(ValueError, match="xpath must be defined"):
            rule.execute("request", self.response_telegram)

    def test_invoke_opcon_test_rule(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value="MES detected a warning.", eq=True
        )
        result = opcon_common.InvokeOpConTestRule(
            rule, "request", self.response_telegram
        )
        assert result.ok is True


class TestOpConTestRuleResult:
    def test_test_rule_result_properties(self):
        result = opcon_common.OpConTestRuleResult(
            rule="test_rule",
            value="test_value",
            request="test_request",
            response="test_response",
            ok=True,
        )
        assert result.rule == "test_rule"
        assert result.value == "test_value"
        assert result.request == "test_request"
        assert result.response == "test_response"
        assert result.ok is True

    def test_test_rule_result_str(self):
        result = opcon_common.OpConTestRuleResult(
            rule="test_rule", value="test_value", ok=True
        )
        str_repr = str(result)
        assert "test_rule" in str_repr
        assert "test_value" in str_repr


class TestGetOpConCommonTestRules:
    def test_get_common_test_rules(self):
        rules = opcon_common.GetOpConCommonTestRules()

        assert "ReturnCode_0" in rules
        assert "ReturnCode_-2" in rules
        assert "ReturnCode_-1" in rules

        assert rules["ReturnCode_0"].xpath == "/root/event/result/@returnCode"
        assert rules["ReturnCode_0"].value == 0


class TestGetOpConCommonTelegrams:
    def test_get_common_telegrams(self):
        telegrams = opcon_common.GetOpConCommonTelegrams()

        expected_keys = [
            "PartGroupCreate",
            "PartGroupMoveToSupermarket",
            "PartGroupDelete",
            "PartGroupGet",
            "PartGroupGetAdditionalDatas",
            "MaterialCreate",
            "MaterialDeleteBlocks",
            "MaterialGet",
            "MaterialVerify",
            "MaterialOpen",
            "MaterialClose",
            "MaterialAdjustExposureTime",
            "MaterialSetup",
            "MaterialTeardown",
        ]

        for key in expected_keys:
            assert key in telegrams


class TestGetOpConTelegramValue:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_get_telegram_value_text(self):
        telegram_with_text = (
            """<root><event><result>Test Content</result></event></root>"""
        )
        value = opcon_common.GetOpConTelegramValue(telegram_with_text, "event/result")
        assert value == "Test Content"

    def test_get_telegram_value_attribute(self):
        value = opcon_common.GetOpConTelegramValue(self.telegram, "header")
        assert value is not None

    def test_get_telegram_value_not_found(self):
        value = opcon_common.GetOpConTelegramValue(self.telegram, "nonexistent/path")
        assert value is None

    def test_get_telegram_value_inner_xml(self):
        telegram_with_children = """<root><parent><child>text</child></parent></root>"""
        value = opcon_common.GetOpConTelegramValue(telegram_with_children, "parent")
        assert value is not None
        assert "<child>text</child>" in value

    def test_get_telegram_value_empty_element(self):
        # Test element with no text and no children - should return element itself
        telegram_empty_element = """<root><empty attr="value"/></root>"""
        value = opcon_common.GetOpConTelegramValue(telegram_empty_element, "empty")
        assert value is not None
        assert "attr" in value or "empty" in value


class TestGetOpConItem:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_get_opcon_item_existing(self):
        item = opcon_common.GetOpConItem(self.telegram, "routeList")
        assert item is not None
        assert item.name == "routeList"
        assert item.value == "SMT_SIP_bottom_1st_side_2SPP"
        assert item.dataType == 8

    def test_get_opcon_item_not_found(self):
        item = opcon_common.GetOpConItem(self.telegram, "nonExistentItem")
        assert item is None


class TestGetOpConArray:
    def test_get_opcon_array_existing(self):
        telegram_with_array = """<?xml version="1.0"?>
<root>
    <body>
        <arrays>
            <array name="testArray" dataType="8">
                <item value="value1"/>
                <item value="value2"/>
                <item value="value3"/>
            </array>
        </arrays>
    </body>
</root>"""
        array = opcon_common.GetOpConArray(telegram_with_array, "testArray")
        assert array is not None
        assert array.name == "testArray"
        assert array.dataType == "8"
        assert len(array.data) == 3
        assert array.data[0].attributes["value"] == "value1"

    def test_get_opcon_array_not_found(self):
        telegram = (
            """<?xml version="1.0"?><root><body><arrays></arrays></body></root>"""
        )
        array = opcon_common.GetOpConArray(telegram, "nonExistent")
        assert array is None


class TestGetOpConStructArray:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_get_struct_array_existing(self):
        struct_array = opcon_common.GetOpConStructArray(self.telegram, "results")
        assert struct_array is not None
        assert struct_array.name == "results"
        assert len(struct_array.structDef) == 6
        assert len(struct_array.data) == 6

    def test_get_struct_array_not_found(self):
        struct_array = opcon_common.GetOpConStructArray(self.telegram, "nonExistent")
        assert struct_array is None


class TestCompareOpConTrace:
    def test_compare_traces_equal(self):
        trace1 = """<root><event><trace><trace text="same" code="100"/></trace></event></root>"""
        trace2 = """<root><event><trace><trace text="same" code="100"/></trace></event></root>"""

        diffs = opcon_common.CompareOpConTrace(trace1, trace2)
        assert len(diffs) == 0

    def test_compare_traces_different_text(self):
        trace1 = """<root><event><trace><trace text="text1" code="100"/></trace></event></root>"""
        trace2 = """<root><event><trace><trace text="text2" code="100"/></trace></event></root>"""

        diffs = opcon_common.CompareOpConTrace(trace1, trace2)
        assert len(diffs) == 1
        assert "text attribute" in diffs[0]

    def test_compare_traces_different_code(self):
        trace1 = """<root><event><trace><trace text="same" code="100"/></trace></event></root>"""
        trace2 = """<root><event><trace><trace text="same" code="200"/></trace></event></root>"""

        diffs = opcon_common.CompareOpConTrace(trace1, trace2)
        assert len(diffs) == 1
        assert "code attribute" in diffs[0]

    def test_compare_traces_missing_node(self):
        trace1 = """<root><header/></root>"""
        trace2 = """<root><header/></root>"""

        with pytest.raises(
            ValueError, match="Both traces must contain the base trace node"
        ):
            opcon_common.CompareOpConTrace(trace1, trace2)


class TestCompareOpConStructArray:
    def test_compare_struct_arrays_equal(self):
        telegram1 = """<root><body><structArrays>
            <array name="test">
                <structDef><item name="a" dataType="8"/><item name="b" dataType="3"/></structDef>
            </array>
        </structArrays></body></root>"""

        telegram2 = """<root><body><structArrays>
            <array name="test">
                <structDef><item name="a" dataType="8"/><item name="b" dataType="3"/></structDef>
            </array>
        </structArrays></body></root>"""

        diffs = opcon_common.CompareOpConStructArray(telegram1, telegram2, "test")
        assert len(diffs) == 0

    def test_compare_struct_arrays_different_datatype(self):
        telegram1 = """<root><body><structArrays>
            <array name="test">
                <structDef><item name="a" dataType="8"/></structDef>
            </array>
        </structArrays></body></root>"""

        telegram2 = """<root><body><structArrays>
            <array name="test">
                <structDef><item name="a" dataType="3"/></structDef>
            </array>
        </structArrays></body></root>"""

        diffs = opcon_common.CompareOpConStructArray(telegram1, telegram2, "test")
        assert len(diffs) > 0

    def test_compare_struct_arrays_missing_item(self):
        telegram1 = """<root><body><structArrays>
            <array name="test">
                <structDef><item name="a" dataType="8"/></structDef>
            </array>
        </structArrays></body></root>"""

        telegram2 = """<root><body><structArrays>
            <array name="test">
                <structDef><item name="a" dataType="8"/><item name="b" dataType="3"/></structDef>
            </array>
        </structArrays></body></root>"""

        diffs = opcon_common.CompareOpConStructArray(telegram1, telegram2, "test")
        assert len(diffs) > 0
        assert any("Right not in Left" in diff for diff in diffs)


class TestOpConLocationEdgeCases:
    def test_location_update_no_location_node(self):
        telegram_no_location = """<?xml version="1.0"?><root><header/></root>"""
        location = opcon_common.NewOpConLocation(lineNo=100)

        with pytest.raises(
            ValueError, match="Telegram does not contain a location node"
        ):
            location.update(telegram_no_location)

    def test_location_invalid_lineNo(self):
        with pytest.raises(ValueError, match="lineNo must be between 1 and 9999"):
            opcon_common.NewOpConLocation(lineNo=0)
        with pytest.raises(ValueError, match="lineNo must be between 1 and 9999"):
            opcon_common.NewOpConLocation(lineNo=10000)

    def test_location_invalid_statNo(self):
        with pytest.raises(ValueError, match="statNo must be between 1 and 9999"):
            opcon_common.NewOpConLocation(statNo=0)

    def test_location_invalid_statIdx(self):
        with pytest.raises(ValueError, match="statIdx must be between 1 and 9999"):
            opcon_common.NewOpConLocation(statIdx=10000)

    def test_location_invalid_workPos(self):
        with pytest.raises(ValueError, match="workPos must be between 1 and 9999"):
            opcon_common.NewOpConLocation(workPos=0)

    def test_location_invalid_toolPos(self):
        with pytest.raises(ValueError, match="toolPos must be between 1 and 9999"):
            opcon_common.NewOpConLocation(toolPos=0)


class TestOpConResHeadEdgeCases:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.telegram_no_reshead = (
            """<?xml version="1.0"?><root><body><structs/></body></root>"""
        )

    def test_reshead_update_no_node(self):
        res_head = opcon_common.NewOpConResHead(result=1)
        with pytest.raises(
            ValueError, match="Telegram does not contain a resHead node"
        ):
            res_head.update(self.telegram_no_reshead)


class TestOpConStructArrayStructDef:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_struct_array_update_structdef(self):
        struct_array = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayStructDef(struct_array, "newField", 8)

        updated = struct_array.update_structDef(self.telegram)
        assert updated != ""

        parsed = ET.fromstring(updated)
        struct_def = parsed.find("body/structArrays/array[@name='results']/structDef")
        assert struct_def is not None
        new_item = struct_def.find("item[@name='newField']")
        assert new_item is not None
        assert new_item.get("dataType") == "8"

    def test_struct_array_update_structdef_no_node(self):
        struct_array = opcon_common.NewOpConStructArray("nonExistent")
        opcon_common.AddOpConStructArrayStructDef(struct_array, "field", 8)

        result = struct_array.update_structDef(self.telegram)
        assert result == ""

    def test_struct_array_str(self):
        struct_array = opcon_common.NewOpConStructArray("testArray")
        str_repr = str(struct_array)
        assert "testArray" in str_repr


class TestOpConHeaderEdgeCases:
    def test_header_none_event_switch(self):
        header = opcon_common.NewOpConHeader(0)
        assert header.event_switch == 0

    def test_header_setter_validation(self):
        header = opcon_common.NewOpConHeader(100)
        with pytest.raises(ValueError, match="event_switch must be a positive integer"):
            header.event_switch = -5

    def test_header_setter_valid_value(self):
        header = opcon_common.NewOpConHeader(0)
        header.event_switch = 500
        assert header.event_switch == 500

    def test_header_setter_zero_value(self):
        header = opcon_common.NewOpConHeader(100)
        header.event_switch = 0
        assert header.event_switch == 0

    def test_header_setter_none_value(self):
        header = opcon_common.NewOpConHeader(100)
        header.event_switch = None
        assert header.event_switch is None


class TestOpConLocationSetters:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        self.location = opcon_common.NewOpConLocation(
            lineNo=1, statNo=1, statIdx=1, fuNo=1, workPos=1, toolPos=1
        )

    def test_lineNo_setter_invalid(self):
        with pytest.raises(ValueError, match="lineNo must be between 1 and 9999"):
            self.location.lineNo = 0

    def test_statNo_setter_invalid(self):
        with pytest.raises(ValueError, match="statNo must be between 1 and 9999"):
            self.location.statNo = 10000

    def test_statIdx_setter_invalid(self):
        with pytest.raises(ValueError, match="statIdx must be between 1 and 9999"):
            self.location.statIdx = 0

    def test_fuNo_setter_invalid(self):
        with pytest.raises(ValueError, match="fuNo must be between 1 and 9"):
            self.location.fuNo = 10

    def test_workPos_setter_invalid(self):
        with pytest.raises(ValueError, match="workPos must be between 1 and 9999"):
            self.location.workPos = 0

    def test_toolPos_setter_invalid(self):
        with pytest.raises(ValueError, match="toolPos must be between 1 and 9999"):
            self.location.toolPos = 10000


class TestOpConResHeadAllFields:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpCon.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_update_res_head_nioBits(self):
        res_head = opcon_common.NewOpConResHead(nioBits=255)
        updated_telegram = res_head.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        res_head_node = parsed_xml.find("body/structs/resHead")
        assert res_head_node is not None
        assert res_head_node.get("nioBits") == "255"

    def test_update_res_head_machineId(self):
        res_head = opcon_common.NewOpConResHead(machineId="TestMachine123")
        updated_telegram = res_head.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        res_head_node = parsed_xml.find("body/structs/resHead")
        assert res_head_node is not None
        assert res_head_node.get("machineId") == "TestMachine123"


class TestOpConItemNoItemsNode:
    def test_item_update_no_items_node(self):
        telegram_no_items = """<?xml version="1.0"?><root><body></body></root>"""
        item = opcon_common.NewOpConItem("TestItem", "TestValue", 8)

        with pytest.raises(ValueError, match="Telegram does not contain an items node"):
            item.update(telegram_no_items)


class TestOpConStructArrayNoneValues:
    def test_struct_array_update_no_values_node(self):
        telegram_no_values = """<?xml version="1.0"?>
<root><body><structArrays>
    <array name="results"><structDef/></array>
</structArrays></body></root>"""

        struct_array = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayValue(
            struct_array, {"pos": "1"}, {"result": "1"}
        )

        result = struct_array.update(telegram_no_values)
        assert result is None


class TestOpConStructArrayEquality:
    def test_struct_array_different_structdef(self):
        struct_array1 = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayStructDef(struct_array1, "field1", 8)

        struct_array2 = opcon_common.NewOpConStructArray("results")
        opcon_common.AddOpConStructArrayStructDef(struct_array2, "field2", 3)

        assert struct_array1 != struct_array2

    def test_struct_array_same_structdef_different_name(self):
        struct_array1 = opcon_common.NewOpConStructArray("array1")
        struct_array2 = opcon_common.NewOpConStructArray("array2")

        assert struct_array1 != struct_array2


class TestOpConArrayNoValues:
    def test_array_update_no_matching_nodes(self):
        telegram_no_match = """<?xml version="1.0"?>
<root><body></body></root>"""

        array = opcon_common.NewOpConArray("testArray", 8)
        opcon_common.AddOpConArrayValue(array, {"pos": "1"}, {"value": "test"})

        result = array.update(telegram_no_match)
        assert result is None


class TestEditOpConTelegramArrays:
    def test_edit_telegram_with_arrays(self):
        telegram_with_arrays = """<?xml version="1.0"?>
<root>
    <body>
        <testArray>
            <item pos="1" value="original"/>
        </testArray>
        <structArrays>
            <array name="testArray">
                <item pos="1" value="original"/>
            </array>
        </structArrays>
    </body>
</root>"""

        array = opcon_common.NewOpConArray("testArray", 8)
        opcon_common.AddOpConArrayValue(array, {"pos": "1"}, {"value": "updated"})

        result = opcon_common.EditOpConTelegram(telegram_with_arrays, arrays=[array])
        parsed = ET.fromstring(result)
        node = parsed.find("body/testArray/item[@pos='1']")
        assert node is not None
        assert node.get("value") == "updated"


class TestOpConTestRuleNodeWithChildren:
    def test_execute_rule_with_inner_xml(self):
        telegram = """<root><parent><child>inner text</child></parent></root>"""
        rule = opcon_common.NewOpConTestRule(
            xpath="parent", value="<child>inner text</child>", contains=True
        )
        result = rule.execute("request", telegram)
        assert result.ok is True

    def test_execute_rule_unsupported_comparator(self):
        rule = opcon_common.OpConTestRule()
        rule.xpath = "event/result"
        rule.comparator = "unsupported"
        rule.value = "test"

        with pytest.raises(ValueError, match="Unsupported comparator"):
            rule.execute("request", "<root><event><result>test</result></event></root>")

    def test_execute_rule_value_none(self):
        rule = opcon_common.NewOpConTestRule(
            xpath="event/result", value=None, exists=True
        )
        rule.value = None  # Explicitly set to None
        result = rule.execute(
            "request", "<root><event><result>test</result></event></root>"
        )
        assert result.ok is True

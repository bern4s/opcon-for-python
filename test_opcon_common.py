import pytest
import xml.etree.ElementTree as ET
from opcon_common import NewOpConHeader, NewOpConLocation, NewOpConResHead, OpConResHead


class TestOpConHeader:
    HEADER_NUMBER = 999

    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpConBasic.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_create_simple_header(self):
        header = NewOpConHeader(self.HEADER_NUMBER)
        assert header.event_switch == self.HEADER_NUMBER

    def test_update_header(self):
        header = NewOpConHeader(self.HEADER_NUMBER)
        updated_telegram = header.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        header_node = parsed_xml.find("header")

        assert header_node is not None
        telegram_event_switch = header_node.get("eventSwitch")
        assert telegram_event_switch == str(self.HEADER_NUMBER)

    def test_invalid_header_event_switch(self):
        with pytest.raises(ValueError, match="event_switch must be a positive integer"):
            NewOpConHeader(-1)


class TestOpConLocation:
    @pytest.fixture(autouse=True)
    def set_up_method(self):
        f = open("telegrams/OpConBasic.Tests.Telegram.xml", "r")
        self.telegram = f.read()
        f.close()

    def test_create_simple_location(self):
        location = NewOpConLocation(
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
        location = NewOpConLocation(
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
        location = NewOpConLocation(
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
        location = NewOpConLocation(
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
            NewOpConLocation(
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
        res_head = NewOpConResHead(
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
        res_head = NewOpConResHead(result=12, typeNo=200, typeVar="Test_Res")
        updated_telegram = res_head.update(self.telegram)
        parsed_xml = ET.fromstring(updated_telegram)
        res_head_node = parsed_xml.find("body/structs/resHead")

        assert res_head_node is not None
        assert res_head_node.get("result") == "12"
        assert res_head_node.get("typeNo") == "200"
        assert res_head_node.get("typeVar") == "Test_Res"

    def test_invalid_result(self):
        with pytest.raises(ValueError, match="result must be one of"):
            o = NewOpConResHead(typeNo=100, typeVar="Test")
            o.result = 888

    def test_invalid_working_code(self):
        with pytest.raises(ValueError, match="workingCode must be between 0 and 15"):
            o = NewOpConResHead(typeNo=100, typeVar="Test")
            o.workingCode = 300

    def test_use_created_res_head(self):
        res_head = NewOpConResHead(
            opConEvent=OpConResHead(typeNo=1234, typeVar="0009"),
            result=1,
            machineId="Machine_99",
        )
        assert res_head.typeNo == 1234
        assert res_head.typeVar == "0009"
        assert res_head.result == 1
        assert res_head.machineId == "Machine_99"

import pytest
import xml.etree.ElementTree as ET
from opcon_common import NewOpConHeader, NewOpConLocation

TELEGRAM = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<root>
  <header eventId="0" eventName="partReceived" version="1.0" eventSwitch="105" contentType="3">
    <location lineNo="666" statNo="9999" statIdx="1" fuNo="1" workPos="1" toolPos="1" application="PLC" processName="" processNo="0" />
  </header>
  <event>
    <partReceived identifier="" typeVar="" typeNo="" typeVersion="" />
  </event>
  <body>
    <structs />
  </body>
</root>
"""


class TestOpConHeader:
    HEADER_NUMBER = 999

    def test_create_simple_header(self):
        header = NewOpConHeader(self.HEADER_NUMBER)
        assert header.event_switch == self.HEADER_NUMBER

    def test_update_header(self):
        header = NewOpConHeader(self.HEADER_NUMBER)
        updated_telegram = header.update(TELEGRAM)
        parsed_xml = ET.fromstring(updated_telegram)
        telegram_event_switch = parsed_xml.find("header").get("eventSwitch")

        assert telegram_event_switch == str(self.HEADER_NUMBER)

    def test_invalid_header_event_switch(self):
        with pytest.raises(ValueError, match="event_switch must be a positive integer"):
            NewOpConHeader(-1)


class TestOpConLocation:
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
        updated_telegram = location.update(TELEGRAM)
        parsed_xml = ET.fromstring(updated_telegram)
        location_node = parsed_xml.find("header/location")

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
        updated_telegram = location.update(TELEGRAM)
        parsed_xml = ET.fromstring(updated_telegram)
        location_node = parsed_xml.find("header/location")

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

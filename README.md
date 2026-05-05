# OpCon for Python

A Python library for communicating with **NEXEED** installations via the **OpConXML** protocol — a messaging standard used in Bosch industrial automation environments. It enables building, modifying, sending, and validating OpConXML telegrams.

---

## Overview

OpConXML telegrams are structured XML messages exchanged between manufacturing systems (PLCs, MES, etc.) and NEXEED. This library provides Python classes and factory functions to construct and manipulate these telegrams, as well as tools to validate responses using XPath-based test rules.

---

## Project Structure

```
opcon_common.py          # Core classes and factory functions
opcon_enums.py           # Enumerations (LabelType, OpConTestComparator)
telegrams/               # Sample XML telegrams used for testing
common/                  # Common telegram XML files (PartGroup, Material operations)
test_opcon_common.py     # pytest test suite
requirements.txt         # Project dependencies
```

---

## Core Components

### `OpConHeader`
Represents the `<header>` node of a telegram. Supports setting the `eventSwitch` attribute.

```python
header = NewOpConHeader(event_switch=105)
updated_telegram = header.update(telegram_xml)
```

### `OpConLocation`
Represents the `<location>` node inside the header. Supports physical machine addressing:

| Field | Description | Valid Range |
|---|---|---|
| `lineNo` | Production line number | 0–9999 |
| `statNo` | Station number | 0–9999 |
| `statIdx` | Station index | 0–9999 |
| `fuNo` | Functional unit number | 1–9 |
| `workPos` | Work position | 1–9999 |
| `toolPos` | Tool position | 1–9999 |
| `application` | Application name (e.g. `PLC`) | — |
| `processName` | Process name (e.g. `EOL`) | — |
| `processNo` | Process number | — |

Can be constructed from a dot-notation location ID string:

```python
location = NewOpConLocation(locationId="666.7001.1.1.1.1")
# or with explicit fields:
location = NewOpConLocation(lineNo=666, statNo=7001, application="PLC")
```

### `OpConEvent`
Represents the `<event>` node, holding part identifier, type number, and type variant.

```python
event = NewOpConEvent(identifier="PLS1SZxMILx0023", typeNo="0000907081", typeVar="0001")
```

### `OpConResHead`
Represents the `<resHead>` node in `<body/structs>`. Validates the `result` field against allowed values: `-1, 0, 1, 2, 12`. The `workingCode` must be between 0 and 15.

```python
resHead = NewOpConResHead(result=1, workingCode=0)
```

### `OpConItem`
Represents a named key-value item in `<body/items>`. Supports a set of valid `dataType` values: `2, 3, 4, 5, 7, 8, 11, 14, 16, 17, 18, 19, 20, 21`.

```python
item = NewOpConItem(name="routeList", value="SMT_SIP_bottom_1st_side", dataType=8)
```

### `OpConStructArray` / `OpConArray`
Represent structured array data inside `<body/structArrays>` and `<body/arrays>`. Support adding struct definitions and updating values by selector.

### `OpConPart` / `OpConGroup`
Model groups of parts with positions and identifiers, used to generate result struct arrays.

```python
group = NewOpConGroups(identifier="PLS1SZ", format="xMILx{1:04d}", parts=6, count=1, start=23)
results = NewOpConResultsStructArray(group)
```

### Telegram Editing

The `EditOpConTelegram` function applies multiple updates to a telegram in one call:

```python
updated = EditOpConTelegram(
    telegram,
    header=header,
    location=location,
    resHead=resHead,
    items=[item1, item2],
    structArrays=[results],
)
```

### Material Items

`NewOpConMaterialItems(label, labelType)` parses a barcode label string (MAT or GTL format) and yields a series of `OpConItem` objects representing material component fields (batch, quantity, manufacturer, expiry date, etc.).

```python
for item in NewOpConMaterialItems(label_string, LabelType.MAT):
    print(item)
```

---

## Response Validation

### `OpConTestRule`
Defines a validation rule using XPath and a comparator:

| Comparator | Description |
|---|---|
| `EQ` | Value equals expected |
| `NEQ` | Value does not equal expected |
| `Contains` | Value contains expected |
| `Absent` | Node/value is absent |
| `Exists` | Node/value exists |

```python
rule = NewOpConTestRule(xpath="body/items/item[@name='routeList']", value="SMT", contains=True)
result = rule.execute(request_telegram, response_telegram)
print(result.ok)  # True or False
```

### Common Test Rules

```python
rules = GetOpConCommonTestRules()
# Includes: ReturnCode_0, ReturnCode_-1, ReturnCode_-2
```

---

## Utility Functions

| Function | Description |
|---|---|
| `GetOpConTelegramValue(telegram, xpath)` | Extract a value from a telegram by XPath |
| `GetOpConItem(telegram, name)` | Get a named item from `<body/items>` |
| `GetOpConArray(telegram, name)` | Get an array from `<body/arrays>` |
| `GetOpConStructArray(telegram, name)` | Get a struct array from `<body/structArrays>` |
| `CompareOpConTrace(trace1, trace2)` | Compare two trace telegrams and return a list of differences |
| `GetOpConCommonTelegrams()` | Get a dict of paths to common telegram XML files |

---

## Development

### Prerequisites

- Python 3.x

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run tests

```bash
pytest
```

### Run tests with coverage

```bash
pytest --cov
```

### Lint

```bash
flake8
```

# Eurotherm Python Driver

A lightweight Python driver for Eurotherm Series 2000 temperature controllers using Modbus RTU over a serial connection.

Currently supported:

- Eurotherm 2408
- Eurotherm 3508

The driver is intended to provide a clean hardware interface. Experiment logging, plotting, temperature ramps, and experiment sequencing are deliberately outside the scope of this package.

The implemented functionality is limited to necessary minimum.


## Installation

For development, install the package in editable mode:

```bash
python -m pip install -e .
```

For a regular installation:

```bash
python -m pip install .
```


## Basic usage

### Eurotherm 2408

```python
from eurotherm import Eurotherm2408

controller = Eurotherm2408(
    port="/dev/ttyUSB0",
    address=1,
)

print(controller.temperature)
```


### Eurotherm 3508

```python
from eurotherm import Eurotherm3508

controller = Eurotherm3508(
    port="/dev/ttyUSB0",
    address=1,
)

print(controller.temperature)
```


## Reading controller parameters

The driver exposes commonly used controller parameters as Python properties:

```python
print(controller.temperature)
print(controller.target_setpoint)
print(controller.working_setpoint)
print(controller.output_level)
print(controller.mode)

print(controller.proportional_band)
print(controller.integral_time)
print(controller.derivative_time)
```

For example:

```text
Temperature:       25.4 °C
Target setpoint:   170.0 °C
Working setpoint:  170.0 °C
Output:            100.0 %
Mode:              Mode.AUTO
```

## Writing controller parameters

Writable parameters can be assigned directly:

```python
controller.target_setpoint = 170.0
```

PID parameters can also be changed:

```python
controller.proportional_band = 10.0
controller.integral_time = 60
controller.derivative_time = 20
```

Manual operation is available through the controller mode and manual output:

```python
from eurotherm import Eurotherm2408, Mode

controller = Eurotherm2408("/dev/ttyUSB0")

controller.mode = Mode.MANUAL
controller.manual_output = 25.0
```

Use caution when writing controller parameters, particularly `mode`,
`manual_output`, and PID parameters, because they directly affect the
operation of the connected temperature controller.



## Persistent serial connection

By default, the serial port is opened and closed for each Modbus transaction.

For applications involving frequent reads and writes, the connection can be
kept open:

```python
controller = Eurotherm3508(
    "/dev/ttyUSB0",
    keep_open=True,
)

print(controller.temperature)
print(controller.output_level)
print(controller.target_setpoint)
```

The connection can also be managed using a context manager:

```python
from eurotherm import Eurotherm3508

with Eurotherm3508("/dev/ttyUSB0") as controller:
    print(controller.temperature)
    print(controller.target_setpoint)

    controller.target_setpoint = 180.0
```

The serial connection is automatically closed when leaving the `with` block,
including when an exception occurs.


## Supported parameters

The current register map contains the following commonly used parameters:

| Property | Description | Units |
|---|---|---|
| `temperature` | Process value | °C |
| `target_setpoint` | Target setpoint | °C |
| `working_setpoint` | Working setpoint | °C |
| `output_level` | Control output | % |
| `mode` | Automatic / Manual mode | — |
| `manual_output` | Manual output level | % |
| `proportional_band` | Proportional band | °C |
| `integral_time` | Integral time | s |
| `derivative_time` | Derivative time | s |

The register definitions are currently shared between the supported Series 2000
controllers.


## Hardware verification

The driver has been tested with physical Eurotherm Series 2000 controllers.

Currently verified:

- Eurotherm 2408
- Eurotherm 3508

Communication has been tested using Modbus RTU over RS-232.


## References

The register map is based on Eurotherm Series 2000 communications
documentation, including:

- 2000 Series MODBUS and EI-BISYNCH Digital Communications Handbook
- Eurotherm 2408 documentation
- Eurotherm 3508 documentation

## License

MIT License
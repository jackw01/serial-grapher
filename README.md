# serial-grapher
Utility for graphing CSV data received over a serial port

## Install
`pip install serialgrapher`

## Screenshot
![](screenshot.png)

## Usage
```
usage: serialgrapher [-h] [-p PORT] [-b BAUD_RATE] [-l LENGTH] [--dont-save]
                     [--rate-limit LIMIT] [--auto-scale-y] [--y-min MIN] [--y-max MAX]

Utility for graphing CSV data received over a serial port

optional arguments:
  -h, --help          show this help message and exit
  -p PORT             Serial port
  -b BAUD_RATE        Baud rate
  -l LENGTH           Number of data points to show on graph
  --dont-save         Don't save the data to a CSV file
  --rate-limit LIMIT  Maximum sample rate in samples/second
  --auto-scale-y      Automatically scale the y axis
  --y-min MIN         Minimum y value
  --y-max MAX         Maximum y value
```

## CSV Format Example
This program receives data in standard CSV format from a serial port and expects a header row to be transmitted before the data.

```
X,Y,Z
-0.90,2.20,9.73
-0.90,2.24,9.69
-0.98,2.16,9.77
-0.90,2.12,9.77
-0.86,2.24,9.73
...
```

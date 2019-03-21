# data-drills
Mine textual data using drills

* Python 3.7.1

## Ip Subnet Mapper

```
$ ./ip_subnet.py -h
usage: ip_subnet.py [-h] [--verbose] [--strict] network_file [file [file ...]]

Maps Ip addresses to their corresponding subnet

positional arguments:
  network_file   file defining networks
  file           input data

optional arguments:
  -h, --help     show this help message and exit
  --verbose, -v
  --strict, -s   forces strict codec parsing
```

## Test

```python
python -m unittest discover
```

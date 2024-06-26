<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"><br>
# Python basic scripts

# uses


### bash
```bash
./get_ip_router.py
```
<br><br>

# Port Scanner 

## Manual
```python3
./class_ports.py -h
```
### in the port_scanner you can write this differents ways to get ports: range, only one port, some ports

## range
```python3
./class_ports.py -l 1.1.1.1 -p 1-100
```

## one_port
```python3
./class_port.py -l 1.1.1.1 -p 80
```

## some_ports
```python3
./class_port.py -l 1.1.1.1 -p 20,80,443,22
```

<br><br>

# Mac changer

## Manual
```python3
./mac_changer.py -h
```

## Change mac
```python3
./mac_changer.py -i <your_interface, Example: eth0> -m <New mac, Example: 00:23:f3:46:tb:3f>
```

## reset your mac to 'Fabric'
```python3
./mac_changer.py -r
```
<br><br>

# ICMP tracer

## Manual
```python3
./ICMP_TRACER.py -h
```

## Use with one IP
```python3
./ICMP_TRACER.py -i 192.168.254.254
```

## Use with range
```python3
./ICMP_TRACER.py -i 192.168.254.1-254
```
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"><br><br>

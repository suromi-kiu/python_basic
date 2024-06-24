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

<br>

## range
```python3
./class_ports.py -l 1.1.1.1 -p 1-100
```
<br>

## one_port
```python3
./class_port.py -l 1.1.1.1 -p 80
```

<br>

## some_ports
```python3
./class_port.py -l 1.1.1.1 -p 20,80,443,22
```

<br>

# Mac changer

## Manual
```python3
./mac_changer.py -h
```
<br>

## Change mac
```python3
./mac_changer.py -i <your_interface, Example: eth0> -m <New mac, Example: 00:23:f3:46:tb:3f>
```
<br>

## reset your mac to 'Fabric'
```python3
./mac_changer.py -r
```
<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif"><br><br>

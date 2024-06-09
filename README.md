# dhcpd-show-leases
This is a very simple script that shows DHCPd leases in human readable format. 

Original code was taken from https://askubuntu.com/questions/219609/how-do-i-show-active-dhcp-leases and adapted to modern times

## Usage

```
$ sudo ./leases.py 
+-----------------+-------------------+-------------+-------------------------------+
| IP Address      | MAC Address       | Expires in  | Hostname                      |
+-----------------+-------------------+-------------+-------------------------------+
| 192.168.1.96    | 50:ff:20:7d:5d:6d | 0:07:48     | Keenetic-8226                 |
| 192.168.1.150   | 50:ff:20:7d:5d:70 | 0:05:30     | Keenetic-8640                 |
| 192.168.1.167   | 02:9a:f8:04:8f:b9 | 0:08:47     | MNA-LX9                       |
| 192.168.1.99    | 38:f3:ab:90:55:d0 | 0:08:13     | MOHCTP                        |
| 192.168.1.98    | ca:2a:71:16:b8:c4 | 0:07:52     | multik                        |
| 192.168.1.119   | 28:2b:b9:41:77:de | 0:07:59     | SberBoom_Mini                 |
| 192.168.1.169   | bc:d0:74:2d:ed:f4 | 0:56:38     | sc-mac-00565                  |
| 192.168.1.196   | 9a:03:cf:46:c7:64 | 0:07:17     | wirenboard-AG4LVLTQ           |
| 192.168.1.157   | b8:87:6e:7c:86:24 | 0:08:10     | yandex-station-lite           |
+-----------------+-------------------+-------------+-------------------------------+

```

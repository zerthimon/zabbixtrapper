# zabbix_trapper
Zabbix Trapper Python interface library

use:
```
from zabbixtrapper import ZabbixTrapper
req= [{"host": "some.host.com", "value": 732248.0, "key": "memory.memory-free", "clock": 1422882561}]
z = ZabbixTrapper('zabbix.host.com', '10051')
r = z.send_traps(req)
print r
```

result:
```
{u'info': u'processed: 1; failed: 0; total: 1; seconds spent: 0.000021', u'response': u'success'}

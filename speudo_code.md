# CBS

** Voir p4cheatsheets pour register notion de file et le counter **
 
```
* High classe typiquement 75 *

CLASS
var prio
var queue
var credit init à 0
var bool isTransmitting init à false
var sendslope = 4  ** Arbitrary value **
var idleslope = (sendslope * 75) / (100 - 75)

SI queue empty et credit >= 0 alors 
    credit = 0 
FSI

* !isTransmitting ASSERT CLASS CAN'T TRANSMIT SERVERALS TIME AT THE SAME TIME *
SI queue != empty && !isTransmitting && credit >= 0 alors
    Tant que credit >= 0 
            isTransmitting = true
            transmet trame
            enlever trame queue
            credit decreased by sendslope
    FTQ
    isTransmitting = false
FSI

SI queue != empty and !isTransmitting
    credit increase by idleslope
FSI

** transmet trame **

** enlever trame queue **

** credit decreased by sendslope **

credit = credit - sendslope

** credit increase by idleslope **

credit = credit + idleslope

```

# TAS

```


```
# La trame 802.1Qav
Ethernet est le protocole cible pour faire du TSN. Dans le cadre du *traffic shaping*, des classes sont attribuées à chaque trame qui doit passer par le réseau. Ces classes là indiquent la priorité de la trame.

Pour indiquer la classe, le champ du VLAN tag est utilisé. Plus précisément le champ *Priority Code Point (PCP)*. L'organisation d'entête dans la trame est la suivante :
```c
header ethernet_t {
    bit<48> dstAddr;
    bit<48> srcAddr;
    bit<32> VLAN_Tag; // bit<16> TPID | bit<3> PRI | bit<1>CFI | bit<12> VID 
    bit<16> etherType;
}
// TPID:=Tag Protocol Identifier | PRI:= Priority Code Point | CFI := Canonical Format Identifier | VID:= VLAN ID
```
## Tag protocol identifier, TPID
Les 16 premiers bits sont utilisés pour identifier le protocole de la balise insérée. Dans le cas de la balise 802.1Q la valeur de ce champ est fixée à 0x8100. 

## Priorité ( PCP : Priority Code Point )
Ce champ de 3 bits fait référence au standard IEEE 802.1p. Sur 3 bits on peut coder 8 niveaux de priorité de 0 à 7. Ces 8 niveaux sont utilisés pour fixer une priorité aux trames d'un VLAN relativement aux autres VLAN. La notion de priorité dans les VLAN (niveau 2) est indépendante des mécanismes de priorité IP (niveau 3). 

## Canonical Format Identifier, CFI
Ce champ codé sur 1 bit assure la compatibilité entre les adresses MAC Ethernet et Token Ring. Un commutateur Ethernet fixera toujours cette valeur à 0. Si un port Ethernet reçoit une valeur 1 pour ce champ, alors la trame ne sera pas propagée puisqu'elle est destinée à un port «sans balise» (untagged port). 

## VLAN Id, VID
Ce champ de 12 bits sert à identifier le virtual lan (VLAN) auquel appartient la trame. Il est possible de coder 4094 VLAN (de 1 à 4094) avec ce champ. La valeur "0" signifie qu'il n'y a pas de VLAN, et la valeur 4095 est réservée. Les valeurs 1002 à 1005 sont réservées pour des protocoles de niveau 2 différents d'Ethernet. 

```
+---------------------+----------------+---------+--------+-------+---------+-------------+---------------+---------+
| Destination Address | Source Address | TPID    | PRI    | CFI   | VID     | Length/Type | Data          | FCS     |
+---------------------+----------------+---------+--------+-------+---------+-------------+---------------+---------+
| 6 bytes             | 6 bytes        | 2 bytes | 3 bits | 1 bit | 12 bits | 2 bytes     | 46-1500 bytes | 4 bytes |
+---------------------+----------------+---------+--------+-------+---------+-------------+---------------+---------+
```
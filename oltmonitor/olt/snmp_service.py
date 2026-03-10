from pysnmp.hlapi import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    nextCmd
)

def snmp_walk(ip, community, oid):

    results = []

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in nextCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),  # SNMP v2c
            UdpTransportTarget((ip, 161), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            lexicographicMode=False):

        if errorIndication:
            print("SNMP error:", errorIndication)
            break

        if errorStatus:
            print("SNMP status:", errorStatus.prettyPrint())
            break

        for varBind in varBinds:
            results.append(varBind)

    return results
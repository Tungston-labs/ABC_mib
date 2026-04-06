from fastapi import FastAPI
from pysnmp.hlapi import *

app = FastAPI()

OLT_IP = "10.10.0.7"
COMMUNITY = "public"

def snmp_get(oid):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(COMMUNITY),
        UdpTransportTarget((OLT_IP, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        return str(errorIndication)

    if errorStatus:
        return str(errorStatus)

    for varBind in varBinds:
        return str(varBind[1])


@app.get("/olt-info")
def get_olt_info():
    return {
        "olt_name": snmp_get("1.3.6.1.2.1.1.5.0"),
        "description": snmp_get("1.3.6.1.2.1.1.1.0"),
        "uptime": snmp_get("1.3.6.1.2.1.1.3.0"),
    }





# from fastapi import FastAPI
# from pysnmp.hlapi import *

# app = FastAPI()

# # Your OLT list
# OLTS = [
#     {"name": "OLT-1", "ip": "10.10.0.7", "community": "public"},
#     {"name": "OLT-2", "ip": "10.10.0.8", "community": "public"},
#     {"name": "OLT-3", "ip": "10.10.0.9", "community": "public"},
# ]

# # -----------------------------
# # SNMP WALK FUNCTION
# # -----------------------------
# def snmp_walk(olt_ip, community, oid):
#     results = []

#     try:
#         for (errorIndication,
#              errorStatus,
#              errorIndex,
#              varBinds) in nextCmd(
#                 SnmpEngine(),
#                 CommunityData(community),
#                 UdpTransportTarget((olt_ip, 161), timeout=3, retries=2),
#                 ContextData(),
#                 ObjectType(ObjectIdentity(oid)),
#                 lexicographicMode=False
#         ):
#             if errorIndication:
#                 print(f"{olt_ip} ERROR: {errorIndication}")
#                 return []

#             elif errorStatus:
#                 print(f"{olt_ip} ERROR: {errorStatus.prettyPrint()}")
#                 return []

#             else:
#                 for varBind in varBinds:
#                     results.append(varBind)

#     except Exception as e:
#         print(f"{olt_ip} EXCEPTION: {e}")
#         return []

#     return results


# # -----------------------------
# # CONVERT SNMP LIST → DICTIONARY (INDEX BASED)
# # -----------------------------
# def convert_to_dict(snmp_data):
#     result = {}

#     for oid, value in snmp_data:
#         try:
#             index = str(oid).split('.')[-1]
#             result[index] = str(value)
#         except:
#             continue

#     return result


# # -----------------------------
# # API: FETCH ALL OLT ONU DATA
# # -----------------------------
# @app.get("/all-olts-onus")
# def get_all_olts_onus():

#     response = []

#     # ⚠️ REPLACE THESE WITH REAL OIDs
#     ONU_ID_OID = "1.3.6.1.2.1.2.2.1.2"   # example (interface name)
#     ONU_PORT_OID = "1.3.6.1.2.1.2.2.1.3" # example
#     ONU_RX_OID = "1.3.6.1.2.1.2.2.1.10"  # example (in traffic)
#     ONU_TX_OID = "1.3.6.1.2.1.2.2.1.16"  # example (out traffic)

#     for olt in OLTS:

#         olt_data = {
#             "olt_name": olt["name"],
#             "ip": olt["ip"],
#             "onus": [],
#             "status": "success"
#         }

#         # -----------------------------
#         # SNMP FETCH
#         # -----------------------------
#         onu_ids = snmp_walk(olt["ip"], olt["community"], ONU_ID_OID)
#         onu_ports = snmp_walk(olt["ip"], olt["community"], ONU_PORT_OID)
#         onu_rx = snmp_walk(olt["ip"], olt["community"], ONU_RX_OID)
#         onu_tx = snmp_walk(olt["ip"], olt["community"], ONU_TX_OID)

#         # If no data → skip
#         if not onu_ids:
#             olt_data["status"] = "failed"
#             olt_data["error"] = "SNMP failed or no data"
#             response.append(olt_data)
#             continue

#         # -----------------------------
#         # CONVERT TO DICTIONARY
#         # -----------------------------
#         onu_id_dict = convert_to_dict(onu_ids)
#         onu_port_dict = convert_to_dict(onu_ports)
#         onu_rx_dict = convert_to_dict(onu_rx)
#         onu_tx_dict = convert_to_dict(onu_tx)

#         # -----------------------------
#         # MERGE USING INDEX
#         # -----------------------------
#         for index in onu_id_dict:

#             olt_data["onus"].append({
#                 "index": index,
#                 "onu_id": onu_id_dict.get(index),
#                 "pon_port": onu_port_dict.get(index),
#                 "rx_signal": onu_rx_dict.get(index),
#                 "tx_signal": onu_tx_dict.get(index),
#             })

#         response.append(olt_data)

#     return response
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import OLT, ONU
from .snmp_service import snmp_walk
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def fetch_olt_onu(request):

    olts = OLT.objects.filter(enabled=True)

    for olt in olts:

        # LOG: Starting poll for this OLT
        logger.info(f"Polling OLT: {olt.name} ({olt.ip_address})")

        try:

            mac_list = snmp_walk(olt.ip_address, olt.community, "MAC_OID")
            signal_list = snmp_walk(olt.ip_address, olt.community, "SIGNAL_OID")
            status_list = snmp_walk(olt.ip_address, olt.community, "STATUS_OID")

            logger.info(f"Fetched {len(mac_list)} ONUs from {olt.name}")

            for i in range(len(mac_list)):

                mac = str(mac_list[i][1])
                signal = float(signal_list[i][1])
                status = str(status_list[i][1])

                # LOG: Each ONU processed
                logger.debug(f"ONU {mac} | Signal {signal} | Status {status}")

                ONU.objects.update_or_create(
                    olt=olt,
                    mac_address=mac,
                    defaults={
                        "signal": signal,
                        "status": status
                    }
                )

        except Exception as e:
            # LOG: Error while polling this OLT
            logger.error(f"SNMP polling failed for {olt.name}: {str(e)}")

        olt.last_polled = timezone.now()
        olt.save(update_fields=['last_polled'])

    onus = ONU.objects.all().values()

    return Response(onus)
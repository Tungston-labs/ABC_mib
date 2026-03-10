from django.db import models

# Create your models here.
from django.db import models

class OLT(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    community = models.CharField(max_length=50)
    enabled = models.BooleanField(default=True)  # Activate/deactivate OLT
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional location info
    olt_number = models.CharField(max_length=50, blank=True, null=True)  # If your OLTs have a unique number
    last_polled = models.DateTimeField(blank=True, null=True)  # Timestamp of last SNMP poll

    def __str__(self):
        return f"{self.name} ({self.ip_address})"

    
    

class ONU(models.Model):
    olt = models.ForeignKey(OLT, on_delete=models.CASCADE)
    pon_port = models.IntegerField(null=True, blank=True)
    onu_index = models.IntegerField(null=True, blank=True)
    mac_address = models.CharField(max_length=50)
    signal = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)
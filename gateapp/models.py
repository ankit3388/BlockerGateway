from django.db import models

class UserDetails(models.Model):
    request_limit = models.IntegerField()
    block_private_ips = models.BooleanField()
    number_of_ips = models.IntegerField(null=True, blank=True)
    private_ips = models.TextField(null=True, blank=True)  # Store IPs as comma-separated values
    public_ips = models.TextField(null=True, blank=True)   # Store IPs as comma-separated values

    def __str__(self):
        return f"User {self.id} Details"
    

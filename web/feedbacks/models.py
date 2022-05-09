from django.db import models

from django.conf import settings

from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Circle(models.Model):
    name = models.CharField(max_length=50, default=0)

    def __str__(self):
        # return u'{0}'.format(self.circle_name)
        return str(self.name)

class Ssa(models.Model):
    name = models.CharField(max_length=50, default=0)
    circle = models.ForeignKey(Circle, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self.name)
        # return u'{0}'.format(self.circle_name)
        # return f"{self.circle}-{self.name}"        


class Mobile(models.Model):
   
    choice = (
        ('poor_network_coverage', 'Poor network coverage'),    
        ('low_data_speed', 'Low data speed'),
        ('absence_of_4g', 'Absence of 4G'),
        ('poor_customer_care', 'Poor customer care'),
        ('recharge_issues', 'Recharge issues'),
        ('billing_issues', 'Billing issues'),
        ('high_tariff', 'High Tariff'),
        ('vas', 'Value Added Services'),
        ('others', 'Others'),
        ('not_answered', 'Not Answered'),
        ('select', 'Select reason'),
    )

    # bool1 = models.BooleanField(blank=True, null=True)
    # bool2 = models.BooleanField(blank=True, null=True)
    # str1 = models.CharField(max_length=10, null=True, blank=True)
    # str2 = models.CharField(max_length=10, null=True, blank=True)
    msisdn = models.CharField(max_length=13)    
    account_no = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    # city = models.CharField(max_length=30, null=True, blank=True)
    ssa = models.ForeignKey(Ssa, on_delete=models.SET_NULL, blank=True, null=True)
    circle = models.ForeignKey(Circle, on_delete=models.SET_NULL, blank=True, null=True)
    upc_date = models.DateField(blank=True, null=True)
    upc_expiry_date = models.DateField(blank=True, null=True)
    connection_type = models.CharField(max_length=15, blank=True, null=True)
    avg_revenue = models.CharField(max_length=100, blank=True, null=True) 
    
    portout_apply_date = models.DateField(null=True, blank=True)
    portout_date = models.DateField(null=True, blank=True)
    port_status = models.CharField(max_length=50, null=True, blank=True)

    called_counter = models.IntegerField(default = 0) 

    reason_for_PO = models.CharField(
        max_length=30,
        choices=choice,
        blank=False,
        default='select',
        help_text='Reason for opting PO',
    )

    remarks = models.TextField(null=True, blank=True)
    feedback_date = models.DateTimeField(null=True, blank=True)
    user = models.CharField(max_length=50,null=True, blank=True)


    class Meta:
        ordering = ['-avg_revenue', 'circle', 'ssa', 'upc_date', 'msisdn']
         
    
    def __str__(self):
        """String for representing the Model object."""
        return str(self.pk)
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('mobile_detail', args=[str(self.id)])

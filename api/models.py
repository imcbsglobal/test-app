# api/models.py
from django.db import models

class AccUsers(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    pass_field = models.CharField(max_length=100, db_column='pass')

    class Meta:
        db_table = 'acc_users'
        managed = False  # Django won't create/migrate this table

    def __str__(self):
        return self.id


class AccInvDetails(models.Model):
    invno = models.DecimalField(max_digits=10, decimal_places=0)
    code = models.CharField(max_length=30)
    quantity = models.DecimalField(max_digits=15, decimal_places=5)
    id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'acc_invdetails'
        managed = False


class AccInvMast(models.Model):
    slno = models.DecimalField(max_digits=10, decimal_places=0, primary_key=True)
    invdate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'acc_invmast'
        managed = False


class AccProduct(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    openingquantity = models.DecimalField(max_digits=15, decimal_places=5, blank=True, null=True)
    stockcatagory = models.CharField(max_length=20, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=True, null=True)
    product = models.CharField(max_length=30, blank=True, null=True)
    brand = models.CharField(max_length=30, blank=True, null=True)
    billedcost = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    basicprice = models.DecimalField(max_digits=14, decimal_places=5, blank=True, null=True)
    partqty = models.DecimalField(max_digits=15, decimal_places=7, blank=True, null=True)

    class Meta:
        db_table = 'acc_product'
        managed = False


class AccProduction(models.Model):
    productionno = models.DecimalField(max_digits=10, decimal_places=0)
    date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'acc_production'
        managed = False


class AccProductionDetails(models.Model):
    masterno = models.DecimalField(max_digits=10, decimal_places=0)
    code = models.CharField(max_length=30)
    qty = models.DecimalField(max_digits=12, decimal_places=5)

    class Meta:
        db_table = 'acc_productiondetails'
        managed = False


class AccPurchaseDetails(models.Model):
    billno = models.DecimalField(max_digits=10, decimal_places=0)
    code = models.CharField(max_length=30)
    quantity = models.DecimalField(max_digits=12, decimal_places=5)

    class Meta:
        db_table = 'acc_purchasedetails'
        managed = False


class AccPurchaseMaster(models.Model):
    slno = models.DecimalField(max_digits=10, decimal_places=0, primary_key=True)
    date = models.DateField(blank=True, null=True)
    pdate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'acc_purchasemaster'
        managed = False

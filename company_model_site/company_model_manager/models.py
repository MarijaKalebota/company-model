from django.db import models

# Create your models here.

class Node(models.Model):
    root = models.ForeignKey('Node', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='+')
    parent = models.ForeignKey('Node', on_delete=models.DO_NOTHING, blank=True, null=True, related_name='+')
    height = models.BigIntegerField()
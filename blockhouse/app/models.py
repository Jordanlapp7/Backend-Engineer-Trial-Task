from django.db import models

# Create your models here.

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'timestamp')
        indexes = [models.Index(fields=['symbol', 'timestamp'])]

    def __str__(self):
        return f"{self.symbol} at {self.timestamp}"
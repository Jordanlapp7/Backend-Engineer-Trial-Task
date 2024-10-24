from django.db import models

# Create your models here.

class StockData(models.Model):
    symbol = models.CharField(max_length=10)
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high_price = models.DecimalField(max_digits=10, decimal_places=2)
    low_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('symbol', 'timestamp')
        indexes = [models.Index(fields=['symbol', 'timestamp'])]

    def __str__(self):
        return f"{self.symbol} at {self.timestamp}"
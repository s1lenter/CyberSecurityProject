from django.db import models

class AnalysisResult(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='parts/')
    table = models.TextField()
    isAll = models.BooleanField(default=True)



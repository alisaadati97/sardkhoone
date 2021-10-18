from django.db import models
from django.db.models.base import Model

# Create your models here.
class Data(models.Model):
    Temp = models.PositiveIntegerField()
    Humid = models.PositiveIntegerField()
    control_t = models.FloatField(null=True)
    control_h = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f'Temp : {self.Temp}  -- Huimid : {self.Humid}'
    
class Control(models.Model):
    auto = models.BooleanField(default=True)

    setpoint_t = models.IntegerField()
    kp_t = models.FloatField(null=True)
    ki_t = models.FloatField(null=True)
    kd_t = models.FloatField(null=True)

    setpoint_h = models.IntegerField(null=True)
    kp_h = models.FloatField(null=True)
    ki_h = models.FloatField(null=True)
    kd_h = models.FloatField(null=True)
    def __str__(self):
        return f'auto : {self.auto} -- setpoint_t : {self.setpoint_t}  -- setpoint_h : {self.setpoint_h}'

class Led(models.Model):
    on_t = models.BooleanField(default=True)
    on_h = models.BooleanField(default=True)
    def __str__(self):
        return f'led_state : {self.on_t} , {self.on_h} '

from django import forms
from .models import *

led_states = [
    ('on', 'open'),
    ('off', 'close'),
    ]
class LedTState(forms.Form):
    led_t_state = forms.CharField(widget=forms.RadioSelect(choices=led_states))

class LedHState(forms.Form):
    led_h_state = forms.CharField(widget=forms.RadioSelect(choices=led_states))

control_states = [
    ('auto', 'auto'),
    ('manual', 'manual'),
    ]
    
class ControlState(forms.Form):
    control_state = forms.CharField(widget=forms.RadioSelect(choices=control_states))

class SetPoint(forms.Form):
    setpoint_t = forms.IntegerField()
    setpoint_h = forms.IntegerField()

class PidT(forms.Form):
    kp_t = forms.CharField(required=False)
    ki_t = forms.CharField(required=False)
    kd_t = forms.CharField(required=False)

class PidH(forms.Form):
    kp_h = forms.CharField(required=False)
    ki_h = forms.CharField(required=False)
    kd_h = forms.CharField(required=False)
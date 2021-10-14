from django import forms

led_states = [
    ('on', 'on'),
    ('off', 'off'),
    ]

class LedState(forms.Form):
    led_state = forms.CharField(widget=forms.RadioSelect(choices=led_states))

control_states = [
    ('auto', 'auto'),
    ('manual', 'manual'),
    ]
    
class ControlState(forms.Form):
    control_state = forms.CharField(widget=forms.RadioSelect(choices=control_states))

class SetPoint(forms.Form):
    setpoint_t = forms.IntegerField()
    setpoint_h = forms.IntegerField()
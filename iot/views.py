from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse 
from .models import Data , Control , Led
from django.views.decorators.csrf import csrf_exempt
from .forms import LedState , ControlState , SetPoint
from simple_pid import PID


# Create your views here.
def savedata(request , H,T):
    print(f" {H},{T}")
    Data.objects.create(Temp = T , Humid = H)
    control = Control.objects.get(id=1)
    auto = control.auto
    if auto :
        #compute output valve for temperature with a pid controller
        setpoint_t = control.setpoint_t 
        pid = PID(13, 0, 0.05, setpoint=setpoint_t)
        pid.output_limits = (-100, 0) 
        control_t = pid(T)
        print(f' control_t is {control_t} ')

        #compute output valve for humidity with a pid controller
        setpoint_h = control.setpoint_h 
        pid = PID(2, 0, 0.05, setpoint=setpoint_h)
        pid.output_limits = (0, 100) 
        control_h = pid(H)
        print(f' control_H is {control_h} ')
        
        #set led state based on pid outputs
        '''led = Led.objects.get(id=1)
        if control_t < 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = -1*control_t)
        else:
            led.on = False
            return HttpResponse("output pid is here!Led is off" , status = 201)
        if control_h > 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = control_h)
        else:
            led.on = False
            return HttpResponse("output pid is here!Led is off" , status = 202)'''

    else : 
        #manual mode is on . there is no pid working and led state is set manually
        return HttpResponse("manual mode is on!" , status = 203)  
    return HttpResponse("output pid is here!Led is off" , status = 200)
def getpidtdata(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    auto = control.auto
    if auto :
        #compute output valve for temperature with a pid controller
        setpoint_t = control.setpoint_t 
        pid = PID(13, 0, 0.05, setpoint=setpoint_t)
        pid.output_limits = (-100, 0) 
        control_t = pid(data.Temp)
        print(f' control_t is {control_t} ')
        led = Led.objects.get(id=1)
        if control_t < 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = -1*control_t + 100)
        else:
            led.on = False
            return HttpResponse("output pid is here!Led is off" , status = 201)
    
def getpidhdata(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    auto = control.auto
    if auto :
        #compute output valve for humidity with a pid controller
        setpoint_h = control.setpoint_h 
        pid = PID(-2, 0, -0.05, setpoint=setpoint_h)
        pid.output_limits = (0, 100) 
        control_h = pid(data.Humid)
        print(f' control_H is {control_h} ')
        led = Led.objects.get(id=1)
        if control_h > 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = 100+control_h)
        else:
            led.on = False
            return HttpResponse("output pid is here!Led is off" , status = 202)

def getdata(request):
    data = Data.objects.all()[0]
    return JsonResponse({'Temp':data.Temp , 'Humid':data.Humid})

def testcase(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    led_obj = Led.objects.get(id=1)
    return JsonResponse({
            'Temp':data.Temp ,
            'Humid':data.Humid ,
            'led_state':led_obj.on,
            'control_state':control.auto,
            'control_setpoint_t':control.setpoint_t,
            'control_setpoint_h':control.setpoint_h,
            })

@csrf_exempt 
def index(request):
    sensor_data = Data.objects.all()[0]
    control = Control.objects.get(id=1)


    led_state_form = LedState(request.POST)
    control_state_form = ControlState(request.POST)
    setpoint_form = SetPoint(request.POST)

    if request.method == 'POST':  
        control_state_form = ControlState(request.POST)
        if control_state_form.is_valid():
            control_state = control_state_form.cleaned_data.get("control_state")
            control.auto = control_state == 'auto'
            control.save()
            control_state_form = ControlState()

    data = {
        'auto': control.auto  ,

        'temp':sensor_data.Temp ,
        'humid':sensor_data.Humid , 

        'led_state_form':led_state_form,
        'control_state_form':control_state_form,
        'setpoint_form':setpoint_form,
    }

    return render(request , 'index.html' , data)

@csrf_exempt 
def automode(request):
    control = Control.objects.get(id=1)
    if request.method == 'POST':
        setpoint_form = SetPoint(request.POST)  
        if setpoint_form.is_valid():
            setpoint_t = setpoint_form.cleaned_data.get("setpoint_t")
            setpoint_h = setpoint_form.cleaned_data.get("setpoint_h")
            control.setpoint_t = setpoint_t
            control.setpoint_h = setpoint_h
            control.save()
    return redirect('index')
 
@csrf_exempt 
def manualmode(request):
    led_obj = Led.objects.get(id=1)
    if request.method == 'POST':  
        led_state_form = LedState(request.POST)
        if led_state_form.is_valid():
            led_state = led_state_form.cleaned_data.get("led_state")
            led_obj.on = led_state == 'on'
            led_obj.save()
    return redirect('index')
     

from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse 
from .models import Data , Control , Led
from django.views.decorators.csrf import csrf_exempt
from .forms import LedTState ,LedHState, ControlState , SetPoint , PidT,PidH
from simple_pid import PID


# Create your views here.
def savedata(request , H , T ):
    print()
    print(f" Humidity: {H} , Tempereture: {T}")
    Data.objects.create(Temp = T , Humid = H)
    return HttpResponse("Data Saved Successfully" , status = 200)

def getpidtdata(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    led_obj = Led.objects.get(id=1)

    auto = control.auto
    if auto :
        #compute output valve for temperature with a pid controller
        setpoint_t = control.setpoint_t 
        pid = PID(control.kp_t, control.ki_t,control.kd_t, setpoint=setpoint_t)
        pid.output_limits = (-100, 0) 
        control_t = pid(data.Temp)
        print(f' output control tempereture is {-1*control_t} ')
        led = Led.objects.get(id=1)
        data.control_t = -1*control_t
        data.save()
        if control_t < 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = -1*control_t + 100)
        else:
            led.on = False
            return HttpResponse("Everything is ok!!" , status = 205)
    if led_obj.on_t:
        return HttpResponse("led  is on!" , status = 210 )
    else:
        return HttpResponse("led  is off!" , status = 211 )



def getpidhdata(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    led_obj = Led.objects.get(id=1)

    auto = control.auto
    if auto :
        #compute output valve for humidity with a pid controller
        setpoint_h = control.setpoint_h 
        pid = PID(control.kp_h, control.ki_h,control.kd_h, setpoint=setpoint_h)
        pid.output_limits = (-100, 0) 
        control_h = pid(data.Humid)
        print(f' output control humidity is {-1*control_h} ')
        led = Led.objects.get(id=1)
        data.control_h = -1*control_h
        data.save()
        if control_h < 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = 100+(-1*control_h))
        else:
            led.on = False
            return HttpResponse("Everything is ok!!" , status = 205)
    
    if led_obj.on_h:
        return HttpResponse("led  is on!" , status = 210 )
    else:
        return HttpResponse("led  is off!" , status = 211 )


def getdata(request):
    data = Data.objects.all()[0]
    return JsonResponse({'Temp':data.Temp , 'Humid':data.Humid , 'control_t':data.control_t , 'control_h':data.control_h})

@csrf_exempt 
def index(request):
    sensor_data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    led_obj = Led.objects.get(id=1)

    if control.auto:
        control_state = 'auto'
    else:
        control_state = 'manual'
    
    if led_obj.on_t:
        led_t_state_form = LedTState(initial={'led_t_state':'on'})
    else:
        led_t_state_form = LedTState(initial={'led_t_state':'off'})
    
    if led_obj.on_h:
        led_h_state_form = LedHState(initial={'led_h_state':'on'})
    else:
        led_h_state_form = LedHState(initial={'led_h_state':'off'})

    control_state_form = ControlState(initial={'control_state':control_state })
    setpoint_form = SetPoint(initial={'setpoint_t':control.setpoint_t , 'setpoint_h':control.setpoint_h})
    pidt_form = PidT(initial={'kp_t':control.kp_t ,'ki_t':control.ki_t ,'kd_t':control.kd_t })
    pidh_form = PidH(initial={'kp_h':control.kp_h ,'ki_h':control.ki_h ,'kd_h':control.kd_h })
    if request.method == 'POST':  
        control_state_form = ControlState(request.POST)
        if control_state_form.is_valid():
            control_state = control_state_form.cleaned_data.get("control_state")
            control.auto = control_state == 'auto'
            control.save()
            control_state_form = ControlState(initial={'control_state':control_state })

    data = {
        'auto': control.auto  ,

        'temp':sensor_data.Temp ,
        'humid':sensor_data.Humid , 

        'led_t_state_form':led_t_state_form,
        'led_h_state_form':led_h_state_form,
        'control_state_form':control_state_form,
        'setpoint_form':setpoint_form,
        'pidt_form':pidt_form,
        'pidh_form':pidh_form,
    }

    return render(request , 'index.html' , data)

@csrf_exempt 
def automode(request):
    control = Control.objects.get(id=1)
    if request.method == 'POST':
        setpoint_form = SetPoint(request.POST)  
        pidt_form = PidT(request.POST)
        pidh_form = PidH(request.POST)
        print(setpoint_form.is_valid() and pidt_form.is_valid() and pidh_form.is_valid())
        if setpoint_form.is_valid() and pidt_form.is_valid() and pidh_form.is_valid():
            setpoint_t = setpoint_form.cleaned_data.get("setpoint_t")
            setpoint_h = setpoint_form.cleaned_data.get("setpoint_h")
            control.setpoint_t = setpoint_t
            control.setpoint_h = setpoint_h

            control.kp_t = pidt_form.cleaned_data.get("kp_t")
            print(control.kp_t)
            print(pidt_form.cleaned_data.get("kp_t") , pidt_form.cleaned_data.get("ki_t") , pidt_form.cleaned_data.get("kd_t"))
            print(pidh_form.cleaned_data.get("kp_h") , pidh_form.cleaned_data.get("ki_h") , pidh_form.cleaned_data.get("kd_h"))
            control.ki_t = pidt_form.cleaned_data.get("ki_t")
            control.kd_t = pidt_form.cleaned_data.get("kd_t")

            control.kp_h = pidh_form.cleaned_data.get("kp_h")
            control.ki_h = pidh_form.cleaned_data.get("ki_h")
            control.kd_h = pidh_form.cleaned_data.get("kd_h")

            control.save()
    return redirect('index')
 
@csrf_exempt 
def manualmode(request):
    led_obj = Led.objects.get(id=1)
    if request.method == 'POST':  
        led_t_state_form = LedTState(request.POST)
        led_h_state_form = LedHState(request.POST)
        if led_t_state_form.is_valid() and led_h_state_form.is_valid() :
            
            led_state = led_t_state_form.cleaned_data.get("led_t_state")
            led_obj.on_t = led_state == 'on'

            led_state = led_h_state_form.cleaned_data.get("led_h_state")
            led_obj.on_h = led_state == 'on'

            led_obj.save()
    return redirect('index')
     


     

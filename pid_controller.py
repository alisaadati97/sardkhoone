from django.http import HttpResponse 
from .models import Data , Control , Led
from simple_pid import PID


# Create your views here.
def savedata(request , H , T ):
    print()
    print(f" Humidity: {H} , Tempereture: {T}")
    Data.objects.create(Temp = T , Humid = H)
    control = Control.objects.get(id=1)
    return HttpResponse("Data Saved Successfully" , status = 200)

def getpidtdata(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    auto = control.auto
    if auto :
        #compute output valve for temperature with a pid controller
        setpoint_t = control.setpoint_t 
        pid = PID(8, 0, 0.5, setpoint=setpoint_t)
        pid.output_limits = (-100, 0) 
        control_t = pid(data.Temp)
        print(f' output control tempereture is {-1*control_t} ')
        led = Led.objects.get(id=1)
        if control_t < 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = -1*control_t + 100)
        else:
            led.on = False
            return HttpResponse("Everything is ok!!" , status = 200)
    
def getpidhdata(request):
    data = Data.objects.all()[0]
    control = Control.objects.get(id=1)
    auto = control.auto
    if auto :
        #compute output valve for humidity with a pid controller
        setpoint_h = control.setpoint_h 
        pid = PID(-5, 0, -0.5, setpoint=setpoint_h)
        pid.output_limits = (0, 100) 
        control_h = pid(data.Humid)
        print(f' output control humidity is {control_h} ')
        led = Led.objects.get(id=1)
        if control_h > 0 :
            led.on = True
            return HttpResponse("output pid is here!" , status = 100+control_h)
        else:
            led.on = False
            return HttpResponse("Everything is ok!!" , status = 200)

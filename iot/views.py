from django.shortcuts import render , redirect
from django.http import HttpResponse , JsonResponse 
from .models import Data , Control , Led
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def savedata(request , H,T):
    print(H,T)
    Data.objects.create(Temp = T , Humid = H)
    control = Control.objects.get(id=1)
    auto = control.auto
    if auto :
        pass
        #pid compute and send data to arduino led
        setpoint = control.setpoint 
        led = Led.objects.get(id=1)
    else : 
        pass    
        #turn on or off manually   
    return HttpResponse("this is working222")

def getdata(request):
    data = Data.objects.all()[0]
    return HttpResponse("this is working" , status=190)
    return JsonResponse({'Temp':data.Temp , 'Humid':data.Humid})

@csrf_exempt 
def index(request):
    sensor_data = Data.objects.all()[0]

    control = Control.objects.get(id=1)
    if request.method == 'POST':  
        Auto = request.POST.get('auto',)
        control.auto = Auto == 'on'
        control.save()
    
    if control.auto:
        data = {
            'auto':1,
            'manual':0,
            'temp':sensor_data.Temp ,
            'humid':sensor_data.Humid , 
        }
        return render(request , 'index.html' , data)
    
    else:
        data = {
            'auto':0,
            'manual':1,
            'temp':sensor_data.Temp ,
            'humid':sensor_data.Humid , 
        }
        return render(request , 'index.html' , data )

@csrf_exempt 
def automode(request):
    control = Control.objects.get(id=1)
    if request.method == 'POST':  
        setpoint = request.POST.get('setpoint',)
        control.setpoint = setpoint
        print(f'setpoint is  {control.setpoint}')
        control.save()
    return redirect('index')
 
@csrf_exempt 
def manualmode(request):
    control = Control.objects.get(id=1)
    led_obj = Led.objects.get(id=1)
    if request.method == 'POST':  
        led_on = request.POST.get('led_on',)
        led_obj.on = led_on == 'on'
        print(f'led is now {led_obj.on}')
        led_obj.save()
    return redirect('index')
     

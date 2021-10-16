function httpGet(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
            xmlHttp.send( null );
            return xmlHttp.responseText;
        }
        function setText(id,newvalue) {
            var s = document.getElementById(id);
            s.innerHTML = newvalue;
            console.log(newvalue)
            }  
        function myFunction() {
            data = httpGet('http://192.106.100.63:8000/iot/getdata')
            data = JSON.parse(data)
            
            setText('temp',data.Temp)
            setText('humid',data.Humid)
            
            
            circle = document.getElementsByClassName('circle-inner')[0]
            gauge = document.getElementsByClassName('gauge-copy')[0]

            circle.style.transform = 'rotate(-45deg)' 
            gauge.style.transform  = 'translate(-50%, -50%) rotate(0deg)'

            temp = data.Temp*1.8-45
            circle.style.transform = 'rotate(' + temp + 'deg)' 
            gauge.style.transform  = 'translate(-50%, -50%) rotate(' + data.Temp * 1.8 + 'deg)'

            circle = document.getElementsByClassName('circle-inner')[1]
            gauge = document.getElementsByClassName('gauge-copy')[1]

            circle.style.transform = 'rotate(-45deg)' 
            gauge.style.transform  = 'translate(-50%, -50%) rotate(0deg)'

            humid = data.Humid*1.8-45
            circle.style.transform = 'rotate(' + humid + 'deg)' 
            gauge.style.transform  = 'translate(-50%, -50%) rotate(' + data.Humid * 1.8 + 'deg)'


        }
        var timer = setInterval( myFunction, 5000);
        
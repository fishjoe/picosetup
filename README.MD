# Micropython Device Setup Template
###### Virsion 1.1 
###### Both boot.py and README.MD are same files with different names. Thanks to MD format which I use ##### to format the readme file and comment in the real code. To use this template, you may simply copy the code into your own boot.py and flash it onto the board. It is reccomanded to name the file into _temp.py_ and run it before you impletement boot.py so it will not cause problem.
###### Modules Needed
import os
import sys
import network
import time
import ubinascii
import machine
import socket

###### TODO   Next update would inlude function to check update for package. 

##### This is a universal Setup *boot.py* file, designed for Raspberry Pi Pico(refered as Pico later). You maybe able to use this on other board but I'm not sure.
###### NOTE 1.2.3.4 For some apps which may create http-requests and send key-value chains to webpage, this function may help on processing such key-value chains.
###### such key-value chains may help on setting up the initial page without really seeing the page. a good example of this app is _**iOS Shortcuts**_, 
###### this setup templete fully support such functionnality.
###### _**CONDITIONS**_ please add "web_key_" in front of the original key, for example if key value included is "command":"setup", you need to name it "web_key_command":"setup" insdead.
###### TODO future update would includ the link to download setup "iOS Shortcut".



####Functions it will do at start up:
#####1. **Initial Check:** 
###### It will check if wifi was set up, by checking the existence of configfile called "config.json" --> if yes --> 3. **Normal Mode** else 2. **Access Point Mode**

config_file_name = "config.json" # *(you may change this value to what ever you want.)*

###### 1.1 It will also create essential objects and functions as a part of UI indication, especially when Pico is not connected to computer.


###### 1.2 A class of Feedback is created to overall manage the feedback actions at different stages, including led-blinks, Printout to screen.
class Feedback: # feedback attribute may include print_string
    def __init__(self, print_string, blink_numbers, blink_length, blind_length, led_gpio = None, sould_gpio = None) -> None:
        self.led_gpio = led_gpio if led_gpio else machine.Pin('LED', machine.Pin.OUT) # Default feedback led is onboard led however you may connect other devices as feedback.
        self.sound_gpio = sould_gpio # By default feedback sound is not active.
        self.print_string = print_string # message to return to user.
        self.blink_numbers = blink_numbers # how many blinks needed as indication.
        self.blink_length = blink_length # how long the led is on
        self.blind_length = blind_length # how long the led is off
        self.led_gpio.off()
        pass

###### 1.2.1 methods to overall generate feedback. you may call _Feedback(st,qty,on,off).feedback_ . 
    def feedback(self):
        self.led_blink()
        self.print_feedback()

###### 1.2.2 blink the onboard led for _self.blink_numbers_ of times, each blink turns on the LED lasting of self.blink_length seconds, with self.blind_length seconds gap. 
    def led_blink(self):
        led = self.led_gpio
        if self.blink_numbers==self.blind_length==self.blink_length==0:
            led.toggle()
        elif led.value() == 0:
            for i in range(self.blink_numbers):
                led.on()
                time.sleep(self.blink_length)
                led.off()
                time.sleep(self.blind_length)
        else:
            for i in range(self.blink_numbers):
                led.off()
                time.sleep(self.blind_length)
                led.on()
                time.sleep(self.blind_length)
                
    def value(self):
        return self.led_gpio.value()

    def sound(self):
        # currently nothing happens as with sound.
        pass

    def print_feedback(self):
        # may improve later.
        print(self.print_string)
        pass

###### 1.2.2.1 TODO instances of feedback methods.


###### 1.2.3 also create the class to create web page. 

class WebPage:
    def __init__(self, server_ip, html, css="", **kwargs) -> None: # **kwargs is the dictionary holding key value chains to create webforms.
###### 1.2.3.1 Originlal Html file to be processed.
        self.server = server_ip
        self.html = html
        self.css = css
        self.kwargs = kwargs
        pass

###### 1.2.3.2 Make the html string for hosing the page.
    def make_page(self):
        varibles_itr = []
        btn_itr = []
        jscode_itr = []
        html = self.html
        for content in self.kwargs:  # this list controls the amout of html elements. TODO: later development will make different types of elements.
            varibles_itr.append(content)
            html = html.replace('<!--_____content_form_____-->',
                                f'<!--_____content_form_____--><label class="label" for="{content}"> {content}: <input class="input" type="text" name="{content}" id="{content}" default="" /></label>')
            btn_itr.append(f"document.getElementById('{content}').value")
            jscode_itr.append(f"xmlhttp.setRequestHeader('{content}', {content})")
        btn_html = f'<button onclick="click_this(' + ',\n'.join(btn_itr) + ')">Okey</button>'
        self.html = html.replace("<!--_____content_button______-->", btn_html).replace("_____jscode_header_____", ";\n".join(jscode_itr)).replace(
            "_____jscode_variables_____", ",".join(varibles_itr)).replace("_____url_____", f"http://{sefl.server}:80")
#         print(staties)
        return self.html

###### 1.2.3.3 CSS code TODO not currently applied. 

###### 1.2.3.4 parse the useful header key-value chains into dics. Please read Note 1.2.3.4 at the beginning of the file. 
    def parse_header(self, request_str) -> dict:  
        keydic = {}
        li = request_str.split("\n")
        
            output = []
            for key_value in li:
                if ":" in key_value:
                    pair = key_value.strip().split(": ")
                    if len(pair) > 1:
                        key, value = pair 

        pass 

###### 1.2.3.5 method to host the page.
    def webpage(self):
    ###### 1.2.3.4.1 load the default_page, create feedback instance.
        html = self.html
    ###### 1.2.3.4.2 create socket connection
        host = socket.getaddrinfo(server, 80)[0][-1]
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(host)
        s.listen(1)
        webpage_feedback = Feedback(f"Listening on: {host}", 3, .2, .2)
        webpage_feedback.feedback()
        x = 0
        while True:
            x+=1
            count = 0
            cl, addr = s.accept()
            Feedback(f'client connected from{addr}', 3, .2, .2).feedback()
            request = cl.recv(1024)
            print(request)
            request = request.decode("utf8")
            # request = str(request)
            keyargs = self.parse_header()

            print("...........................................requested string........................................\n", request, "\n...................................................end string........................................\n")
           
                    
            
    #         response = "<p> led 1 </p>"
            # print(response)
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            time.sleep(1)        

###### 1.2.4 function on updating onboard packages. if needed
def update_mip():
    # under construction
    for f in os.listdir():
        if "." not in f:
            for subf in os.listdir("/"+f):                
                sublist = sublist + os.listdir("/"+f)
    pass


#####2. **Access Point Mode:** It will then run into Access Point mode to create a setup page with following credentials. 

if config_file_name not in os.listdir(): # if "config.json" exsits.....

######* 2.1 Create and access piont (ap) with following credentials:
###### These ssid and password are pre set into _Pico_ only for setup. Setup will create a config file so later on It will run as **Normal Mode**
    ap_ssid = "PicoWSetup"  # *(you may change these values to what you want.)*
    ap_psd = "0123456789"
    
###### Setup Access Point if suceed, led indicator would remain on untill user connect to the page.
###### If it fails, it means either the settings or the board has problem. it would blink 4 times in 2 seconds.    
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ap_ssid, password=ap_psd)
    ap.active(True)
    if ap.isconnected():
        print_str = f"Access Point is ready at {ap.ifconfig()[0]}, SSID : {ap_ssid}, Password : {ap_psd}"
        qty, on, off = 0,0,0 # turn the led on
    else:
        print_str = f"Access Point is failed, Please restart. If problem continues, you need to re-flash the board."
        qty, on, off = 4, .2, .3 # indecating the ap is not working. 
    fb_ap = Feedback(print_str, qty, on, off)
    fb_ap.feedback()    
    if fb_ap.led_gpio.value() == 0:
        sys.exit()

######* 2.2 Create a setup page for user to enter key information to connect to WIFI, at following ip_address, a default page is also loaded.:
    
    server = ap.ifconfig()[0] # ideally this value is going to be 192.168.4.1 for Pico, it might be different if you use other board  
    default_page = '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>SMARTGUI 1.0.0</title>
    <link rel="icon" type="image/png" href="http://smartgui.w3spaces.com/oldlogo32.png">
    <link rel="apple-touch-icon" type="image/png" href="http://smartgui.w3spaces.com/oldlogo180.png">
    <script type="application/javascript">
        
        var click_this = function (_____jscode_variables_____) {
        var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance
        var url = '_____url_____';
        xmlhttp.open("POST", url);
        _____jscode_header_____
        xmlhttp.send();
        console.log("complete");
        }

    </script>

    <style>/* Place your CSS styles in this file */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            background-color: rgb(250, 255, 225);
            color: rgb(70,10,10);
        }
        
        h1,p {
            margin: 1em auto;
            margin-bottom: 0;
            text-align: center;
            font-weight: bolder;
            padding: 0;
        }
        
        form {
            width: 60vw;
            background-color: rgb(250, 255, 225);
            margin-left: auto;
            margin-right: auto;
            padding: 20px;
            max-width: 380px;
            min-width: 300px;
        }
        
        fieldset {
            border: none;
            padding: 2rem 0;
          }
        
        label {
            display: block;
            margin: 1rem 0;
        }
        
        /* p {
            margin: auto;
        } */
        
        input {
            font-size: 18px;
            width: 100%;
            margin: 0;
            margin-top: 5px;
            background-color: rgb(255, 255, 255);
            border: 0;
            border-bottom: 1px solid rgb(240, 240, 225);
            border-radius: 5px;
            padding: 5px;
        }
        
        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
          -webkit-appearance: none;
          margin: 0;
        }
        
        .inline {
            width: unset;
            margin-top:  1em;
            margin-left: 1em;
        }
        
        .note {
            font-size: smaller;
        }
        
        button {
            display: block;
            width: 100%;
            margin: 0 auto;
            margin-top: -15px;
            font-size: 1.1rem;
            background-color: #e2e2e2;
            border: solid 1px black;
            border-radius: 5px;
        }
        
        </style>
    <title>Set Up Page</title>
</head>
<body>
        <h1>Initialise Setup</h1>
        <p>Thank you for choosing SMARTGUI. Please enter the wifi detail to start the service</p>
        <form>
            <fieldset class="item">
                <!--_____content_form_____-->
            </fieldset>
            <!--_____content_button______-->
        </form>

</body>
</html>
'''
######* The page will determine the following values:

    ssid = ""   
    password = ""
    is_static = False
    static_ip = "192.168.1.99"

###### This following function will return the above key info. function is at ###### 1.2.3 (serch keyword 1.2.3)

    ssid, password, is_static, static_ip = webpage(server, default_page)

######* 2.3 Save the infomation into "config.json" and restart the machine.




        

    
#####3. **Normal Mode:** connect to wifi
else: # Calls Normal Mode when "config.json" exists.
######* 3.1 Future Update: inside "config.json", a key would indicate if needed to update firmware and or packages. Then the function will be called depends.
    pass



if __name__ == "__main__":
    pass

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
import json

###### TODO   Next update would inlude function to check update for package. 

#####This is a universal Setup *boot.py* file, designed for Raspberry Pi Pico(refered as Pico later). You maybe able to use this on other board but I'm not sure.
###### NOTE 1.2.3.4 For some apps which may create http-requests and send key-value chains to webpage, this function may help on processing such key-value chains.
###### such key-value chains may help on setting up the initial page without really seeing the page. a good example of this app is _**iOS Shortcuts**_, 
###### this setup templete fully support such functionnality.
###### _**CONDITIONS**_ please add "web_key_" in front of the original key, for example if key value included is "command":"setup", you need to name it "web_key_command":"setup" insdead. 
###### only word without spaces are supported in key-value chains, not space in values. i.e "web_key_name":"Michael_Jackson" is supported, "web_key_name":"Michael Jackson" is not supported.
###### A standard setup iOS Shortcut may include "web_key_ssid":"YOUR_SSID", "web_key_password":"YOUR_PASSWORD", "web_key_is_static":"True", "web_key_staticIP":"192.168.1.125"......
###### TODO future update would includ the link to download setup "iOS Shortcut".



####Functions it will do at start up:
#####1. **Initial Check:** 
###### It will check if wifi was set up, by checking the existence of configfile called "config.json" --> if yes --> 3. **Normal Mode** else 2. **Access Point Mode**
static_ip = '192.168.1.98'
config_file_name = "config.json" # *(you may change this value to what ever you want.)*

###### 1.1 It will also create essential objects and functions as a part of UI indication, especially when Pico is not connected to computer.

led_gpio = machine.Pin('LED', machine.Pin.OUT) # example only, by default led_gpio would be onboard LED.
#buzzer = machine.Pin(1, machine.Pin.OUT)  # example.

<<<<<<< HEAD
####### adinition control step by setting the reset_ready variable
=======
url = "http://192.168.1.212:8000/picosetup" # This is variable made for 4.1, url used to update files.

>>>>>>> a26c7353594f0e6da0a1067cc1d5049a8102a30d

###### 1.2 A class of Feedback is created to overall manage the feedback actions at different stages, including led-blinks, Printout to screen.
class Feedback: # feedback attribute may include print_string
    def __init__(self, print_string, blink_numbers, blink_length, blind_length, print_sep=" ", print_end= "\r", led_gpio = None, sould_gpio = None) -> None:
        self.led_gpio = led_gpio if led_gpio else machine.Pin('LED', machine.Pin.OUT) # Default feedback led is onboard led however you may connect other devices as feedback.
        self.sound_gpio = sould_gpio # By default feedback sound is not active.
        self.print_string = print_string # message to return to user.
        self.print_end = print_end
        self.print_sep = print_sep
        self.blink_numbers = blink_numbers # how many blinks needed as indication.
        self.blink_length = blink_length # how long the led is on
        self.blind_length = blind_length # how long the led is off
        self.led_gpio.off()
        self.reset_ready = False
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
        print(self.print_string, sep = self.print_sep, end= self.print_end)
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
        self.html_default = html
        pass

###### 1.2.3.2 Make and process the html code as string, for hosing the page. 
    def make_page(self):
        varibles_itr = []
        btn_itr = []
        jscode_itr = []
        html = self.html_default
        if self.kwargs == {}:
            html=self.html_default
            self.html = html.replace('<!--_____content_form_____-->',
                                f'<p>Update Successfull</p>').replace("<!--_____content_button______-->","")
        else:
            for key, value in self.kwargs.items():  # this list controls the amout of html elements. TODO: later development will make different types of elements.
                dft = value
                content = key.upper()
                varibles_itr.append(content)
                html = html.replace('<!--_____content_form_____-->',
                                    f'<!--_____content_form_____--><label class="label" for="{content}"> {content}: <input class="input" type="text" name="{content}" id="{content}" default="{dft}" placeholder="{dft}" /></label>')
                btn_itr.append(f"document.getElementById('{content}').value")
                jscode_itr.append(f"xmlhttp.setRequestHeader('{content}', {content})")
            btn_html = f'<button onclick="click_this(' + ',\n'.join(btn_itr) + ')">Okey</button>'
            self.html = html.replace("<!--_____content_button______-->", btn_html).replace("_____jscode_header_____", ";\n".join(jscode_itr)).replace(
                "_____jscode_variables_____", ",".join(varibles_itr)).replace("_____url_____", f"http://{self.server}:80")
    #         print(staties)
        return self.html

###### 1.2.3.3 CSS code TODO not currently applied. 

###### 1.2.3.4 Parse the useful header key-value chains into dics. Please read Note 1.2.3.4 at the beginning of the file. 
    def parse_header(self, UTF8_decoded_request_str) -> dict: 
        def re_split(strr, rgx):
            import re
            regex = re.compile(rgx)
            return regex.split(strr)
        keydic = {}
        keylist = self.kwargs.keys()
#         print([key for key in keylist])
        li = UTF8_decoded_request_str.split("\n")
        rgx = "web_key_|:| |\'|\""
        for line in li:
            if "web_key_" in line:
                *_, second_half_line = line.replace("web_key_", "second_half_web_key_").split("second_half_")
                key, value, *_ = [i for i in re_split(second_half_line, rgx) if i != ""]
                keydic[key] = value
            elif ":" in line and any(key in line.split(":")[0] for key in self.kwargs.keys()): # condition any of items.keys in kwargs exist
#                 key, value, *_ = line.split(" |:")
                pair = line.split(":")
                pair = [i.strip().replace("\r", "") for i in pair]
                print(pair)
                key, value = pair[0].lower(), pair[1]
#                 print(f"this line -------- {line}")
#                 print(line.split(":"))
                keydic[key] = value
            else:
                pass
        self.kwargs = keydic if keydic != {} else self.kwargs # update dic with value
        return self.kwargs["ssid"], self.kwargs["password"], self.kwargs["static_ip"] 
    
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
        webpage_feedback = Feedback(f"\nListening on: {host}", 0, 0, 0)
        webpage_feedback.feedback()
        x = 0
        while True:
            x+=1
            count = 0
            cl, addr = s.accept()
            Feedback(f'client connected from{addr}', 3, .2, .2).feedback()
            request = cl.recv(1024)
#             print(request)
            request = request.decode("utf8")
            # request = str(request)

            print("...........................................requested string........................................\n", request, "\n...................................................end string........................................\n")

            ssid, password, static_ip = self.parse_header(request)
            response = self.make_page()
            if all([ssid!="", password!=""]):
                is_static = True if static_ip != "" else False
                return_dic = self.kwargs
                self.kwargs = {}
                response = self.make_page()
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                break
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.send(response)
            cl.close()
            time.sleep(1)
        return return_dic, ssid, password, is_static, static_ip
            
            

###### 1.2.4 function on updating onboard packages. if needed
def update_mip():
    # under construction
    for f in os.listdir():
        if "." not in f:
            for subf in os.listdir("/"+f):                
                sublist = sublist + os.listdir("/"+f)
    pass

###### 1.2.5 function to save ssid/password and static_ip setting into config.json.

def update_config(dic): # update json file
    with open(config_file_name, "w") as config:
        json.dump(dic, config)
    
###### 1.2.6 function to connect wifi.

def wifi_connection(ssid, psd, isAp=False, isStatic=True, iptp=(static_ip, '255.255.255.0', '192.168.1.254', '8.8.8.8')): # Keys may include ssid, password, isAP, isStatic, staticIPPresetTuple)
    count_on_attempts=0
    if isAp:
        isStatic = False
        wifi = network.WLAN(network.AP_IF)
        wifi.config(essid=ssid, password=psd)
        wifi.active(True)
        iptp=wifi.ifconfig()
        if wifi.isconnected():
            Feedback(f"Access Point is ready at {iptp[0]}, SSID : {ssid}, Password : {psd}", 0, 0, 0).feedback()
            time.sleep(.5)
            return wifi
        # access point is ready
    else:
        wifi = network.WLAN(network.STA_IF)
        Feedback("", 3, .1, .1).feedback()
        while True:
            if isStatic:
                wifi.ifconfig(iptp)
            wifi.active(True)
            wifi.connect(ssid, psd)
            count_on_attempts += 1
            if count_on_attempts == 10:
                Feedback(f"too many fails, please check settings or repair corrupted file", 10 , .2, .3).feedback()
                sys.exit()
#             print(count_on_attempts, "attempts")
#             print("network.status()code : ", wifi.status())
#             print("network.isconnected() : ", wifi.isconnected())
            print(".", end="", sep="")
            time.sleep(0.5)
            Feedback(f"too many fails, please check settings or repair corrupted file", count_on_attempts , .2, .3).feedback()
            ip = iptp[0] if not isStatic else wifi.ifconfig()[0]
            # print(wifi.isconnected()*bool(wifi.status()==3)*bool(wifi.ifconfig()[0]==iptp[0]))
#             print(ip)

            if all(
                    [
                        wifi.isconnected(),
                        wifi.status() == 3,
                        wifi.ifconfig()[0] == iptp[0]
                    ]
            ):
                # Wifi has problem sometimes, so I use "uping" to test and internal machine and an external site for
                # connection. uping module has been loaded in this file. I'm not using it for any comercial process. this is only
                # for learning.
                print("\nConnection Established")
                try:
                    internal_result = ping(wifi.ifconfig()[3], quiet=True)[1]
                    Feedback(f"Pinging an internal machine......", 4, .1, .1).feedback()
                    print(internal_result, "/ 4  Done")
                    print("Pinging an external site......", end="")
                    external_result = ping("google.com", quiet=True)[1]
                    print(external_result, "/ 4  Done")
                except:
                    internal_result=external_result=0
                    pass
                if internal_result * external_result == 0:
                    Feedback(f"Wifi not working,retry.....", 4, .1, .1).feedback()
                else:
                    print("WIFI connection succesfull")
                    break
        return wifi

###### 1.2.7 PINGing function from thirdparty.

# ----------------------------------------- including Olav Morken's "uping" ---------------------------
# ----------------------------------------- for learning purpose only ---------------------------

# µPing (MicroPing) for MicroPython
# copyright (c) 2018 Shawwwn <shawwwn1@gmail.com>
# License: MIT

# Internet Checksum Algorithm
# Author: Olav Morken
# https://github.com/olavmrk/python-ping/blob/master/ping.py
# @data: bytes
def checksum(data):
    if len(data) & 0x1:  # Odd number of bytes
        data += b"\0"
    cs = 0
    for pos in range(0, len(data), 2):
        b1 = data[pos]
        b2 = data[pos + 1]
        cs += (b1 << 8) + b2
    while cs >= 0x10000:
        cs = (cs & 0xFFFF) + (cs >> 16)
    cs = ~cs & 0xFFFF
    return cs


def ping(host, count=4, timeout=5000, interval=10, quiet=False, size=64):
    import utime
    import uselect
    import uctypes
    import usocket
    import ustruct
    import urandom

    # prepare packet
    assert size >= 16, "pkt size too small"
    pkt = b"Q" * size
    pkt_desc = {
        "type": uctypes.UINT8 | 0,
        "code": uctypes.UINT8 | 1,
        "checksum": uctypes.UINT16 | 2,
        "id": uctypes.UINT16 | 4,
        "seq": uctypes.INT16 | 6,
        "timestamp": uctypes.UINT64 | 8,
    }  # packet header descriptor
    h = uctypes.struct(uctypes.addressof(pkt), pkt_desc, uctypes.BIG_ENDIAN)
    h.type = 8  # ICMP_ECHO_REQUEST
    h.code = 0
    h.checksum = 0
    h.id = urandom.randint(0, 65535)
    h.seq = 1

    # init socket
    sock = usocket.socket(usocket.AF_INET, usocket.SOCK_RAW, 1)
    sock.setblocking(0)
    sock.settimeout(timeout / 1000)
    addr = usocket.getaddrinfo(host, 1)[0][-1][0]  # ip address
    sock.connect((addr, 1))
    not quiet and print("PING %s (%s): %u data bytes" % (host, addr, len(pkt)))

    seqs = list(range(1, count + 1))  # [1,2,...,count]
    c = 1
    t = 0
    n_trans = 0
    n_recv = 0
    finish = False
    while t < timeout:
        if t == interval and c <= count:
            # send packet
            h.checksum = 0
            h.seq = c
            h.timestamp = utime.ticks_us()
            h.checksum = checksum(pkt)
            if sock.send(pkt) == size:
                n_trans += 1
                t = 0  # reset timeout
            else:
                seqs.remove(c)
            c += 1

        # recv packet
        while 1:
            socks, _, _ = uselect.select([sock], [], [], 0)
            if socks:
                resp = socks[0].recv(4096)
                resp_mv = memoryview(resp)
                h2 = uctypes.struct(
                    uctypes.addressof(resp_mv[20:]), pkt_desc, uctypes.BIG_ENDIAN
                )
                # TODO: validate checksum (optional)
                seq = h2.seq
                if (
                    h2.type == 0 and h2.id == h.id and (seq in seqs)
                ):  # 0: ICMP_ECHO_REPLY
                    t_elasped = (utime.ticks_us() - h2.timestamp) / 1000
                    ttl = ustruct.unpack("!B", resp_mv[8:9])[0]  # time-to-live
                    n_recv += 1
                    not quiet and print(
                        "%u bytes from %s: icmp_seq=%u, ttl=%u, time=%f ms"
                        % (len(resp), addr, seq, ttl, t_elasped)
                    )
                    seqs.remove(seq)
                    if len(seqs) == 0:
                        finish = True
                        break
            else:
                break

        if finish:
            break

        utime.sleep_ms(1)
        t += 1

    # close
    sock.close()
    ret = (n_trans, n_recv)
    not quiet and print(
        "%u packets transmitted, %u packets received" % (n_trans, n_recv)
    )
    return (n_trans, n_recv)


# ----------------------------------------- "uping" end  ---------------------------------------------



#####2. **Access Point Mode:** It will then run into Access Point mode to create a setup page with following credentials. 

if config_file_name not in os.listdir(): # if "config.json" exsits.....

######* 2.1 Create and access piont (ap) with following credentials:
###### These ssid and password are pre set into _Pico_ only for setup. Setup will create a config file so later on It will run as **Normal Mode**
    ap_ssid = "PicoWSetup"  # *(you may change these values to what you want.)*
    ap_psd = "0123456789"
    
###### Setup Access Point if suceed, led indicator would remain on untill user connect to the page.
###### If it fails, it means either the settings or the board has problem. it would blink 4 times in 2 seconds.    

    
    ap = wifi_connection(ap_ssid, ap_psd, True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
#     print(mac)
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
    static_ip = "Leave Empty for DCHP"

###### This following function will return the above key info. function is at ###### 1.2.3 (serch keyword 1.2.3)
    page = WebPage(server, default_page, ssid = "", password = "", static_ip = "Leave Empty for DHCP")
    returnvalue = page.webpage() # values returned from processing the web request. Will be saved into json file.
    print(returnvalue[0])

######* 2.3 Save the infomation into "config.json" and restart the machine.
    update_config(returnvalue[0])  # use 1.2.5 function at line 211
    reset_feedback = Feedback(f"Reset in 5 Secs", 5, .2, .8)
    reset_feedback.feedback()
    # if reset_feedback.reset_ready == True:
    machine.reset()


###### 3. **Normal Mode:** connect to wifi
else: # Calls Normal Mode when "config.json" exists.
######* 3.1 Future Update: inside "config.json", a key would indicate if needed to update firmware and or packages. Then the function will be called depends.
    with open(config_file_name, "r") as config:
        dic = json.load(config)
        ssid = dic["ssid"]
        psd = dic["password"]
        static_ip = dic["static_ip"]
        is_static = False if static_ip == "" else True
        
###### 3.2 attempts to connect WIFI as a client with new infomation.
    wifi=network.WLAN()
    if all(
                    [
                        wifi.isconnected(),
                        wifi.status() == 3,
                        wifi.ifconfig()[0] != '0.0.0.0'
                    ]
            ):
        
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    else:
        wlan = wifi_connection(ssid, psd)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print(mac)

####### 3.3 Transport data.

####### 4. Testing if the remote server contains file for update.
# url = "http://192.168.1.212:8000"

def testing_url(url):
    target_ip = url.split("//")[1].split(":")[0]
    ping_result = ping(target_ip, quiet=True)
    if int(ping_result[0])*int(ping_result[1])==0:
        return False
    

testing_url(url)




from newfile import ping
url = "http://192.168.1.212:8000"

def testing_url(url):
    target_ip = url.split("//")[1].split(":")[0]
    ping_result = ping(target_ip, quiet=True)
    if int(ping_result[0])*int(ping_result[1])==0:
        return False
    else:
        return True    


result = testing_url(url)
print(result)
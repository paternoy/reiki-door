#!/usr/bin/env python

from flask import Flask,request,render_template, redirect, url_for, jsonify, Response
import logging
import time
import RPi.GPIO as GPIO
from SequenceMatcher import SequenceMatcher

lockPin = 18
callPin=17
app = Flask(__name__, static_url_path='')
lastPulseStart=-1
isPressed=0
sampleSequence = [[0.0, 0.38469886779785156], [0.7873218059539795, 0.3878810405731201], [1.5543298721313477, 0.45166516304016113]]
sampleSequence = [[0.0, 0.38469886779785156], [0.3333333333333333, 0.3878810405731201], [1.0, 0.45166516304016113]]
sequenceMatcher=SequenceMatcher()

def init():
  logging.info('Initializing...')
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(lockPin,GPIO.OUT)
  GPIO.setup(callPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.output(lockPin,False)
  GPIO.add_event_detect(callPin, GPIO.BOTH, callback=buttonCallback)
  sequenceMatcher.setTargetSequence(sampleSequence)

def buttonCallback(channel):
  isPressed = GPIO.input(callPin)
  logging.debug("Callback: {}".format(isPressed))
  if isPressed:
    buttonPressed()
  else:
    buttonReleased()

def buttonPressed():
  global lastPulseStart,isPressed
  logging.debug("Button Pressed")
  isPressed=1
  pressTime=time.time()
  if pressTime-lastPulseStart>3:
    sequenceMatcher.cleanup()
  if pressTime-lastPulseStart>0.1:
    lastPulseStart=pressTime

def buttonReleased():
  global lastPulseStart,isPressed
  if isPressed:
    releaseTime=time.time()
    duration=releaseTime-lastPulseStart
    if duration > 0.1:
      logging.debug("Button Released")
      sequenceMatcher.addPulse(lastPulseStart,duration)
      isPressed = 0
      matches = sequenceMatcher.checkMatch()
      if matches:
        logging.info('Sequence matches')
        sequenceMatcher.cleanup()
      else:
        logging.info('Sequence does not match')




@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/api/open',methods=['POST'])
def post():
  logging.debug("Open")
  GPIO.output(lockPin, True)
  time.sleep(1)
  GPIO.output(lockPin, False)
  return ('', 204)




if __name__ == '__main__':
  try:
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    init()
    app.run(host='0.0.0.0',port=8080,debug=False)
  finally:
    GPIO.cleanup()
    logging.info('Cleanup')

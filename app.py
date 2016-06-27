#!/usr/bin/env python

from flask import Flask,request,render_template, redirect, url_for, jsonify, Response
import logging
import time
import RPi.GPIO as GPIO

relePin = 18
app = Flask(__name__, static_url_path='')
GPIO.setmode(GPIO.BCM)
GPIO.setup(relePin,GPIO.OUT)
GPIO.output(relePin,False)

@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/api/open',methods=['POST'])
def post():
  logging.debug("Open")
  GPIO.output(relePin, True)
  time.sleep(1)
  GPIO.output(relePin, False)
  return ('', 204)


if __name__ == '__main__':
  try:
    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    logging.info('Initializing...')
    app.run(host='0.0.0.0',port=80,debug=False)
#  except KeyboardInterrupt:
#    logging.info('KeyboardInterrupt')
  finally:
    GPIO.cleanup()
    logging.info('Cleanup')

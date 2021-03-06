#!/usr/bin/env python
# -*- coding: utf-8 -*-

from stem.control import Controller
from flask import Flask

@app.route('/')
def index():
  return "<h1>Tor Service</h1>"
  
if __name__ == "__main__":
    app = Flask("serbot")
    port = 5000
    host = "127.0.0.1"
    hidden_svc_dir = "/tmp/"
    controller = Controller.from_port(address="127.0.0.1", port=9151)
    try:
        controller.authenticate()
        controller.set_options([
            ("HiddenServiceDir", hidden_svc_dir),
            ("HiddenServicePort", "80 %s:%s" % (host, str(port)))
            ])
        svc_name = open(hidden_svc_dir + "/hostname", "r").read().strip()
        print " [*] Created host: {service}".format(service=svc_name)
    except Exception as e:
        print e
    app.run()

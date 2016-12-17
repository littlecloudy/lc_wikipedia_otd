#! /env/bin python3

import sys
from gi.repository import Gio,GLib
from wikipediaotd import *
import threading


class App (Gtk.Application):
  def __init__ (self):
    Gtk.Application.__init__ (self,
                              application_id='org.littlecloudy.wikipediaotd',
                              flags=Gio.ApplicationFlags.FLAGS_NONE)

    GLib.set_application_name ('Wikipedia On This Day by Little Cloudy')
    self.connect ('activate', self.on_activate_app)

  def on_activate_app (self, app):
    win = Gtk.ApplicationWindow ()
    app.add_window (win)

    otd = WikipediaOtdApp (self,win)
    win.add (otd)
    
    win.show_all ()
    

if __name__ == '__main__':
  app = App ()
  app.run (None)

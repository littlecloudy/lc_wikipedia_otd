#! /env/bin python3

license_txt = """
  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
  
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
  MA 02110-1301, USA.
"""


from gi.repository import Gtk,GLib,Pango,Gio
from parser import *
import time, datetime

class WikipediaOtdApp (Gtk.Grid):
  def __init__ (self, application, parent_window):
    Gtk.Grid.__init__ (self)
    self.set_hexpand (True)

    header = Gtk.HeaderBar ()
    header.set_title ('Wikipedia On This Day')
    header.set_subtitle ('by Little Cloudy')
    header.set_show_close_button (True)
    parent_window.set_titlebar (header)

    cal_button = Gtk.Button.new_from_icon_name ('office-calendar',Gtk.IconSize.BUTTON)
    header.pack_start (cal_button)

    cal_popover = Gtk.Popover ()
    cal_popover.hide ()
    cal_popover.set_relative_to (cal_button)

    calendar = Gtk.Calendar ()
    cal_popover.add (calendar)

    section_combo = Gtk.ComboBoxText ()
    header.pack_start (section_combo)    
    
    sort_button = Gtk.Button.new_from_icon_name ('view-filter-symbolic', Gtk.IconSize.BUTTON)
    section_combo.add (sort_button)   
    Gtk.StyleContext.add_class (section_combo.get_style_context(), 'linked')

    menu_button = Gtk.MenuButton ()
    menu_image = Gtk.Image.new_from_icon_name ('view-more-symbolic', Gtk.IconSize.BUTTON)
    menu_button.add (menu_image)
    header.pack_end (menu_button)

    # menus
    menu_model = Gio.Menu ()
    
    first_menu = Gio.Menu ()
    first_menu.insert (0, 'Preferences', None)   
    first_menu.insert (1, 'About', 'app.about')

    about_action = Gio.SimpleAction.new ('about', None)
    application.add_action (about_action)

    second_menu = Gio.Menu ()
    second_menu.insert (0, 'Exit', 'app.exit')

    exit_action = Gio.SimpleAction.new ('exit', None)
    application.add_action (exit_action)

    first_section  = Gio.MenuItem.new_section (None, first_menu)
    second_section = Gio.MenuItem.new_section (None, second_menu)
    
    menu_model.insert_item (0, first_section)
    menu_model.insert_item (1, second_section)

    menu_button.set_menu_model (menu_model)
    menu_button.set_use_popover (True)

    scr_win = Gtk.ScrolledWindow ()
    scr_win.set_hexpand (True)
    scr_win.set_vexpand (True)
    self.attach (scr_win, 0,3,1,1)

    tView = Gtk.TreeView ()
    tView.set_headers_visible (False)
    scr_win.add (tView)
  
    tModel = Gtk.ListStore (str, str)
    tView.set_model (tModel)

    renderer = Gtk.CellRendererText ()
    renderer.set_property ('font-desc', Pango.FontDescription.from_string ('12'))

    date_column = Gtk.TreeViewColumn ('Date', renderer, text=0)
    date_column.set_sort_column_id (0)
    tView.append_column (date_column)

    data_column = Gtk.TreeViewColumn ('Events', renderer, text=1)
    tView.append_column (data_column)
  
    

    self.populate_section (section_combo)

    today = datetime.date.today ()
    month = CountryMonth.EN [today.month-1]
    day   = today.day

    self.parser = WikipediaOtdParser ('en', month, str(day))
    self.start_parsing ()

    
    cal_button.connect    ('clicked', self.show_calendar, cal_popover)
    section_combo.connect ('changed', self.populate_event_data, tModel)
    sort_button.connect   ('clicked', self.sort_data, date_column)
    about_action.connect  ('activate',self.show_about_dialog, parent_window)
    exit_action.connect   ('activate', self.exit_app, application)
    calendar.connect      ('day-selected', self.on_choose_date, cal_popover)

  def on_choose_date (self, calendar, cal_popover):
    year,month,day = calendar.get_date ()
    self.parser = None
    self.parser = WikipediaOtdParser ('en', CountryMonth.EN [month], str(day)) 
    self.start_parsing ()
    cal_popover.hide ()


  def exit_app (self, action, param, app):
    app.quit ()

  def show_about_dialog (self, action, param, parent_window):
    dialog = Gtk.AboutDialog ()
    dialog.set_program_name (GLib.get_application_name () )
    dialog.set_version ('0.0.0')
    dialog.set_copyright ('@ 2016-2017 little cloudy')
    dialog.set_license_type (Gtk.License.GPL_3_0)
    dialog.set_license (license_txt)
    dialog.set_wrap_license (True)
    dialog.set_authors (['William Thomas'])
    dialog.set_comments ("An Application to read\nWikipedia's On This Day article\nin convenient way")
    dialog.show_all ()
    res = dialog.run ()
    if res == Gtk.ResponseType.CANCEL:
      dialog.destroy ()
    dialog.destroy ()

  def sort_data (self, button, column):
    column.clicked ()

  def show_calendar (self, button, popover):
    popover.show_all  ()

  def start_parsing (self):
    self.parser.parsing_api ()

  def populate_section (self, section_combo):
    sections = ['Events', 'Births', 'Deaths', 'Holiday and rememberance']
    for item in sections:
      section_combo.append_text (item)

  def populate_event_data (self, section_combo, tModel):  
    if section_combo.get_active () == 0:
      val = self.parser.get_events_data_en ()
      tModel.clear ()
      for item in val:
        tModel.append ([item[0],item[1]])
    if section_combo.get_active () == 1:
      val = self.parser.get_births_data_en ()
      tModel.clear ()
      for item in val:
        tModel.append ([item[0],item[1]])
    if section_combo.get_active () == 2:
      val = self.parser.get_deaths_data_en ()
      tModel.clear ()
      for item in val:
        tModel.append ([item[0],item[1]])
    if section_combo.get_active () == 3:
      val = self.parser.get_holidays_data_en ()
      tModel.clear ()
      for item in val:
        tModel.append ([item[0],item[1]]) 


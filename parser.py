#! /env/bin python3
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  @ 2016 William 'Duncan' Thomas <littlecloudy@gmail.com>

import urllib.request
import json,re
from gi.repository import Gtk,GLib
import threading,time


class CountryCode :
  EN = 'en'
  DE = 'de'

class CountrySection :
  EN = ['==EVENTS==', '==BIRTHS==', '==DEATHS==', '==Holidays and observances==']
  
class CountryMonth:
  EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'Augustus', 'September', 'October', 'November', 'December']


class WikipediaOtdParser:
  def __init__ (self, country_title, month_title, date_text):
    # default : english wikipedia
    if country_title is None:
      country_title = 'en'

    self.wikipedia_otd_url_template = "http://{}.wikipedia.org/w/api.php?format=json&action=query&titles={}&rvprop=content&prop=revisions""".format (country_title, month_title + "_" + str(date_text))
    #self.wikipedia_otd_url_template = GLib.filename_to_uri ('/home/william/Desktop/fufu.json')    
    print (self.wikipedia_otd_url_template)
  def parsing_api (self):  
    try:
      uopen = urllib.request.urlopen (self.wikipedia_otd_url_template)
      data  = uopen.read ().decode ('utf-8')
      self.json_data = json.loads (data)
  
      for pagenumber,value in self.json_data ['query'] ['pages'].items ():
        pagenumber = pagenumber  
 
      self.content = self.json_data ['query'] ['pages'] [pagenumber] ['revisions'] [0] ['*']
    except urllib.error.URLError as e:
      pass
    return True

  def get_json_data (self):
    return self.json_data

  def get_events_data_en (self):
    val = []
    events_data = self.content.split ('==Births==')[0].split ('==Events==')[1]
    for line in events_data.splitlines ():
      whole_data = line.strip().split ('&ndash;', maxsplit=1)
      try:
        year  = whole_data[0].strip ().strip ('*[]').strip (' []')
        desc  = whole_data[1].strip ()
        # special thx to Martin Ender on his stackoverflow answer
        desc  = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', desc)

        val.append ( (year,desc) )
        #print (year,desc)
      except IndexError as e:
        pass
    return val
    

  def get_births_data_en (self):
    val = []
    birth_data = self.content.split ('==Deaths==')[0].split ('==Births==')[1]
    for line in birth_data.splitlines ():
      whole_data = line.strip().split ('&ndash;')
      try:
        year = whole_data[0].strip ().strip ('*[]').strip (' []')
        desc = whole_data[1].strip ()
        desc = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', desc)
        val.append ( (year,desc) )
        #print (year,desc)
      except IndexError as e:
        pass 
    return val

  def get_deaths_data_en (self):
    val = []
    death_data = self.content.split ('==Holidays and observances==')[0].split ('==Deaths==')[1]
    for line in death_data.splitlines ():
      whole_data = line.strip().split ('&ndash;')
      try:
        year = whole_data[0].strip ().strip ('*[]').strip (' []')
        desc = whole_data[1].strip ()
        desc = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', desc)
        val.append ( (year,desc) )
        #print (year,content)
      except IndexError as e:
        pass
    return val

  def get_holidays_data_en (self):
    val = []
    holiday_data = self.content.split ('==Holidays and observances==')[1].split ('==External links==')[0]
    for line in holiday_data.splitlines ():
      whole_data = line.strip().split ('*', maxsplit=1)
      try:
        year  = whole_data[0].strip ().strip ('*[]').strip (' []')
        desc  = whole_data[1].strip ()
        desc  = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]|]*)\]\]', r'\1', desc)
        val.append ( (year,desc) )
        #print (year,content)
      except IndexError as e:
        pass
    return val


#\[\[        # match two literal [
#(?:         # start optional non-capturing subpattern for pre-| text
   #[^\]|]   # this looks a bit confusing but it is a negated character class
            ## allowing any character except for ] and |
   #*        # zero or more of those
   #\|       # a literal |
#)?          # end of subpattern; make it optional
#(           # start of capturing group 1 - the text you want to keep
    #[^\]|]* # the same character class as above
#)           # end of capturing group
#\]\]        # match two literal ]

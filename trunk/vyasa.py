# --------------------------------------------------------------- #
# vyasa.py -- A simple text editor in PyGTk                       #
# Copyright (C) 2006, Baishampayan Ghose <b.ghose@gnu.org>        #
#                                                                 #
# This program is free software; you can redistribute it and/or   #
# modify it under the terms of the GNU General Public License as  #
# published by the Free Software Foundation; either version 2 of  #
# the License, or (at your option) any later version.             #
#                                                                 #
# This program is distributed in the hope that it will be useful, #
# but WITHOUT ANY WARRANTY; without even the implied warranty of  #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the    #
# GNU General Public License for more details.                    #
#                                                                 #
# You should have received a copy of the GNU General Public       #
# License along with this program; if not, write to the Free      #
# Software Foundation, Inc., 51 Franklin Street - Fifth Floor,    #
# Boston, MA 02110-1301, USA.                                     #
# --------------------------------------------------------------- #

import os
import pygtk
pygtk.require('2.0')
import gtk
import gtk.glade

class Vyasa:
	def __init__(self):
		self.xml = gtk.glade.XML('vyasa.glade')
		self.xml.signal_autoconnect(self)
		self.status_bar = self.xml.get_widget("statusbar1")
		self.context_id = self.status_bar.get_context_id("Vyasa Text Editor")
		self.filename = "Untitled"
		self.win = self.xml.get_widget("main")
		self.title = "Vyasa Text Editor"
		self.win.set_title(self.title + " - " + self.filename)
		
	
	def on_main_destroy(self, widget, data=None):
		self.textview = self.xml.get_widget("textview1")
		self.textbuffer = self.textview.get_buffer()
		if (self.textbuffer.get_modified()):
			self.warn_dialog = self.xml.get_widget("warn_dialog")
			response = self.warn_dialog.run()
			self.warn_dialog.destroy()
			if (response == gtk.RESPONSE_YES):
				self.on_save_as_activate(self, widget)
		gtk.main_quit()


	def on_quit_activate(self, widget, data=None):
		self.on_main_destroy(self, widget)

	def	on_about_activate(self, widget, data=None):
		self.about = self.xml.get_widget("aboutdialog")
		self.about.run()
		
	def on_open_activate(self, widget, data=None):
		self.filechooser = FileSelection()
		if (self.filechooser.fname):
			self.show_file(self.filechooser.fname)
			
	def show_file(self, filename):
		if (filename):
			self.fname = filename
			self.textview = self.xml.get_widget("textview1")
			self.textbuffer = self.textview.get_buffer()
			self.infile = open(filename, "r")
			if (self.infile):
				self.string = self.infile.read()
				self.infile.close()
				self.textbuffer.set_text(self.string)
				self.textbuffer.set_modified(False)
				self.main = self.xml.get_widget("main")
				title = "Vyasa Text Editor"
				title = title + " - " + os.path.basename(filename)
				self.main.set_title(title)
				self.status_bar.push(self.context_id, "File opened")
				
	def new_file(self, widget, data=None):
		self.textview = self.xml.get_widget("textview1")
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("")
		self.main = self.xml.get_widget("main")
		self.main.set_title("Vyasa Text Editor" + " - " + self.filename)
		self.status_bar.push(self.context_id, "New file")
		self.textbuffer.set_modified(False)

	def write_file(self, filename, textbuffer):
		fp = open(filename, "w")
		if (fp):
			start, end = textbuffer.get_bounds()
			chars = textbuffer.get_slice(start, end, False)
			fp.write(chars)
			fp.close()
			self.status_bar.push(self.context_id, "Saved")
			self.textbuffer.set_modified(False)
			
	def on_save_activate(self, widget, data=None):
		self.textview = self.xml.get_widget("textview1")
		self.textbuffer = self.textview.get_buffer()
		if (self.textbuffer.get_modified()):
			try:
				if self.fname:
					bak_filename = self.fname + "~"
					os.rename(self.fname, bak_filename)
					self.write_file(self.fname, self.textbuffer)
			except(AttributeError):
				self.on_save_as_activate(self, widget)
		else:
			self.status_bar.push(self.context_id, "Nothing to save")

	def on_word_wrap_toggled(self, widget, data=None):
		self.word_wrap = self.xml.get_widget("word_wrap")
		self.textview = self.xml.get_widget("textview1")
		if (self.word_wrap.get_active()):
			self.textview.set_wrap_mode(gtk.WRAP_WORD)
		else:
			self.textview.set_wrap_mode(gtk.WRAP_NONE)
			
	def on_save_as_activate(self, widget, data=None):
		self.textview = self.xml.get_widget("textview1")
		self.textbuffer = self.textview.get_buffer()
		self.filechooser = SaveAsDialog()
		if (self.filechooser.fname):
				self.write_file(self.filechooser.fname, self.textbuffer)
			
	def main(self):
		gtk.main()

class FileSelection:
	def __init__(self):
		dialog = gtk.FileChooserDialog("Open Files...", None, gtk.FILE_CHOOSER_ACTION_OPEN, 
					(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		dialog.set_default_response(gtk.RESPONSE_OK)
		
		filter = gtk.FileFilter()
		filter.set_name("Text Files")
		filter.add_pattern("*.txt")
		filter.add_pattern("*.html")
		filter.add_pattern("*.xml")
		filter.add_pattern("*.c")
		filter.add_pattern("*.py")
		filter.add_pattern("*.cpp")
		filter.add_pattern("*.java")
		filter.add_mime_type("text/plain")
		dialog.add_filter(filter)
		
		response = dialog.run()

		if (response == gtk.RESPONSE_OK):
		    self.fname =  dialog.get_filename()
		else:
		    self.fname = False
		dialog.destroy()

class SaveAsDialog:
	def __init__(self):
		dialog = gtk.FileSelection("Save as...")
		response = dialog.run()
		if (response == gtk.RESPONSE_OK):
			self.fname = dialog.get_filename()
		else:
			self.fname = False
		dialog.destroy()
		
app = Vyasa()
app.main()

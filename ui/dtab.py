import linuxcnc
import thread
import time
import os
import hal
import hal_glib

s = linuxcnc.stat()
c = linuxcnc.command()

def get_handlers(halcomp,builder,useropts):
        return [multiTable(halcomp,builder, useropts)]

class multiTable:
	ab_active_st = False
	cd_active_st = False
        def __init__(self,halcomp,builder,useropts):
                #hal_glib.GPin(halcomp.newpin('hal_currF', hal.HAL_FLOAT, hal.HAL_OUT))
                self.halcomp = halcomp
                self.builder = builder
		#self.sawThick = 4.0
		#self.builder.get_object("panelWidthSpin").set_active()
	
	def btn_active_ab_state(self,gtkobj,data=None):
		self.builder.get_object("button1").set_sensitive(self.ab_active_st)
		self.ab_active_st = not self.ab_active_st
		c.set_digital_output(29, self.ab_active_st)
		print(self.builder.get_object("filechooserbutton1").get_filename())
	def btn_active_cd_state(self,gtkobj,data=None):
		self.builder.get_object("button2").set_sensitive(self.cd_active_st)
                self.cd_active_st = not self.cd_active_st
		c.set_digital_output(30, self.cd_active_st)

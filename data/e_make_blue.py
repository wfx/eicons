#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, glob
import pygtk, gtk
from gimpfu import *
from gimpenums import *

# something to help with debugging
def debugMessage(Message):
    dialog = gtk.MessageDialog(None, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, Message)
    dialog.run()
    dialog.hide()


# make blue
def my_script_function(image,drawable) :
    for layer in image.layers:
        if layer.visible:
            pdb.gimp_image_set_active_layer(image, layer)
            pdb.gimp_invert(layer)
            pdb.plug_in_palettemap(image, image.active_layer)
            pdb.gimp_brightness_contrast(image.active_layer, -52, 32)
            #debugMessage(pdb.gimp_item_get_name(layer))
    return

# This is the plugin registration function
register(
    "python_fu_e_makeblue",
    "Make blue icons",
    "A simple Python Script that color map each visible layer into selected palette",
    "Wolfgang Morawetz",
    "GPLv3",
    "01 2015",
    "<Image>/Enlightenment/Icon: Make blue",
    "*",
    [],
    [],
    my_script_function,
)

main()
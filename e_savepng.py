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


# convert & save
def my_script_function(image,drawable) :
    # where is the source image
    directory_name = os.path.dirname(pdb.gimp_image_get_filename(image))
    for layer in image.layers:
        if layer.visible:
            layer_name = pdb.gimp_item_get_name(layer)
            layer_name = "icon_" + layer_name.replace("-","_")
            png_file = os.path.join(directory_name, layer_name)
            pdb.file_png_save2(image, layer, png_file, png_file, 1, 9, 1, 1, 0, 1, 1, 1, 1)
            #debugMessage(png_file)
    return



# This is the plugin registration function
register(
    "python_fu_e_savepng",
    "Make blue icons",
    "A simple Python Script that save each visible layer as layername.png.",
    "Wolfgang Morawetz",
    "GPLv3",
    "01 2015",
    "<Image>/Enlightenment/Icon: Save all as PNG",
    "*",
    [],
    [],
    my_script_function,
)

main()
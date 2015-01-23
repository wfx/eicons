#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, glob
from gimpfu import *
from gimpenums import *


# create an output function that redirects to gimp's Error Console
def gprint( text ):
   pdb.gimp_message(text)
   return 

# make blue
def my_script_function(image,item) :
    pdb.gimp_context_set_palette('Enlightenment')

    color_brightness = -52
    color_contrast = 32

    blur_color = pdb.gimp_palette_entry_get_color('Enlightenment', 15)
    blur_radius = 4
    blur_opacity = 48

    for layer in image.layers:
        if layer.visible:
            pdb.gimp_image_set_active_layer(image, layer)
            #pdb.gimp_invert(layer)
            pdb.plug_in_palettemap(image, image.active_layer)
            pdb.gimp_brightness_contrast(image.active_layer, color_brightness, color_contrast)
            pdb.script_fu_drop_shadow(image, image.active_layer, 0, 0, blur_radius, blur_color, blur_opacity, 0)
            shadow_layer = pdb.gimp_image_get_layer_by_name(image, 'Drop Shadow')
            pdb.gimp_image_lower_item(image, image.active_layer)
            gprint(shadow_layer)
            new_icon = pdb.gimp_image_merge_down(image, shadow_layer, 2)
    return

# plugin registration
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
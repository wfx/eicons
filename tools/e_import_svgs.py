#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, glob
from gimpfu import *
from gimpenums import *

# create an output function that redirects to gimp's Error Console
def gprint( text ):
   pdb.gimp_message(text)
   return 

# import svg's
def my_script_function(image,item,dir) :

    svgs = glob.glob(dir + "/*.svg")

    width = pdb.gimp_image_width(image)
    height = pdb.gimp_image_height(image)
    resolution = 90

    RGBA_IMAGE = 1

    for filename in svgs:
        svg_img = pdb.file_svg_load(filename, filename, resolution, width, height, 0)
        pdb.gimp_selection_all(svg_img)
        pdb.gimp_edit_copy(svg_img.layers[0])
        head, tail = os.path.split(filename)
        image.new_layer(name=tail)
        floating_sel = pdb.gimp_edit_paste(image.layers[0], -1)
        pdb.gimp_floating_sel_anchor(floating_sel)
        pdb.gimp_image_delete(svg_img)

    return

# plugin registration
register(
    "python_fu_e_import_svgs",
    "Import SVG's",
    "A simple Python Script to import all svg file's as layers form a folder",
    "Wolfgang Morawetz",
    "GPLv3",
    "01 2015",
    "<Image>/Enlightenment/Icon/_Import SVG files",
    "*",
    [
        (PF_DIRNAME, "dir", "SVG's", "~/"),
    ],
    [],
    my_script_function,
)

main()
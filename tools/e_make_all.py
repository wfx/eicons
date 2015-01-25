#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, glob
from gimpfu import *
from gimpenums import *


# create an output function that redirects to gimp's Error Console
def gprint( text ):
   pdb.gimp_message(text)
   return 


def make_all(base_src, dest_src):

    #icon_group = ("actions", "apps", "categories", "devices", "emblems", "emotes", "mimetypes", "places", "status")
    icon_group = ("intl",)
    icon_size = ("16", "22", "24", "32", "48")

    for group in icon_group:
        for size in icon_size:
            image = pdb.gimp_image_new(size, size, 0)
            #drawable = image.layers[0]
            #file_xcf = dest_src + "/" + group + "/" + group + "_" + size
            base_svg = base_src + "/" + group
            dest_png = dest_src + "/" + group + "/" + size
            load_svgs(image, base_svg)
            e_color_map(image)
            save_png(image, dest_png)
    return


def load_svgs(image,dir):

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


# color map
def e_color_map(image) :
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


# save png
def save_png(image, dir) :
    if not os.path.exists(dir):
        os.mkdir( dir, 0755 );

    for layer in image.layers:
        if layer.visible:
            layer_name = pdb.gimp_item_get_name(layer)
            layer_name = "icon_" + layer_name.replace("-","_")
            layer_name = layer_name.replace("svg","png")
            png_file = os.path.join(dir, layer_name)
            pdb.file_png_save2(image, layer, png_file, png_file, 1, 9, 1, 1, 0, 1, 1, 1, 1)
    return


# plugin registration
register(
    "python_fu_e_make_all",
    "Make all icons for 16, 22, 24, 32 and 48px",
    "A simple Python Script to make all icons",
    "Wolfgang Morawetz",
    "GPLv3",
    "01 2015",
    "<Toolbox>/Enlightenment/Icon/_Make all eicons",
    "",
    [
        (PF_DIRNAME, "base_src", "Source for SVG's", "~/"),
        (PF_DIRNAME, "dest_src", "Destination for PNG's", "~/"),
    ],
    [],
    make_all,
)
main()
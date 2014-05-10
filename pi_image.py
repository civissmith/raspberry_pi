#!/usr/bin/python -B
################################################################################
# Copyright 2014 Phil Smith
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
################################################################################
# @Title: pi_image.py
#
# @Author: Phil Smith
#
# @Date: Sat, 10-May-14 04:37AM
#
# @Project: Raspberry Pi
#
# @Purpose: Writes an OS image from <image> to the SD card specified by 
#           <device>.
#
# @Revision:
# $Id: $
#
################################################################################
import argparse
import zipfile
import subprocess as sp
import os

#
# ImageWriter class
#
class ImageWriter:
  """ 
      The ImageWriter class is responsible for getting the image information
      and writing it to the SD card.
  """
  #
  # ImageWriter.__init__()
  #
  def __init__(self, image, device):
    self.image = image
    self.device = device
  #
  # End of ImageWriter.__init__()
  #

  #
  # ImageWriter.run()
  #
  def run(self):
    """
    Main routine for the ImageWriter.
    """
    # Assume OS is Linux for now.
    dd_func = []
    dd_func.append('sudo')
    dd_func.append('dd')
    # May make block size a parameter since it might need to be 1M instead of 4M.
    dd_func.append('bs=4M')
    dd_func.append('if='+self.image)
    dd_func.append('of='+self.device)
    print "Writing %s to %s, this may take several minutes!" % (self.image, self.device)
    sp.call(dd_func)
    
  #
  # End of ImageWriter.run()
  #

  #
  # ImageWriter.decompress_zip()
  #
  def decompress_zip(self, image):
    """ 
    Check to make sure that the image file exists and determine
    if it's a regular file or a zip file.
    """
    if zipfile.is_zipfile(image):

      # Open the zip file
      zFile = zipfile.ZipFile(image)
      
      # The "Advanced" images are stored with only one image, store
      # the name of the image and update the class.
      # This shouldn't be used for NOOBS images.
      zImage = zFile.namelist()[0]
      self.image = zImage
 
      # Extract the image, if it doesn't exist
      if not os.path.isfile(self.image):
        print "Decompressing %s" % self.image
        zFile.extract(zImage) 
      zFile.close() 

  #
  # End of ImageWriter.decompress_zip()
  #

#
# End ImageWriter class
#

#
# Invocation Check:
#
if __name__ == "__main__":
  descStr = """
  Write an Raspberry Pi OS image to an SD card.
  """
  parser = argparse.ArgumentParser(description=descStr)
  parser.add_argument('-i', '--image', help='Image file to write.')
  parser.add_argument('-d', '--dev', help='Path to the SD card.')
  args = parser.parse_args()

  if not args.image:
    print "No Image"
    exit(1)
  if not args.dev:
    print "No Device"
    exit(2)

  iw = ImageWriter(args.image, args.dev)
  iw.decompress_zip(args.image)
  iw.run()

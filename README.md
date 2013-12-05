pytclip
==========

Python implementation of [tclip](https://github.com/exinnet/tclip), a smart image cropping tool using OpenCV.

Installation
------------

If you're using Homebrew on Mac OS X and had Python 2.7 installed::

    pip-2.7 install numpy
    
    brew install Homebrew/science/opencv
    
    git clone https://github.com/CNBorn/pytclip.git

Usage
-----

.. code-block:: bash

    python pytclip.py -s source_image.jpg -d crop_image.jpg --width 300 --height 180


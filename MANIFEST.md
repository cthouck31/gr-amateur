title: The AMATEUR OOT Module
brief: Short description of gr-amateur
tags: # Tags are arbitrary, but look at CGRAN what other authors are using
  - sdr
author:
  - Author Name <authors@email.address>
copyright_owner:
  - Copyright Owner 1
license:
#repo: # Put the URL of the repository here, or leave blank for default
#website: <module_website> # If you have a separate project website, put it here
#icon: <icon_url> # Put a URL to a square image here that will be used as an icon on CGRAN
---
A longer, multi-line description of gr-amateur.
You may use some *basic* Markdown here.
If left empty, it will try to find a README file instead.


INSTALL

mkdir build
cd build
cmake ..
make
sudo make install
make applications


The last step is a result of the need to generate hierarchical blocks
that use OOT components. These have to be generated after the OOT module
has been installed to the system so the 'grcc' command can find the 
components. Unfortunately GNU Radio has not integrated a seemless
method for building/managing hierarchical blocks with OOT modules.

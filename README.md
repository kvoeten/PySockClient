# SIMLY

SIMLY is a project that enables rapid prototyping of Mixed Reality devices by offering ready to use, scalable communication technologies. This repository is for the Hub-Client, which acts as an intermediate between a Simulation and any number of Simly devices. Since python is a bit annoying to me the buffer performance is quite poor in this current implementation. It hasn't been tested with more than two devices at once, which works fine, but when scaling up you may encounter performance issues. For prototyping the Simly system python was selected due to it's easy multi-platform bluetooth libraries. Ideally this gets reworked into a C language in the future, or at least gets reworked to re-use byte buffers!

This repository also includes the arduino 'firmware', aka the code that runs on an arduino in order to make it compatible with all these Simly systems. The code on the arduino is quite performance friendly, using buffers and pointers to re-use memory almost constantly. (The only exception currently being allocating memory when finalizing packets.)

# Installation

It's in python so just make sure you have python3 installed and you can instantly run it from the command line. For more detailled instructions simply follow the guide in the documentation.

# Documentation

For more detailled instructions and some guides for setting up the whole Simly system with multiple XR devices, consult the documatation located at: https://simly.kazvoeten.com/

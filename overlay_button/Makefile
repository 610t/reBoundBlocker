# Makefile for BSD make(bmake)
LIB=-lX11 -lcairo -lXcomposite

all:	overlay_button

overlay_button:	overlay_button.cc
	c++ -o ${.TARGET} ${.ALLSRC} -I /usr/include/cairo ${LIB}

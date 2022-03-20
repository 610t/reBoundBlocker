#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/X.h>
#include <X11/Xutil.h>
#include <X11/keysym.h>
#include <X11/XKBlib.h>

#include <cairo.h>
#include <cairo-xlib.h>

#include <chrono>
#include <thread>

void draw(cairo_t *c, int width, int height)
{
    /* background */
    cairo_set_source_rgb(c, 1, 1, 1);
    cairo_rectangle(c, 0, 0, width, height);
    cairo_fill(c);
    /* red two triangles */
    cairo_set_source_rgb(c, 1, 0, 0);
    cairo_move_to(c, 0, 0);
    cairo_line_to(c, 0, height);
    cairo_line_to(c, width / 2, height / 2);
    cairo_line_to(c, 0, 0);
    cairo_fill(c);
    cairo_set_source_rgb(c, 1, 0, 0);
    cairo_move_to(c, width / 2, 0);
    cairo_line_to(c, width / 2, height);
    cairo_line_to(c, width, height / 2);
    cairo_line_to(c, width / 2, 0);
    cairo_fill(c);
}

int main()
{
    Display *d = XOpenDisplay(NULL);
    Window root = DefaultRootWindow(d);
    XEvent event;
    int default_screen = XDefaultScreen(d);
    unsigned int root_width, root_height;
    unsigned int width, height;
    unsigned int xoffset, yoffset;
    int quit_flag = 0;
    XWindowAttributes attr;

    //// Set window size
    // Application window width & height is 1/3 of root window's it.
    // And window shows at top right corner.
    XGetWindowAttributes(d, root, &attr);
    root_width = attr.width;
    root_height = attr.height;
    width = root_width / 3;
    height = root_height / 3;
    xoffset = root_width - width;
    yoffset = 0;

    // override_redirect means the window manager ignore this window.
    XSetWindowAttributes attrs;
    attrs.override_redirect = true;

    XVisualInfo vinfo;
    if (!XMatchVisualInfo(d, DefaultScreen(d), 32, TrueColor, &vinfo))
    {
        printf("No visual found supporting 32 bit color, terminating\n");
        exit(EXIT_FAILURE);
    }
    // these next three lines add 32 bit depth, remove if you dont need and change the flags below
    attrs.colormap = XCreateColormap(d, root, vinfo.visual, AllocNone);
    attrs.background_pixel = 0;
    attrs.border_pixel = 0;

    Window overlay = XCreateWindow(
        d, root,
        xoffset, yoffset, width, height, 0,
        vinfo.depth, InputOutput,
        vinfo.visual,
        CWOverrideRedirect | CWColormap | CWBackPixel | CWBorderPixel, &attrs);
    XMapWindow(d, overlay);
    XSelectInput(d, overlay, ButtonPressMask | KeyPressMask | KeyReleaseMask);

    cairo_surface_t *surf = cairo_xlib_surface_create(d, overlay,
                                                      vinfo.visual,
                                                      width, height);
    cairo_t *c = cairo_create(surf);

    draw(c, width, height);
    XFlush(d);

    while (quit_flag != 1)
    {
        XNextEvent(d, &event);

        switch (event.type)
        {
        case ButtonPress:
            system("/home/pi/reBoundBlocker/URL_changer/URL_changer.py &");
            break;
        case KeyPress:
            switch (XkbKeycodeToKeysym(d, event.xkey.keycode, 0, 0))
            {
            case XK_q:
            case XK_Q:
            case XK_Escape:
                quit_flag = 1;
            default:;
            }
            break;
        default:;
        }
    }

    cairo_destroy(c);
    cairo_surface_destroy(surf);

    XUnmapWindow(d, overlay);
    XCloseDisplay(d);
    return 0;
}

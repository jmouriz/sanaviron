#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

from objects.gradientcolor import GradientColor
from objects.gradient import Gradient
from interfaces.signalizable import Signalizable


class GradientLine(gtk.Viewport):
    def __init__(self, moving_callback=None, color_callback=None, gradient=None):
        """
        moving_callback - callback function to be called when changing position of the selected color(for spin widget)
        gradient - editable gradient
        """
        gtk.Viewport.__init__(self)
        self.set_size_request(-1, 70)
        self.set_shadow_type(gtk.SHADOW_NONE)
        self.width = 0
        self.height = 0
        self._motion = False
        self.selected = -1
        self.x = 0
        self.move = False
        self.gradient = gradient
        self.gradient.change_size(0, 0, 1, 0)
        self.moving_callback = moving_callback
        self.color_callback = color_callback
        self.layout = gtk.Layout()
        self.add(self.layout)

        self.layout.set_events(0)

        self.layout.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.layout.connect("button-press-event", self.press)
        self.layout.add_events(gtk.gdk.EXPOSURE_MASK)
        self.layout.connect("expose-event", self.expose)
        self.layout.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.layout.connect("button-release-event", self.release)
        self.layout.add_events(gtk.gdk.POINTER_MOTION_MASK)
        self.layout.connect("motion-notify-event", self.motion)
        self.layout.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
        self.layout.connect("enter-notify-event", self.enter)
        self.layout.add_events(gtk.gdk.LEAVE_NOTIFY_MASK)
        self.layout.connect("leave-notify-event", self.leave)

    def update(self):
        self.queue_draw()

    def set_position_for_selected(self, x):
        self.gradient.set_position(self.selected, x)

    def set_color_for_selected(self, color):
        color.position = self.gradient.colors[self.selected].position
        self.gradient.set_color(self.selected, color)

    def motion(self, widget, event):
        self._motion = True
        self.x = event.x
        if self.move:
            if self.selected >= 0:
                if self.moving_callback:
                    self.moving_callback(event.x / self.width)
                    self.set_position_for_selected(event.x / self.width)
                self.gradient.update()
        self.queue_draw()
        return True

    def enter(self, widget, event):
        return True

    def leave(self, widget, event):
        self._motion = False
        self.x = event.x
        self.queue_draw()
        return True

    def press(self, widget, event):
        self.move = True
        cnt = len(self.gradient.colors)
        if cnt > 0:
            for col in range(0, cnt):
                if (self.gradient.colors[col].position > (event.x / self.width - 0.01)) and (
                    self.gradient.colors[col].position < (event.x / self.width + 0.01)):
                    self.selected = col
                    self.moving_callback(self.gradient.colors[col].position)
                    self.color_callback(self.gradient.colors[col])
                    break
                else:
                    self.selected = -1

        if self.selected == -1 or not cnt:
            self.gradient.add_new_color(GradientColor(1, 1, 0.1, 1.0, event.x / self.width))
            self.selected = len(self.gradient.colors)-1
            self.moving_callback(self.gradient.colors[self.selected].position)
            self.color_callback(self.gradient.colors[self.selected])
            self.gradient.update()

        self.queue_draw()

    def release(self, widget, event):
        self.move = False
        self.queue_draw()

    def expose(self, widget, event):
        context = widget.bin_window.cairo_create()
        self.width, self.height = widget.window.get_size()

        context.save()
        context.new_path()
        #context.translate(0, 0)
        if (self.width > 0) and (self.height > 0):
            context.scale(self.width, self.height)

        context.rectangle(0, 0, 1, 1)
        context.set_source(self.gradient.gradient)
        context.fill_preserve()
        context.restore()

        if self._motion and not self.move:
            context.new_path()
            dash = list()
            context.set_dash(dash)
            context.set_line_width(2)
            context.move_to(self.x, 0)
            context.line_to(self.x, 30)
            context.move_to(self.x, self.height - 30)
            context.line_to(self.x, self.height)

            scol = sorted(self.gradient.colors,
                key=lambda color: color.position) # better in __init__ and update when necessary
            cnt = len(scol)
            rx = self.x / self.width
            index = 0
            for col in scol:
                if rx < col.position:
                    for c in range(0, cnt):
                        if self.gradient.colors[c].position == col.position:
                            index = c
                            break
                    break

            r = self.gradient.colors[index].red
            g = self.gradient.colors[index].green
            b = self.gradient.colors[index].blue
            l = 1 - (r + g + b) / 3.0
            if l >= 0.5:
                l = 1
            else:
                l = 0
            r, g, b = l, l, l
            context.set_source_rgba(r, g, b, 1.0)
            context.stroke()

        for color in range(len(self.gradient.colors)):
            if color == self.selected:
                delta = 10
            else:
                delta = 0

            context.new_path()
            pos = int(self.width * self.gradient.colors[color].position)
            context.move_to(pos - 5, 0)
            context.line_to(pos + 5, 0)
            context.line_to(pos, 20)
            context.line_to(pos - 5, 0)
            context.set_source_rgb(self.gradient.colors[color].alpha, self.gradient.colors[color].alpha,
                self.gradient.colors[color].alpha)
            context.fill_preserve()
            if delta:
                context.move_to(pos, 20)
                context.line_to(pos, 20 + delta)
            context.set_source_rgb(0.44, 0.62, 0.81)
            context.stroke()


class LinearGradientEditor(gtk.VBox, Signalizable):
    def __init__(self):
        gtk.VBox.__init__(self)

        from canvas import Canvas
        self.canvas = Canvas()

        table = gtk.Table(4, 4, False)
        self.pack_start(table)
        self.combobox = gtk.combo_box_new_text()
        table.attach(self.combobox, 1, 2, 0, 1, gtk.FILL, 0)

        gradient = Gradient()
        self.gl = GradientLine(self.moving_callback, self.color_callback, gradient)

        table.attach(self.gl, 1, 2, 1, 2, gtk.FILL | gtk.EXPAND, 0)
        new_color = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_NEW, gtk.ICON_SIZE_MENU)
        new_color.add(image)
        table.attach(new_color, 2, 3, 0, 1, 0, 0, 0)

        button = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GO_FORWARD, gtk.ICON_SIZE_MENU)
        button.add(image)
        button.connect("clicked", self.forward)
        table.attach(button, 2, 3, 1, 2, 0, gtk.FILL, 0)

        button = gtk.Button()
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_GO_BACK, gtk.ICON_SIZE_MENU)
        button.add(image)
        button.connect("clicked", self.back)
        table.attach(button, 0, 1, 1, 2, 0, gtk.FILL, 0)

        hbox = gtk.HBox()

        label = gtk.Label(_("Color:"))
        hbox.pack_start(label)

        self.color_button = gtk.ColorButton()
        self.color_button.set_use_alpha(True)
        self.color_button.connect("color-set", self.set_gradient_color)
        hbox.pack_start(self.color_button)

        label = gtk.Label(_("Position:"))
        hbox.pack_start(label)

        self.sel_position = gtk.SpinButton(climb_rate=0.00001, digits=5)
        self.sel_position.set_range(0.0, 1.0)
        self.sel_position.set_wrap(True)
        self.sel_position.set_increments(0.00001, 0.1)
        self.sel_position.connect("value-changed", self.move_color)
        hbox.pack_start(self.sel_position)

        table.attach(hbox, 1, 2, 2, 3, gtk.FILL, 0, 0)

        self.install_signal("update")

        self.show_all()

    def set_value(self, value):
        self.gl.gradient = Gradient(string=str(value))

    def forward(self, widget):
        if self.gl:
            if self.gl.selected < len(self.gl.gradient.colors) - 1:
                self.gl.selected += 1
            else:
                self.gl.selected = -1
        self.moving_callback(self.gl.gradient.colors[self.gl.selected].position)
        self.update()

    def back(self, widget):
        if self.gl:
            if self.gl.selected > -1:
                self.gl.selected -= 1
            else:
                self.gl.selected = len(self.gl.gradient.colors) - 1
            self.moving_callback(self.gl.gradient.colors[self.gl.selected].position)
            self.update()

    def moving_callback(self, x):
        self.sel_position.set_value(x)
        self.update()

    def color_callback(self, color):
        self.color_button.set_color(gtk.gdk.Color(float(color.red), float(color.green), float(color.blue)))
        self.color_button.set_alpha(int(color.alpha * 65535))
        self.update()

    def move_color(self, widget):
        if self.gl:
            self.gl.set_position_for_selected(widget.get_value())
            self.update()

    def set_gradient_color(self, widget):
        if self.gl:
            col = GradientColor(widget.get_color().red_float, widget.get_color().green_float,
                widget.get_color().blue_float, widget.get_alpha() / 65535.0,0)
            self.gl.set_color_for_selected(col)
            self.update()

    def update(self):
        self.gl.update()
        self.emit("update", self)
        #self.canvas.update()

if __name__ == '__main__':
    horizontal_window = gtk.Window()
    horizontal_window.set_default_size(500, 100)
    horizontal_window.connect("delete-event", gtk.main_quit)

    ge = LinearGradientEditor()
    horizontal_window.add(ge)

    horizontal_window.show_all()
    gtk.main()

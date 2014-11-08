# PyCha embedded in GTK example

#import pygtk
#pygtk.require('2.0')
import gtk

class gtk_example:
    def drawing_area_expose_event(self, widget, event, data=None):
        if self.chart is None:
            return

        cr = widget.window.cairo_create()
        cr.rectangle(event.area.x, event.area.y,
            event.area.width, event.area.height)
        cr.clip()
        cr.set_source_surface(self.chart.surface, 0, 0)
        cr.paint()

    def drawing_area_size_allocate_event(self, widget, event, data=None):
        if self.chart is not None:
            self.refresh()

    def refresh(self, action=None):
        alloc = self.drawing_area.get_allocation()
        self.chart = self.get_chart(alloc.width, alloc.height)
        self.drawing_area.queue_draw()

    def set_options(self):
        self.options = {
            'axis': {
                'labelFontSize': 12,
                'x': {
                    'ticks': self.xvals,
                    'label': self.setting,
                    'rotate': 45,
                    },
                'y': {
                    'tickCount': 0,
                    'rotate': 25,
                    'label': 'Precipitation (mm)',
                    }
            },
            'background': {
                'chartColor': '#d8e7ec',
                'baseColor': '#efebe7',
                'lineColor': '#444444'
            },
            'colorScheme': '#6eafc1',
            'legend': {
                'hide': False,
                },
            'padding': {
                'left': 75,
                'bottom': 55,
                },
            'stroke': {'hide': True},
            'title': 'Precipitation',
            }

    def set_data(self):
        self.dataset = (('lines', self.yvals),)

    def get_chart(self, width, height):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        chart = pycha.bar.VerticalBarChart(self.surface, self.options)
        chart.addDataset(self.dataset)
        chart.render()
        return chart

    def graph_update(self):
        self.set_data()
        self.set_options()
        self.refresh()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(500, 500)
        self.window.set_title("PyCha GTK Example")
        self.window.connect("delete_event", lambda w, e: gtk.main_quit())
        self.window.set_border_width(2)

        self.drawing_area = gtk.DrawingArea()
        self.drawing_area.connect('expose_event',
            self.drawing_area_expose_event)
        self.drawing_area.connect('size_allocate',
            self.drawing_area_size_allocate_event)

        self.widget.table.attach(self.drawing_area, 0, 4, 0, 14)
        self.drawing_area.show()

if __name__ == "main":
    gtk_example()

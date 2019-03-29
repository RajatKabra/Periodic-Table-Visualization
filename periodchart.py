from __future__ import absolute_import, division, print_function, unicode_literals
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.sampledata.periodic_table import elements
from bokeh.transform import dodge, factor_cmap
import logging
from bokeh.models.widgets import Slider, Select, TextInput, Button, MultiSelect, RadioGroup
import pandas as pd
from os.path import abspath, dirname, exists, expanduser, isdir, isfile, join, splitext
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.models.widgets import Slider, Select, TextInput
from bokeh.io import curdoc
from bokeh.layouts import column, row

log = logging.getLogger(__name__)
# from bokeh.util.api import public, internal ; public, internal
__all__ = (
    'elements',
)
def package_dir():
    '''
    '''
    return abspath(join(dirname(__file__), "..", "periodic"))
def package_path(filename):
    '''
    '''
    return join(package_dir(), filename)
def package_csv(module, name, **kw):
    '''
    '''
    return pd.read_csv(package_path(name), **kw)

elements = package_csv('periodic_table', 'elements.csv')

desc = Div(text="""<h1>Periodic Table Explorer</h1>

<p>
The graph presents the periodic table on web with features like hover over tips and filtering.

</p>
<p>
Prepared by <b>Rajat Kabra</b>.<br/>
Presented to <b>Prof. Kevin Smith</b>.<br/>
Under <b>Assignment 4 of CS 235</b>.
</p>
<br/>""")

div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
are <i>200</i> and <i>100</i> respectively.""",
width=200, height=100)


tsize = Slider(title="Period", start=1, end=7, value=7, step=1)
button = Button(label="Filter Hover View", button_type="success")
radio_group = RadioGroup(
        labels=["Name", "Atomic Number", "Atomic Mass","Metal","CPK Color"], active=0)
periods = ["I", "II", "III", "IV", "V", "VI", "VII"]
groups = [str(x) for x in range(1, 19)]

df = elements.copy()
df["atomic mass"] = df["atomic mass"].astype(str)
df["group"] = df["group"].astype(str)
df["period"] = [periods[x-1] for x in df.period]
df = df[df.group != "-"]
df = df[df.symbol != "Lr"]
df = df[df.symbol != "Lu"]

cmap = {
    "alkali metal"         : "#aacde4",
    "alkaline earth metal" : "#1f78b4",
    "metal"                : "#d93b43",
    "halogen"              : "#999d9a",
    "metalloid"            : "#e08d49",
    "noble gas"            : "#eaeaea",
    "nonmetal"             : "#f1d4Af",
    "transition metal"     : "#599d7A",
}

source = ColumnDataSource(df)
TOOLS="crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"
p = figure(title="Periodic Table (omitting LA and AC Series)", plot_width=1100, plot_height=550,
           tools='crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,lasso_select',
           x_range=groups, y_range=list(reversed(periods)))

p.rect("group", "period", 0.95, 0.95, source=source, fill_alpha=0.6, legend="metal",
       color=factor_cmap('metal', palette=list(cmap.values()), factors=list(cmap.keys())))

text_props = {"source": source, "text_align": "left", "text_baseline": "middle"}

x = dodge("group", -0.4, range=p.x_range)

r = p.text(x=x, y="period", text="symbol", **text_props)
r.glyph.text_font_style="bold"

r = p.text(x=x, y=dodge("period", 0.3, range=p.y_range), text="atomic number", **text_props)
r.glyph.text_font_size="8pt"

r = p.text(x=x, y=dodge("period", -0.35, range=p.y_range), text="name", **text_props)
r.glyph.text_font_size="5pt"

r = p.text(x=x, y=dodge("period", -0.2, range=p.y_range), text="atomic mass", **text_props)
r.glyph.text_font_size="5pt"

p.text(x=["3", "3"], y=["VI", "VII"], text=["LA", "AC"], text_align="center", text_baseline="middle")

p.add_tools(HoverTool(tooltips = [
    ("Name", "@name"),
    ("Atomic number", "@{atomic number}"),
    ("Atomic mass", "@{atomic mass}"),
    ("Type", "@metal"),
    ("CPK color", "$color[hex, swatch]:CPK"),
    ("Electronic configuration", "@{electronic configuration}"),
]))
axis_map = {
    "name": "name",
    "atomic number": "atomic number",
    "atomic mass":"atomic mass",
    "metal":"metal",
    "CPK":"CPK",
}
ent = Select(title="Remove from hover tip", options=sorted(axis_map.keys()), value="gini")
p.outline_line_color = None
p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_standoff = 0
p.legend.orientation = "horizontal"
p.legend.location ="top_center"

def update_points():
    print()
    N=ent.value

    if(N=="name"):
        p.add_tools(HoverTool(tooltips = [
        ("Atomic number", "@{atomic number}"),
        ("Atomic mass", "@{atomic mass}"),
        ("Type", "@metal"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
        ]))
    if(N=="atomic number"):
        p.add_tools(HoverTool(tooltips = [
        ("Name", "@name"),
        ("Atomic mass", "@{atomic mass}"),
        ("Type", "@metal"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
        ]))
    if(N=="atomic mass"):
        p.add_tools(HoverTool(tooltips = [
        ("Name", "@name"),
        ("Atomic number", "@{atomic number}"),
        ("Type", "@metal"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
        ]))
    if(N=="metal"):
        p.add_tools(HoverTool(tooltips = [
        ("Name", "@name"),
        ("Atomic number", "@{atomic number}"),
        ("Atomic mass", "@{atomic mass}"),
        ("CPK color", "$color[hex, swatch]:CPK"),
        ("Electronic configuration", "@{electronic configuration}"),
        ]))
    if(N=="CPK"):
        p.add_tools(HoverTool(tooltips = [
        ("Name", "@name"),
        ("Atomic number", "@{atomic number}"),
        ("Atomic mass", "@{atomic mass}"),
        ("Type", "@metal"),
        ("Electronic configuration", "@{electronic configuration}"),
        ]))

button.on_click(update_points)

layout = layout([
    [desc],
    [ent,button],
    [row(p)]
])
curdoc().add_root(layout)
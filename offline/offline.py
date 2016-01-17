""" Plotly Offline
    A module to use Plotly's graphing library with Python
    without connecting to a public or private plotly enterprise
    server.
"""
from __future__ import absolute_import

import json
import os
import uuid
import warnings
from pkg_resources import resource_string

import plotly
from plotly import tools, utils
from plotly.exceptions import PlotlyError


__PLOTLY_OFFLINE_INITIALIZED = True

def get_plotlyjs():
    path = os.path.join('offline', 'plotly.min.js')
    plotlyjs = resource_string('plotly', path).decode('utf-8')
    return plotlyjs

def init_notebook_mode():
    pass

def iplot(figure_or_data, show_link=False, link_text='',
          validate=True):
    """
    Draw plotly graphs inside a Zeppelin notebook without
    connecting to an external server.
    To save the chart to Plotly Cloud or Plotly Enterprise, use
    `plotly.plotly.iplot`.
    To embed an image of the chart, use `plotly.image.ishow`.

    figure_or_data -- a plotly.graph_objs.Figure or plotly.graph_objs.Data or
                      dict or list that describes a Plotly graph.
                      See https://plot.ly/python/ for examples of
                      graph descriptions.

    Keyword arguments:
    show_link (default=True) -- display a link in the bottom-right corner of
                                of the chart that will export the chart to
                                Plotly Cloud or Plotly Enterprise
    link_text (default='Export to plot.ly') -- the text of export link
    validate (default=True) -- validate that all of the keys in the figure
                               are valid? omit if your version of plotly.js
                               has become outdated with your version of
                               graph_reference.json or if you need to include
                               extra, unnecessary keys in your figure.

    Example:
    ```
    from plotly.offline import init_notebook_mode, iplot
    init_notebook_mode()

    iplot([{'x': [1, 2, 3], 'y': [5, 2, 7]}])
    ```
    """

    figure = tools.return_figure_from_figure_or_data(figure_or_data, validate)

    width = figure.get('layout', {}).get('width', '100%')
    height = figure.get('layout', {}).get('height', 525)
    try:
        float(width)
    except (ValueError, TypeError):
        pass
    else:
        width = str(width) + 'px'

    try:
        float(width)
    except (ValueError, TypeError):
        pass
    else:
        width = str(width) + 'px'

    plotdivid = uuid.uuid4()
    jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
    jlayout = json.dumps(figure.get('layout', {}), cls=utils.PlotlyJSONEncoder)

    config = {}
    config['showLink'] = show_link
    config['linkText'] = link_text
    config['displayModeBar'] = False
    jconfig = json.dumps(config)

    script = '\n'.join([
        'Plotly.plot("{id}", {data}, {layout}, {config}).then(function() {{',
        '    $(".{id}.loading").remove();',
        '}})'
    ]).format(id=plotdivid,
              data=jdata,
              layout=jlayout,
              config=jconfig)

    print("""%html
        <div class="{id} loading" style="color: rgb(50,50,50);">
        Drawing...</div>
        <div id="{id}" style="height: {height}; width: {width};" 
            class="plotly-graph-div">
        </div>
        <script type="text/javascript">
        {script}
        </script>
        """.format(id=plotdivid, script=script,
                           height=height, width=width))

def plot():
    """ Configured to work with localhost Plotly graph viewer
    """
    raise NotImplementedError


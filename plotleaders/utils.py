import os
import plotly
import json
import uuid
from plotly import tools, utils


def get_area(x_array, y_array):
    dist_x = max(x_array) - min(x_array)
    dist_y = max(y_array) - min(y_array)
    return dist_x * dist_y


def write_templates(blocks, app_name):
    runtime_template_dir = os.path.join(app_name, 'templates', 'runtime')
    if not os.path.exists(runtime_template_dir):
        os.makedirs(runtime_template_dir)

    for block in blocks:
        runtime_template_block = os.path.join(runtime_template_dir,
                                              block + '.html')
        with open(runtime_template_block, 'w') as f:
            template = '\n'.join(blocks[block])
            f.write(template)


def plot_to_div(figure_or_data, validate=True, show_link=True, plotdivid='', added_js='', link_text="View on plot.ly",
                default_width='100%', default_height='100%'):
    figure = tools.return_figure_from_figure_or_data(figure_or_data, validate)

    width = figure.get('layout', {}).get('width', default_width)
    height = figure.get('layout', {}).get('height', default_height)

    try:
        float(width)
    except (ValueError, TypeError):
        pass
    else:
        width = str(width) + 'px'

    try:
        float(height)
    except (ValueError, TypeError):
        pass
    else:
        height = str(height) + 'px'

    if plotdivid == '':
        plotdivid = uuid.uuid4()
    jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
    jlayout = json.dumps(figure.get('layout', {}), cls=utils.PlotlyJSONEncoder)

    config = {}
    config['showLink'] = show_link
    config['linkText'] = link_text
    jconfig = json.dumps(config)

    plotly_platform_url = plotly.plotly.get_config().get('plotly_domain',
                                                         'https://plot.ly')
    if (plotly_platform_url != 'https://plot.ly' and
                link_text == 'Export to plot.ly'):
        link_domain = plotly_platform_url \
            .replace('https://', '') \
            .replace('http://', '')
        link_text = link_text.replace('plot.ly', link_domain)

    script = 'Plotly.newPlot("{id}", {data}, {layout}, {config})'.format(
            id=plotdivid,
            data=jdata,
            layout=jlayout,
            config=jconfig)

    plotly_html_div = (
        ''
        '<div id="{id}" style="height: {height}; width: {width};" '
        'class="plotly-graph-div">'
        '</div>'
        '').format(
            id=plotdivid, height=height, width=width)

    plotly_script = (
        ''
        'window.PLOTLYENV=window.PLOTLYENV || {{}};'
        'window.PLOTLYENV.BASE_URL="' + plotly_platform_url + '";'
                                                              '{script};{added_js}').format(script=script,
                                                                                            added_js=added_js)

    return plotly_html_div, plotly_script

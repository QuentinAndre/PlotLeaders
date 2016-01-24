import os
import json
from plotly import tools, utils

def write_controls(cats, opts, opts_null):
    """
    Write the controls to the main page app.
    :param cats: list
    :param opts: list
    :param opts_null: list
    :return: string
    """
    x = element('select', {'class': "form-control", 'name': 'x-axis'}, opt=opts, select_id=0)
    y = element('select', {'class': "form-control", 'name': 'y-axis'}, opt=opts, select_id=1)
    z = element('select', {'class': "form-control", 'name': 'z-axis'}, opt=opts_null, select_id=2)
    categories = write_categories(cats)
    html = """
    <form>
        <div class="form-group">
            <label for='x-axis'> Horizontal Axis </label>
            {xcontrols}
        </div>
        <div class="form-group">
            <label for='y-axis'> Vertical Axis </label>
            {ycontrols}
        </div>
        <div class="form-group">
            <label for='z-axis'> Color-Coding </label>
            {zcontrols}
        </div>
        <div class="form-group">
            <label for='leadtype'> Domains to Include </label><br>
            {categories}
        </div>
    </form>
            """.format(xcontrols=x, ycontrols=y, zcontrols=z, categories=categories)
    return html

def write_categories(cats):
    """
    Write the categories of leaders as radio button, and return the corresponding html
    :param cats: list
    :return: string
    """
    base = """
            <label class="checkbox-inline no_indent">
                <input type="checkbox" name="{}" value="1" checked>
                {}
            </label>
            """
    html = ""
    for c in cats:
        html += base.format(c, c)
    return html


def element(element='div', attributes={}, content='', opt={}, select_id=0):
    """
    Utility function to write HTML elements conveniently
    :param element: string
    :param attributes: dict
    :param content: string
    :param opt: dict
    :param select_id: int
    :return:
    """
    if element in ['input', 'img']:
        is_closing = False
    else:
        is_closing = True
    if not is_closing and content != '':
        raise Exception("Can't have content in a non-closing HTML tag!")

    if element in ['input', 'select'] and 'name' not in attributes:
        raise Exception('"name" attribute not found in {}. '
                        'This element will not appear in '
                        'the app_state.'.format(element))

    if element == "select" and opt == {}:
        raise Exception("No options given for element 'Select'")

    el = '<{}'.format(element)
    for attribute, value in attributes.items():
        el += ' {}="{}"'.format(attribute, value)
    el += '>'

    el += content

    for i, (value, content) in enumerate(opt.items()):
        if i == select_id:
            el += '<option value={} selected>{}</option>'.format(value, content)
        else:
            el += '<option value={}>{}</option>'.format(value, content)

    if is_closing:
        el += '</{}>'.format(element)

    return el

def get_area(x_array, y_array):
    """
    Compute the area of the plot generated from the data specified in x_array and y_array
    :param x_array: list
    :param y_array: list
    :return: float
    """
    dist_x = max(x_array) - min(x_array)
    dist_y = max(y_array) - min(y_array)
    return dist_x * dist_y


def write_templates(blocks, app_name):
    """
    Utility function: write templates from corresponding blocks, and save them in the runtime folder of the app.
    :param blocks: dict
    :param app_name: string
    :return: None
    """
    runtime_template_dir = os.path.join(app_name, 'templates', 'runtime')
    if not os.path.exists(runtime_template_dir):
        os.makedirs(runtime_template_dir)

    for block in blocks:
        runtime_template_block = os.path.join(runtime_template_dir,
                                              block + '.html')
        with open(runtime_template_block, 'w') as f:
            template = '\n'.join(blocks[block])
            f.write(template)
    return None


def plot_to_div(figure_or_data, plotdivid='', added_js='',  default_width='100%', default_height='100%'):
    """
    Generate the Plotly plot, and return the HTML and Javascript needed to generate the plot.
    :param figure_or_data: dict
    :param plotdivid: string
    :param added_js: bool
    :param default_width: string
    :param default_height: string
    :return: tuple
    """
    figure = tools.return_figure_from_figure_or_data(figure_or_data, validate_figure=True)

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

    jdata = json.dumps(figure.get('data', []), cls=utils.PlotlyJSONEncoder)
    jlayout = json.dumps(figure.get('layout', {}), cls=utils.PlotlyJSONEncoder)

    config = {}
    config['showLink'] = True
    config['linkText'] = "View on plot.ly"
    jconfig = json.dumps(config)
    plotly_platform_url = 'https://plot.ly'

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

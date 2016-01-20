def write_controls(opts, opts_null):
    x = element('select', {'class': "form-control", 'name': 'x-axis'}, opt=opts)
    y = element('select', {'class': "form-control", 'name': 'y-axis'}, opt=opts)
    z = element('select', {'class': "form-control", 'name': 'z-axis'}, opt=opts_null)
    button = element('button', {'class': "btn btn-default", 'onclick': 'sendState({}, {})'}, 'View Plot!', {})
    html = """
            <div class="panel panel-info">
                <div class="panel-heading">How it Works</div>
                <div class="panel-body">
                    We have surveyed several thousands of individuals in the U.S. and have asked them to rate the personality of real and fictitious leaders on several dimensions.
                    </br>
                    You can now visualize those results in the form of a perceptual map. Who is the most benevolent leader? The least authoritarian? Check it out!
                </div>
            </div>

            <div class="panel panel-success">
                <div class="panel-heading">Using the App</div>
                <div class="panel-body">
                    Select the variables you want to appear on the horizontal axis, the
                    vertical axis, and the one you want to use to color-code the leaders. <br><br>
                    Once you are done, generate the plot by clicking the button!
                    <br><br>
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
                            <label class="radio-inline"><input type="radio" name="optradio" value="real">Real leaders</label>
                            <label class="radio-inline"><input type="radio" name="optradio" value="fict">Fictitious leaders</label>
                            <label class="radio-inline"><input type="radio" name="optradio" value="all">All leaders</label>
                        </div>

                    </form>
                    {button}
                </div>
            </div>
            """.format(xcontrols=x, ycontrols=y, zcontrols=z, button=button)
    return html


def element(element='div', attributes={}, content='', opt={}):
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

    content = content

    el = '<{}'.format(element)
    for attribute, value in attributes.items():
        el += ' {}="{}"'.format(attribute, value)
    el += '>'

    el += content

    for value, content in opt.items():
        el += '<option value={}>{}</option>'.format(value, content)

    if is_closing:
        el += '</{}>'.format(element)

    return el


def graph():
    return element('div', dict(
            id="plot_content",
            style="width: 100%; height: 600px; border: none;"
    ))

def write_controls(cats, opts, opts_null):
    x = element('select', {'class': "form-control", 'name': 'x-axis'}, opt=opts)
    y = element('select', {'class': "form-control", 'name': 'y-axis'}, opt=opts)
    z = element('select', {'class': "form-control", 'name': 'z-axis'}, opt=opts_null)
    button = element('button', {'class': "btn btn-default", 'onclick': 'sendState({}, {})'}, 'View Plot!', {})
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
            <label for='leadtype'> Leader Types to Include </label><br>
            {categories}
        </div>
    </form>
    {button}
            """.format(xcontrols=x, ycontrols=y, zcontrols=z, button=button, categories=categories)
    return html

def write_categories(cats):
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

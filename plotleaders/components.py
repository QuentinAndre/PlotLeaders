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

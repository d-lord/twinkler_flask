from typing import Tuple, Iterable

from flask import Flask, render_template, request, make_response
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter
app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# pygments stuff
formatter = HtmlFormatter(linenos=False)


def get_pygments_classes() -> Tuple[Iterable[str], Iterable[str]]:
    """ A function to contain the ugly.
    Get a list of pygments' possible CSS classes and turn them into
        1) CSS selectors
        2) names for variables to accompany them. """
    pygments_css_classes = HtmlFormatter().get_token_style_defs('.highlight')
    classes = [line[:line.find('{')].replace('.highlight ', 'span') for line in pygments_css_classes]
    var_names = [line.replace('.', '. ', 1).replace('.', '-').replace(' ', '') for line in classes]
    return classes, var_names

pygments_css_classes, pygments_css_variables = get_pygments_classes()


@app.route('/', methods=['GET', 'POST'])
def markup():
    if request.method == 'POST':
        code = request.form['code']
        lexer = guess_lexer(code)
        result = highlight(code, lexer, formatter)
        get_pygments_classes()
        return render_template('show_twinkle.html', code=result)
    else:
        return render_template('form.html')


@app.route('/smart_css.css')
def smart_css():
    rendered = render_template('twinkle_smart.css',
                               # we must list() the zip() because it will be iterated over multiple times
                               css_classes_and_variables=list(zip(pygments_css_classes, pygments_css_variables)))
    response = make_response(rendered)
    # set the content-type manually; by default it'll be text/html
    response.headers['Content-Type'] = 'text/css'
    return response


@app.route('/smart_js.js')
def smart_js():
    rendered = render_template('twinkle_smart.js', css_variables=pygments_css_variables)
    response = make_response(rendered)
    response.headers['Content-Type'] = 'application/javascript'
    return response

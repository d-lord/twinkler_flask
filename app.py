from typing import Tuple, Iterable

from flask import Flask, render_template, request, make_response, redirect
from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

# These templates are rendered once at launch and then re-used for every request.
# They're global variables as that really seems like the most Flasky way to do it:
# flask.g: is per "application context" which is per-request, despite the name
# flask.current_app['varname']: doesn't work like that
# flask.current_app['config']: works, but feels wrong as it's not configuration
# flask.session: is per user/client session, not app 'session'
rendered_smart_css, rendered_smart_js = None, None
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


@app.before_first_request
def set_up() -> None:
    global rendered_smart_css, rendered_smart_js
    pygments_css_classes, pygments_css_variables = get_pygments_classes()
    rendered_smart_css = render_template(
        'twinkle_smart.css',
        # we must list() the zip() because it will be iterated over multiple times
        css_classes_and_variables=list(zip(pygments_css_classes, pygments_css_variables)))
    rendered_smart_js = render_template('twinkle_smart.js', css_variables=pygments_css_variables)
    rendered_smart_css = rendered_smart_css


@app.route('/', methods=['GET', 'POST'])
def markup():
    if request.method == 'POST':
        try:
            code = request.form['code']
            if not code:
                raise FileNotFoundError
        except:
            return redirect('/')
        lexer = guess_lexer(code)
        result = highlight(code, lexer, formatter)
        get_pygments_classes()
        return render_template('show_twinkle.html', code=result)
    else:
        return render_template('form.html')


@app.route('/smart_css.css')
def smart_css():
    response = make_response(rendered_smart_css)
    # set the content-type manually; by default it'll be text/html
    response.headers['Content-Type'] = 'text/css'
    return response


@app.route('/smart_js.js')
def smart_js():
    response = make_response(rendered_smart_js)
    response.headers['Content-Type'] = 'application/javascript'
    return response

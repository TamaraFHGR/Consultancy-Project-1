from dash import Dash
import dash_html_components as html
from flask import request

app = Dash(__name__)
server = app.server  # Access the underlying Flask server

@server.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

app.layout = html.Div([
    html.H1("Dash App"),
    # Your app's components
])

if __name__ == '__main__':
    app.run_server(debug=True)
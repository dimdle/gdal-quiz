"""
dirk.schroer (dimdle@aquadraht.de)
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from utils import *


app = dash.Dash(title='gdal-quiz')


"""
BEGIN LAYOUT
"""
app.layout = html.Div([

    html.P(),
    dbc.Row([
        dbc.Col(
            [html.Img(id='logo-gdal', src=app.get_asset_url('gdalicon.png'))], 
            width={'size': 2, 'offset': 0, 'order': 1}
        ),
        dbc.Col(
            [dbc.Button('start quiz', id='start-quiz')], 
            width={'size': 2, 'offset': 0, 'order': 2}
        )
    ], align="end"
    ),
    html.P(),
    dbc.Row([
        dbc.Col(
            id='question-asked',
            width={'size': 'auto', 'offset': 2, 'order': 2}
        )
    ]),

    dbc.Row(
        [
            dbc.Col(
                id='possible-answer',
                width={'size': 'auto', 'offset': 2, 'order': 1}
            ),
            dbc.Col(
                id='is-correct',
                width={'size': 'auto', 'offset': 0, 'order': 2}
            )
        ]
    ),
    html.P(),
    dbc.Row(
        [
            dbc.Col(
                [dbc.Button('submit', id='submit')],
                width={'size': 1, 'offset': 2, 'order': 1}
            ),
            dbc.Col(
                [dbc.Button('next question', id='next-q')],
                width={'size': 2, 'offset': 1, 'order': 2}
            )
        ]
    ),
    html.P(),
    dbc.Row(
        [
            dbc.Col(
                id='progress-bar',
                width={'size': 'auto', 'offset': 2}
            ),
        ]
    ),
    html.P(),

    dcc.Store(id='data-memory1'),
    dcc.Store(id='data-memory2'),
    dcc.Store(id='right-answers', data=0),
])

"""
END LAYOUT
"""

@app.callback(
    Output('data-memory1', 'clear_data'),
    Output('data-memory2', 'clear_data'),
    Output('right-answers', 'clear_data'),
    Input("start-quiz", "n_clicks")
)
def clear(n_clicks):
    '''Clears memory (at startup'''
    if n_clicks is None:
        raise PreventUpdate

    if n_clicks > 0:
        return True, True, True


@app.callback(
    Output('data-memory1', 'data'),
    Input("start-quiz", "n_clicks")
)
def start_quiz(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    data = load_yaml('questions.yaml')
    data = add_bool_subkey(data, 'asked')
    data = add_bool_subkey(data, 'ask')   
    data = add_bool_subkey(data, 'is_correct')

    random_key = random_question(not_asked(data))
    data[random_key]['asked'] = True
    data[random_key]['ask'] = True

    return data


@app.callback(
    Output('question-asked', 'children'),
    Output('possible-answer', 'children'),
    Input('data-memory1', 'data'),
    Input('data-memory2', 'data'),
)
def update_data(data_init, data):
    if (data_init is None):  # prevents firing callback at startup
        raise PreventUpdate

    if (n_asked_questions(data_init) == 1) & (data is None):
        data = data_init

    _question = get_question(data)

    return (_question['question'],
            [dcc.RadioItems(
                options=dict_to_labellist(_question['answers']), 
                labelStyle={'display': 'block'},
                id='answers'
            )]
    )


@app.callback(
    Output('data-memory2', 'data'),
    Input('next-q', 'n_clicks'),
    State('data-memory1', 'data'),
    State('data-memory2', 'data')
)
def next_question(n_clicks, data_init, data):
    if n_clicks is None:
        raise PreventUpdate

    if (n_asked_questions(data_init) == 1) & (data is None):
        data = data_init

    data = rm_ask(data)
    random_key = random_question(not_asked(data))
    data[random_key]['asked'] = True
    data[random_key]['ask'] = True

    return data


@app.callback(
    Output('is-correct', 'children'),
    Output('right-answers', 'data'),
    Input('submit', 'n_clicks'),
    State('data-memory1', 'data'),
    State('data-memory2', 'data'),
    State('right-answers', 'data'),
    State('answers', 'value')
)
def check_answer(n_clicks, data_init, data, right_a, answer):
    if n_clicks is None:
        raise PreventUpdate

    if (n_asked_questions(data_init) == 1) & (data is None):
        data = data_init


    if get_question(data)['correct'] == answer:
        return dcc.Markdown("corect!! :rocket:"), right_a + 1
    else:
        return dcc.Markdown("wrong answer"), right_a



@app.callback(
    Output('progress-bar', 'children'),
    Input('right-answers', 'data')
)
def update_progress(n_right):
    if n_right is None:
        raise PreventUpdate

    return dcc.Markdown(progress(n_right))

def finish_game():
    pass # ToDo



if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=8062, debug=True, use_reloader=False)


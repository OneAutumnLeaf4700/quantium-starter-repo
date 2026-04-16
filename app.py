import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

df = pd.read_csv('output.csv', parse_dates=['date'])
df_daily = df.groupby('date', as_index=False)['sales'].sum()
df_daily = df_daily.sort_values('date')

price_increase_date = pd.Timestamp('2021-01-15')

fig = px.line(
    df_daily,
    x='date',
    y='sales',
    labels={'date': 'Date', 'sales': 'Sales ($)'},
    title='Pink Morsel Daily Sales'
)

fig.add_vline(
    x=price_increase_date.timestamp() * 1000,
    line_dash='dash',
    line_color='red',
    annotation_text='Price Increase (Jan 15, 2021)',
    annotation_position='top left'
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1(
        'Pink Morsel Sales Visualiser',
        style={'textAlign': 'center', 'fontFamily': 'Arial, sans-serif'}
    ),
    dcc.Graph(figure=fig)
])

if __name__ == '__main__':
    app.run(debug=True)

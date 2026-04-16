import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

df = pd.read_csv('output.csv', parse_dates=['date'])

price_increase_date = pd.Timestamp('2021-01-15')

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': '#0f1117',
        'minHeight': '100vh',
        'padding': '0 0 40px 0',
        'fontFamily': '"Segoe UI", Arial, sans-serif',
    },
    children=[
        html.Div(
            style={
                'background': 'linear-gradient(135deg, #c0392b 0%, #8e0a1e 100%)',
                'padding': '32px 0 24px 0',
                'textAlign': 'center',
                'boxShadow': '0 4px 20px rgba(0,0,0,0.5)',
                'marginBottom': '32px',
            },
            children=[
                html.H1(
                    'Pink Morsel Sales Visualiser',
                    style={
                        'color': '#ffffff',
                        'fontSize': '2.4rem',
                        'fontWeight': '700',
                        'letterSpacing': '1px',
                        'margin': '0 0 6px 0',
                    }
                ),
                html.P(
                    'Soul Foods — Regional Sales Dashboard',
                    style={
                        'color': 'rgba(255,255,255,0.7)',
                        'fontSize': '1rem',
                        'margin': '0',
                        'letterSpacing': '2px',
                        'textTransform': 'uppercase',
                    }
                ),
            ]
        ),

        html.Div(
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'marginBottom': '28px',
            },
            children=[
                html.Div(
                    style={
                        'backgroundColor': '#1a1d27',
                        'borderRadius': '12px',
                        'padding': '18px 32px',
                        'boxShadow': '0 2px 12px rgba(0,0,0,0.4)',
                        'display': 'flex',
                        'alignItems': 'center',
                        'gap': '20px',
                    },
                    children=[
                        html.Span(
                            'Filter by Region:',
                            style={
                                'color': '#aab0c6',
                                'fontSize': '0.95rem',
                                'fontWeight': '600',
                                'letterSpacing': '0.5px',
                            }
                        ),
                        dcc.RadioItems(
                            id='region-filter',
                            options=[
                                {'label': 'All', 'value': 'all'},
                                {'label': 'North', 'value': 'north'},
                                {'label': 'East', 'value': 'east'},
                                {'label': 'South', 'value': 'south'},
                                {'label': 'West', 'value': 'west'},
                            ],
                            value='all',
                            inline=True,
                            inputStyle={
                                'marginRight': '5px',
                                'accentColor': '#e74c3c',
                            },
                            labelStyle={
                                'color': '#ffffff',
                                'fontSize': '0.95rem',
                                'marginRight': '20px',
                                'cursor': 'pointer',
                            },
                        ),
                    ]
                )
            ]
        ),

        html.Div(
            style={
                'maxWidth': '1200px',
                'margin': '0 auto',
                'padding': '0 24px',
            },
            children=[
                dcc.Graph(
                    id='sales-chart',
                    config={'displayModeBar': False},
                    style={
                        'borderRadius': '12px',
                        'overflow': 'hidden',
                        'boxShadow': '0 4px 24px rgba(0,0,0,0.5)',
                    }
                )
            ]
        )
    ]
)


@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    if region == 'all':
        filtered = df.groupby('date', as_index=False)['sales'].sum()
    else:
        filtered = df[df['region'] == region].groupby('date', as_index=False)['sales'].sum()

    filtered = filtered.sort_values('date')

    fig = px.line(
        filtered,
        x='date',
        y='sales',
        labels={'date': 'Date', 'sales': 'Sales ($)'},
    )

    fig.add_vline(
        x=price_increase_date.timestamp() * 1000,
        line_dash='dash',
        line_color='#e74c3c',
        annotation_text='Price Increase — Jan 15 2021',
        annotation_position='top left',
        annotation_font_color='#e74c3c',
    )

    fig.update_traces(
        line=dict(color='#e74c3c', width=2),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.08)',
    )

    fig.update_layout(
        paper_bgcolor='#1a1d27',
        plot_bgcolor='#1a1d27',
        font=dict(color='#aab0c6', family='"Segoe UI", Arial, sans-serif'),
        title=None,
        xaxis=dict(
            title='Date',
            gridcolor='#2a2d3a',
            showline=True,
            linecolor='#2a2d3a',
            tickfont=dict(color='#aab0c6'),
            title_font=dict(color='#ffffff', size=13),
        ),
        yaxis=dict(
            title='Sales ($)',
            gridcolor='#2a2d3a',
            showline=True,
            linecolor='#2a2d3a',
            tickfont=dict(color='#aab0c6'),
            title_font=dict(color='#ffffff', size=13),
        ),
        margin=dict(l=60, r=40, t=40, b=60),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor='#2a2d3a',
            bordercolor='#e74c3c',
            font=dict(color='#ffffff'),
        ),
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)

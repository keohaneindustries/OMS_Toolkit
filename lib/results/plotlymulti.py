import pandas as pd
import plotly.graph_objs as go


class AnotherChart(object):
    layout = lambda title, titley: dict(title=title, yaxis=dict(title=titley), xaxis=dict(title='Date'), hovermode='x',
                                        showlegend=True, margin=dict(l=30, r=30, t=35, b=25))
    main_color = '#519156'
    comp_colors = ['#4286f4', '#e83c75', '#d3ba3f', '#ab26ff', '#44ebf4', '#7eff54']

    @classmethod
    def build_comp_diff(cls, comp_diff_data, params):
        titley = "X"
        title = ''

        data = []
        for i, col in enumerate(comp_diff_data.columns.drop('date')):
            data.append(
                go.Scatter(
                    x=comp_diff_data['date'],
                    y=comp_diff_data[col],
                    mode='lines',
                    name=col,
                    hoverinfo='all',
                    line=dict(
                        color=cls.comp_colors[i],
                        width=2
                    )
                )
            )

        figure = dict(data=data, layout=cls.layout(title, titley))

        return figure

#%%

from collections import OrderedDict


class TrailingDistChart:
    colors = OrderedDict()
    colors[0] = '#0D76BF'
    colors[1] = '#f493ff'  # '#00cc96'
    colors[2] = '#ffb33a'  # '#EF553B'
    colors[3] = '#5effbf'  # '#EF553B'

    bid_color = 'rgb(92, 209, 123)'
    ask_color = 'rgb(204, 67, 67)'

    @staticmethod
    def get_config():
        config = {
            # 'setBackground': {'color':MyChart.background_color},
            'scrollZoom': False, 'displayModeBar': False, 'showAxisDragHandles': False,
            'showAxisRangeEntryBoxes': False, 'linkText': False, 'sendData': False,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian']}
        return config

    @staticmethod
    def compile(*args):
        return [arg for arg in args if arg is not None]

    @staticmethod
    def vert_lines(sym, bid_color, ask_color, curr_bid, curr_ask, typ_bid, typ_ask):
        traces_lines = []
        if isinstance(bid_color, str) and isinstance(curr_bid, float):
            traces_lines.append(
            {
                'type': 'line',
                'x0': curr_bid,
                'x1': curr_bid,
                'xref': 'x',
                'yref': 'paper',
                'y0': 0,
                'y1': 0.90,
                'line': {
                    'color': bid_color,
                    'width': 3,
                },
            })
        if isinstance(ask_color, str) and isinstance(curr_ask, float):
            traces_lines.append(
            {
                'type': 'line',
                'x0': curr_ask,
                'x1': curr_ask,
                'xref': 'x',
                'yref': 'paper',
                'y0': 0,
                'y1': 0.90,
                'line': {
                    'color': ask_color,
                    'width': 3,
                },
            })
        if isinstance(typ_bid, float):
            traces_lines.append(
            {
                'type': 'line',
                'x0': typ_bid,
                'x1': typ_bid,
                'xref': 'x',
                'yref': 'paper',
                'y0': 0,
                'y1': 1.0,
                'line': {
                    'color': 'rgb(211, 207, 2)',
                    'width': 3,
                    'dash': 'dot'
                },
            })
        if isinstance(typ_ask, float):
            traces_lines.append(
            {
                'type': 'line',
                'x0': typ_ask,
                'x1': typ_ask,
                'xref': 'x',
                'yref': 'paper',
                'y0': 0,
                'y1': 1.0,
                'line': {
                    'color': 'rgb(211, 207, 2)',
                    'width': 3,
                    'dash': 'dot'
                },
            })
        return traces_lines

    @staticmethod
    def zero_line():
        liner = {
            'type': 'line',
            'x0': 0,
            'x1': 0,
            'xref': 'x',
            'yref': 'paper',
            'y0': 0,
            'y1': 1.0,
            'line': {
                'color': 'rgb(100, 100, 100)',
                'width': 2,
                'dash': 'dot'
            },
        }
        return liner

    @staticmethod
    def histogram_overlays(df, syms, colors):
        data = []
        for i, key in enumerate(syms):
            dirty = df[key]
            min_lvl = dirty.quantile(0.01)
            max_lvl = dirty.quantile(0.99)
            dirty = dirty[(dirty>min_lvl)&(dirty<max_lvl)&(dirty.round(2)!=0.00)]
            trace = dict(
                type='histogram',
                x=list(dirty),
                opacity=0.6,
                marker=dict(color=colors[i]),
                name=key,
                histnorm='probability density'
            )
            data.append(trace)
        return data

    @classmethod
    def plot(cls, df, syms, metric_string, curr_bid, curr_ask, typ_bid, typ_ask):
        traces_lines = cls.vert_lines(syms[0], cls.bid_color, cls.ask_color, curr_bid, curr_ask, typ_bid, typ_ask)
        histos = cls.histogram_overlays(df, syms, cls.colors)

        titlex = ""
        layout = dict(
            barmode='overlay',
            xaxis=dict(title=titlex),
            yaxis=dict(title='PDF - trailing 4 years'),
            title='Distribution of hist {} relative to now'.format(metric_string),
            shapes = TrailingDistChart.compile(
                TrailingDistChart.zero_line(),
                *traces_lines
            )
        )
        figure = dict(data=histos, layout=layout)
        return figure

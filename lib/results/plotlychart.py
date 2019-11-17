import numpy as np
import pandas as pd
import plotly.graph_objs as go
from datetime import date
import math
from collections import namedtuple


class MyChart:
    name = ""
    clr_skew = "#eb4034"
    clr_skew_alt = "#00ffff"
    clr_skew_range = "#AAAAAA"
    clr_skew_range_fill = "rgba(170,170,170,0.22)"
    clr_earnings_fill = "rgba(0,0,170,0.22)"
    clr_stk = "#ec3838"
    # background_color = "#333333"
    background_color = "rgba(0,0,0,0)"
    margins = {'l':40,'r':25,'t':40,'b':50,'pad':3,'autoexpand':True}

    def __init__(self):
        pass

    @staticmethod
    def get_config():
        config = {
            # 'setBackground': {'color':MyChart.background_color},
                  'scrollZoom': False, 'displayModeBar': False, 'showAxisDragHandles': False,
                  'showAxisRangeEntryBoxes': False, 'linkText': False, 'sendData': False,
                  'displaylogo': False,
                  'modeBarButtonsToRemove': ['toggleSpikelines', 'hoverCompareCartesian']}
        return config

    # region helper_methods
    @staticmethod
    def reminder_annotation(text, stk_candlestick=False):
        return {
            'text': text,
            'yref': 'paper',
            'xref': 'paper',
            'y': 0.39 if stk_candlestick else 0.01,
            'x': 0.01,
            'font': {'size': 15, 'color': "white"},
            'opacity': 0.6,
            'bgcolor': "rgb(80,80,80)",
            'showarrow':False

        }

    @staticmethod
    def consume_point_circle(consume_point=None):
        if consume_point is None:
            return None
        return {
            'type': 'circle',
            'yref': 'y1',
            'xref': 'x1',
            'xsizemode':'pixel',
            'ysizemode':'pixel',
            'xanchor': consume_point.x,
            'yanchor': consume_point.y,
            'opacity':1.0,
            'x0': 0,
            'x1': 7,
            'y0': 0,
            'y1': 7,
            'fillcolor':"LightGreen",
            'line':{'color':"Green", 'width':1},
            'layer':'above'
        }

    @staticmethod
    def compile(*args):
        return [arg for arg in args if arg is not None]

    @staticmethod
    def _make_steps(data):
        steps = [{'method': 'restyle',
                  'args': ['visible', [False] * i + [True] + [False] * (data['date'].unique().size - (i + 1))],
                  'label': pd.Timestamp(data['date'].unique()[i]).date().isoformat()}
                 for i in range(data['date'].unique().size)]
        return steps

    @staticmethod
    def _make_slider(steps):

        sliders = [{'active': len(steps)-1,
                    'currentvalue': {'prefix': 'Date: ', 'visible': True},
                    'steps': steps
                    }]
        return sliders

    @classmethod
    def _make_skew_plot(cls, ticker, iv_by_delta, earnings_dates):
        skew_plot = []
        skew_plot.extend([{
            "type": "scatter",
            'visible': False if date != iv_by_delta['date'].max() else True,
            'name': ticker,
            'xaxis': 'x1',
            'yaxis': 'y1',
            # 'textposition': "middle center",
            # 'textfont': {'size':16,'color':'rgba(0,0,0,1.0)'},
            # 'text': ["{0:.2f}".format(skew) if skew != 0 else "" for skew in iv_by_delta[iv_by_delta['date'].isin([date])]['skewPoints'].values],
            # 'fillcolor': cls.clr_skew,
            'line': {'color': cls.clr_skew_alt if date in earnings_dates else cls.clr_skew},
            # 'mode': 'lines+markers+text',
            'mode': 'lines+markers',
            'hoveron': 'points+fills',
            'x': iv_by_delta[iv_by_delta['date'].isin([date])]['delta'].values,
            'y': iv_by_delta[iv_by_delta['date'].isin([date])]['iv'].values,
        } for date in pd.to_datetime(iv_by_delta['date'].unique())])
        return skew_plot

    @classmethod
    def _make_skew_range(cls, iv_by_delta, iv_by_delta_range):
        iv_by_delta['date'] = pd.to_datetime(iv_by_delta['date'])
        mids = iv_by_delta[iv_by_delta['delta'] == 0.5][['date', 'iv']].set_index('date').sort_index()['iv']

        skew_range_plot = []
        skew_range_plot.extend([{
            "type": "scatter",
            'visible': False if date != iv_by_delta['date'].max() else True,
            'name': "skew range max",
            'xaxis': 'x1',
            'yaxis': 'y2',
            'textposition': "top center",
            'textfont': {'size': 10, 'color': 'rgba(50,50,50,0.7)'},
            'line': {'color': cls.clr_skew_range},
            'mode': 'lines+text',
            'text': ["{0:.2f}".format(skew) if skew != 0 else "" for skew in iv_by_delta_range['skewPointsMax'].values],
            'hoveron': 'points+fills',
            'x': iv_by_delta_range['delta'].values,
            'y': iv_by_delta_range['skewPointsMax'].values + mids.loc[date],
        } for date in pd.to_datetime(iv_by_delta['date'].unique())])
        # } for mid in mids])

        skew_range_plot.extend([{
            "type": "scatter",
            'visible': False if date != iv_by_delta['date'].max() else True,
            'name': "skew range min",
            'xaxis': 'x1',
            'yaxis': 'y2',
            'textposition': "bottom center",
            'textfont': {'size': 10, 'color': 'rgba(50,50,50,0.7)'},
            'fillcolor': cls.clr_skew_range_fill,
            'line': {'color': cls.clr_skew_range},
            'mode': 'lines+text',
            'text': ["{0:.2f}".format(skew) if skew != 0 else "" for skew in iv_by_delta_range['skewPointsMin'].values],
            'hoveron': 'points+fills',
            'fill': 'tonexty',
            'x': iv_by_delta_range['delta'].values,
            'y': iv_by_delta_range['skewPointsMin'].values + mids.loc[date],
        } for date in pd.to_datetime(iv_by_delta['date'].unique())])
        # } for mid in mids])

        return skew_range_plot

    @classmethod
    def _make_candlestick_plot(cls, iv_by_delta, hist_stock, stock_lookback):
        stock_plot = []
        stock_plot.extend([{
            "type": "candlestick",
            'visible': False if date != iv_by_delta['date'].max() else True,
            'name': 'stk_px',
            'xaxis': 'x3',
            'yaxis': 'y3',
            "x": pd.to_datetime(hist_stock[hist_stock['date'].between(date - USTDay * stock_lookback, date)]['date']),
            "open": hist_stock[hist_stock['date'].between(date - USTDay * stock_lookback, date)]['stock_open'].values,
            "high": hist_stock[hist_stock['date'].between(date - USTDay * stock_lookback, date)]['stock_high'].values,
            "low": hist_stock[hist_stock['date'].between(date - USTDay * stock_lookback, date)]['stock_low'].values,
            "close": hist_stock[hist_stock['date'].between(date - USTDay * stock_lookback, date)]['stock_close'].values,
        } for date in pd.to_datetime(iv_by_delta['date'].unique())])
        return stock_plot

    @classmethod
    def _make_earnings_highlights(cls, earnings_dates):
        earnings_highlighting = []
        earnings_highlighting.extend([{
            'type': 'rect',
            # x-reference is assigned to the x-values
            'xref': 'x3',
            # y-reference is assigned to the plot paper [0,1]
            'yref': 'y3',
            'x0': date,
            'y0': 0,
            'x1': date,
            'y1': 1000,
            'fillcolor': cls.clr_earnings_fill,
            # 'opacity': 0.2,
            'line': {
                'color': cls.clr_earnings_fill,
                'width': 3,
            }} for date in pd.to_datetime(earnings_dates[:-1])])
        return earnings_highlighting
    # endregion

    # region figure_types

    @classmethod
    def simple(cls, ticker, iv_text, iv_by_delta, earnings_dates, iv_by_delta_range=None, consume_point=None):
        steps = MyChart._make_steps(iv_by_delta)
        slider = MyChart._make_slider(steps)

        y1_min = math.floor(iv_by_delta['iv'].min())
        y1_max = math.ceil(iv_by_delta['iv'].max())

        if iv_by_delta_range is not None:
            data = MyChart._make_skew_range(iv_by_delta, iv_by_delta_range) + \
                   MyChart._make_skew_plot(ticker, iv_by_delta, earnings_dates)
        else:
            data = MyChart._make_skew_plot(ticker, iv_by_delta, earnings_dates)

        layout = dict(
                    margin=MyChart.margins,
                      sliders=slider,
                    xaxis={'domain': [0.0, 1.0], 'anchor': 'x1', 'title': {'text': 'Interpolated Delta','font':{'size':10}}, 'range': [0.15, 0.85], 'side': 'top', 'tickmode': 'array', 'tickvals': [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]},
                    yaxis={'domain': [0.0, 1.0], 'anchor': 'y1', 'title': {'text': 'IV'}, 'range': [y1_min, y1_max], 'mirror': 'all'},
                    yaxis2={'domain': [0.0, 1.0], 'anchor': 'y1', 'overlaying':'y','range': [y1_min, y1_max], 'mirror': 'all'},
                      autosize=True,
                      showlegend=False,
                    paper_bgcolor=cls.background_color,
                    plot_bgcolor=cls.background_color,
                    annotations=MyChart.compile(
                        MyChart.reminder_annotation(text=ticker + " -- " + iv_text)
                    ),
                    shapes=MyChart.compile(
                        MyChart.consume_point_circle(consume_point)
                    ),
                      # height=700,
                      # width=950,
                      )

        figure = {'data': data,
                  'layout': layout
                  }
        return figure

    @classmethod
    def stk_candlestick(cls, ticker, iv_text, iv_by_delta, hist_stock, earnings_dates, stock_lookback: int=126, iv_by_delta_range=None, consume_point=None):

        steps = MyChart._make_steps(iv_by_delta)
        slider = MyChart._make_slider(steps)

        y1_min = math.floor(iv_by_delta['iv'].min())
        y1_max = math.ceil(iv_by_delta['iv'].max())
        y2_min = math.floor(hist_stock['stock_close'].min())
        y2_max = math.ceil(hist_stock['stock_close'].max())

        if iv_by_delta_range is not None:
            data = MyChart._make_skew_range(iv_by_delta, iv_by_delta_range) + \
                   MyChart._make_skew_plot(ticker, iv_by_delta, earnings_dates) + \
                   MyChart._make_candlestick_plot(iv_by_delta, hist_stock, stock_lookback)
        else:
            data = MyChart._make_skew_plot(ticker, iv_by_delta, earnings_dates) + \
                   MyChart._make_candlestick_plot(iv_by_delta, hist_stock, stock_lookback)

        layout = dict(
            margin=MyChart.margins,
                      sliders=slider,
                      xaxis={'domain': [0.0, 1.0], 'anchor': 'x1', 'title': {'text':'Interpolated Delta','font':{'size':10}}, 'range': [0.15,0.85], 'side':'top','tickmode':'array','tickvals':[0.2,0.3,0.4,0.5,0.6,0.7,0.8]},
                      yaxis={'domain': [0.36, 1.0], 'anchor': 'y1', 'title': {'text':'IV'}, 'range': [y1_min, y1_max],'mirror':'all'},
                      yaxis2={'domain': [0.36, 1.0], 'anchor': 'y1', 'overlaying': 'y', 'range': [y1_min, y1_max], 'mirror': 'all'},
                      yaxis3={'domain': [0.0, 0.30],'anchor':'y3', 'title': {'text':'Hist Stk Px','font':{'size':10}} ,'range': [y2_min, y2_max], 'mirror':'all'},
                      xaxis3={'domain': [0.0, 0.99], 'anchor': 'x3', 'rangeslider': {'visible': False}, 'side': 'bottom',},
                        # 'automargin':True, 'layer': 'above traces'
                      autosize=True,
                      # height=700,
                      # width=950,
                      # hovermode='closest',
                      showlegend=False,
                    paper_bgcolor=cls.background_color,
                    plot_bgcolor=cls.background_color,
                    annotations=MyChart.compile(
                        MyChart.reminder_annotation(text=ticker + " -- " + iv_text)
                    ),
                    shapes=MyChart.compile(
                        MyChart.consume_point_circle(consume_point),
                        *MyChart._make_earnings_highlights(earnings_dates)
                    ),
                      )


        figure = {'data': data,
                  'layout': layout
                  }
        return figure
    # endregion


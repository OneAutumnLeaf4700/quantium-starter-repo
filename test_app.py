import pytest
from app import app


def test_header_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element('h1', timeout=10)
    header = dash_duo.find_element('h1')
    assert header.text == 'Pink Morsel Sales Visualiser'


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element('#sales-chart', timeout=10)
    chart = dash_duo.find_element('#sales-chart')
    assert chart is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element('#region-filter', timeout=10)
    radio = dash_duo.find_element('#region-filter')
    assert radio is not None
    labels = dash_duo.find_elements('#region-filter label')
    regions = {label.text for label in labels}
    assert {'All', 'North', 'East', 'South', 'West'} == regions

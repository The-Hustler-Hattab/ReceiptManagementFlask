from datetime import datetime, timedelta

from flask import request

from app import app, verify_jwt
from app.service.analytics import AnalyticsService


@app.route('/get-bar-chart-data', methods=['GET'])
@verify_jwt
def get_bar_chart_data():
    """
    Get bar chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: bar chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_bar_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500


@app.route('/get-pie-chart-data', methods=['GET'])
@verify_jwt
def get_pie_chart_data():
    """
    Get pie chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: bar chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_pie_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500


@app.route('/get-line-chart-data', methods=['GET'])
@verify_jwt
def get_line_chart_data():
    """
    Get line chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: line chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_line_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500


@app.route('/get-horizontal-chart-data', methods=['GET'])
@verify_jwt
def get_horizontal_chart_data():
    """
    Get horizontal chart data
    ---
    tags:
      - Analytics-Controller
    parameters:
      - name: start_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD
      - name: end_date
        in: query
        type: string
        required: true
        description: YYYY-MM-DD

    responses:
      200:
        description: horizontal chart data retrieved successfully
      400:
        description: Bad request
      500:
        description: Internal server error
    """
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    print(start_date)
    print(end_date)

    try:
        # Parse the date strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        # Set the start_date to the first day of the month
        start_date = start_date.replace(day=1)

        # Set the end_date to the last day of the month
        end_date = end_date.replace(day=1) + timedelta(days=32)
        end_date = end_date.replace(day=1) - timedelta(days=1)
        print(start_date)
        print(end_date)
        return AnalyticsService.get_horizontal_chart_data(start_date, end_date)
    except Exception as e:
        raise e
        # return jsonify({'error': str(e)}), 500

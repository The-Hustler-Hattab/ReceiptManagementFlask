import io
from datetime import datetime, timedelta
from typing import Tuple, Dict

from app import app


@app.route('/health', methods=['GET'])
def health() -> Tuple[Dict[str, str], int]:
    """
    Health Check Endpoint
    ---
    tags:
      - Health
    responses:
      200:
        description: OK if the service is healthy.
    """
    return {'status': 'OK',
            'msg': 'API is up'}, 200


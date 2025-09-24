from square import Square
from square.environment import SquareEnvironment

from dotenv import load_dotenv
import os

load_dotenv()
SQUARE_ACCESS_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
SQUARE_ENVIRONMENT = os.getenv("SQUARE_ENVIRONMENT")
SQUARE_API_VERSION = os.getenv("SQUARE_API_VERSION")

"""
Required API's
----------------------------------------
Catalog:
    - List Catalog
    - Batch retrieve catalog objects?

Customers:
    - List customers

Locations:
    - List locations

Orders:
    - Batch retrieve orders

Payments:
    - List payments
"""


def get_square_client():
    """
    Connect to Square API
    """

    return Square(environment=SquareEnvironment.PRODUCTION, token=SQUARE_ACCESS_TOKEN)

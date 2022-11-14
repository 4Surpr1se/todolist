from pytest_factoryboy import register

from tests.factories import UserFactory
from tests.fixtures import signingup

pytest_plugins = "tests.fixtures"

register(UserFactory)

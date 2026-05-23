from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from accounts.tests.helpers import create_user


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def existing_user(db):
    return create_user()


@pytest.fixture
def mock_twilio_send():
    """Prevent real Twilio calls; pretend SMS succeeded."""
    with patch(
        "accounts.services.otp_service.TwilioService.send_sms",
        return_value="SMpytest00000000000000000000000000",
    ) as mocked:
        yield mocked


@pytest.fixture
def mock_twilio_send_failure():
    with patch(
        "accounts.services.otp_service.TwilioService.send_sms",
        return_value=None,
    ) as mocked:
        yield mocked


@pytest.fixture
def second_phone() -> str:
    return "+919876543211"

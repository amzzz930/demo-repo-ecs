import pytest
from unittest.mock import patch, MagicMock
import botocore.exceptions
from helpers.ssm.parameter_store import (
    SSMParameterStore,
)


@pytest.fixture
def mock_ssm_client():
    """Fixture to mock the boto3 SSM client."""
    with patch("boto3.client") as mock_boto_client:
        mock_client = MagicMock()
        mock_boto_client.return_value = mock_client
        yield mock_client


def test_get_parameter_success(mock_ssm_client):
    """Test successful retrieval of an SSM parameter."""
    mock_ssm_client.get_parameter.return_value = {"Parameter": {"Value": "test-value"}}

    ssm_store = SSMParameterStore()
    result = ssm_store.get_parameter("/test/parameter")

    assert result == "test-value"
    mock_ssm_client.get_parameter.assert_called_once_with(
        Name="/test/parameter", WithDecryption=True
    )


def test_get_parameter_not_found(mock_ssm_client):
    """Test handling of missing parameter (ParameterNotFound error)."""
    mock_ssm_client.get_parameter.side_effect = botocore.exceptions.ClientError(
        {"Error": {"Code": "ParameterNotFound", "Message": "Parameter does not exist"}},
        "GetParameter",
    )

    ssm_store = SSMParameterStore()
    result = ssm_store.get_parameter("/missing/parameter")

    assert result is None
    mock_ssm_client.get_parameter.assert_called_once_with(
        Name="/missing/parameter", WithDecryption=True
    )


def test_get_parameter_access_denied(mock_ssm_client):
    """Test handling of access denied error."""
    mock_ssm_client.get_parameter.side_effect = botocore.exceptions.ClientError(
        {"Error": {"Code": "AccessDeniedException", "Message": "Access denied"}},
        "GetParameter",
    )

    ssm_store = SSMParameterStore()
    result = ssm_store.get_parameter("/restricted/parameter")

    assert result is None
    mock_ssm_client.get_parameter.assert_called_once_with(
        Name="/restricted/parameter", WithDecryption=True
    )


def test_get_parameter_with_custom_region(mock_ssm_client):
    """Test SSM Parameter Store with a custom AWS region."""
    mock_ssm_client.get_parameter.return_value = {
        "Parameter": {"Value": "custom-region-value"}
    }

    ssm_store = SSMParameterStore(region="us-west-2")
    result = ssm_store.get_parameter("/custom/region/parameter")

    assert result == "custom-region-value"
    mock_ssm_client.get_parameter.assert_called_once_with(
        Name="/custom/region/parameter", WithDecryption=True
    )

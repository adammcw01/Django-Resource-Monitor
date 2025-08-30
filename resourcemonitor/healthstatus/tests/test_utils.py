"""
This file is a test suite for the utility functions in the healthstatus app.
"""
import pytest
from healthstatus.utils import generateLog, getDeviceAvail, getAvailTable
from healthstatus.models import SystemMetric, DeviceStatus
from unittest.mock import patch


@pytest.mark.django_db
def testGenerateLogSuccess():
    """
    Test that generateLog writes a log entry to the DB when successful.
    """
    
    generateLog(endpoint="/devices", status_code=200, success=True)

    log = SystemMetric.objects.first()
    assert log is not None
    assert log.endpoint == "/devices"
    assert log.status_code == 200
    assert log.success is True


@pytest.mark.django_db
def testGenerateLogFailure():
    """
    Test that generateLog writes a log entry to the DB when unsuccessful.
    """
    generateLog(endpoint="/metrics", status_code=500, success=False)

    log = SystemMetric.objects.first()
    assert log.endpoint == "/metrics"
    assert log.status_code == 500
    assert log.success is False


@pytest.mark.django_db
def testGenerateLogMultiCall():
    """
    Test multiple calls create multiple records.
    Uses mock db to reduce impact.
    """
    with patch("healthstatus.utils.SystemMetric.objects.create") as mockDB:
        generateLog("/devices", 200, True)
        generateLog("/metrics", 404, False)

        mockDB.assert_any_call(endpoint="/devices", status_code=200, success=True)
        mockDB.assert_any_call(endpoint="/metrics", status_code=404, success=False)


@pytest.mark.django_db
def testGetDeviceAvail():
    """
    Test getDeviceAvail when the database is not empty.
    """

    DeviceStatus.objects.create(
                device_id=100,
                name='TestDevice1',
                ip_address="192.168.1.1",
                status=1,
            )

    df = getDeviceAvail()

    assert not df.empty
    assert (df.columns == ['DEVICE_NAME', 'SUCCESSFUL_ATTEMPTS', 'TOTAL_ATTEMPTS', 'AVAILABILITY']).all()
    assert len(df) > 0

@pytest.mark.django_db
def testGetDeviceAvailEmpty():
    """
    Test getDeviceAvail when the database is empty.
    """
    with patch("healthstatus.models.DeviceStatus.objects.create") as mockDB:
        df = getDeviceAvail()

        assert df.empty


@pytest.mark.django_db
def testGetAvailTable():
    """
    Test getAvailTable when the database is not empty.
    """
    DeviceStatus.objects.create(
        device_id=100,
        name='TestDevice1',
        ip_address="192.168.1.1",
        status=1,
    )

    df = getDeviceAvail()
    df['AVAILABILITY'] = round(df['AVAILABILITY'], 1).astype(str) + '%'
    df['DEVICE_NAME'] = "<strong>" + df['DEVICE_NAME'].astype(str) + "</strong>"

    expected: str = df.to_html(index=False, escape=False, classes="table table-striped table-sm", table_id="availTable")
    actual: str = getAvailTable()

    assert actual == expected


@pytest.mark.django_db
def testGetAvailTableEmpty():
    """
    Test getAvailTable when the database is empty.
    """
    assert getAvailTable() == '<p>No device records available</p>'
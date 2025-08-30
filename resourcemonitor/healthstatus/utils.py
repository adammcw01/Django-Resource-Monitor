"""
This file contains utility functions for the health status app.
"""
from healthstatus.models import DeviceStatus, SystemMetric
import pandas as pd

def generateLog(endpoint: str, status_code: int, success: bool) -> None:
    """
    Generates a log and writes to SystemMetric.
    Used to monitor network traffic.

    Args:
        endpoint (str): The API endpoint being monitored.
        status_code (int): The HTTP status code returned by the endpoint.
        success (bool): Whether the request was successful (2xx status code).
    
    Returns:
        None
    """
    SystemMetric.objects.create(
        endpoint=endpoint,
        status_code=status_code,
        success=success,
    )
    return

def getDeviceAvail() -> pd.DataFrame:
    """
    Generates an aggregated dataset from the DeviceStatus model.
    Calculates device availability by
        number of successful attempts / total attempts.

    Args:
        None
    
    Returns:
        pandas.DataFrame: The aggregated DataFrame.
    """
    query = DeviceStatus.objects.all().values()
    df: pd.DataFrame = pd.DataFrame(query)

    if df.empty:
        return pd.DataFrame(columns=["DEVICE_NAME", "SUCCESSFUL_ATTEMPTS", "TOTAL_ATTEMPTS", "AVAILABILITY"])

    df = df.groupby('name').agg(
        SUCCESSFUL_ATTEMPTS=('status', 'sum'),
        TOTAL_ATTEMPTS=('status', 'count')
    )

    df['AVAILABILITY'] = (df['SUCCESSFUL_ATTEMPTS'] / df['TOTAL_ATTEMPTS']) * 100 # Availability %

    df = df.reset_index().rename(columns={'name': 'DEVICE_NAME'})
    df = df.sort_values(by='AVAILABILITY', ascending=False) # Rank best performing devices first.
    return df

def getAvailTable() -> str:
    """
    Generates an HTML table for device availability.
    """
    df = getDeviceAvail()

    if df.empty: return "<p>No device records available</p>"

    # Table formatting:
    # Make device names bold and format availability percentages.
    df['AVAILABILITY'] = round(df['AVAILABILITY'], 1).astype(str) + '%'
    df['DEVICE_NAME'] = "<strong>" + df['DEVICE_NAME'].astype(str) + "</strong>"

    return df.to_html(
            classes="table table-striped table-sm",
            index=False,
            table_id="availTable",
            escape=False # Allows bold tags
        )

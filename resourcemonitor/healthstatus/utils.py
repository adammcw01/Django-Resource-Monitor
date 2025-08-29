from healthstatus.models import DeviceStatus
import pandas as pd

def generateLog(endpoint, status_code, success):
    from .models import SystemMetric
    SystemMetric.objects.create(
        endpoint=endpoint,
        status_code=status_code,
        success=success,
    )

def getDeviceAvail():
    qs = DeviceStatus.objects.all().values()
    df = pd.DataFrame(qs)

    df = df.groupby('name').agg(
        SUCCESSFUL_ATTEMPTS=('status', 'sum'),
        TOTAL_ATTEMPTS=('status', 'count')
    )

    df['AVAILABILITY'] = (df['SUCCESSFUL_ATTEMPTS'] / df['TOTAL_ATTEMPTS']) * 100

    df = df.reset_index().rename(columns={'name': 'DEVICE_NAME'})
    df = df.sort_values(by='AVAILABILITY', ascending=False)
    return df

def getAvailTable():
    df = getDeviceAvail()

    if df.empty: return "<p>No device records available</p>"

    df['AVAILABILITY'] = round(df['AVAILABILITY'], 1).astype(str) + '%'
    df['DEVICE_NAME'] = "<strong>" + df['DEVICE_NAME'].astype(str) + "</strong>"

    return df.to_html(
            classes="table table-striped table-sm",
            index=False,
            table_id="availTable",
            escape=False
        )


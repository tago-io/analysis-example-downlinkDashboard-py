"""
Analysis Example
Sending downlink using dashboard
Using an Input Widget in the dashboard, you will be able to trigger a downlink to
any LoraWaN network server.
You can get the dashboard template to use here: http://admin.tago.io/template/5f514218d4555600278023c4

Environment Variables
In order to use this analysis, you must setup the Environment Variable table.

default_PORT: The default port to be used if not sent by the dashboard.
device_id: The default device id to be used if not sent by the dashboard (OPTIONAL).
payload: The default payload to be used if not sent by the dashboard (OPTIONAL).
"""
from tagoio_sdk import Resources, Analysis
from tagoio_sdk.modules.Utils.sendDownlink import sendDownlink


# The function myAnalysis will run when you execute your analysis
def my_analysis(context, scope: list[dict]) -> None:
    resources = Resources()
    # Get the variables form_payload, form_port and device_id sent by the widget/dashboard.
    payload = list(filter(lambda payload: payload["variable"] == "form_payload", scope))

    if not payload:
        return print('Missing "form_payload" in the data scope.')

    payload = payload[0]["value"]

    port = list(filter(lambda payload: payload["variable"] == "form_port", scope))

    if not port:
        return print('Missing "form_port" in the data scope o.')

    port = port[0]["value"]

    device_id = scope[0]["device"]

    result = sendDownlink(
        resource=resources,
        device_id=device_id,
        dn_options={"port": port, "payload": payload},
    )
    print(result)


# The analysis token in only necessary to run the analysis outside TagoIO
Analysis.use(my_analysis, params={"token": "MY-ANALYSIS-TOKEN-HERE"})

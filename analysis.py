# Analysis Example
# Sending downlink using dashboard
# Using an Input Widget in the dashboard, you will be able to trigger a downlink to
# any LoraWaN network server.
# You can get the dashboard template to use here: http://admin.tago.io/template/5f514218d4555600278023c4
#
# Environment Variables
# In order to use this analysis, you must setup the Environment Variable table.
#
# account_token: Your account token. Check bellow how to get this.
# default_PORT: The default port to be used if not sent by the dashboard.
# device_id: The default device id to be used if not sent by the dashboard (OPTIONAL).
# payload: The default payload to be used if not sent by the dashboard (OPTIONAL).
#
# Steps to generate an account_token:
# 1 - Enter the following link: https://admin.tago.io/account/
# 2 - Select your Profile.
# 3 - Enter Tokens tab.
# 4 - Generate a new Token with Expires Never.
# 5 - Press the Copy Button and place at the Environment Variables tab of this analysis.
from tago import Analysis
from tago import Account
from os import error
import requests
# The function myAnalysis will run when you execute your analysis
def myAnalysis(context,scope):
  account_token = list(filter(lambda account_token: account_token['key'] == 'account_token', context.environment))
  account_token = account_token[0]['value']

  if not account_token:
   return context.log("Missing account_token Environment Variable.")

  my_account = Account(account_token)
  # Get the variables form_payload, form_port and device_id sent by the widget/dashboard.
  payload = list(filter(lambda payload:payload['variable'] == 'form_payload', scope))
  device_id = payload[0]['origin']
  payload = payload[0]['value']

  port = list(filter(lambda payload:payload['variable'] == 'form_port', scope))
  port = port[0]['value']

  if not payload:
    return context.log("Payload not found")
  if not port:
    return context.log("Port not found")

  network_id = my_account.devices.info(device_id)
  network_id = network_id['result']['network']
  context.log(network_id)
  # get network info(middleware_endpoint) using api 
  middleware_endpoint = my_account.integration_network.info(network_id,['id', 'middleware_endpoint', "name"])
  middleware_endpoint = middleware_endpoint['result']['middleware_endpoint']
  if not middleware_endpoint:
    return context.log("Couldn't find a network middleware for this device.")

  # Set the parameters for the device. Some NS like Everynet need this.
  params = my_account.devices.paramList(device_id,"false")
  downlink_param = list(filter(lambda downlink_param: downlink_param['key'] == 'downlink', params['result']))
  downlink_param = downlink_param[0]
  my_account.devices.paramSet(device_id,downlink_param)
  # Find the token containing the authorization code used.
  device_tokens = my_account.devices.tokenList(device_id,1,10,{},['name', 'serie_number', 'last_authorization'])
  token_result = device_tokens['result']
  token_serie_number = token_result[0]['serie_number']
  token_last_authorization = token_result[0]['last_authorization']
  if not token_serie_number:
    return context.log("Couldn't find a token with serial for this device")
  if not token_last_authorization:
    return context.log("Couldn't find a token with last authorization for this device")

  context.log('Trying to send the downlink')
  data = {'device':token_serie_number,'authorization': token_last_authorization,'payload': payload,'port': port}
  context.log(data)

  try:result = requests.post("https://"+ middleware_endpoint +"/downlink" , data)  
  except error:context.log(error)
  context.log(result)
# The analysis token in only necessary to run the analysis outside TagoIO
Analysis('my analysis token here').init(myAnalysis)

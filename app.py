from bottle import (post, request, response, route, run, )
from twilio import twiml
from twilio.rest import TwilioRestClient


client = TwilioRestClient()

# this URL variable can be dynamic or customized later
MMS_URL = "https://wiki.factorio.com/images/Fast_transport_belt_fulldensity.gif"


@route('/')
def check_app():
    # returns a simple string stating the app is working
    return "Bottle web app up and running!"


@route('/send-sms/<to_number>/<from_number>/<message_body>/')
def outbound_sms(to_number, from_number, message_body):
    # use the Twilio helper library to send an outbound SMS
    # via the REST API
    client.messages.create(to=to_number, from_=from_number,
                           body=message_body)
    # this response is sent back to the web browser client
    return "SMS sent to " + to_number


@route('/send-mms/<to_number>/<from_number>/<message_body>/')
def outbound_mms(to_number, from_number, message_body):
    # uses the Twilio helper library to send an outbound MMS
    # via the REST API
    client.messages.create(to=to_number, from_=from_number,
                           body=message_body, media_url=MMS_URL)
    return "MMS sent to " + to_number


@post('/twilio-webhook')
def inbound_sms():
    twiml_response = twiml.Response()
    # obtain message body from the request. could also get the "To" and 
    # "From" phone numbers as well from parameters with those names
    inbound_message = request.forms.get("Body")
    response_message = "I don't understand what you meant...need more code!"
    # we can use the incoming message text in a condition statement
    if inbound_message == "Hello":
        response_message = "Well, hello right back at ya!"
    twiml_response.message("Hello from Bottle right back at you!")
    # we return back the mimetype because Twilio needs an XML response
    response.content_type = "application/xml"
    return str(twiml_response)


if __name__ == '__main__':
    # use the Bottle framework run function to start the development server
    run(host='127.0.0.1', port=5000, debug=True, reloader=True)

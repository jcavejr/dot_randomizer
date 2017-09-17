import json
import random

def lambda_handler(event, context):
    # Verify the Correct Application ID
    if (event['session']['application']['applicationId'] !=
        "amzn1.ask.skill.1bb7b351-0ab0-4bb9-a707-33a55440bb29"):
        raise ValueError("Invalid Application ID")
    
    # New Session
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])
    
        # Launch Request
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])    

        # Intent Request
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])    

        #Session Ended Request
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])
    
def on_session_started(session_started_request, session):
    print("Starting new session")

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "Randomize":
        return get_randomize(intent)
    elif intent_name == "FlipCoin":
        return get_flipcoin()
    elif intent_name == "RollDice":
        return get_rolldice()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid Intent")

def on_session_ended(session_ended_request, session):
    print("Ending session")
    #cleanup

def handle_session_end_request():
    card_title = "Randomize - Thanks"
    speech_input = "Thank you for using Randomize, make sure to tell your friends about my new skill."
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "RANDOMIZE"
    speech_output = "Welcome to the Randomize skill. " \
                    "Try asking me to flip a coin, roll a dice, or pick a random number from x to y"
    reprompt_text = "Try asking me to flip a coin, roll a dice, or pick a random number from x to y"
    should_end_session = False
   
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def get_randomize(intent):
    session_attributes = {}
    card_title = "RANDOMIZE"
    should_end_session = True

    start_number = int(intent["slots"]["StartNumber"]["value"])
    end_number = int(intent["slots"]["EndNumber"]["value"])

    random_number = random.randint(start_number, end_number)

    speech_output = str(random_number) 
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, 
        reprompt_text, should_end_session))

def get_flipcoin():
    session_attributes = {}
    card_title = "RANDOMIZE"
    should_end_session = True

    random_number = random.randint(1, 2)
    if random_number == 1:
        coin_face = "heads"
    elif random_number == 2:
        coin_face = "tails"

    speech_output = coin_face
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output,
        reprompt_text, should_end_session))

def get_rolldice():
    session_attributes = {}
    card_title = "RANDOMIZE"
    should_end_session = True

    die_face = random.randint(1, 6)

    speech_output = str(die_face)
    reprompt_text = ""

    return build_response(session_attributes, build_speechlet_response(card_title, speech_output,
        reprompt_text, should_end_session))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "contain": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
}

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }


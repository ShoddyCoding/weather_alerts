import utilities as u
import os
import telnyx
import eventlogger as er

def send_message(to_number, message):
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    telnyx.api_key = config["TEXTING"]["API"]
    fromnum = config["TEXTING"]["FROMNUMBER"]
    try:
        if len(to_number) == 12 and to_number.startswith("+") and len(message) < 163:
            sent_response = telnyx.Message.create(
                from_= fromnum,
                to= to_number,
                text = message
            )
    except Exception as e:
        er.add_events("ERROR: Issue sending out a message to {0}: {1}".format(to_number,e.string))
    finally:
        return sent_response

if __name__ == "__main__":
    __location__ = u.get_local_file_path()
    config = u.read_json(os.path.join(__location__, 'config.json'))
    telnyx.api_key = config["TEXTING"]["API"]
    fromnum = config["TEXTING"]["FROMNUMBER"]
    tonum = config["TEXTING"]["TESTNUMBER"]
    message = "Test for Refactoring"
    if len(tonum) == 12 and tonum.startswith("+") and len(message) < 163:
            sent_response = telnyx.Message.create(
                from_= fromnum,
                to= tonum,
                text = message
            )
    print(sent_response)
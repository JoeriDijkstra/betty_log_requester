import json
import requests
from datetime import datetime
import subprocess

# Get response


def make_request_params(log_id, url_var, username, password):
    params = (
        ('log_id', log_id),
    )
    response = request(params, url_var, username, password)
    print(pretty_print_json(response.json()))


def make_request(url, username, password):
    response = request(None, url, username, password)
    print_menu(response.json())


def request(params, url_var, username, password):
    response = requests.get('https://' + url_var + '.bettyblocks.com/api/newlogs',
                            params=params, auth=(username, password))
    subprocess.run("pbcopy", universal_newlines=True,
                   input=pretty_print_json(response.json()))
    return response

# Print out JSON


def pretty_print_json(var_json):
    json_object = var_json
    json_formatted_str = json.dumps(json_object, indent=2)
    return json_formatted_str


def print_menu(var_json):
    print("There are " + str(len(var_json["records"])) + " logs found")
    for x in var_json["records"]:
        time = datetime.fromtimestamp(x["time"])

        # Construct final string
        output = "\033[94m" + str(time) + "\033[0m"
        divider = " | "
        output += divider
        output += x["log_id"]
        output += divider
        output += "\033[93m" + str(x["additional_severity"]) + "\033[0m"
        print(output)


# Get user initial input
print("\033[95m - Log request tool - \033[0m")
identifier = input("Application Identifier: ")
username = input("Betty Username: ")
password = input("API key: ")
print("\033[95m - Q to Quit, M to show all logs - \033[0m")

# Core loop
inp = input("Log Id: ")
while inp != "q":
    if(inp == "m"):
        make_request(identifier, username, password)
    else:
        make_request_params(inp, identifier, username, password)
        print("\033[92mCopied to clipboard\033[0m")

    inp = input("Log Id: ")

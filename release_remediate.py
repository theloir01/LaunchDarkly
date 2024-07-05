'''
REQUIRED PYTHON PACKAGES
------------------------
flask
launchdarkly-server-sdk

HOW TO RUN THE CODE
-------------------
Obtain your SDK key from LaunchDarkly UI

Run from terminal as follows or use environment variable to hold SDK key:

LAUNCHDARKLY_SDK_KEY="<your-sdk-key>" python release_remediate.py

BACKGROUND
----------

This file runs a Flask server on locahost at http://127.0.0.1:5000

The server interacts with the LaunchDarkly library to interact with flags and metrics

A separate web page has been created as a faux UI front-end to provide an interactive experience

This UI takes the forms of a Pricing page offering the visitor three pricing plans at increasing cost

When the feature-flag key of your choosing is toggled on, the visitor, if in the appropriate segment,
sees discounted pricing with a banner displaying an Exclusive Discount with a countdown timer.
The feature flag status is automatically pushed to the UI such that when it is turned off the pricing
reverts to standard, and when it is turned on the pricing displays the special discount offer.

The feature-flag has been designed to be targeted by both rules-based and individual segments.

In LaunchDarkly I have created two segments:

Segment 1 - target users(contexts) where their country is set to the United Kingdom
Segment 2 - target a specific user as Excluded from this feature

To test this out there are two contexts created below:

Context 1: By default this is uncommented and is the starting point. The context should see the feature
           in the UI assuming the flag is turned on inside of LaunchDarkly. Try changing the country to
           something other than the United Kingdom. The feature should disappear automatically. Change it back
           to the United Kingdom before trying out the second context.

Context 2: By default this is commented out. This context belongs to an Excluded Users segment. Despite the
           country being set to the United Kingdom this context is not allowed to see the feature. To test this
           out, comment out Context 1 and uncomment this context. The feature should disappear automatically
           assuming it was visible before changing contexts.

Now we have established the ability to:
 a) remediate a feature by toggling the flag off in LaunchDarkly, and
 b) target specific contexts based upon both a rules and individual approach

We now want to be able to track how the visitor interacts with the pricing page.
 - I want to know when they click on each one of the three pricing offer (register-interest)
 - I also want to know when they complete their registration (complete-register-interest)

We therefore have 6 metrics defined in LaunchDarkly and for each event the visitor undertakes it is
tracked to the appropriate metric.

This is useful for understanding conversion rates as it relates to the feature e.g. what is the conversion
rate of the Essentials plan without the special offer versus with it? What is the conversion rate between
clicking on the Register Interest button and actually submitting their interest?

I hope you enjoy!
'''

from flask import Flask, jsonify, render_template, request
import ldclient
from ldclient.config import Config
from ldclient import Context
import os

# Set sdk_key to your LaunchDarkly SDK key.
sdk_key = os.getenv("LAUNCHDARKLY_SDK_KEY")

# Set the project_key - use the value of "default" if it's your only project
project_key = "<your_project_key>"

# Set feature_flag_key to the feature flag key you want to evaluate. I have used release-remediate here
feature_flag_key = "<your_flag_key>"

# Set the environment key. If this is your first time with LaunchDarkly this is likely to be the test environment
environment_key = "<your_environment_key>"

# Set the API key.
# If you haven't done so already go to LaunchDarkly https://app.launchdarkly.com/settings/authorization
# Create an Access Token and copy that value here
api_key = "<your_api_key>"

# Begin Flask
app = Flask(__name__)

# Initialize LaunchDarkly client with the SDK key you passed in when starting the app
ldclient.set_config(Config(sdk_key))
client = ldclient.get()

''' Context 1 is focused on segmentation by country
The segment in LaunchDarkly has been configured to only show the feature if the context country is 
the United Kingdom

The context key is required here - you can obtain the key per context by clicking on Contexts in 
LaunchDarkly and copying the appropriate key that is displayed in the Context table 

Usage:
1. Ensure the flag is turned on
2. Set the country to the United Kingdom in the context below and confirm the feature is visible
3. Change the country to something other than the United Kingdom and confirm the feature disappears automatically
'''

context = Context.builder("<your-context-key>") \
    .set("firstName", "firstName") \
    .set("lastName", "lastName") \
    .set("email", "email_address") \
    .set("country", "United Kingdom") \
    .build()

''' Context 2 is focused on segmentation by Excluded User
This segment in LaunchDarkly has been configured to not display the feature irrespective of their country

The context key is required here - LaunchDarkly ships with a default context called Sandy that has a context key
of example-user-key

Usage:

1. Ensure the feature flag is turned on
2. Ensure that the UI correctly shows the offer
3. Uncomment the context below ensuring the country is set to the United Kingdom
4. Confirm that despite the user being in the United Kingdom they cannot see the feature
'''
# context = Context.builder("example-user-key") \
#     .set("firstName", "Sandy") \
#     .set("lastName", "Lyle") \
#     .set("email", "sandy.lyle@gmail.com") \
#     .set("country", "United Kingdom") \
#     .build()

# Function to post metric data back to LaunchDarkly
def track_metric(
    metric_name: str,
    data: str,
):

    print(f"metric name is {metric_name} and data is {data}")
    client.track(metric_name, context, data)

# Flask - serve up index.html page to visitor
@app.route('/')
def index():
    # Evaluate feature flag to determine if special offer should be shown
    # show_special_offer = client.variation(feature_flag_key, context, False)
    return render_template('index.html')

# Flask - route to handle the LaunchDarkly feature flag in index.html
@app.route('/get-special-offer-status')
def get_special_offer_status():
    # Evaluate feature flag to determine if special offer should be shown
    show_special_offer = client.variation(feature_flag_key, context, False)
    return jsonify({"show_special_offer": show_special_offer})


'''Route to handle the beginning of the registering interest process
Fired off when the visitor clicks on each of the Register Interest buttons
Captures visitor intent on a per-button basis which is mapped to the appropriate metric
Calls the track_metric function to post back to LaunchDarkly
'''
@app.route('/register-interest-event', methods=['POST'])
def register_interest():
    data = request.get_json()
    plan_name = data.get('plan')

    # Print to terminal - useful for debugging
    print(f"User clicked on button and may be registering interest for {plan_name}")

    # Based upon which button the visitor interacted with send this to the appropriate metric
    if plan_name.upper() == "ESSENTIALS":
        track_metric("register-interest-essentials", data)
    elif plan_name.upper() == "PRO":
        track_metric("register-interest-pro", data)
    elif plan_name.upper() == "ENTERPRISE":
        track_metric("register-interest-enterprise", data)

    return jsonify({"success": True})

'''Route to handle the completion of the registering interest process
Fired off when the visitor clicks on each on the Submit Interest button in the pop-up form
Captures visitor intent on a per-plan basis which is mapped to the appropriate metric
Calls the track_metric function to post back to LaunchDarkly
Useful to be able to track conversion rates and which of the three pricing plans converts more
'''
@app.route('/submit-interest', methods=['POST'])
def submit_interest():
    data = request.get_json()
    plan_name = data.get('plan')

    # Print to terminal - useful for debugging
    print(f"User clicked on button and confirmed their registration for {plan_name}")

    # Based upon which plan the visitor confirmed interest with, send this to the appropriate metric
    if plan_name.upper() == "ESSENTIALS":
        track_metric("complete-register-interest-essentials", data)
    elif plan_name.upper() == "PRO":
        track_metric("complete-register-interest-pro", data)
    elif plan_name.upper() == "ENTERPRISE":
        track_metric("complete-register-interest-enterprise", data)

    return jsonify({"success": True})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
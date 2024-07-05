This repo has been created for the LaunchDarkly technical assessment

The goal of the assessment is as follows:

1. Demonstrate Remediation of a Feature using a Flag
2. Demonstrate targetting in both a rules and individual basis
3. [OPTIONAL] Create metrics to track visitor behaviour
4. [OPTIONAL] Create an experiment on the metrics created <--- NOTE that this feature is gated on the Trial account and is considered out of scope
5. [OPTIONAL] Explore integrations

PREREQUISITES
-------------

LaunchDarkly Trial Account
Python3 locally installed


GETTING STARTED IN LAUNCHDARKLY
-------------------------------

1. Create trial account by heading over to https://launchdarkly.com/start-trial/
2. Create an API key by heading over to https://app.launchdarkly.com/settings/authorization and clicking on "Create token"
3. Create a feature flag by heading over to https://app.launchdarkly.com/projects/default/flags?env=test&selected-env=test and clicking on "Create flag" - make a copy of the feature flag key
4. Create two segments by heading over to https://app.launchdarkly.com/projects/default/segments?env=test&selected-env=test
   a. Create a segment called Excluded Users and under Targeting add the default user Sandy
   b. Create a segment called UK Users Only and under Targeting add a rule where user country equals United Kingdom
5. Go back to your flags and add two rules
   a. Rule 1 should target the Excluded Users segment
   b. Rule 2 should target the UK Users Only segment
6. Create six metrics by heading over to https://app.launchdarkly.com/projects/default/metrics?env=test&selected-env=test and clicking on "Create"
   a. register-interest-enterprise - this will track when a user begins the registration process for the Enterprise pricing
   b. register-interest-essentials - this will track when a user begins the registration process for the Essentials pricing
   c. register-interest-pro - this will track when a user begins the registration process for the Pro pricing
   d. complete-register-interest-enterprise - this will track when a visitor completes their registration request for the Enterprise pricing
   e. complete-register-interest-essentials - this will track when a visitor completes their registration request for the Essentials pricing
   f. complete-register-interest-pro - this will track when a visitor completes their registration request for the Pro pricing
7. Obtain the context key for each context in scope by heading to https://app.launchdarkly.com/projects/default/contexts?env=test&selected-env=test. This will be one for the default user Sandy, and the other for your user
8. Obtain your SDK key for the test environment by heading to https://app.launchdarkly.com/projects/default/settings/environments?env=test&selected-env=test

Make a note of all keys for adding to the Python code

GETTING STARTED WITH THE PYTHON FILE
------------------------------------

1. Download and install both flask and launchdarkly-server-sdk
2. Replace the project_key placeholder with your project key (this is likely to be the value of "default")
3. Replace the feature_flag_key placeholder with your flag key
4. Replace the environment_key placeholder with your environment key (this is likely to be the value of "test")
5. Replace the api_key placeholder with your API key
6. Replace the your-context-key placeholder with the context-key you obtained for your user
7. Replace the example-user-key placeholder with the context-key you obtained for the default user called Sandy (this is like to be the value of "example-user-key")

RECOMMENDED USAGE
-----------------

Start the demo
--------------

Run the python file in an IDE (I use PyCharm) as follows: LAUNCHDARKLY_SDK_KEY="<your_sdk_key>" release_remediate.py
This will start a flask server on http://127.0.0.1:5000
Open up a browser and go to http://127.0.0.1:5000 where you should see a Pricing webpage

Remediate demo
--------------

Open up the LaunchDarkly UI and toggle the flag on/off
Confirm that special pricing appears/disappears depending on flag status

Note that if you have configured Slack integration this will fire off Slack alerts (see Integrations Demo section below)

Targeting Demo - Rule-based
---------------------------

Within your IDE scroll to the first context in the python file and change the country to something other than United Kingdom e.g. Albania
Confirm that the special pricing disapperas when the country is not the United Kingdom 
Revert the country back to United Kingdom
Confirm that the special pricing reappears

Targeting Demo - Individual-based
---------------------------------

Within your IDE scroll to the first context in the python file and comment that out then Save
Scroll to the second context in the python file and uncomment that then Save
Confirm that the special pricing disapperas when the user is in the Excluded List
Revert back to the first context
Confirm that the special pricing reappears

Metrics Demo

Within the Pricing webpage, click on any of the Register Interest
Confirm that the IDE prints the streaming of the target back to LaunchDarkly tied to the specific pricing plan tier
Fill out the web form and click on Submit Interest
Confirm that the IDE prints the streaming of the target back to LaunchDarkly tied to the specific pricing plan tier
Go to LaunchDarkly Metrics page and click on the metrics that you had interacted with
Wait for the data to load and show that the metric was successfully hit
NOTE - I have experienced delays in these showing up - not sure if this is a limitation of the Trial account. Might be a good idea to prepopulate here before the demo

Experiment Demo
---------------

As mentioned above, this feature is gated on Trial accounts and as such has not been included

Integrations Demo
-----------------

I have used Slack for the demo which is tied to the flag created.
Slack channel created to subscribe to events on the flag created
Slack channel is updated when the flag is toggled on/off




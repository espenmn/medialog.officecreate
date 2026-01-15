# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s medialog.officecreate -t test_template.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src medialog.officecreate.testing.MEDIALOG_OFFICECREATE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/medialog/officecreate/tests/robot/test_template.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Template
  Given a logged-in site administrator
    and an add Template form
   When I type 'My Template' into the title field
    and I submit the form
   Then a Template with the title 'My Template' has been created

Scenario: As a site administrator I can view a Template
  Given a logged-in site administrator
    and a Template 'My Template'
   When I go to the Template view
   Then I can see the Template title 'My Template'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add Template form
  Go To  ${PLONE_URL}/++add++Template

a Template 'My Template'
  Create content  type=Template  id=my-template  title=My Template

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the Template view
  Go To  ${PLONE_URL}/my-template
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a Template with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the Template title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

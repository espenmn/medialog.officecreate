# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s medialog.officecreate -t test_power_point_dummy.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src medialog.officecreate.testing.MEDIALOG_OFFICECREATE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/medialog/officecreate/tests/robot/test_power_point_dummy.robot
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

Scenario: As a site administrator I can add a PowerPointDummy
  Given a logged-in site administrator
    and an add PowerPointDummy form
   When I type 'My PowerPointDummy' into the title field
    and I submit the form
   Then a PowerPointDummy with the title 'My PowerPointDummy' has been created

Scenario: As a site administrator I can view a PowerPointDummy
  Given a logged-in site administrator
    and a PowerPointDummy 'My PowerPointDummy'
   When I go to the PowerPointDummy view
   Then I can see the PowerPointDummy title 'My PowerPointDummy'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add PowerPointDummy form
  Go To  ${PLONE_URL}/++add++PowerPointDummy

a PowerPointDummy 'My PowerPointDummy'
  Create content  type=PowerPointDummy  id=my-power_point_dummy  title=My PowerPointDummy

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the PowerPointDummy view
  Go To  ${PLONE_URL}/my-power_point_dummy
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a PowerPointDummy with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the PowerPointDummy title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

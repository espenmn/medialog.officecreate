# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s medialog.officecreate -t test_docx_example.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src medialog.officecreate.testing.MEDIALOG_OFFICECREATE_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot /src/medialog/officecreate/tests/robot/test_docx_example.robot
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

Scenario: As a site administrator I can add a DocxExample
  Given a logged-in site administrator
    and an add DocxExample form
   When I type 'My DocxExample' into the title field
    and I submit the form
   Then a DocxExample with the title 'My DocxExample' has been created

Scenario: As a site administrator I can view a DocxExample
  Given a logged-in site administrator
    and a DocxExample 'My DocxExample'
   When I go to the DocxExample view
   Then I can see the DocxExample title 'My DocxExample'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add DocxExample form
  Go To  ${PLONE_URL}/++add++DocxExample

a DocxExample 'My DocxExample'
  Create content  type=DocxExample  id=my-docx_example  title=My DocxExample

# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.IBasic.title  ${title}

I submit the form
  Click Button  Save

I go to the DocxExample view
  Go To  ${PLONE_URL}/my-docx_example
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a DocxExample with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the DocxExample title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}

*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers

*** Test Cases ***

Let me think what to do next
    Enable autologin as  Site Administrator
    Go to  ${PLONE_URL}

    Import library  Dialogs

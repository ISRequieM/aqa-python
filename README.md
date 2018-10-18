# aqa-python project
This project provides Jira UI and Rest API tests for learning purposes.

To perform run of tests perform the next:
python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -n=4 --dist loadfile --reruns=4 --alluredir=test-reports -v -l

After finishing run - generate allure report using the next command (you should have allure cli tool installed)
allure serv test-reports
It will bring up small web server and show report in your web browser.

The next allure epic names are available:
"Learning"
"Jira WebUI"
"Jira REST API"

To run test for specific epic please add additional option --allure-epics to command line, example:
python -m pytest --reruns=4 --alluredir=test-reports --allure-epics "epic1" "epic2" -v -l
For some reason parallel execution fails if using --allure-epics option.
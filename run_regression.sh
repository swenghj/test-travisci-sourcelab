#!/usr/bin/env bash

#-- this is example --#
#python testsite/manage.py runserver &
#mkdir saucelab; cd saucelab
#git clone -b selenium https://github.com/swenghj/test-travisci-sourcelab.git
#cd test-travisci-sourcelab
#ls .
#cd selenium/automation
#python demo-regression.py
#ls reports
#git config --global user.name "My Name"
#git config --global user.email "me@example.com"
#git branch htmlresults selenium
#git checkout htmlresults
#git add reports/* -f
#git commit -m "regression results HTMLs"
#git push https://$GIT_USER:$GIT_API_KEY@github.com/swenghj/test-travisci-sourcelab.git htmlresults -f

#-- ap test --#
git clone https://github.com/attendanceproject/djattendance.git
ls .
cd djattendance
export DJANGO_SETTINGS_MODULE=ap.settings.travis
pip install -r requirements/dev.txt
which python
mypython=$(which python)
sudo $mypython dependencies/ortools/setup.py install
virtualenvpath=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
sudo chmod -R +rw $virtualenvpath
psql -c 'create database djattendance;' -U postgres
psql -d djattendance -c "CREATE EXTENSION IF NOT EXISTS hstore;"
python ap/makeallmigrations.py --settings=ap.settings.travis
#python ap/makeallmigrations.py
#python ap/manage.py migrate --noinput
python ap/manage.py migrate --settings=ap.settings.travis

# automation starts from here

# create a super user
echo "super user creation"
echo "from accounts.models import User; User.objects.filter(email='ap_test@gmail.com').delete(); User.objects.create_superuser('ap_test@gmail.com', 'ap')" | python ap/manage.py shell

# populate initial data
#python ap/manage.py populate_testers
#python ap/manage.py populate_events
#python ap/manage.py populate_tas --settings=ap.settings.dev
#python ap/manage.py populate_terms 
#python ap/manage.py populate_rolls #the population script runs it for the 2016 winter term
python ap/manage.py populate_testers --settings=ap.settings.travis
python ap/manage.py populate_events --settings=ap.settings.travis
#python ap/manage.py populate_tas --settings=ap.settings.dev
python ap/manage.py populate_terms --settings=ap.settings.travis
#python ap/manage.py populate_rolls --settings=ap.settings.dev #the population script runs it for the 2016 winter term

# run the server
echo "run the test server"
#python ap/manage.py runserver --settings=ap.settings.dev &
python ap/manage.py runserver &
sleep 30

# run the regression
echo "run the regression tests"
cd ../; ls .; mkdir saucelab; cd saucelab
#git clone -b selenium https://github.com/swenghj/test-travisci-sourcelab.git
git clone -b automation https://github.com/attendanceproject/djattendance.git
#cd test-travisci-sourcelab
cd djattendance
ls .
cd selenium/automation
echo "inside 'automation' directory"
ls .

# run the regressions
echo "run python-selenium regressions"
#python ap-demo-regression.py
python run_regression.py

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
python ap/makeallmigrations.py
python ap/manage.py migrate --noinput

# automation starts from here
# run the server
echo "run the test server"
python ap/manage.py runserver &

# run the regression
echo "run the regression tests"
cd ../; ls .; mkdir saucelab; cd saucelab
git clone -b selenium https://github.com/swenghj/test-travisci-sourcelab.git
cd test-travisci-sourcelab
ls .
cd selenium/automation
ls .

# run the regressions
echo "run python-selenium regressions"
python ap-demo-regression.py


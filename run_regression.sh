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




#-- ap test: SET UP TEST ENVIRONMENT --#
sudo apt-get install nodejs npm -y
git clone https://github.com/attendanceproject/djattendance.git
sudo chmod 775 djattendance/ -R
echo "######### download finished, current directory: #########"
ls .
echo "######### moved to inside: #########"
cd djattendance
ls .
export DJANGO_SETTINGS_MODULE=ap.settings.travis
pip install -r requirements/dev.txt
which python
mypython=$(which python)
sudo $mypython dependencies/ortools/setup.py install
virtualenvpath=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
sudo chmod -R +rw $virtualenvpath

# Run build for webpack
npm install
npm run build

# DB
sudo -u postgres psql postgres -c "create user ap with createrole superuser password '4livingcreatures'"
psql -c 'create database djattendance;' -U postgres
psql -d djattendance -c "CREATE EXTENSION IF NOT EXISTS hstore;"

# Attendance build 
echo "######### Loading webpack ... ... #########"
npm run start > run_webpack.log 2>&1 &
############ wait ############
while ! grep -qw "webpack: Compiled successfully." run_webpack.log; do sleep 5; done


python ap/makeallmigrations.py
python ap/manage.py migrate


################################################################################################
# automation starts from here
################################################################################################

# populate initial data
python ap/manage.py populate_terms #--settings=ap.settings.test
python ap/manage.py populate_services #--settings=ap.settings.test
python ap/manage.py populate_trainees #--settings=ap.settings.test
python ap/manage.py populate_tas #--settings=ap.settings.test
python ap/manage.py populate_events #--settings=ap.settings.test
python ap/manage.py populate_rolls #--settings=ap.settings.test
python ap/manage.py populate_schedules #--settings=ap.settings.test

# create a super user
echo "######### super user creation #########"
echo "from accounts.models import User; User.objects.filter(email='ap_test@gmail.com').delete(); User.objects.create_superuser('ap_test@gmail.com', 'ap')" | python ap/manage.py shell

##### TODO: fix tester population #####
#python ap/manage.py populate_testers

# run the server
echo "######### Loading Django ... ... #########"
python ap/manage.py runserver &
sleep 40

# run the regression
echo "######### run the regression tests #########"
cd ../; ls .; mkdir saucelab; cd saucelab
#git clone -b selenium https://github.com/swenghj/test-travisci-sourcelab.git
git clone -b automation https://github.com/attendanceproject/djattendance.git
#cd test-travisci-sourcelab
cd djattendance
ls .
cd selenium/automation
echo "######### inside 'automation' directory #########"
ls .

# run the regressions
echo "######### run python-selenium regressions #########"
#python ap-demo-regression.py
python run_regression.py

# email test results
echo "######### email test results: inside report directory #########"
ls reports
echo "######### TRAVIS BUILD DIR #########"
echo $TRAVIS_BUILD_DIR


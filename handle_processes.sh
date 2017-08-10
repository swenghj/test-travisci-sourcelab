#! /bin/bash
cd ~/ap/dserver/ap/
source `which virtualenvwrapper.sh`
workon dev
echo "Loading webpack ... ..."
#npm run start &
npm run start > run_webpack.log 2>&1 &
while ! grep -qw "webpack: Compiled successfully." run_webpack.log; do sleep 5; done
#PID=$!
#wait $PID

echo "Loading Django ... ..."
export DJANGO_SETTINGS_MODULE=ap.settings.test
#python manage.py runserver > run_server.log 2>&1 &
python manage.py runserver &
#while ! grep -qw "Starting development server" run_server.log; do sleep 5; done
#PID=$!
#wait $PID
sleep 30
echo "all ran successfully"


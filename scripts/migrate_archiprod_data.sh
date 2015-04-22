#mysqldump -h mysql2.ircam.fr -u mdang -pE74RT9Y890QQBD --default-character-set=utf8 --add-drop-database --database archiprod > archiprod.sql
mysql -u root -padmin < archiprod.sql 
mysql -u root -padmin < post_dump.sql
cd ..
python manage.py syncdb
python manage.py migrate old --fake 0001
python manage.py migrate old
mysql -u root -padmin < post_migration.sql
python manage.py migrate utils
python manage.py migrate events
sed -i -e "s/RealtimeSignalProcessor/BaseSignalProcessor/g" archiprod/settings.py #to disable haystack realtime update in migration 0027
python manage.py migrate archives
sed -i -e "s/BaseSignalProcessor/RealtimeSignalProcessor/g" archiprod/settings.py #
python manage.py loaddata utils/group_data.json
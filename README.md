ARCHIPROD
=========


Install
-------


# Third-party libraries or executables to install first

	* MySQL
	* FFmpeg with supported formats: ogg, web, mp4 and codecs: vorbis, theora, vp8, aac, h264, mp3
	* Redis >= 2.2.0
	* Solr >= 3.5
	* recess (https://github.com/twitter/recess)


# Archiprod source code


## Local development

	1. Get the code and install Python/django dependencies

		mkvirtualenv archiprod  # or any other name, this assumes that virtualenv and virtualenvwrapper are installed on your system
		cd $HOME  # or wherever you want to install the code
		git clone git+ssh://git@git.forge.ircam.fr/archiprod.git
		cd archiprod
		pip install -r requirements/development.txt

		The default settings assume your solr has a "dev core" running there: http://127.0.0.1:8983/solr/dev

	2. Set environment specific configuration
	    Settings with * are required, other have got default value, suitable for development

		DATABASE_NAME (*)
		DATABASE_USER (*)
		DATABASE_PASSWORD (*)
		DATABASE_HOST
		DATABASE_PORT
		DEBUG (default to False, for development, you should set it to True)
		DJANGO_SETTINGS_MODULE (*)
		EMAIL_HOST
		EMAIL_PORT
		FTP_ROOT
		MEDIA_ROOT
		MEDIA_URL
		REDIS_URL (host:port)
		STATIC_ROOT
		STATIC_URL
		STREAM_ROOT
		STREAM_URL
		SECRET_KEY (*)
		SOLR_URL
		SOLR_ROOT (*) (to be used in the future to put solr schema.xml file in the right directory)
		TMP_ROOT

	3. Create the database

		python manage.py syncdb
		python manage.py migrate

	4. Services:

		Run the worker (for asynchrone process: encode and watermark)

		python manage.py rqworker default archive


		Be sure Solr is running


		Run a smtp server

		python -m smtpd -n -c DebuggingServer localhost:1025

	5. Run the local server

		python manage.py runserver --nothreading --noreload

	6. Test this app

		python manage.py test archives events utils

		The default settings assume your solr has a "test core" running there: http://127.0.0.1:8983/solr/test


## Server deployment

	1. Get the code and install Python/Django dependencies

		mkvirtualenv archiprod
		git clone git+ssh://git@git.forge.ircam.fr/archiprod.git
		cd archiprod
		python setup.py install

	2. Set environment specific configuration (see 2. in Local development)

	3. Create database or make migrations

	4. Be sure services: Webserver, Redis and Solr are running



Third-party libraries
---------------------

# Solr

http://yuji.wordpress.com/2011/08/15/django-haystack-solr-setup-guide/


	python manage.py build_solr_schema > schema.xml

	### Local development
	mv schema.xml $SOLR_ROOT
	# Start solr
	cd /usr/local/Cellar/solr/<solr_version>/libexec/example/
	java -jar start.jar

	### Staging
	sed -i '' 's/stopwords_en.txt/stopwords.txt/g' schema.xml
	mv schema.xml $SOLR_ROOT
	# Start solr via jetty
	sudo /etc/init.d/jetty jetty restart


Generate index
python manage.py rebuild_index



# Mysql migration (DATAMODEL)

le fichier `scripts/migrate_archiprod_date.sh` permet de faire les migrations
depuis la base en prod vers ce nouveau code.

Après un dump, il faut appliquer le fichier post_dump.sql
Attention: CharField cannot have a "max_length" greater than 255 when using "unique=True".

# Migration DATAS

Sandra : mise à jour des données
* champ date nul pour les 4 *volumes* 'Forum des percussions'
* le champs Doris_id dans personne ? A qui , A quoi ? Pour quoi faire ?


Miscellaneous
-------------

* media encode is done with `encode <media_id> <media_id> ...` command
* command `create_watermark <text>` generate a pdf watermark with <text>
* for data migration, the application use south (a django application)
* scripts for data migration from old archiprod system are in `scripts` folder


Server helpers
--------------

Activate virtualenv
cd /srv/archiprod/envs/archiprod/bin
source activate

Restart supervisord
sudo supervisorctl restart all

uwsgi
sudo /etc/init.d/uwsgi stop
sudo /etc/init.d/uwsgi start



# archiprod

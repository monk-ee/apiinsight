VERSION = 12.0.5
ZIPNAME= api_tester.zip

all:
        /bin/rm -rf venv
        /usr/bin/virtualenv venv -p /usr/bin/python3.4
        venv/bin/pip install --upgrade pip
        venv/bin/pip install -r requirements.txt
        /bin/rm -rf deploy/$(ZIPNAME)
        /usr/bin/zip -r deploy/$(ZIPNAME) venv api_tester.py index.py root-ca.pem --exclude=*Makefile* --exclude=*deploy*
        /usr/bin/aws s3 cp deploy/api_tester.zip s3://artisan-lambda/api_tester.zip

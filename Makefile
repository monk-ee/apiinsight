VERSION = 12.0.5
ZIPNAME= api_insight.zip

all:
        /bin/rm -rf deploy/$(ZIPNAME)
        /usr/bin/zip -r deploy/$(ZIPNAME) venv api_insight.py lambda.py root-ca.pem --exclude=*Makefile* --exclude=*deploy*
        /usr/bin/aws s3 cp deploy/$(ZIPNAME) s3://artisan-lambda/$(ZIPNAME)
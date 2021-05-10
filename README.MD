# CowiNotify
**Get SMS when vaccine is available at specific pincode**\
**Tested and working well (helped me get the dose as well :P)**

-----

*Instructions and details being added*

## Initial setup

1. Make a copy of ```.env.default``` as ```.env```
2. Make a copy of ```config.sample.py``` as ```config.py```
3. Edit these 2 files to configure


### Run/deploy using Docker:

1. Create an AWS User with SNS Full access permission
2. Paste the user's access key ID and secret in .env
3. RUN docker-compose up --build


### Deploy to lambda function:

1. Run ```chmod +x ./build_lambda.sh```
2. Create lambda function and add SNS Full Access permission to it's role.
3. Create a Event rule (from AWS Cloudwatch dashboard) of type schedule and frequency 1 min and with target lambda function.
5. Run ```./build_lambda.sh``` whenever you change config/code.
6. Upload the created ```build.zip``` as code to lambda function


## Do give a Star 🌟 if you liked/found it useful!

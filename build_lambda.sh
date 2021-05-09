mkdir build
cp -t build check_availability.py config.py lambda_function.py sms.py
pip3 install -r requirements.txt -t build
cd build
chmod -R 755 .
zip -r ../build.zip .
cd ..
rm -rf build

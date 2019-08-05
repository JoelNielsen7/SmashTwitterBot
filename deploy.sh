rm -r ./package
pip3 install --target ./package -r requirements.txt --system
cd package
zip -r9 ${OLDPWD}/function.zip .
cd $OLDPWD
zip -g function.zip ./*

# aws s3 cp function.zip s3://twitter-webhook-smashbot
aws lambda update-function-code --function-name scanner --zip-file fileb://function.zip
aws lambda update-function-code --function-name twitter_webhook_post --zip-file fileb://function.zip
rm function.zip

git pull origin master
env BOT_TOKEN=$BOT_TOKEN DEVELOPER_KEY=$DEVELOPER_KEY  REDDIT_CLIENT_ID=$REDDIT_CLIENT_ID REDDIT_CLIENT_SECRET=$REDDIT_CLIENT_SECRET REDDIT_USER_AGENT='$REDDIT_USER_AGENT' PG_PASSWORD=$PG_PASSWORD GAG_USERNAME=$GAG_USERNAME GAG_PASSWORD=$GAG_PASSWORD nohup python3.6 -u main.py &

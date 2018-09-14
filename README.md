# python_simpleHealthCheck
Python script for simple Server Health Check

Using cron job to trigger the script on the server
# crontab -e
====================================================================================================

0 * * * * /{path}/{Health Check Script Check}.py >> /{path}/{Health Check Log}-`date +\%Y\%m`.log

====================================================================================================
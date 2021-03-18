# npm-package-download-updates

Deployed an NPM package, and want to keep track of the weekly downloads? Why visit every week, when you can have Telegram notify you when you desire?

Steps to run:
<ol>
  <li>Update the values of <b>TOKEN, PACKAGE_NAME</b> and <b>TELEGRAM_CHAT_ID</b> in <b>npm_updates.py</b>.</li>
  <li>To avoid manually running the code each time, setup a Heroku cron job (Resources > Add-ons > Heroku Scheduler) to automatically send you updates every day / week.</li> 
</ol>

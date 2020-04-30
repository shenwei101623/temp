import logging
import requests
import time
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

token=""
email=""
passwd=""
url="https://n3ro.best/"
my_tg_id=

login_url = '{}/auth/login'.format(url)
checkin_url = '{}/user/checkin'.format(url)
user_url = '{}/user'.format(url)
postDict = {
	'email':email,
	'passwd':passwd
}

requests.packages.urllib3.disable_warnings()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
	update.message.reply_text('你好')


def checkin(update, context):
	if update.message.from_user.id == my_tg_id:
		session = requests.Session()
		r = session.post(login_url, data=postDict, verify=False)
		r = session.post(checkin_url, verify=False)
		data = r.json()
		msg = data['msg'].replace("<br/>","\n")
		print(time.strftime('%Y-%m-%d %H:%M:%S')+":"+msg)
		update.message.reply_text(msg)
	else:
		update.message.reply_text("这是一个私人bot哦")


def traffic(update, context):
	if update.message.from_user.id == my_tg_id:
		session = requests.Session()
		r = session.post(login_url, data=postDict, verify=False)
		r = session.get(user_url, verify=False)
		traffic_used_today = re.findall(r'(?<=<code class="card-tag tag-red">)([-]?[0-9]+(\.[0-9]+)?(K|M|G|T)?B)(?=</code>)', r.text)
		traffic_used_today = traffic_used_today[0][0]
		traffic_used_past = re.findall(r'(?<=<code class="card-tag tag-orange">)([-]?[0-9]+(\.[0-9]+)?(K|M|G|T)?B)(?=</code>)', r.text)
		traffic_used_past = traffic_used_past[0][0]
		traffic_remained = re.findall(r'(?<=<code class="card-tag tag-green" id="remain">)([-]?[0-9]+(\.[0-9]+)?(K|M|G|T)?B)(?=</code>)', r.text)
		traffic_remained = traffic_remained[0][0]
		traffic_msg = "今日已用：" + traffic_used_today + "\n" + "过去已用：" + traffic_used_past + "\n" + "剩余流量：" + traffic_remained
		print(time.strftime('%Y-%m-%d %H:%M:%S')+":"+traffic_msg)
		update.message.reply_text(traffic_msg)
	else:
		update.message.reply_text("这是一个私人bot哦")



def echo(update, context):
	update.message.reply_text(update.message.text)



def error(update, context):
	update.message.reply_text("遇到了奇怪的bug")
	logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
	updater = Updater(token, use_context=True)

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("checkin", checkin))
	dp.add_handler(CommandHandler("traffic", traffic))

	dp.add_handler(MessageHandler(Filters.text, echo))

	dp.add_error_handler(error)

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()

import config as c
import datetime
import os
import requests
import time


chat_id = os.getenv('CHAT_ID', c.chat_id)
string = os.getenv('STRING', c.string)
token = os.getenv('TOKEN', c.token)
url = os.getenv('URL', c.url)


class CheckUrl:

    def __init__(self):
        self.timeout = 60
        self.last_msg_date = None

    def send_msg(self, msg):
        if self.last_msg_date:
            curr_time = datetime.datetime.now()
            diff_time = (curr_time - self.last_msg_date).total_seconds()
            if diff_time < self.timeout:
                # Пропуск. Предыдущее сообщение было раньше минуты назад
                return
        data = {'chat_id': chat_id, 'text': msg}
        with requests.post('https://api.telegram.org/bot{token}/{method}'.format(token=token, method='sendMessage'), data=data) as r:
            self.last_msg_date = datetime.datetime.fromtimestamp(
                r.json()['result']['date'])

    def check(self):
        # -----------  Startup  -----------
        self.send_msg('Monitoring up')

        # -----------  Checking  -----------
        while True:
            with requests.get(url) as r:
                if r.text != string:
                    self.send_msg('"{url}" is broken. "{string}" not found'.format(
                        url=url, string=string))
            time.sleep(1)

check_url = CheckUrl()
check_url.check()

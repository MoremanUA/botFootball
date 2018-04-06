import datetime, sys, re, requests, os
from flask import Flask

app = Flask(__name__)

class BotHandler:
    def __init__(self):
        self.token = '465043467:AAFKMMkS7BZ5GF8x1-D0AZUCiUubqegGeRk'
        self.api_url = "https://api.telegram.org/bot{}/".format(self.token)
        self.list = []

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text, mode = False):
        params = {'chat_id': chat_id, 'text': text}
        if mode:
            params.update({"parse_mode":"Markdown"})
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def send_stickers(self, chat_id, stick):
        params = {'chat_id': chat_id, 'sticker': stick}
        method = 'sendSticker'
        resp = requests.post(self.api_url + method, params)

    def getSticker(self,text):
        if text == 'футбола нет':
            res = 'CAADAgADAgQAAhmGAwABdyWcY6kAAYt8Ag'
        else:
            res = 'CAADAgADAgQAAhmGAwABdyWcY6kAAYt8Ag'
        return res

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = False

        return last_update
    def showList(self):
        res = ''
        k = 1
        if len(self.list)!= 0:
            for i in self.list:
                res = res+str(k)+'.'+i+'\n\r'
                k=k+1
        else: res = 'Пусто!'
        return res
        

    def search_command(self, comm, name=None):
        if comm == 'help':
            res = 'Все команды начинаются c */*\n\r1.*help* - список доступных команд\n\r2.*list* - показать список игроков \n\r3.*clear* - очичтить список \n\r\
4. *+* - добавить себя в список\n\r5.*+*_name_ - добавить в список имя(_name_)'
            return res
        elif re.match('\+', comm):
            if len(comm.strip()) == 1:
                self.list.append(name)
            else:
                self.list.append(comm[1:])
            res = self.showList()
            return res
        elif re.match('-\d', comm):
            if 0<int(comm[1:])<=len(self.list):
                self.list.pop(int(comm[1:])-1)
                res = self.showList()            
            else:
                res = 'Нет такого номера'
            return res
        elif comm == 'clear':
            self.list.clear()
            res = 'Список пуст'
            return res
        elif comm == 'list':
            res = self.showList()
            return res
            
        else:
            return False
            
@app.route('/')
def index():
    return '<h1>Hellou world</h1>'

def main():
    greet_bot = BotHandler()
    new_offset=None
    while True:
            greet_bot.get_updates(new_offset)
            last_update = greet_bot.get_last_update()
            if last_update:
                last_update_id = last_update['update_id']
                message = last_update['message']
                last_chat_text = message.get('text', 'none')
                chat = message['chat']
                sticker = message.get('sticker','none')
                if sticker != 'none':
                    print(sticker['file_id'])
                last_chat_id = chat['id']
                last_chat_name = chat.get('first_name','none')
                if last_chat_name == 'none':
                    last_chat_name = message['from']['first_name']
                if re.match("\/",last_chat_text):
                    res = greet_bot.search_command(last_chat_text[1:], last_chat_name)
                    if res:
                        greet_bot.send_message(last_chat_id, res,True)
                    else:
                        stick = greet_bot.getSticker(last_chat_text[1:])
                        greet_bot.send_stickers(last_chat_id, stick)
                new_offset = last_update_id + 1
                
if __name__ == '__main__':
    try:
        #main()
        app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    except KeyboardInterrupt:
        exit()

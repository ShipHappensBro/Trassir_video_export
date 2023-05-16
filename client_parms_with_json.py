import socket
import json
import requests
import os.path
from datetime import datetime
start=datetime.now()

class main():

    def parms(self):
        with open('parms.json','r',encoding='utf-8') as parms:
            json_data=json.load(parms)
            for elements in json_data:
                self.name=elements['name']
                self.year_start=int(elements['year_to_start'])
                self.mounth_to_start=int(elements['mounth_to_start'])
                self.day_to_start=int(elements['day_to_start'])
                self.hour_to_start=int(elements['hour_to_start'])
                self.minute_to_start=int(elements['minute_to_start'])
                self.year_to_end=int(elements['year_to_end'])
                self.mounth_to_end=int(elements['mounth_to_end'])
                self.day_to_end=int(elements['day_to_end'])
                self.hour_to_end=int(elements['hour_to_end'])
                self.minute_to_end=int(elements['hour_to_end'])
                self.duration=(elements['duration'])

    def urljson(self):
        urls=[
              '10.17.2.60',
              '10.17.2.62',
              '10.17.2.63',
              '10.17.2.64',
              '10.17.2.65',
              '10.17.2.66',
              '10.17.2.67',
              '10.17.2.68',
              '10.17.2.89',
              '10.17.2.93',
              '10.17.2.96', #Вписать адреса регистраторов
              ]
        postfix=':8080/objects/?password=' #Добавить пароль
        prefix='https://'
        if not os.path.exists('urls'):
            os.mkdir('urls')
        for elements in urls:
            full_addr=prefix+elements+postfix
            with open(f'urls\\{elements}.json',"w+",encoding='utf-8') as file:
                response=requests.get(full_addr,verify=False)
                json.dump(response.json(),file,ensure_ascii=False,indent=8,)


    def takeguid(self):
        global server_guid,channel_guid
        with os.scandir('urls') as it:
            for entry in it:
                if entry.name.endswith('.json'):
                    with open(entry,'r',encoding='utf-8') as file:
                        json_data=json.load(file)
                        for channel_name in json_data:
                            if self.name==channel_name['name']:
                                channel_guid=(channel_name['guid'])
                                for server_name in json_data:
                                    if 'Server' in server_name['class']:
                                        server_guid=(server_name['guid'])
                                        print(f'Имя камеры: "{self.name}"')
                                        print(f"ID Канала:'{channel_guid}'")
                                        print(f"ID Сервера:'{server_guid}'")
                                        print(f"Имя файла:'{file.name}'\n")
    def send_guid(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 10000)
        

        info=[
            {
            'server_guid':server_guid,
            'channel_guid':channel_guid,
            'duration':self.duration,
            'year_to_start':self.year_start,
            'mounth_to_start':self.mounth_to_start,
            'day_to_start':self.day_to_start,
            'hour_to_start':self.hour_to_start,
            'minute_to_start':self.minute_to_start,
            'year_to_end':self.year_to_end,
            'mounth_to_end':self.mounth_to_end,
            'day_to_end':self.day_to_end,
            'hour_to_end':self.hour_to_end,
            'minute_to_end':self.minute_to_end
            }
            ]
        
        info_encode=json.dumps(info,indent=2).encode('utf-8')
        
        try:
            sock.connect(server_address)
            print(f'Отправка: {info}\n')
            sock.send(info_encode)
            data = sock.recv(1024)
            print(f'Получено: {data.decode()}\n')
        finally:
            print(f'Закрытие сокета...\n')
            sock.close()

if __name__=='__main__':
    app=main()
    app.parms()
    app.urljson()
    app.takeguid()
    app.send_guid()
    print(f'Время работы: {datetime.now()-start}')


'''
<parameters>
	<company>My Company</company>
	<title>My Script</title>
	<version>1.0</version>
</parameters>
'''

import socket
import datetime
import json
from video_exporter import VideoExporter

dt = datetime.datetime.now() - datetime.timedelta(seconds=15)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
ve = VideoExporter()
ve.cancel_task_with_states = tuple()

print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)

sock.listen(1)

while True:
    print('Ожидание соединения...')
    connection, client_address = sock.accept()
    try:
        print('Подключено к:', client_address)
        while True:
            data = connection.recv(1024)
            if data:
                with open('server_parms.json','wb+') as file:
                    file.write(data)
                with open('server_parms.json','r') as file:
                    json_data=json.load(file)
                    for info in json_data:
                        guid=info['channel_guid']+'_'+info["server_guid"]
                        test=info['time_to_start']
                        year_start=info['year_to_start']
                        mount_start=info['mounth_to_start']
                        day_start=info['day_to_start']
                        hour_start=info['hour_to_start']
                        minute_start=info['minute_to_start']

                        year_end=info['year_to_end']
                        mount_end=info['mounth_to_end']
                        day_end=info['day_to_end']
                        hour_end=info['hour_to_end']
                        minute_end=info['minute_to_end']
                        
                        duration=info['duration']

                        start=datetime.datetime(year_start,
                                                mount_start,
                                                day_start,
                                                hour_start,
                                                minute_start)
                        
                        end=datetime.datetime(year_end,
                                              mount_end,
                                              day_end,
                                              hour_end,
                                              minute_end)
                        
                ve.export(guid,start,end,file_path='path_to_file')
                print(guid)
                print(start)
                print(end)
                print(duration)



                print('Отправка обратно клиенту.')
                connection.sendall(data)
            else:
                print('Нет данных от:', client_address)
                break
               
    finally:
        connection.close()
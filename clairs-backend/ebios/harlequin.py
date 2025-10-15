import requests
import urllib


response=requests.get('https://cyber.gouv.fr/sites/default/files/2018/10/fiches-methodes-ebios_projet.pdf',
             proxies={
                 'http': 'http://myusername:mypassword@10.20.30.40:8080',
                 'https': 'http://myusername:mypassword@10.20.30.40:8080'
             },
             verify=False)

file_Path = 'fiches-methodes-ebios_projet.pdf'

if response.status_code == 200:
    with open(file_Path, 'wb') as file:
        file.write(response.content)
    print('erm : File downloaded successfully')
else:
    print('erm : Failed to download file')

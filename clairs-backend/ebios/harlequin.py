import requests
url = 'https://cyber.gouv.fr/sites/default/files/2018/10/fiches-methodes-ebios_projet.pdf'

response = requests.get(url)
file_Path = 'research_Paper_1.pdf'

if response.status_code == 200:
    with open(file_Path, 'wb') as file:
        file.write(response.content)
    print('ebios : File downloaded successfully')
else:
    print('ebios : Failed to download file')

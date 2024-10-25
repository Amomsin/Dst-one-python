import requests

url = 'http://localhost:3000/data'
data = {
    'name': 'John Doe',
    'message': 'Hello from Python!'
}

response = requests.post(url, json=data)
print('Response from Node.js:', response.text)
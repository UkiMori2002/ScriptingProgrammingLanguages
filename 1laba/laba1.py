import requests

def task_one():
    data = requests.get('https://jsonplaceholder.typicode.com/posts')
    data = data.json()
    for i in range(len(data)):
        if i % 2 != 0:
            print(data[i])


def task_two():
    data = {
        'id': '100',
        'title': 'Тестовый пост',
        'body': 'Повар спрашивает повара: \n- Какова твоя профессия? Ты милиционер? \n- Нееет! \n- отвечает повар, \n- моя главная профессия - пооовар! \nА твоя, наверное, врач? \n- Нееет! \nЯ пооовар!'.encode('utf-8').decode('utf-8'),
        'userId': '1'
    }
    post = requests.post('https://jsonplaceholder.typicode.com/posts', json=data)
    print(post.json())


# не возможно обновить 101 элемент так как он создается фальшивым, поэтому обновляем 100 пост
def task_three():
    data = {
        'id': '100',
        'title': 'Обновлённый тестовый пост',
        'body': 'курлык',
        'userId': '1'
    }
    put = requests.put('https://jsonplaceholder.typicode.com/posts/100', json=data)
    print(put.json())


task_one()
task_two()
task_three()

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
# Create your views here.

tags = ['Java', 'Python', 'HTML', 'CSS', 'Bootstrap', 'Ubuntu']

QUESTIONS = [
        {
            'id': i,
            'title': f'Question {i}',
            'content': f'Long lorem ipsum {i}',
            'like': i % 10,
            'tags': {
                'tag_1': tags[i % 6],
                'tag_2': tags[(i + 1) % 6],
                'tag_3': tags[(i + 2) % 6],
            }
        } for i in range(45)
]

pop_tags = [
    {
        'tag': tags[i % 6]
    } for i in range(6)
]

answers = [
    {
        'like': i,
        'content': f'Answer {i}',
        'correct': False,
    } for i in range(15)
]
new_answers = sorted(answers, key=lambda d: d['like'])
new_answers.reverse()
new_answers[0]['correct'] = True

newlist = sorted(QUESTIONS, key=lambda d: d['like'])
newlist.reverse()


def paginate(request, objects, page_namber, per_page=10):
    page = request.GET.get('page', page_namber)  # получаем параметр page из request или автоматом делаем равным 1
    paginator = Paginator(objects, 10)
    return paginator.page(page)
def index(request, page_number=1):
    return render(request, 'index.html', {'objects': paginate(request, QUESTIONS, page_number), 'pop_tags': pop_tags})

def hot(request, page_number=1):
    return render(request, 'index.html', {'objects': paginate(request, newlist, page_number), 'pop_tags': pop_tags})

def question(request, question_id, page_number=1):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item, 'pop_tags': pop_tags, 'objects': paginate(request, new_answers, page_number)})

def ask(request):
    return render(request, 'ask.html', {'pop_tags': pop_tags})

def login(request):
    return render(request, 'login.html', {'pop_tags': pop_tags})

def signup(request):
    return render(request, 'register.html', {'pop_tags': pop_tags})

def profile(request):
    return render(request, 'profile.html', {'pop_tags': pop_tags})

def popular_tags(request, tag = '', page_number=1):
    new_question = []
    for i in range(len(QUESTIONS)):
        if QUESTIONS[i]['tags']['tag_1'] == tag or QUESTIONS[i]['tags']['tag_2'] == tag or QUESTIONS[i]['tags']['tag_3'] == tag:
            new_question.append(
                {
                    'id': i,
                    'title': f'Question {i}',
                    'content': f'Long lorem ipsum {i}',
                    'tags': QUESTIONS[i]['tags'],
                    'like': QUESTIONS[i]['like']
                }
            )
    return render(request, 'index.html', {'objects': paginate(request, new_question, page_number), 'pop_tags': pop_tags})
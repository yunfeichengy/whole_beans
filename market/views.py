from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.html import escape
from django.utils import timezone
from market.models import *

# Create your views here.

"""
view take in a 'request' as a parameter
view must return an HttpResponse object
"""

def index(request):
    return HttpResponse('<h1>Hello World</h1>')


def index2(request):
    return HttpResponse('<h1>matched "/test" </h1>')


def add_question(request):
    context = {}
    if request.method == 'POST':
        text = escape(request.POST['question'])  # we get the question from request.POST. escape the input
        # create q, an entry in the Question model
        q = Question(
         question_text=text,
         pub_date = timezone.now())
        q.save()  # this line makes changes to the database
        Choice(question=q, choice_text='Yes').save()
        Choice(question=q, choice_text='No').save()
        context['question_text'] = text
    return render(request, 'market/add_question.html', context)


# list all questions in database
def list_questions(request):
    questions = []
    # Question.objects.all() returns an object that you can iterate. can loop through all entries of the Question table
    for q in Question.objects.all():
        questions.append({
          'question_text': q.question_text,  # can access properties of object q like so
          # timezone.localtime converts time to the time in settings. isoformat is just one of the time formats
          'pub_date': timezone.localtime(q.pub_date).isoformat()
        })
    context = {'questions': questions}
    return render(request, 'market/list_questions.html', context)


# list questions that allows user to vote
def list_questions2(request):
    questions = Question.objects.all().order_by('-pub_date')
    context = {'questions': questions}
    return render(request, 'market/list_questions2.html', context)


def vote(request, question_id=None):
    questions = Question.objects.filter(id=question_id)
    if not questions:
        # Use 404 status code instead of 200
        return HttpResponseNotFound('<h1>Page not found</h1>')
    question = questions[0]
    context = {'question': question}

    if request.method == 'POST':
        if 'choice' in request.POST:
            choices = Choice.objects.filter(
                id=int(request.POST['choice'])
            )
            choice = choices[0]
            choice.votes += 1
            choice.save()
            redirect_url = reverse('list_question2')
            return HttpResponseRedirect(redirect_url)
        context['error_message'] = 'You must select a choice'

    return render(request, 'market/vote.html', context)


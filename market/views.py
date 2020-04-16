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

        # create yes and no Choice tables pointing to the same q. save them
        Choice(question=q, choice_text='Yes').save()
        Choice(question=q, choice_text='No').save()

        # set a value for the context dictionary for use in add_question.html
        context['question_text'] = text

    # first thing to render is always the request. then the path.
    # then a dictionary such that keys in dictionary becomes variables in a template.
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


# list questions that allows user to vote. links to voting each question
def list_questions2(request):
    questions = Question.objects.all().order_by('-pub_date')  # - means reorder in descending order
    context = {'questions': questions}
    return render(request, 'market/list_questions2.html', context)


# page for users to vote yes or no
# notice it takes an input question_id that was captured in url by urls.py
def vote(request, question_id=None):
    # use question_id as the primary key when looking for the Question of interest
    questions = Question.objects.filter(id=question_id)  # filter returns query set that satisfies the given criteria
    # since we use primary key, the returned query set has size of one or zero
    if not questions:  # this is how you check if query set has any records
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
            redirect_url = reverse('list_question2')  # redirects to /market/list2
            return HttpResponseRedirect(redirect_url)

        # if not POST request, set context to error_message
        context['error_message'] = 'You must select a choice'

    return render(request, 'market/vote.html', context)


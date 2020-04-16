from django.urls import path, re_path

import market.views

urlpatterns = [

    # this matches with the url "http://localhost:8000/market/". notice after "market/" is an empty string
    # then, the "index" function in view.py will handle stuff
    path('', market.views.index, name='index'),

    # matched "http://localhost:8000/market/test". the index2 function is called
    path('test', market.views.index2, name='index2'),

    # name is used to uniquely identify a path


    path('add', market.views.add_question),
    path('list', market.views.list_questions, name='list_question'),

    path('list2', market.views.list_questions2, name='list_question2'),
    path('<int:question_id>/vote', market.views.vote, name='vote')
]
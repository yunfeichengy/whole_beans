from django.urls import path, re_path

import market.views

urlpatterns = [

    # this matches with the url "http://localhost:8000/market/". notice after "market/" is an empty string
    # then, the "index" function in view.py will handle stuff
    path('', market.views.index, name='index'),

    # matched "http://localhost:8000/market/test". the index2 function is called
    path('test', market.views.index2, name='index2')




    # path('add', polls.views.add_question),
    # path('list', polls.views.list_questions, name='list_question'),
    #
    # path('list2', polls.views.list_questions2, name='list_question2'),
    # path('<int:question_id>/vote', polls.views.vote, name='vote')
]
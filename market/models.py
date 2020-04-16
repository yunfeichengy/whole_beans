from django.db import models

# Create your models here.

# model is a class that corresponds to a database table

# by default, all tables will have a primary key column called id which will have auto_increment enabled


# database 1
class Question(models.Model):
    question_text = models.CharField(max_length=200)  # string attribute. question_text is the name of this column
    pub_date = models.DateTimeField('date published')  # time attribute.  'date published' is just a human-readable name

    def __str__(self):
        return self.question_text


# database 2
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # foreign key pointing to primary key of Question.
    # cascade means delete corresponding entries in Choice as well. another option is models.SET_NULL
    choice_text = models.CharField(max_length=200)  # string attribute
    votes = models.IntegerField(default=0)  # string attribute

    def __str__(self):
        return self.choice_text


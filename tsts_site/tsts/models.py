import math
import random
from random import randint

from django.db import models
from django.db.models import Count, Max


class Question(models.Model):
    question = models.CharField('Вопрос', max_length=200)
    image = models.ImageField('Изображение', upload_to='question/', blank=True)
    right_answer = models.IntegerField("ID правильного ответа", default=0)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question


def random_object():
    count = Question.objects.aggregate(count=Count('id'))['count']
    random_index = randint(0, count - 1)
    return Question.objects.all()[random_index]


def get_random_item(model, max_id=None):
    if max_id is None:
        max_id = model.objects.aggregate(max_id=Max('id'))['max_id']
    min_id = math.ceil(max_id * random.random())
    return model.objects.filter(id__gte=min_id)[0]


# def random_list():
#     randomlist = []
#     for i in range(3):
#         rnd_object = get_random_item(Question)
#         # rnd_object = random_object()
#         if rnd_object:
#             randomlist.append(rnd_object)
#     return randomlist

def random_list(model, count):
    count_objects = model.objects.aggregate(count=Count('id'))['count']
    object_list = []
    if count >= count_objects:
        object_list = list(model.objects.all())
        random.shuffle(object_list)
    else:
        while len(object_list) < count:
            random_index = randint(0, count_objects - 1)
            random_item = model.objects.all()[random_index]
            if random_item in object_list:
                continue
            else:
                object_list.append(random_item)
    return object_list


class Answer(models.Model):
    answer = models.CharField('Ответ', max_length=200)
    image = models.ImageField('Изображение', upload_to='answer/', blank=True)
    question = models.ForeignKey(
        Question, verbose_name="Вопрос", on_delete=models.CASCADE,
        related_name='answers'
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return '#id {}'.format(self.id)


class T(models.Model):
    t_date = models.DateTimeField('Время', auto_now_add=True)
    status = models.BooleanField('Статус', default=False)
    questions = models.ManyToManyField(Question, through='T_Result')

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def save(self, *args, **kwargs):
        new_t = False
        if not self.pk:
            new_t = True
        super().save(*args, **kwargs)
        if new_t:
            question_list = random_list(Question, 3)
            for item in question_list:
                if item.answers.all().count() > 0:
                    self.questions.add(item, through_defaults={'answered': False, 'right_answered': False,
                                                               'answered_id': 0})

    def t_close(self):
        self.status = True
        self.save()
        return self

    def next_prev_question(self, question_id):
        question_list = [question_t_result.question.id for question_t_result in
                         self.t_result_set.order_by('id').all()]
        next_question_id = None
        prev_question_id = None
        if question_id in question_list:
            question_index = question_list.index(question_id)
            if (question_index + 1) < len(question_list):
                next_question_id = question_list[question_index + 1]
            if question_index > 0:
                prev_question_id = question_list[question_index - 1]
        return {'next_question_id': next_question_id, 'prev_question_id': prev_question_id}

    def __str__(self):
        return '#id {}'.format(self.id)


class T_Result(models.Model):
    t = models.ForeignKey(T, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    right_answered = models.BooleanField(default=False)
    answered_id = models.IntegerField(default=0)
    answered = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Статус ответа"
        verbose_name_plural = "Статусы ответов "

    def __str__(self):
        return '#id {}'.format(self.id)

    def t_question_answered(self, answer_id):
        self.right_answered = answer_id == self.question.right_answer
        self.answered = True
        self.answered_id = answer_id
        self.save()
        return self

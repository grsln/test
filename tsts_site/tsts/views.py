from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import QuestionSerializer, AnswerSerializer, TSerializer, TResultSerializer
from .models import Question, T, T_Result, Answer


@login_required
def index(request):
    return render(request, 'tsts/index.html')


@login_required
def tstng(request):
    new_tst = T.objects.create(t_date=timezone.now(), status=False)
    first_question = new_tst.t_result_set.order_by('id').first()
    if first_question:
        question = first_question.question
        return HttpResponseRedirect(reverse('tsts:tst_questions', args=(new_tst.id, question.id,)))
    else:
        return HttpResponse("В тесте нет вопросов.")


class TstContextMixin:
    def get_context_data(self, **kwargs):
        context = super(TstContextMixin, self).get_context_data(**kwargs)
        next_prev = self.object.next_prev_question(self.kwargs['question_id'])
        context['next_question_id'] = next_prev['next_question_id']
        context['prev_question_id'] = next_prev['prev_question_id']
        context['question'] = get_object_or_404(Question, pk=self.kwargs['question_id'])
        question_result = get_object_or_404(T_Result, t=self.object, question=self.kwargs['question_id'])
        context['question_result'] = question_result
        self.template_name = 'tsts/tstng.html'
        if question_result.answered or self.object.status:
            context['answer_id'] = question_result.answered_id
            self.template_name = 'tsts/answer_result.html'
        return context


class TstQuestionView(LoginRequiredMixin, TstContextMixin, DetailView):
    model = T
    context_object_name = "tst_item"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        question_result = context['question_result']
        try:
            answer_id = int(request.POST['choice'])
        except (KeyError):
            context['error_message'] = 'Не выбран вариант ответа.'
        else:
            question_result.t_question_answered(answer_id)
            context['answer_id'] = answer_id
            self.template_name = 'tsts/answer_result.html'
        return render(request, template_name=self.template_name, context=context)


class TstQuitView(LoginRequiredMixin, DetailView):
    template_name = "tsts/quit.html"
    model = T
    context_object_name = "tst_item"

    def get_context_data(self, **kwargs):
        context = super(TstQuitView, self).get_context_data(**kwargs)
        tst_item = self.object.t_close()
        context['questions_count'] = tst_item.questions.all().count()
        context['right_answer_count'] = tst_item.t_result_set.filter(right_answered=True).count
        return context


class TResultView(APIView):
    def get(self, request, pk):
        t_result = T_Result.objects.filter(pk=pk)
        serializer = TResultSerializer(t_result, many=True)
        return Response({"t_result": serializer.data})


class AnswerView(APIView):
    def get(self, request, pk):
        answer = Answer.objects.filter(pk=pk)
        serializer = AnswerSerializer(answer, many=True)
        return Response({"answer": serializer.data})


class QuestionView(APIView):
    def get(self, request, pk):
        question = Question.objects.filter(pk=pk)
        serializer = QuestionSerializer(question, many=True)
        return Response({"question": serializer.data})


class QuestionAnswersView(APIView):
    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        question_answers = question.answers.all()
        serializer = AnswerSerializer(question_answers, many=True)
        return Response({"question_answers": serializer.data})


class TView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        t = T.objects.get(pk=pk)
        serializer = TSerializer(t, many=False)
        return Response({"T": serializer.data})

    def put(self, request, pk):
        saved_t = get_object_or_404(T.objects.all(), pk=pk)
        if not saved_t.status:
            request_t = request.data.get('T')
            answers_list = request_t['t_result']
            for answers_item in answers_list:
                t_result_item = saved_t.t_result_set.get(id=answers_item['id'])
                serializer = TResultSerializer(instance=t_result_item, data=answers_item, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    t_result_item.t_question_answered(answer_id=answers_item['answered_id'])
            saved_t.status = True
            saved_t.save()
            return Response({"success": "Test save successfully"})
        return Response({"error": "Test was saved"})


class TCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        t = T.objects.create(t_date=timezone.now(), status=False)
        serializer = TSerializer(t, many=False)
        return Response({"T": serializer.data})

# class TView(RetrieveUpdateAPIView):
#     queryset = T.objects.all()
#     serializer_class = TSerializer

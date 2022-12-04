from django.http import HttpResponse
from django.views import generic
from .models import Survey


class SurveysListView(generic.ListView):
    model = Survey
    template_name = 'surveys/surveys_list.html'
    context_object_name = 'surveys_list'
    queryset = Survey.objects.all()


class SurveyDetailView(generic.DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'

    def post(self, request, *args, **kwargs):
        survey = self.get_object()
        correct_answers = 0
        number_of_questions = survey.questions.count()

        for question in survey.questions.all():

            answers = []
            for answer in question.answer_options.filter(correct=True):
                answers.append(answer.text)

            if answers == request.POST.getlist(f'{question}'):
                correct_answers += 1

        if correct_answers / number_of_questions >= 0.6:
            user = request.user
            user.profile.balance += survey.price
            user.profile.save()

            return HttpResponse(f'<h1> You have successfully completed the survey. '
                                f'Get {survey.price} for it</h1>'
                                f'<a href="/">Main page</a>')
        else:
            return HttpResponse(f'<h1> Too many mistakes </h1> <a href="/{survey.id}">Try again</a>')

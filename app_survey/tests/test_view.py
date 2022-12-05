from django.test import TestCase
from app_survey.models import Survey, Question, AnswerOption
from django.contrib.auth.models import User
from django.urls import reverse


class MainPageTest(TestCase):
    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'surveys/surveys_list.html')


class SurveyPageTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_admin')
        self.user.set_password('pass@123')
        self.user.save()
        self.survey = Survey.objects.create(title='test_survey', price=50)
        self.question = Question.objects.create(text='test?', survey=self.survey)
        self.answer_option_1 = AnswerOption.objects.create(text='true_answer',
                                                           question=self.question,
                                                           correct=True)
        self.answer_option_2 = AnswerOption.objects.create(text='false_answer',
                                                           question=self.question,
                                                           correct=False)

    def test_survey_page(self):
        response = self.client.get(reverse('survey_detail', kwargs={'pk': self.survey.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'surveys/survey_detail.html')

    def test_survey_true_answer(self):
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.post(reverse('survey_detail', kwargs={'pk': self.survey.pk}),
                                    {'test?': 'true_answer'})
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.balance, 50)

    def test_survey_true_answer(self):
        self.client.login(username='test_admin', password='pass@123')
        response = self.client.post(reverse('survey_detail', kwargs={'pk': self.survey.pk}),
                                    {'test?': 'false_answer'})
        self.assertEqual(response.status_code, 200)
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.balance, 0)

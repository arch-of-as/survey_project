from django.db import models
from django.utils.translation import gettext_lazy as _


class Survey(models.Model):
    title = models.CharField(max_length=30, verbose_name=_('title'))
    price = models.IntegerField(default=100, verbose_name=_('price'))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name_plural = _('surveys')
        verbose_name = _('survey')


class Question(models.Model):
    text = models.CharField(max_length=70, verbose_name=_('text'))
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name=_('survey'), related_name='questions')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name_plural = _('questions')
        verbose_name = _('question')


class AnswerOption(models.Model):
    text = models.CharField(max_length=30, verbose_name=_('text'))
    correct = models.BooleanField(default=False, verbose_name=_('correct'))
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name=_('question'),
                                 related_name='answer_options')

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name_plural = _('answer options')
        verbose_name = _('answer option')

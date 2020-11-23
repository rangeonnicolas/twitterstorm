from django.db import models


class SentPlannedMessage(models.Model):
    campain_id = models.CharField(max_length=50)
    planned_message_id = models.CharField(max_length=50)
    sent_at = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo : a transformer en foreign key quand on pourra
    sent_text = models.TextField()


class PostedTweet(models.Model):
    campain_id = models.CharField(max_length=50)
    url = models.CharField(
        max_length=300)  # todo: vu que l'url est clé primaire théorique, faire une normalisation d'url
    date_received = models.DateTimeField()
    sender_id = models.CharField(max_length=50)  # todo : a transformer en foreign key quand on pourra
    sender_name = models.CharField(max_length=100)  # todo : à jater quand la foreign key sera faite


class SentTweetUrl(models.Model):
    campain_id = models.CharField(max_length=50)
    url = models.CharField(max_length=300)
    date_sent = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo : a transformer en foreign key quand on pourra


class SentTextSuggestion(models.Model):
    campain_id = models.CharField(max_length=50)
    text_id = models.CharField(max_length=50)
    sent_at = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo : a transformer en foreign key quand on pourra
    sent_text = models.TextField()

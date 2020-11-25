from django.db import models


class SentPlannedMessage(models.Model):
    campain_id = models.CharField(max_length=50)
    planned_message_id = models.CharField(max_length=50)
    sent_at = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo_es : a transformer en foreign key quand on pourra
    sent_text = models.TextField()


class PostedTweet(models.Model):
    campain_id = models.CharField(max_length=50)
    url = models.CharField(
        max_length=300)
    date_received = models.DateTimeField()
    sender_id = models.CharField(max_length=50)  # todo_es : a transformer en foreign key quand on pourra
    sender_name = models.CharField(max_length=100)  # todo_es : à jater quand la foreign key sera faite


class SentTweetUrl(models.Model):
    campain_id = models.CharField(max_length=50)
    url = models.CharField(max_length=300)
    date_sent = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo_es : a transformer en foreign key quand on pourra


class SentTextSuggestion(models.Model):
    campain_id = models.CharField(max_length=50)
    text_id = models.CharField(max_length=50)
    sent_at = models.DateTimeField()
    receiver_id = models.CharField(max_length=50)  # todo_es : a transformer en foreign key quand on pourra
    sent_text = models.TextField()

# todo_es : il faudrait grouper tout  ça en un unique table "role" car les rôles ne sont pas cumulables
class ConfigParticicipantlist(models.Model):
    campain_id = models.CharField(max_length=50)
    participant_id = models.CharField(max_length=50)
    display_name_for_animators = models.CharField(max_length=300, null = True)

class ConfigReachableParticipants(ConfigParticicipantlist):
    pass

class ConfigScribes(ConfigParticicipantlist):
    pass

class ConfigRobotScribes(ConfigParticicipantlist):
    pass

class ConfigAdmins(ConfigParticicipantlist):
    pass

class ConfigVars(models.Model):
    campain_id = models.CharField(max_length=50)
    key = models.CharField(max_length=300)
    value_str = models.TextField(null=True)
    value_float = models.FloatField(null=True)
    value_bool = models.BooleanField(null=True)
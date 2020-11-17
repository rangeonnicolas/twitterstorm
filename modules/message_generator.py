import datetime as dt
import random
import re


class MessageGenerator:

    @staticmethod
    def generate_all_messages(messages, max_length=None):
        final_messages = []
        for message in messages:
            final_messages += [MessageGenerator._generate_all_possibilities(message)]

        final_messages = MessageGenerator._correct_messages(final_messages)
        if max_length:
            final_messages = MessageGenerator._filter_messages(final_messages, max_length)

        return final_messages

    @staticmethod
    def generate_one_message(raw_messages, max_length=None):
        MessageGenerator._random_seed()
        raw_message = random.choice(raw_messages)
        possible_messages = MessageGenerator._generate_all_possibilities(raw_message)
        possible_messages = MessageGenerator._correct_messages([possible_messages])
        if max_length:
            possible_messages = MessageGenerator._filter_messages(possible_messages, max_length)
        try:
            res = random.choice(possible_messages[0])
        except IndexError:
            # todo : signaler à l'utilisateur que c'est la merde
            res = ""
        return res

    @staticmethod
    def _add_a_single_part(alternatives, part):
        result = []
        if len(alternatives) == 0:
            result = [part]
        else:
            for alt in alternatives:
                result += [alt + " " + part]
        return result

    @staticmethod
    def _add_a_multiple_part(alternatives, part):
        choices = []

        for choice in part:
            if type(choice) == str:
                choices += [choice]
            elif type(part) == list:
                choices = choices + MessageGenerator._generate_all_possibilities(choice)
            else:
                print(
                    "La variable MESSAGES est mal formée aux alentours de : " + part +
                    ". Seules les Strings ou les listes sont autorisées")

        result = []

        if len(alternatives) == 0:
            result = [a for a in choices]
        else:
            for alt in alternatives:
                for ch in choices:
                    result += [alt + " " + ch]

        return result

    @staticmethod
    def _generate_all_possibilities(message):
        alternatives = []

        for part in message:
            if type(part) == str:
                alternatives = MessageGenerator._add_a_single_part(alternatives, part)
            elif type(part) == list:
                alternatives = MessageGenerator._add_a_multiple_part(alternatives, part)
            else:
                print(
                    "La variable MESSAGES est mal formée aux alentours de : " + part +
                    ". Seuls les Strings ou les listes sont autorisées")

        return alternatives

    @staticmethod
    def _correct_messages(final_messages):
        result = []
        for m in final_messages:
            tmp = []
            for message in m:
                # delete double spaces
                message = re.sub(r'\s\s+', ' ', message)

                # french typography rules (https://archive.framalibre.org/article2225.html > ponctuation)
                message = re.sub(r'\s,', ',', message)
                message = re.sub(r'\s\.', '.', message)
                message = re.sub(r'\s\'', "'", message)
                message = re.sub(r'\'\s', "'", message)
                tmp += [message]

            result += [tmp]
        return result

    @staticmethod
    def _filter_messages(final_messages, max_length):
        result = []

        for m in final_messages:
            tmp = []
            for message in m:
                if len(message) <= max_length:
                    tmp += [message]
                    result += [tmp]

        return result

    @staticmethod
    def _random_seed():
        a = dt.datetime.now().microsecond
        b = dt.datetime.now().second + 1
        c = dt.datetime.now().microsecond
        return random.seed(a * b * c)

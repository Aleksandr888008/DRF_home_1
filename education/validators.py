from rest_framework import serializers

WORDS_URL = ['https://www.youtube.com/', 'www.youtube.com']


def validator_url(value):
    if value.lower() not in WORDS_URL:
        raise serializers.ValidationError('Ссылка может быть только на youtube')

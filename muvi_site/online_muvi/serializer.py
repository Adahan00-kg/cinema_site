from django.db.models import DateField, DateTimeField
from rest_framework import serializers
from .models import *


from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'status']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user


class MovieListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = ['id','movie_name','janre',
                  'movie_image','status_movie']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id','name','phone_number','status','age']



class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']

class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']




class DirectorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name','bio','age','director_image']



class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name','actor_image']


class ActorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name','bio','age','actor_image']


class JanreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Janre
        fields = ['janre_name']



class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language','video']


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = ['movie','movie_moments']

class RatingSerializer(serializers.ModelSerializer):
    user_rating = ProfileSerializer(many=True,read_only=True)
    created_date = serializers.DateTimeField(format="%d/%m/%Y %H:%M")
    class Meta:
        model = Rating
        fields = ['user_rating','parent','text','created_date']

class FavoriteSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%Y')
    class Meta:
        model = Favorite
        fields = ['user','created_date',]


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = ['cart','movie']

class HistorySerializer(serializers.ModelSerializer):
    viewed_at = serializers.DateField(format='%d-%m-%Y')
    class Meta:
        model = History
        fields = ['user','movie','viewed_at']






class MovieDetailSerializer(serializers.ModelSerializer):
    director = DirectorListSerializer(read_only=True,many=True)
    actor = ActorListSerializer(read_only=True,many=True)
    janre = JanreSerializer(read_only=True)
    country = CountrySerializer(read_only=True)
    movie_rating = RatingSerializer(read_only=True,many=True)
    movie_language = MovieLanguagesSerializer(read_only=True,many=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['movie_name','year','country','director','actor',
                  'janre','types',
                  'movie_time','description','movie_trailer','movie_image',
                  'movie_language',
                  'status_movie','movie_rating','average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()
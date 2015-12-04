# -*- coding: utf-8 -*-

import json
import datetime

from django.template import Context
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from collections import defaultdict
from .models import Exercises, Sets, Categories, Repeats, BodySize
from .myserializer import ExercisesSerializer, SetsByDateSerializer, CategoriesSerializer, RepeatsSerializer, ProfileSerializer, BodySizeSerializer
from .forms import SetForm, RepeatsForm


class Registration(View):
    def post(self, request):
        errors = dict()
        if request.user.is_authenticated():
            errors['auth'] = u'Вы уже авторизованы'
            return HttpResponse(json.dumps(errors), status='403')
        else:
            in_data = json.loads(request.body)
            data = in_data['reg']
            try:
                u = User.objects.create_user(data['name'], data['email'], data['password'])
                u.save()
            except Exception as e:
                errors[type(e)] = e.message
                return HttpResponse(json.dumps(str(errors)), status='404')
            return HttpResponse(status='200')


class LogIn(View):
    def post(self, request):
        errors = {}
        if request.user.is_authenticated():
            errors['auth'] = u'Вы уже авторизованы'
            return HttpResponse(json.dumps(errors), status='403')
        else:
            in_data = json.loads(request.body)
            data = in_data['login']
            print data
            try:
                User.objects.get(username=data['name'])
            except ObjectDoesNotExist:
                errors['error'] = u'Пользователь с таким именем не найден'
                return HttpResponse(json.dumps(errors), status='404')
            user = authenticate(username=data['name'], password=data['password'])
            if user is None:
                errors['error'] = u'Не правильно введен логин или пароль'
                return HttpResponse(json.dumps(errors), status='404')
            login(request, user)
            print 'user authorized!'
            return HttpResponse(json.dumps(user.username), status='200')

    def get(self, request):
        if request.user.is_authenticated():
            print ('Vewis::LogIn->GET->username->', request.user.username)
            return HttpResponse(status='403')
        else:
            return HttpResponse(status='404')


class LogOut(View):
    def post(self, request):
        if request.user.is_authenticated():
            logout(request)
            return HttpResponse(status='200')
        else:
            return HttpResponse(status='403')


class Base(View):
    create_form_class = None
    update_form_class = None
    serializer = None
    model = None
    by_user = None
    return_last_id = None

    def read(self, request):
        if self.object_id:
            return self.get_single_item()
        else:
            return self.get_collection()

    def create(self, request):
        if self.create_form_class is None:
            self.failed_response(405)
        print self.data
        form = self.create_form_class(self.data['add'])
        if form.is_valid():
            instance = form.save(commit=True)
            if self.return_last_id:
                last_set_id = {'set': instance.id}
                return self.success_response(last_set_id)
            else:
                return HttpResponse()
        else:
            self.failed_response(405)

    def update(self, request):
        if self.update_form_class is None or not self.object_id:
            self.failed_response(405)
        try:
            instance = self.get_queryset().get(pk=self.object_id)
        except ObjectDoesNotExist:
            self.failed_response(404)
        form = self.update_form_class(self.data['update'], instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponse()
        else:
            print('form not valid')

    def remove(self, request):
        if not self.object_id:
             self.failed_response(404)
        qs = self.get_queryset().filter(pk=self.object_id)
        qs.delete()
        return HttpResponse()

    # get data from request
    @cached_property
    def data(self):
        _data = {}
        for k in self.request.GET:
            _data[k] = self.request.GET[k]
            print("GET -> {0}".format(_data))
        if self.request.method.upper() == 'POST':
            try:
                data = json.loads(self.request.body)
                print("POST -> {0}".format(data))
            except ValueError:
                pass
            else:
                _data.update(data)
        return Context(_data)

    # get ID from request
    @property
    def object_id(self):
        return self.data.get('id')

    @property
    def category_id(self):
        return self.data.get('category_id')
    
    def get_single_item(self):
        try:
            qs = self.get_queryset().filter(pk=self.object_id)
            assert len(qs) == 1
        except AssertionError:
            return self.failed_response(404)
        out_data = self.serialize_qs(qs)
        print('single item - {0}'.format(out_data))
        return self.success_response(out_data)

    def get_collection(self):
        if self.category_id:
            qs = self.get_queryset().filter(category=self.category_id)
        else:
            qs = self.get_queryset()
        out_data = self.serialize_qs(qs)
        print('collection - {0}'.format(out_data))
        return self.success_response(out_data)

    # get all objects from database
    def get_queryset(self):
        if self.by_user:
            return self.model.objects.all().filter(user=self.request.user.id)
        else:
            return self.model.objects.all()

    # serialize object
    def serialize_qs(self, qs):
        return self.serializer.serialize(qs)

    # success response with data
    def success_response(self, data):
        return HttpResponse(json.dumps(data), status=200, content_type='application/json')

    # failed response with data
    def failed_response(self, status, msg='SYSTEM ERROR!'):
        data = dict()
        data['error'] = msg
        return HttpResponse(json.dumps(data), status=status)


class Main(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['user_id'] = self.request.user.id
        # else:
        #     context['user'] = u'этот гавнюк не авторизован'
        return context


class Exercises(Base):
    model = Exercises
    serializer = ExercisesSerializer()

    def get(self, request):
        return self.read(request)


class Sets(Base):
    model = Sets
    serializer = SetsByDateSerializer()
    create_form_class = SetForm
    update_form_class = SetForm
    by_user = True

    def get(self, request):
        return self.read(request)

    def post(self, request):
        print('obj id -> {0}'.format(self.object_id))
        if self.object_id:
            return self.update(request)
        else:
            self.return_last_id = True
            return self.create(request)

    def delete(self, request):
        return self.remove(request)

    @property
    def date_train(self):
        return self.data.get('date_train')

    @property
    def sets_month(self):
        return self.data.get('month')

    @property
    def sets_year(self):
        return self.data.get('year')

    def get_collection(self):
        if self.date_train:
            qs = self.get_queryset().filter(date=self.date_train)
        else:
            if self.sets_month and self.sets_year:
                qs = self.get_queryset().filter(date__month=self.sets_month, date__year=self.sets_year)
            else:
                qs = self.get_queryset().filter(date__month=get_month(), date__year=get_year())
        data = self.serialize_qs(qs)
        out_data = defaultdict(list)
        for item in data:
            out_data[item["date"]].append(item)
        return self.success_response(out_data)


class Repeats(Base):
    model = Repeats
    serializer = RepeatsSerializer()
    create_form_class = RepeatsForm
    update_form_class = RepeatsForm

    def get(self, request):
        return self.read(request)

    def post(self, request):
        if self.object_id:
            return self.update(request)
        else:
            return self.create(request)

    def delete(self, request):
        return self.remove(request)


class Categories(Base):
    model = Categories
    serializer = CategoriesSerializer()

    def get(self, request):
        return self.read(request)


class AddTraining(Base):
    def post(self, request):
        return self.create(request)

    def create(self, request):
        data_add = self.data['add']
        print data_add
        for data in data_add:
            form_set = SetForm(data)
            if form_set.is_valid():
                instance = form_set.save(commit=True)
                for repeats in data['repeats']:
                    repeats['set'] = instance.id
                    form_repeats = RepeatsForm(repeats)
                    if form_repeats.is_valid():
                        form_repeats.save()
        return HttpResponse()


class Profile(Base):
    model = User
    serializer = ProfileSerializer()

    def get(self, request):
        return self.read(request)

    def get_queryset(self):
        return self.model.objects.all().filter(pk=self.request.user.id)


class BodySizeView(Base):
    model = BodySize
    serializer = BodySizeSerializer()
    by_user = True

    def get(self, request):
        return self.read(request)


class CheckReg(View):
    def post(self, request):
        data = json.loads(request.body)
        for k, v in data.items():
            try:
                if k == 'username':
                    u = User.objects.get(username=v)
                if k == 'email':
                    u = User.objects.get(email=v)
            except ObjectDoesNotExist:
                print v
                return HttpResponse(status='200')
            return HttpResponse(status='404')


class CheckAuth(View):
    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponse(status='200')
        else:
            return HttpResponse(status='401')


def get_month():
    now_date = datetime.date.today()
    return now_date.month

def get_year():
    now_date = datetime.date.today()
    return now_date.year

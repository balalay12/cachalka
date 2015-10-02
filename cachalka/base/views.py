# -*- coding: utf-8 -*-

import json

from django.template import Context
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Exercises, Sets
from .myserializer import ExercisesSerializer, SetSerializer, SetsByDateSerializer

class Registration(View):
    def post(self, request):
        errors = {}
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
                return HttpResponse(json.dumps(errors), status='404')
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
                errors['error'] = u'Пальзователь с таким именем не найден'
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
            # instance.user.add(self.request.user.id)
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
            # TODO: make validation error
            pass

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
        if self.request.method.upper() == 'POST':
            try:
                data = json.loads(self.request.body)
            except ValueError:
                pass
            else:
                _data.update(data)
        print(_data)
        return Context(_data)

    # get ID from request
    @property
    def object_id(self):
        return self.data.get('id')

    def get_single_item(self):
        try:
            qs = self.get_queryset().filter(pk=self.object_id)
            # ne rabotaet
            print 'len %s' % len(qs)
            assert len(qs) == 1
        except AssertionError:
            return self.failed_response(404)
        out_data = self.serialize_qs(qs)
        print out_data
        return self.success_response(out_data)

    def get_collection(self):
        qs = self.get_queryset()
        out_data = self.serialize_qs(qs)
        return self.success_response(out_data)

    # get all objects from database
    def get_queryset(self):
        return self.model.objects.all()

    # serialize object
    def serialize_qs(self, qs):
        return self.serializer.serialize(qs)

    # success response with data
    def success_response(self, data):
        return HttpResponse(json.dumps(data), content_type='application/json')

    # failed response with data
    def failed_response(self, status, msg='SYSTEM ERROR!'):
        data = {}
        data['error'] = msg
        return HttpResponse(json.dumps(data), status=status)


class Main(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            context['user'] = self.request.user.username
        else:
            context['user'] = u'этот гавнюк не авторизован'
        return context


class Exercises(Base):
    model = Exercises
    serializer = ExercisesSerializer()

    def get(self, request):
        return self.read(request)


class Sets(Base):
    model = Sets
    # serializer = SetSerializer()
    serializer = SetsByDateSerializer()

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
        # return HttpResponse(status='404')


class CheckAuth(View):
    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponse(status='200')
        else:
            return HttpResponse(status='401')

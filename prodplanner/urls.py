"""prodplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from planner import viewsets

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'planner/daytemplaterules', viewsets.DayTemplateRuleViewSet)
router.register(r'planner/rulesetelements', viewsets.RuleSetElementViewSet)
router.register(r'planner/rulesets', viewsets.RuleSetViewSet)
router.register(r'planner/baserules', viewsets.BaseRuleViewSet)
router.register(r'planner/daterules', viewsets.DateRuleViewSet)
router.register(r'planner/deltas', viewsets.DeltaViewSet)
router.register(r'planner/schedules', viewsets.ScheduleViewSet)
router.register(r'planner/tasks', viewsets.TaskViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]


# urlpatterns += [
#    url(r'^admin/', admin.site.urls),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('patients', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/records', views.patient_records, name='patient_records'),
    path('patients/<int:patient_id>/medicines', views.patient_medicines, name='patient_medicines'),
    path('medications/mark_given/<int:med_id>', views.mark_medication_given, name='mark_medication_given'),
    path('daily/record', views.daily_record, name='daily_record'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('calendar/events', views.calendar_events, name='calendar_events'),
    path('calendar/events/<str:event_id>/complete', views.complete_event, name='complete_event'),
    path('reports', views.reports_data, name='reports_data'),
]

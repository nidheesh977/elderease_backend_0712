from django.db import models
from datetime import date

class Patient(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    chief_complaint = models.TextField(null=True, blank=True)
    date_of_joining = models.DateField(default=date.today)

    class Meta:
        db_table = 'patient'

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

class Medication(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=20, default="count")
    dose = models.CharField(max_length=100)
    timing = models.CharField(max_length=20, null=True, blank=True)
    food_relation = models.CharField(max_length=20, null=True, blank=True)
    is_given_today = models.BooleanField(default=False)
    given_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'medication'

class DailyRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='daily_records')
    date = models.DateField(default=date.today)
    weight = models.FloatField(null=True, blank=True)
    
    # Keeping both ways for flexibility as per Flask model
    bp_systolic = models.IntegerField(null=True, blank=True)
    bp_diastolic = models.IntegerField(null=True, blank=True)
    bp = models.CharField(max_length=20, null=True, blank=True)
    
    notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'daily_record'
        constraints = [
            models.UniqueConstraint(fields=['patient', 'date'], name='unique_patient_date')
        ]

    def to_dict(self):
        # Prefer combined bp if exists, else fallback to separate
        bp_display = self.bp or (f"{self.bp_systolic}/{self.bp_diastolic}" if self.bp_systolic and self.bp_diastolic else None)
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "date": self.date.isoformat(),
            "weight": self.weight,
            "bp": bp_display,
            "notes": self.notes
        }

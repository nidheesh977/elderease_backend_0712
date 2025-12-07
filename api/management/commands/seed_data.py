from django.core.management.base import BaseCommand
from api.models import Patient, Medication, DailyRecord
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Seeds the database with dummy data'

    def handle(self, *args, **kwargs):
        self.stdout.write("🌱 Seeding dummy data...")

        # Clear existing data
        DailyRecord.objects.all().delete()
        Medication.objects.all().delete()
        Patient.objects.all().delete()

        # Sample Indian patient names
        patient_names = [
            "Ramesh Kumar", "Sita Devi", "Govind Singh", "Lakshmi Bai", 
            "Mohan Lal", "Radha Rani", "Shankar Das", "Kamal Devi",
            "Baldev Singh", "Geeta Joshi", "Arjun Patel", "Sunita Sharma"
        ]
        
        genders = ["Male", "Female"]
        chief_complaints = [
            "Hypertension, Diabetes", "Joint pain, Arthritis", 
            "Chronic cough, Weakness", "Gastric issues, Constipation",
            "Insomnia, Memory issues", "Breathing difficulty",
            "Diabetes, High BP", "Knee pain, Back pain"
        ]
        
        # Sample medications (Ayurvedic + Allopathic)
        medications_list = [
            ("Ashwagandha Tablet", "1 tab", "morning"),
            ("Giloy Juice", "15ml", "morning"),
            ("Amla Juice", "20ml", "morning"),
            ("Triphala Churna", "1 tsp", "night"),
            ("Tulsi Tablet", "1 tab", "morning"),
            ("Amlapitta Syrup", "10ml", "after_food"),
            ("Mahasudarshan Churna", "1 tsp", "before_food"),
            ("Panchsakar Churna", "1 tsp", "night"),
            ("Arogyavardhini Vati", "1 tab", "after_food"),
            ("Laksmivilas Ras", "1 tab", "morning"),
            ("Metformin 500mg", "1 tab", "after_food"),
            ("Amlodipine 5mg", "1 tab", "morning"),
            ("Losartan 50mg", "1 tab", "morning"),
            ("Atorvastatin 10mg", "1 tab", "night")
        ]
        
        # Create 12 patients
        patients = []
        for i in range(12):
            patient = Patient.objects.create(
                name=patient_names[i],
                age=random.randint(65, 92),
                gender=random.choice(genders),
                chief_complaint=random.choice(chief_complaints)
            )
            patients.append(patient)
        
        # Add medications to each patient (2-4 meds each)
        for patient in patients:
            num_meds = random.randint(2, 4)
            for _ in range(num_meds):
                med_name, dose, timing = random.choice(medications_list)
                Medication.objects.create(
                    patient=patient,
                    name=med_name,
                    type="count" if "tab" in dose.lower() or "tsp" in dose.lower() else "ml",
                    dose=dose,
                    timing=timing,
                    food_relation=random.choice(["before_food", "after_food", None])
                )
        
        # Add daily records for last 7 days for some patients
        recent_dates = [date.today() - timedelta(days=x) for x in range(7)]
        
        for patient in patients[:8]:  # First 8 patients
            for date_obj in recent_dates:
                if random.random() > 0.3:  # 70% chance of having record
                    bp_systolic = random.randint(110, 160)
                    bp_diastolic = random.randint(70, 100)
                    DailyRecord.objects.create(
                        patient=patient,
                        date=date_obj,
                        weight=round(random.uniform(55, 85), 1),
                        bp_systolic=bp_systolic,
                        bp_diastolic=bp_diastolic,
                        bp=f"{bp_systolic}/{bp_diastolic}",
                        notes=random.choice([
                            "Patient active, ate well",
                            "Slight headache, BP controlled",
                            "Good appetite, slept well",
                            "Joint pain mild, walking with support",
                            "Feeling better today",
                            "Constipation, advised more water"
                        ])
                    )
        
        # Print summary
        total_patients = Patient.objects.count()
        total_meds = Medication.objects.count()
        total_records = DailyRecord.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f"✅ Seeding completed!"))
        self.stdout.write(f"   📊 {total_patients} patients added")
        self.stdout.write(f"   💊 {total_meds} medications added") 
        self.stdout.write(f"   📋 {total_records} daily records added")

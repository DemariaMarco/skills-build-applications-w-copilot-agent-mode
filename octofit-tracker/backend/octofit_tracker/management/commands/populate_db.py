from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Cancellazione dati esistenti...')
        # Svuota le collezioni direttamente tramite pymongo
        from django.conf import settings
        from pymongo import MongoClient
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'], settings.DATABASES['default']['CLIENT']['port'])
        db = client[settings.DATABASES['default']['NAME']]
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.workouts.delete_many({})
        db.leaderboard.delete_many({})

        self.stdout.write('Creazione team...')
        marvel = Team.objects.create(name='Marvel', description='Team Marvel')
        dc = Team.objects.create(name='DC', description='Team DC')

        self.stdout.write('Creazione utenti...')
        users = [
            User.objects.create(email='ironman@marvel.com', username='Ironman', team=marvel, is_superhero=True),
            User.objects.create(email='spiderman@marvel.com', username='Spiderman', team=marvel, is_superhero=True),
            User.objects.create(email='hulk@marvel.com', username='Hulk', team=marvel, is_superhero=True),
            User.objects.create(email='batman@dc.com', username='Batman', team=dc, is_superhero=True),
            User.objects.create(email='superman@dc.com', username='Superman', team=dc, is_superhero=True),
            User.objects.create(email='flash@dc.com', username='Flash', team=dc, is_superhero=True),
        ]

        self.stdout.write('Creazione attività...')
        Activity.objects.create(user=users[0], type='Corsa', duration=30, date='2024-01-01')
        Activity.objects.create(user=users[1], type='Nuoto', duration=45, date='2024-01-02')
        Activity.objects.create(user=users[2], type='Bici', duration=60, date='2024-01-03')
        Activity.objects.create(user=users[3], type='Corsa', duration=25, date='2024-01-01')
        Activity.objects.create(user=users[4], type='Nuoto', duration=50, date='2024-01-02')
        Activity.objects.create(user=users[5], type='Bici', duration=70, date='2024-01-03')

        self.stdout.write('Creazione workout...')
        w1 = Workout.objects.create(name='Pushups', description='Upper body')
        w2 = Workout.objects.create(name='Squats', description='Lower body')
        w1.suggested_for.set([users[0], users[3]])
        w2.suggested_for.set([users[1], users[4]])

        self.stdout.write('Creazione leaderboard...')
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[2], score=80)
        Leaderboard.objects.create(user=users[3], score=110)
        Leaderboard.objects.create(user=users[4], score=95)
        Leaderboard.objects.create(user=users[5], score=85)

        self.stdout.write(self.style.SUCCESS('Database popolato con dati di test!'))

        # Crea indice univoco su email (solo per MongoDB) tramite pymongo
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Indice univoco su email creato!'))

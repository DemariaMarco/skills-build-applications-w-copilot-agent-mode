from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelSmokeTest(TestCase):
    def test_team_create(self):
        team = Team.objects.create(name='Marvel', description='Team Marvel')
        self.assertEqual(str(team), 'Marvel')
    def test_user_create(self):
        team = Team.objects.create(name='DC', description='Team DC')
        user = User.objects.create(email='batman@dc.com', username='Batman', team=team, is_superhero=True)
        self.assertEqual(str(user), 'Batman')
    def test_activity_create(self):
        team = Team.objects.create(name='Marvel')
        user = User.objects.create(email='spiderman@marvel.com', username='Spiderman', team=team)
        activity = Activity.objects.create(user=user, type='Run', duration=30, date='2024-01-01')
        self.assertEqual(str(activity), 'Spiderman - Run')
    def test_workout_create(self):
        workout = Workout.objects.create(name='Pushups', description='Upper body')
        self.assertEqual(str(workout), 'Pushups')
    def test_leaderboard_create(self):
        team = Team.objects.create(name='Marvel')
        user = User.objects.create(email='ironman@marvel.com', username='Ironman', team=team)
        lb = Leaderboard.objects.create(user=user, score=100)
        self.assertEqual(str(lb), 'Ironman - 100')

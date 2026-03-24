from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import UserProfile
from spotify.models import SpotifyData


class Command(BaseCommand):
    help = 'Populates the database with test users for development'

    def handle(self, *args, **kwargs):

        users_data = [
            {
                'username': 'alice',
                'email': 'alice@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Alice',
                    'bio': 'Indie pop lover and coffee addict ☕',
                    'age': 24,
                    'gender': 'female',
                    'location': 'Manchester',
                    'looking_for': 'romantic',
                    'matching_preference': 'top_artists',
                    'preferred_min_age': 22,
                    'preferred_max_age': 30,
                    'preferred_gender': 'male',
                    'preferred_location': 'Manchester',
                },
                'spotify': {
                    'top_artists': ['Arctic Monkeys', 'Tame Impala', 'The 1975'],
                    'top_genres': ['Indie', 'Alt-Rock', 'Dream Pop'],
                    'top_tracks': [
                        {'name': 'Do I Wanna Know?', 'artist': 'Arctic Monkeys'},
                        {'name': 'The Less I Know The Better', 'artist': 'Tame Impala'},
                    ],
                },
            },
            {
                'username': 'bob',
                'email': 'bob@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Bob',
                    'bio': 'Guitar player, hip-hop head 🎸',
                    'age': 26,
                    'gender': 'male',
                    'location': 'Birmingham',
                    'looking_for': 'both',
                    'matching_preference': 'genre',
                    'preferred_min_age': 20,
                    'preferred_max_age': 30,
                    'preferred_gender': 'female',
                    'preferred_location': 'Birmingham',
                },
                'spotify': {
                    'top_artists': ['Kendrick Lamar', 'Frank Ocean', 'Tyler the Creator'],
                    'top_genres': ['Hip-Hop', 'R&B', 'Neo-Soul'],
                    'top_tracks': [
                        {'name': 'HUMBLE.', 'artist': 'Kendrick Lamar'},
                        {'name': 'Pyramids', 'artist': 'Frank Ocean'},
                    ],
                },
            },
            {
                'username': 'charlie',
                'email': 'charlie@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Charlie',
                    'bio': 'Late night electronic music & early morning runs 🎧',
                    'age': 28,
                    'gender': 'non_binary',
                    'location': 'London',
                    'looking_for': 'platonic',
                    'matching_preference': 'era',
                    'preferred_min_age': 24,
                    'preferred_max_age': 35,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': 'London',
                },
                'spotify': {
                    'top_artists': ['Daft Punk', 'Aphex Twin', 'Four Tet'],
                    'top_genres': ['Electronic', 'IDM', 'House'],
                    'top_tracks': [
                        {'name': 'Get Lucky', 'artist': 'Daft Punk'},
                        {'name': 'Windowlicker', 'artist': 'Aphex Twin'},
                    ],
                },
            },
            {
                'username': 'dana',
                'email': 'dana@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Dana',
                    'bio': 'Classical by day, jazz by night 🎻',
                    'age': 22,
                    'gender': 'female',
                    'location': 'Leeds',
                    'looking_for': 'romantic',
                    'matching_preference': 'opposite_genre',
                    'preferred_min_age': 21,
                    'preferred_max_age': 28,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': 'Leeds',
                },
                'spotify': {
                    'top_artists': ['Miles Davis', 'Bill Evans', 'Chet Baker'],
                    'top_genres': ['Jazz', 'Classical', 'Blues'],
                    'top_tracks': [
                        {'name': 'So What', 'artist': 'Miles Davis'},
                        {'name': 'Waltz for Debby', 'artist': 'Bill Evans'},
                    ],
                },
            },
            {
                'username': 'testuser',
                'email': 'testuser@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Test User',
                    'bio': 'This is the account to log in with for testing.',
                    'age': 25,
                    'gender': 'prefer_not_to_say',
                    'location': 'Anywhere',
                    'looking_for': 'both',
                    'matching_preference': 'top_artists',
                    'preferred_min_age': 18,
                    'preferred_max_age': 40,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': '',
                },
                'spotify': {
                    'top_artists': ['Radiohead', 'Bon Iver', 'Sufjan Stevens'],
                    'top_genres': ['Indie', 'Folk', 'Alternative'],
                    'top_tracks': [
                        {'name': 'Karma Police', 'artist': 'Radiohead'},
                        {'name': 'Skinny Love', 'artist': 'Bon Iver'},
                    ],
                },
            },
        ]

        self.stdout.write('Creating test users...')

        for data in users_data:
            user, created = User.objects.get_or_create(
                username=data['username'],
                defaults={'email': data['email']}
            )

            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created user: {data['username']}"))
            else:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(f"  ~ Already exists, updated password: {data['username']}")

            UserProfile.objects.get_or_create(user=user, defaults=data['profile'])
            SpotifyData.objects.get_or_create(user=user, defaults=data['spotify'])

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('Done! Test accounts ready:'))
        self.stdout.write('  All passwords: testpass123')
        self.stdout.write('  Users: alice, bob, charlie, dana, testuser')
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

            # --- New users with overlapping taste for testing the matching algorithm ---

            # High overlap with testuser (Indie + Folk + shared artists)
            {
                'username': 'elena',
                'email': 'elena@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Elena',
                    'bio': 'Folk festivals and rainy days 🌧️',
                    'age': 24,
                    'gender': 'female',
                    'location': 'Bristol',
                    'looking_for': 'romantic',
                    'matching_preference': 'top_artists',
                    'preferred_min_age': 22,
                    'preferred_max_age': 30,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': 'Bristol',
                },
                'spotify': {
                    'top_artists': ['Bon Iver', 'Sufjan Stevens', 'Fleet Foxes'],
                    'top_genres': ['Folk', 'Indie', 'Chamber Pop'],
                    'top_tracks': [
                        {'name': 'Skinny Love', 'artist': 'Bon Iver'},
                        {'name': 'Chicago', 'artist': 'Sufjan Stevens'},
                    ],
                },
            },

            # Medium overlap with testuser (Indie + Alternative, different artists)
            {
                'username': 'finn',
                'email': 'finn@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Finn',
                    'bio': 'Vinyl collector and part-time dreamer 🎶',
                    'age': 27,
                    'gender': 'male',
                    'location': 'Edinburgh',
                    'looking_for': 'both',
                    'matching_preference': 'genre',
                    'preferred_min_age': 22,
                    'preferred_max_age': 32,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': '',
                },
                'spotify': {
                    'top_artists': ['Radiohead', 'Arcade Fire', 'The National'],
                    'top_genres': ['Alternative', 'Indie', 'Post-Rock'],
                    'top_tracks': [
                        {'name': 'Karma Police', 'artist': 'Radiohead'},
                        {'name': 'Wake Up', 'artist': 'Arcade Fire'},
                    ],
                },
            },

            # High overlap with alice (Indie + Alt-Rock + shared artists)
            {
                'username': 'grace',
                'email': 'grace@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Grace',
                    'bio': 'Arctic Monkeys changed my life 🎸',
                    'age': 23,
                    'gender': 'female',
                    'location': 'Manchester',
                    'looking_for': 'romantic',
                    'matching_preference': 'top_artists',
                    'preferred_min_age': 21,
                    'preferred_max_age': 29,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': 'Manchester',
                },
                'spotify': {
                    'top_artists': ['Arctic Monkeys', 'The 1975', 'Swim Deep'],
                    'top_genres': ['Indie', 'Alt-Rock', 'Britpop'],
                    'top_tracks': [
                        {'name': 'R U Mine?', 'artist': 'Arctic Monkeys'},
                        {'name': 'Somebody Else', 'artist': 'The 1975'},
                    ],
                },
            },

            # High overlap with bob (Hip-Hop + R&B + shared artists)
            {
                'username': 'hassan',
                'email': 'hassan@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Hassan',
                    'bio': 'Hip-hop is poetry 🎤',
                    'age': 25,
                    'gender': 'male',
                    'location': 'Birmingham',
                    'looking_for': 'both',
                    'matching_preference': 'genre',
                    'preferred_min_age': 20,
                    'preferred_max_age': 30,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': '',
                },
                'spotify': {
                    'top_artists': ['Kendrick Lamar', 'J. Cole', 'Frank Ocean'],
                    'top_genres': ['Hip-Hop', 'R&B', 'Conscious Rap'],
                    'top_tracks': [
                        {'name': 'Alright', 'artist': 'Kendrick Lamar'},
                        {'name': 'No Role Modelz', 'artist': 'J. Cole'},
                    ],
                },
            },

            # High overlap with charlie (Electronic + House + shared artists)
            {
                'username': 'iris',
                'email': 'iris@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Iris',
                    'bio': 'Rave culture and ambient soundscapes 🌀',
                    'age': 26,
                    'gender': 'female',
                    'location': 'London',
                    'looking_for': 'platonic',
                    'matching_preference': 'genre',
                    'preferred_min_age': 22,
                    'preferred_max_age': 34,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': 'London',
                },
                'spotify': {
                    'top_artists': ['Four Tet', 'Burial', 'Aphex Twin'],
                    'top_genres': ['Electronic', 'House', 'Ambient'],
                    'top_tracks': [
                        {'name': 'Moth', 'artist': 'Four Tet'},
                        {'name': 'Archangel', 'artist': 'Burial'},
                    ],
                },
            },

            # Low overlap with everyone — used to test that they appear last
            {
                'username': 'jake',
                'email': 'jake@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Jake',
                    'bio': 'Country roads and campfires 🤠',
                    'age': 29,
                    'gender': 'male',
                    'location': 'Cardiff',
                    'looking_for': 'romantic',
                    'matching_preference': 'top_artists',
                    'preferred_min_age': 24,
                    'preferred_max_age': 35,
                    'preferred_gender': 'female',
                    'preferred_location': '',
                },
                'spotify': {
                    'top_artists': ['Johnny Cash', 'Willie Nelson', 'Dolly Parton'],
                    'top_genres': ['Country', 'Americana', 'Bluegrass'],
                    'top_tracks': [
                        {'name': 'Ring of Fire', 'artist': 'Johnny Cash'},
                        {'name': 'On the Road Again', 'artist': 'Willie Nelson'},
                    ],
                },
            },

            # Overlaps with both testuser AND alice (Indie + Alt-Rock + Folk crossover)
            {
                'username': 'kate',
                'email': 'kate@test.com',
                'password': 'testpass123',
                'profile': {
                    'display_name': 'Kate',
                    'bio': 'Genre fluid — from folk to noise rock 🎵',
                    'age': 25,
                    'gender': 'female',
                    'location': 'Glasgow',
                    'looking_for': 'both',
                    'matching_preference': 'top_artists',
                    'preferred_min_age': 22,
                    'preferred_max_age': 32,
                    'preferred_gender': 'prefer_not_to_say',
                    'preferred_location': '',
                },
                'spotify': {
                    'top_artists': ['Radiohead', 'Bon Iver', 'Arctic Monkeys'],
                    'top_genres': ['Indie', 'Alternative', 'Folk'],
                    'top_tracks': [
                        {'name': 'Karma Police', 'artist': 'Radiohead'},
                        {'name': 'Do I Wanna Know?', 'artist': 'Arctic Monkeys'},
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
        self.stdout.write(
            '  Users: alice, bob, charlie, dana, testuser, elena, finn, grace, hassan, iris, jake, kate'
        )
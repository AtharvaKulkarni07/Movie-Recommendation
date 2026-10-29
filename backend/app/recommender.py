import pandas as pd

from app.data_loader import load_movies


class MovieRecommender:

    def __init__(self):
        # Load movie dataset
        self.movies = load_movies()

        # Map movie IDs to their row positions
        self.movie_id_to_index = {
            int(movie_id): index
            for index, movie_id in enumerate(
                self.movies["id"]
            )
        }

        # Genre transition probabilities
        # These are illustrative, manually defined probabilities.
        self.genre_transitions = {
            "Action": {
                "Adventure": 0.35,
                "Thriller": 0.30,
                "Science Fiction": 0.20,
                "Crime": 0.15
            },

            "Adventure": {
                "Fantasy": 0.35,
                "Action": 0.30,
                "Family": 0.20,
                "Science Fiction": 0.15
            },

            "Animation": {
                "Family": 0.40,
                "Comedy": 0.30,
                "Adventure": 0.20,
                "Fantasy": 0.10
            },

            "Comedy": {
                "Romance": 0.35,
                "Family": 0.25,
                "Drama": 0.20,
                "Adventure": 0.20
            },

            "Crime": {
                "Thriller": 0.40,
                "Drama": 0.30,
                "Action": 0.20,
                "Mystery": 0.10
            },

            "Drama": {
                "Romance": 0.30,
                "Crime": 0.25,
                "Thriller": 0.25,
                "History": 0.20
            },

            "Family": {
                "Animation": 0.35,
                "Comedy": 0.30,
                "Adventure": 0.20,
                "Fantasy": 0.15
            },

            "Fantasy": {
                "Adventure": 0.40,
                "Science Fiction": 0.25,
                "Action": 0.20,
                "Family": 0.15
            },

            "Horror": {
                "Thriller": 0.40,
                "Mystery": 0.30,
                "Drama": 0.20,
                "Science Fiction": 0.10
            },

            "Romance": {
                "Comedy": 0.40,
                "Drama": 0.35,
                "Family": 0.15,
                "Music": 0.10
            },

            "Science Fiction": {
                "Adventure": 0.30,
                "Action": 0.30,
                "Thriller": 0.25,
                "Fantasy": 0.15
            },

            "Thriller": {
                "Crime": 0.35,
                "Mystery": 0.30,
                "Action": 0.20,
                "Drama": 0.15
            },

            "Mystery": {
                "Thriller": 0.40,
                "Crime": 0.30,
                "Drama": 0.20,
                "Horror": 0.10
            },

            "History": {
                "Drama": 0.40,
                "War": 0.30,
                "Adventure": 0.20,
                "Romance": 0.10
            },

            "War": {
                "History": 0.35,
                "Drama": 0.35,
                "Action": 0.20,
                "Adventure": 0.10
            },

            "Music": {
                "Romance": 0.30,
                "Drama": 0.30,
                "Comedy": 0.25,
                "Family": 0.15
            },

            "Documentary": {
                "Drama": 0.35,
                "History": 0.30,
                "Music": 0.20,
                "Adventure": 0.15
            },

            "Western": {
                "Action": 0.35,
                "Adventure": 0.30,
                "Drama": 0.25,
                "Crime": 0.10
            }
        }

    def search_movies(self, query, limit=10):
        """Search for movies by title."""

        query = query.strip().lower()

        if not query:
            return []

        matches = self.movies[
            self.movies["title"]
            .str.lower()
            .str.contains(query, regex=False, na=False)
        ].head(limit)

        return [
            {
                "id": int(row["id"]),
                "title": row["title"],
                "genres": row["genres"],
                "vote_average": (
                    float(row["vote_average"])
                    if pd.notna(row["vote_average"])
                    else None
                )
            }
            for _, row in matches.iterrows()
        ]

    def recommend_movies(self, movie_id, k=10):
        """
        Recommend movies using genre-transition probabilities.

        The selected movie's genres are starting states.
        Candidate movie genres are evaluated as possible next states.
        """

        if movie_id not in self.movie_id_to_index:
            raise ValueError("Movie not found")

        if k < 1:
            raise ValueError(
                "k must be greater than or equal to 1"
            )

        query_index = self.movie_id_to_index[movie_id]
        query_movie = self.movies.iloc[query_index]

        query_genres = query_movie["genres"]

        if not query_genres:
            return []

        # Calculate transition scores for candidate movies.
        recommendations = []

        for index, row in self.movies.iterrows():

            # Do not recommend the selected movie itself.
            if int(row["id"]) == movie_id:
                continue

            candidate_genres = row["genres"]

            if not candidate_genres:
                continue

            # Average the transition probabilities from
            # the selected movie's genres to the candidate's genres.
            total_score = 0.0

            for current_genre in query_genres:

                transitions = self.genre_transitions.get(
                    current_genre, {}
                )

                if not transitions:
                    continue

                # Sum probabilities associated with the
                # candidate movie's genres.
                genre_score = sum(
                    transitions.get(next_genre, 0.0)
                    for next_genre in candidate_genres
                )

                total_score += genre_score

            transition_probability = (
                total_score / len(query_genres)
            )

            if transition_probability <= 0:
                continue

            vote_average = row["vote_average"]

            recommendations.append({
                "id": int(row["id"]),
                "title": row["title"],
                "genres": candidate_genres,
                "transition_probability": round(
                    transition_probability, 4
                ),
                "vote_average": (
                    float(vote_average)
                    if pd.notna(vote_average)
                    else None
                )
            })

        # Rank candidates by their transition scores.
        recommendations.sort(
            key=lambda movie: movie[
                "transition_probability"
            ],
            reverse=True
        )

        return recommendations[:k]
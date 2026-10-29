from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.recommender import MovieRecommender


recommender = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global recommender

    # Initialize the recommendation engine when the API starts.
    recommender = MovieRecommender()

    yield

    # Clean up when the API shuts down.
    recommender = None


# Define the FastAPI application BEFORE declaring endpoints.
app = FastAPI(
    title="CineMatch API",
    description="Markov Chain-based movie recommendation system",
    version="1.0.0",
    lifespan=lifespan
)


# Allow requests from the React development server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {
        "message": "Welcome to the Movie Recommendation API",
        "docs": "/docs"
    }


@app.get("/api/movies/search")
def search_movies(
    q: str = Query(
        ...,
        min_length=1,
        description="Movie title to search for"
    ),
    limit: int = Query(10, ge=1, le=50)
):
    return {
        "results": recommender.search_movies(
            query=q,
            limit=limit
        )
    }


@app.get("/api/movies/{movie_id}/recommendations")
def get_recommendations(
    movie_id: int,
    k: int = Query(10, ge=1, le=50)
):
    try:
        recommendations = recommender.recommend_movies(
            movie_id=movie_id,
            k=k
        )

        query_movie = recommender.movies[
            recommender.movies["id"] == movie_id
        ]

        if query_movie.empty:
            raise ValueError("Movie not found")

        row = query_movie.iloc[0]

        return {
            "query_movie": {
                "id": int(row["id"]),
                "title": row["title"],
                "genres": row["genres"]
            },
            "count": len(recommendations),
            "recommendations": recommendations
        }

    except ValueError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )
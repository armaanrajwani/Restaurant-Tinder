
# FastAPI provides the web server application and API endpoints.
from fastapi import FastAPI
# Import the separate groups of API endpoints from the routes folder.
from routes import restaurants, auth, swipes, saved, reviews

# Create the Dishr API application (also shown in Swagger UI).
app = FastAPI(title="Dishr API")


# Simple health-check endpoint: confirms the backend is running.
@app.get("/")
def home():
    return {"message": "Dishr backend is running!"}


# Add endpoints for listing and viewing restaurants.
app.include_router(restaurants.router)
# Add account registration, login, and current-user endpoints.
app.include_router(auth.router)
# Add endpoints for liking, disliking, and tracking restaurant swipes.
app.include_router(swipes.router)
# Add endpoints for saving and unsaving restaurants.
app.include_router(saved.router)
# Add endpoints for reviews and restaurant ratings.
app.include_router(reviews.router)

from routes import owners, promotions
app.include_router(owners.router)
app.include_router(promotions.router)

from fastapi import FastAPI
from .database import engine, get_db
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from .models import Post
import os

seeder_complete_file = "seeding_complete.txt"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Check if the seeder has already run
    if not os.path.exists(seeder_complete_file):
        # Seed the database
        db = Session(engine)
        try:
            # Seed posts
            posts_data = [
                {
                'title': 'The Future of Artificial Intelligence: Trends and Insights',
                'content': 'Explore the latest advancements and innovations in AI technology.',
                'published': True
                },
                {
                'title': 'Cybersecurity 101: Protecting Yourself Online',
                'content': 'Learn the basics of online security and how to safeguard your digital presence.',
                'published': True
                },
                {
                'title': 'The Rise of Quantum Computing: What You Need to Know',
                'content': 'Delve into the world of quantum computing and its potential to revolutionize technology.',
                'published': True
                },
                # ... Add more initial post data here ...
            ]
            for post_item in posts_data:
                new_post = Post(**post_item)  # Create a Post object
                db.add(new_post)  # Add it to the session
            db.commit()  # Commit the changes

            # Create a file to indicate seeding completion
            with open(seeder_complete_file, 'w') as f:
                f.write("Seeding completed.")

        except Exception as e:
            print(f"Error seeding the database: {e}")
        finally:
            db.close()  # Close the database session

    # Yield control to the FastAPI app after seeding
    yield
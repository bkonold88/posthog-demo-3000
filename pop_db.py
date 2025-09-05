from app import app, db
from models import Movie, User


def ensure_movie(title, genre, description, youtube_link, image_url):
    existing = Movie.query.filter_by(title=title).first()
    if existing:
        # Optionally update mutable fields to keep data fresh
        existing.genre = genre
        existing.description = description
        existing.youtube_link = youtube_link
        existing.image_url = image_url
        return existing
    movie = Movie(
        title=title,
        genre=genre,
        description=description,
        youtube_link=youtube_link,
        image_url=image_url,
    )
    db.session.add(movie)
    return movie


def ensure_admin(email, username, plan, is_admin, is_adult, password):
    user = User.query.filter_by(email=email).first()
    if user is None:
        user = User(
            username=username,
            email=email,
            plan=plan,
            is_admin=is_admin,
            is_adult=is_adult,
        )
        user.set_password(password)
        db.session.add(user)
        return user
    # Update existing admin to desired state
    user.username = username
    user.plan = plan
    user.is_admin = is_admin
    user.is_adult = is_adult
    user.set_password(password)
    return user


with app.app_context():
    db.create_all()

    # Ensure movies exist (idempotent)
    ensure_movie(
        title="Code & Quills",
        genre="Family",
        description="Max, a brilliant hedgehog programmer, embarks on a thrilling journey to create the ultimate app, while navigating the quirks and joys of coding from his cozy home office.",
        youtube_link="https://www.youtube.com/embed/2jQco8hEvTI",
        image_url="/static/images/hedgehog_developer.png",
    )
    ensure_movie(
        title="Palette of Prickles",
        genre="Family",
        description="In his vibrant studio, Max, the creative hedgehog, brings his imaginative designs to life with colorful sketches and digital artistry, aiming to win a prestigious design contest.",
        youtube_link="https://www.youtube.com/embed/TIxxIEEvczM",
        image_url="/static/images/hedgehog_designer.png",
    )
    ensure_movie(
        title="Data Spikes",
        genre="Family",
        description="Donning his lab coat, Max delves into the world of data analysis, uncovering fascinating insights and solving complex problems, all from his sleek, modern office.",
        youtube_link="https://www.youtube.com/embed/lYBUbBu4W08?si=b65lgJb43lzHLh5x",
        image_url="/static/images/hedgehog_data_scientist.png",
    )
    ensure_movie(
        title="Fists of Fury",
        genre="Action",
        description="Max, the underdog hedgehog with a heart of gold, steps into the ring to prove his worth against the toughest opponents. With each punch, he battles not just for victory, but for his place in a world that underestimates him, fighting to rise as the champion of the streets.",
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_rocky.jpg",
    )
    ensure_movie(
        title="Spikes & Consequences",
        genre="Action",
        description="In the shadowy underworld of Hedgetown, Max finds himself embroiled in a high-stakes confrontation with some of the most dangerous figures in town. With quick reflexes and a sharper tongue, he navigates a web of crime and chaos, making sure every action has its consequence.",
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_pulp.jpg",
    )
    ensure_movie(
        title="The Hedge Abides",
        genre="Action",
        description=" Max, the laid-back but sharp-witted hedgehog, finds himself drawn into a bizarre mystery at the local bowling alley. Armed with nothing but his easy-going charm and a strong sense of right and wrong, he rolls through life’s oddities with style, proving that sometimes, the coolest heroes are the most unexpected.",
        youtube_link="https://www.youtube.com/embed/dQw4w9WgXcQ",
        image_url="/static/images/hedgehog_dude.jpg",
    )

    # Ensure admin user exists (idempotent)
    ensure_admin(
        email="admin@posthog.com",
        username="admin",
        plan="Premium",
        is_admin=True,
        is_adult=False,
        password="admin",
    )

    db.session.commit()

    print("Database seeded: movies ensured and admin user ensured.")
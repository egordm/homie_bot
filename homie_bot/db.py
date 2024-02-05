from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from homie_bot.models import Base, recent_messages_index, recent_user_messages_index

engine = create_engine("sqlite:///db.sqlite")

Base.metadata.create_all(engine)
recent_messages_index.create(bind=engine, checkfirst=True)
recent_user_messages_index.create(bind=engine, checkfirst=True)

Session = sessionmaker(engine)


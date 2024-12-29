from sqlalchemy import Integer, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column



class Base(DeclarativeBase):
    description: Mapped[str] = mapped_column(Text, nullable=True)


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    game_state: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    difficult_id: Mapped[int] = mapped_column(Integer, nullable=True)
    loc1: Mapped[bool] = mapped_column(Boolean, nullable=True)
    loc2: Mapped[bool] = mapped_column(Boolean, nullable=True)
    loc3: Mapped[bool] = mapped_column(Boolean, nullable=True)


"""
game states
0 - none game
1 - prehistory (prehistory_0)
2 - choose difficult (ask_for_difficult)
3 - fork (fork)
4 - prehistory location 1 (prehistory_1)
5 - minigame 1 (minigame_1)
6 - prehistory location 2 (prehistory_2)
7 - minigame 2 (minigame_2)
8 - prehistory location 3 (prehistory_3)
9 - minigame 3 (minigame_3)
10 - finish game (finish)
"""


class Difficult(Base):
    __tablename__ = 'difficults'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)


class Image(Base):
    __tablename__ = 'images'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    data: Mapped[str] = mapped_column(Text, nullable=False)


"""class Answer(Base):
    __tablename__ = 'answers'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    category: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)"""


class Slide(Base):
    __tablename__ = 'slides'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    image_id: Mapped[int] = mapped_column(Integer, nullable=True)
    #answer_category: Mapped[int] = mapped_column(ForeignKey('answers.category'), nullable=False)
    
    #_image: Mapped['Image'] = relationship('Image', back_populates='slide')
    #answer: Mapped['Answer'] = relationship('Answer', back_populates='slide')

class Banner(Base):
    __tablename__ = 'banners'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=True)
    image_id: Mapped[int] = mapped_column(Integer, nullable=True)
    #answer_category: Mapped[int] = mapped_column(ForeignKey('answers.category'), nullable=False)
    
    #image: Mapped['Image'] = relationship('Image', back_populates='banner')
    #answer: Mapped['Answer'] = relationship('Answer', back_populates='banner')
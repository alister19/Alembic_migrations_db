from sqlalchemy import ARRAY, JSON, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base
from sql_enums import GenderEnum, ProfessionEnum, StatusPost, RatingEnum

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    profile_id: Mapped[int | None] = mapped_column(ForeignKey("profiles.id"))

    # Связь с моделью Профиль, один-к-одному
    profile: Mapped["Profile"] = relationship(
        "Profile",
        back_populates="user",
        uselist=False,    # ключевой параметр для связи один-к-одному
        lazy="joined"    # автоматически подгружает profile при запросе user
    )
    # Связь с моделью Пост один-ко-многим
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="user",
        cascade="all, delete-orphan"    # удаляет посты при удалении пользователя
    )
    # Связь с моделью Комментарии один-ко-многим
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="user",
        cascade="all, delete-orphan"
    )

class Profile(Base):
    first_name: Mapped[str]
    last_name: Mapped[str | None]
    age: Mapped[int | None]
    gender: Mapped[GenderEnum]
    profession: Mapped[ProfessionEnum] = mapped_column(
        default=ProfessionEnum.DEVELOPER,
        server_default=text("'UNEMPLOYED'")
    )
    interests: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    contacts: Mapped[dict | None] = mapped_column(JSON)

    # Связь с моделью Юзер один-к-одному
    user: Mapped["User"] = relationship(
        "User",
        back_populates="profiles",
        uselist=False
    )

class Post(Base):
    title: Mapped[str]
    content: Mapped[str] = mapped_column(Text)
    main_photo_url: Mapped[str]
    photos_url: Mapped[list[str] | None] = mapped_column(ARRAY(String))
    status: Mapped[StatusPost] = mapped_column(
        default=StatusPost.PUBLISHED,
        server_default=text("'DRAFT'"),
        nullable=False
    )

    # Связь с моделью Юзер многие-к-одному
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts"
    )
    # Связь с моделью Комментарии один-ко-многим
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )

class Comment(Base):
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    is_published: Mapped[bool] = mapped_column(default=True, server_default=text("'false'"))
    rating: Mapped[RatingEnum] = mapped_column(default=RatingEnum.FIVE, server_default=text("'SEVEN'"))

    # Связь с моделью Юзер многие-к-одному
    user: Mapped["User"] = relationship(
        "User",
        back_populates="comments"
    )

    # Связь многие-к-одному с Пост
    post: Mapped["Post"] = relationship(
        "Post",
        back_populates="comments"
    )
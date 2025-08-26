from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int = Field(description="Unique User ID")
    username: str = Field(description="Unique Username Field", min_length=3, max_length=64)
    email: str = Field(description="Unique Email Field", min_length=6, max_length=64)
    password: str = Field(description="Password Field", min_length=8, max_length=64)
    role: int = Field(description="User Role Field")

class UserCreate(BaseModel):
    username: str = Field(description="Unique Username Field", min_length=3, max_length=64)
    email: str = Field(description="Unique Email Field", min_length=6, max_length=64)
    password: str = Field(description="Password Field", min_length=8, max_length=64)

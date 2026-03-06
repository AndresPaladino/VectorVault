from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://user:password@localhost:5432/vectorvault"
    storage_path: str = "./storage"
    clip_model_name: str = "ViT-B-32"
    clip_pretrained: str = "laion2b_s34b_b79k"

    model_config = {"env_file": ".env"}


settings = Settings()

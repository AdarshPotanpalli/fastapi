from pydantic_settings import BaseSettings

# validates if all the environment variables have been properly defined
class Settings(BaseSettings):
    # the environment variables are usually upper case, but pydantic variables are case insensetive
    
    database_name: str
    database_hostname: str
    database_port: str 
    database_username: str
    database_password: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"
    
settings = Settings()
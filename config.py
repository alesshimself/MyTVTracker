import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    TMDB_API_KEY = os.environ.get('TMDB_API_KEY') or 'your-tmdb-api-key-here'
    MILVUS_HOST = os.environ.get('MILVUS_HOST') or 'localhost'
    MILVUS_PORT = os.environ.get('MILVUS_PORT') or '19530'

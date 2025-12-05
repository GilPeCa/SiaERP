from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Archivo
DB_URL = "sqlite:///./sql_app.db"

#Configuracion multi hilos
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})    

#Forzar commit
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
Base = declarative_base()
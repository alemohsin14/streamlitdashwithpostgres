FROM python:3.8


WORKDIR /app

COPY . /app/


RUN pip install streamlit


EXPOSE 8501


CMD ["streamlit", "run", "new.py"]

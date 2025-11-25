FROM python:3.9-slim

# CHANGE THIS DATE TO FORCE REBUILD: 2025-11-24-v2
ENV REFRESHED_AT 2025-11-24-v2

ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
WORKDIR $APP_HOME

COPY . ./

# Install pip and force install requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --force-reinstall -r requirements.txt

EXPOSE 8080
CMD streamlit run app.py --server.port 8080 --server.address 0.0.0.0
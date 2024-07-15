FROM python:3.12-slim

ENV SOURCE_URL=https://picsum.photos/1920/1080
ENV CACHE_NAME=cache
ENV MIN_CONTENT_BYTES=10240
RUN pip install requests Flask
WORKDIR /app
COPY main.py /app/main.py
EXPOSE 5000
CMD ["python", "main.py"]

FROM python:3.9
WORKDIR /cms

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY ./ ./
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "iclassroom_api.wsgi"]

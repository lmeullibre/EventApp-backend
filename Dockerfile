FROM python:3.7-stretch
COPY . /app
WORKDIR /app
ENV DATABASE_ENVIRONMENT=Production
ENV AWS_ACCESS_KEY_ID=AKIAXFNMNLILNXNUHN7U
ENV AWS_SECRET_ACCESS_KEY=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
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

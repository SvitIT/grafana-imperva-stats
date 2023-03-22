FROM python:3.10-alpine
WORKDIR /app
COPY . .
ENV FLASK_APP=api.py
EXPOSE 5000
RUN pip install -r requirements.txt


#api mainloop
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
FROM --platform=linux/amd64 python:3.9
COPY src/ /lab1
COPY requirements.txt /lab1
WORKDIR /lab1
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python3", "main.py"]
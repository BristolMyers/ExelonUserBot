FROM sandy1709/catuserbot:latest

# Çalışma dizini
ENV PATH="/home/userbot/bin:$PATH"
WORKDIR /root/userbot

# Repoyu klonla
RUN git clone https://github.com/BristolMyers/ExelonUserBot /root/userbot

RUN pip3 install -U -r requirements.txt
# Botu çalıştır
CMD ["python3","-m","userbot"]

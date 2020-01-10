FROM ubuntu:latest

RUN apt-get install git && \
    git clone https://github.com/ppke-nlpg/emmorphpy.git


RUN wget -O hfst-dbgsym.deb http://apertium.projectjj.com/apt/nightly/pool/main/h/hfst/hfst-dbgsym_3.15.1+g3723~95ec8680-1~bullseye1_amd64.deb

RUN apt install hfst

RUN ls -la && apt-get install -f ./hfst-dbgsym.deb

WORKDIR emmorphpy

EXPOSE 80

CMD ['python', 'emmorphrest']

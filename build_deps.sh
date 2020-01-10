#!/bin/bash

mkdir deps && \
cd deps && \
# source venv/bin/activate && \
git clone https://github.com/ppke-nlpg/emmorphpy.git && \
cd emmorphypy && \
pip install -r requirements.txt
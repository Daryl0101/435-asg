FROM apache/hadoop:3

WORKDIR "/opt/hadoop"
COPY mapper.py mapper.py
COPY reducer.py reducer.py

RUN mkdir input
COPY gutenberg_txt.txt ./input/input_text.txt
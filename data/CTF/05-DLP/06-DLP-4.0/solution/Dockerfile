FROM sagemath/sagemath:10.1

RUN sage -pip install --no-cache-dir pwntools==4.11.1
COPY solve.sage /home/sage/solve.sage

CMD ["sage", "/home/sage/solve.sage"]

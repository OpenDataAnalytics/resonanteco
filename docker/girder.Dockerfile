FROM girder/girder:latest-py3

WORKDIR /home

COPY docker/provision provision
COPY server /home/resonanteco
COPY client/dist /usr/share/girder/static/resonanteco

RUN pip install -e /home/resonanteco && girder build

ENTRYPOINT ["/home/provision/girder_entrypoint.sh"]
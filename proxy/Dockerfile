FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y apt-transport-https software-properties-common
RUN echo deb https://dl.bintray.com/fanout/debian fanout-bionic main | tee /etc/apt/sources.list.d/fanout.list
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
RUN apt-get update

RUN apt-get update
RUN apt-get install -y pushpin


# Configure Pushpin
RUN \
  sed -i \
    -e 's/zurl_out_specs=.*/zurl_out_specs=ipc:\/\/\{rundir\}\/pushpin-zurl-in/' \
    -e 's/zurl_out_stream_specs=.*/zurl_out_stream_specs=ipc:\/\/\{rundir\}\/pushpin-zurl-in-stream/' \
    -e 's/zurl_in_specs=.*/zurl_in_specs=ipc:\/\/\{rundir\}\/pushpin-zurl-out/' \
    /usr/lib/pushpin/internal.conf && \
  sed -i \
    -e 's/services=.*/services=mongrel2,m2adapter,zurl,pushpin-proxy,pushpin-handler/' \
    -e 's/push_in_spec=.*/push_in_spec=tcp:\/\/\*:5560/' \
    -e 's/push_in_http_addr=.*/push_in_http_addr=0.0.0.0/' \
    -e 's/push_in_sub_spec=.*/push_in_sub_spec=tcp:\/\/\*:5562/' \
    -e 's/command_spec=.*/command_spec=tcp:\/\/\*:5563/' \
    /etc/pushpin/pushpin.conf

# Cleanup
RUN \
  apt-get clean && \
  rm -fr /var/lib/apt/lists/* && \
  rm -fr /tmp/*

ADD . ./etc/pushpin/

CMD ["pushpin"]

EXPOSE 7999
EXPOSE 5561
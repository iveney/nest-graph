# Nest Data Collector
#
# VERSION               0.0.2
#
# RUN THE CONTAINER WITH THE FOLLOWING COMMAND
# docker run -d -p 4242:4242 -p 3000:3000 --restart unless-stopped jeff89179/nest-graph-v2.2
#
# TAG THE IMAGE WITH THE FOLLOWING COMMAND
# docker tag [image id] jeff89179/nest-graph-v2.2
#
# CONFIGURE THE LOGIN WITH THE FOLLOWING COMMAND
# docker exec -it [container id] /usr/bin/python /opt/nest-auth.py

FROM      ubuntu
LABEL maintainer="jeff89179"

RUN apt-get update && \
    apt-get install -y apt-utils unzip wget openjdk-8-jdk gnuplot openssh-server supervisor adduser libfontconfig curl && \
    apt-get install -y python python-setuptools python-pip
RUN mkdir -p  /var/run/sshd /var/log/supervisor /data/hbase /data/zookeeper

# Download the peterot nest-graph files 
RUN wget https://github.com/peterot/nest-graph/archive/master.zip && \
    unzip master.zip -d /tmp/

# Install HBase...1.1.0 is current as of 2018-10-17
WORKDIR /opt
RUN wget http://archive.apache.org/dist/hbase/hbase-1.1.0/hbase-1.1.0-bin.tar.gz && \
    tar -xzvf hbase-1.1.0-bin.tar.gz && \
    rm hbase-*.gz

RUN cp /tmp/nest-graph-master/hbase-site.xml /opt/hbase-1.1.0/conf/
RUN echo "export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/" >> /opt/hbase-1.1.0/conf/hbase-env.sh

# Install OpenTSDB...2.3.1 is current as of 2018-10-17
ADD https://github.com/OpenTSDB/opentsdb/releases/download/v2.3.1/opentsdb-2.3.1_all.deb /tmp/
RUN dpkg -i /tmp/opentsdb-2.3.1_all.deb && rm /tmp/opentsdb-2.3.1_all.deb && \
    cp /tmp/nest-graph-master/opentsdb.sh /opt/

# Install Grafana...5.3.1 is current as of 2018-10-17
ADD  https://s3-us-west-2.amazonaws.com/grafana-releases/release/grafana_5.3.1_amd64.deb  /tmp/
RUN dpkg -i /tmp/grafana_5.3.1_amd64.deb && rm /tmp/grafana_5.3.1_amd64.deb && \
    cp /tmp/nest-graph-master/grafana.sh /opt/ && \
    cp -r /tmp/nest-graph-master/dashboards /opt/dashboards

# Install tCollector...1.3.2 is current as of 2018-10-17
RUN wget https://github.com/OpenTSDB/tcollector/archive/v1.3.2.tar.gz && tar xzf v1.3.2.tar.gz && rm v1.3.2.tar.gz && \
    cp -r /tmp/nest-graph-master/home_collectors /opt/home_collectors

RUN pip install python-nest && \
    cp /tmp/nest-graph-master/tCollector.sh /opt/ && \
    cp /tmp/nest-graph-master/nest-auth.py /opt/

# Configure Supervisor
RUN cp /tmp/nest-graph-master/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

expose 22 3000 4242
CMD ["/usr/bin/supervisord"]

VOLUME /data


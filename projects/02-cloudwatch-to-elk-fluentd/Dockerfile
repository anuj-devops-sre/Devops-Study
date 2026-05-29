FROM fluent/fluentd:v1.16-debian-1
USER root
RUN gem install fluent-plugin-cloudwatch-logs
RUN gem install fluent-plugin-elasticsearch
USER fluent

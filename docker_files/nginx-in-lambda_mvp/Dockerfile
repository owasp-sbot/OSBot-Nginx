FROM public.ecr.aws/awsguru/nginx:1.23.2023.3.11.1

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.3 /lambda-adapter /opt/extensions/lambda-adapter

# config files
ADD nginx.conf /opt/nginx/conf/nginx.conf

# code files
COPY public /var/task/app/public

EXPOSE 8080
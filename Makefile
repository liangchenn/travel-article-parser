.PHONY: print-vars build run stop rmi up down

IMAGE_NAME := article-parser
TARGET_TAG := latest
CONTAINER_NAME := my-klook-article-parser

print-vars:
	@echo 'IMAGE_NAME: $(IMAGE_NAME)'
	@echo 'TARGET_TAG: $(TARGET_TAG)'
	@echo 'CONTAINER_NAME: $(CONTAINER_NAME)'

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d --name $(CONTAINER_NAME) -v $(PWD)/cached_data:/app/cached_data -p 8501:8501 $(IMAGE_NAME)

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

rmi:
	docker rmi $(IMAGE_NAME):$(TARGET_TAG)

up: build run

down: stop rmi
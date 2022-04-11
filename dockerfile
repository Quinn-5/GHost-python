#Download Python from DockerHub and use it
FROM python:3.10.4

#Set the working directory in the Docker container
WORKDIR /code

#Copy the dependencies file to the working directory
COPY requirements.txt .
COPY ./kubeconfig /root/.kube/config

#Install the dependencies
RUN pip install -r requirements.txt

#Copy the Flask app code to the working directory
COPY . .

#Run the container
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app" ]

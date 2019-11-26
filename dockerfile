FROM python:3

WORKDIR /usr/src/app
# Install the necessary dependencies
RUN pip install numpy matplotlib
# Set the environment variable to ensure, that log messages will be printed directly
# to the console. Without setting this value, the log will only be updated after the 
# execution, which is not a desired behavior.
ENV PYTHONUNBUFFERED=1
# Copy the whole folder into the image
COPY . .
# Set the script which should be executed
CMD [ "python", "./automated_script.py" ]

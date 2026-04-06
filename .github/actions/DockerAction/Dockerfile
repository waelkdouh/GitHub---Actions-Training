# Use a lightweight base image
FROM alpine:3.10

# Copy the shell script from your repo to the container
COPY entrypoint.sh /entrypoint.sh

# Make the script executable
RUN chmod +x /entrypoint.sh

# Code to run when the container starts
ENTRYPOINT ["/entrypoint.sh"]

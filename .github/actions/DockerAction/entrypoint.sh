#!/bin/sh -l

# $1 is the first argument passed from the 'args' section in action.yml
NAME=$1

echo "Hello $NAME"

# Setting an output for GitHub Actions
# This syntax allows subsequent steps to use the 'greeting' variable
echo "greeting=Hello $NAME" >> $GITHUB_OUTPUT

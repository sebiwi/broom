# BROOM

Enforce strict tagging policies on AWS EC2 instances, using Lambda.

I made this because I wanted to analyze each instance that is created on my
AWS account, and destroy it if it is not properly tagged. I also wanted to get
a notification when this happens. If that's what you want too, Broom will do the
job for you!

## Requirements

For this to work, you will need to use:

- Cloudtrail, and an S3 bucket
- An SNS topic
- An IAM role
- A Lambda function

## Usage

Create a Cloudtrail trail, apply it to all regions (or the regions you want to
monitor), and synchronize it with an S3 bucket of your choice. You can create an
S3 bucket on the AWS console if you don't have one already.

Next, create an SNS topic for Broom notifications, and subscribe yourself to it
if you want to receive notifications.

Create an IAM role for Broom, using the policy that comes with this repository.
You will have to modify it and add your SNS topic ARN so that your Lambda
function can interact with it.

Next up, create the function on Lambda. You can create it on the console editing
the code inline, since all the used libraries are available in AWS, or you can
create a function package an upload it. Set up a trigger from the previously
created S3 bucket, on object creation, and increase the timeout limit. Ten
seconds should do.

By default, Broom verifies if the instance is tagged with the 'Code' key, and
either the 'LOL', 'GGG', "BRB' or 'YLO' values. You will probably want to change
this according to your needs. If it is not, it will destroy the instance, and
publish a report on the SNS topic.

## This is pretty cool, thanks!

You're welcome. Any suggestions/comments are welcomed!

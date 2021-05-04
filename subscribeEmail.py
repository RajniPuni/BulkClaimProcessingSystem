import json
import logging
import time
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SnsWrapper:
    """Encapsulates Amazon SNS topic and subscription functions."""
    def __init__(self, sns_resource):
        """
        :param sns_resource: A Boto3 Amazon SNS resource.
        """
        self.sns_resource = sns_resource

    def create_topic(self, name):
        """
        Creates a notification topic.

        :param name: The name of the topic to create.
        :return: The newly created topic.
        """
        try:
            topic = self.sns_resource.create_topic(Name=name)
            print("---------------------------arn---------------------")
            print(topic.arn)
            logger.info("Created topic %s with ARN %s.", name, topic.arn)
        except ClientError:
            logger.exception("Couldn't create topic %s.", name)
            raise
        else:
            return topic

    
    @staticmethod
    def subscribe(topic, protocol, endpoint):
        """
        Subscribes an endpoint to the topic. Some endpoint types, such as email,
        must be confirmed before their subscriptions are active. When a subscription
        is not confirmed, its Amazon Resource Number (ARN) is set to
        'PendingConfirmation'.

        :param topic: The topic to subscribe to.
        :param protocol: The protocol of the endpoint, such as 'sms' or 'email'.
        :param endpoint: The endpoint that receives messages, such as a phone number
                         (in E.164 format) for SMS messages, or an email address for
                         email messages.
        :return: The newly added subscription.
        """
        try:
            subscription = topic.subscribe(
                Protocol=protocol, Endpoint=endpoint, ReturnSubscriptionArn=True)
            logger.info("Subscribed %s %s to topic %s.", protocol, endpoint, topic.arn)
        except ClientError:
            logger.exception(
                "Couldn't subscribe %s %s to topic %s.", protocol, endpoint, topic.arn)
            raise
        else:
            return subscription

    
    

def usage_demo():
    print('-'*88)
    print("Welcome to the Amazon Simple Notification Service (Amazon SNS) demo!")
    print('-'*88)

    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    region_name = "us-east-1"
    aws_access_key_id='ASIAZ56BHUDMR5SWDF4V'
    aws_secret_access_key='XuAnNSQZHkrPMEFkqBWQkOpiRPGqj8eMJ0PtQYaw'
    aws_session_token='IQoJb3JpZ2luX2VjEOP//////////wEaCXVzLXdlc3QtMiJHMEUCIQDjiO5P/pFEF0pk6kQVeCK5by405qv2wawArxfWPJ/S5gIgAOp87p3JHaVvCiYMOVOoc0jLguWW8rOfGb1U90pqcAEqqAIIPBAAGgw2ODI3NjgxNzk0MTciDFYPSx1vNu0oO+S5WyqFAgsKDAiSxwRbRrujkydUt5xVHbz9gfqiS2odf901qz+2XdMzaVDCfZlDmqrynKBwkYL96fuXxVt1N7EcezeVsvVJstTzU2Mq9KK56+aipzrHLJYNAUyJSRJrlvrmWZA3efgG9B2ausYde/OU9a0Mn5R4TjIgR83BEU8kH6lsbjKpUeWRDmBXQPrvQ4+V+sHvKu+f4OPPtrs3Bfj2yQK6qZVtyDyccIVFd/kNIMtFB7HXj6s0q/MWF/NRCPsWoEJx3tOKbq2yKUFwyc8F6f8XDqIz1tMxwBqV0J/LvM1EZNm7VLLBBe46TXqnKBb4BisLgede7+Hc3gMaqVvqfRytYGhWzIm4tzCxuLSDBjqdAQjqYPQO3KXqeSqggnbZDXWcgv/e455GzdFTQxUiTPCmIR8bdhxQXe1skgC8eZLLJ1IO/wthR/WGd6mSWWiOb8/E+D33xa3kQ3MfX9SMq9dKcrb7llKDkjUeBFfQ5tNebaRESPegKkAILl3vlLfg4iF6P5mv3RkG4HKDzGaqEi445Tw0hwP+nMO91zjtV75b3DuuEFQc4Ju3gsOhpIo='

    sns_wrapper = SnsWrapper(boto3.resource('sns', region_name=region_name, aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token))
    topic_name = f'demo-basics-topic-{time.time_ns()}'

    print(f"Creating topic {topic_name}.")
    topic = sns_wrapper.create_topic(topic_name)

    email = input(
        f"Enter an email address to subscribe to {topic_name} and receive "
        f"a message: ")

    if email != '':
        print(f"Subscribing {email} to {topic_name}.")
        email_sub = sns_wrapper.subscribe(topic, 'email', email)
        answer = input(
            f"Confirmation email sent to {email}. To receive SNS messages, "
            f"follow the instructions in the email. When confirmed, press "
            f"Enter to continue.")
        while (email_sub.attributes['PendingConfirmation'] == 'true'
               and answer.lower() != 's'):
            answer = input(
                f"Email address {email} is not confirmed. Follow the "
                f"instructions in the email to confirm and receive SNS messages. "
                f"Press Enter when confirmed or enter 's' to skip. ")
            email_sub.reload()

    
    print("Thanks for watching!")
    print('-'*88)


if __name__ == '__main__':
    usage_demo()
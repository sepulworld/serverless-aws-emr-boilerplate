import boto3
import datetime
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

master_instance_type = os.environ.get('master_instance_type')
core_instance_type = os.environ.get('core_instance_type')
core_instance_count = os.environ.get('core_instance_count')
core_instance_fallback_type = os.environ.get('core_instance_fallback_type')
core_instance_fallback_count = os.environ.get('core_instance_fallback_count')
key_name = os.environ.get('key_name')
release_label = os.environ.get('release_label')
emr_name = os.environ.get('emr_name')
bid_percent = os.environ.get('bid_percent')
date_key = (datetime.date.today()).strftime('%Y%m%d')
env = os.environ.get('env')
jar_class = os.environ.get('jar_class')
spark_executor_cores = os.environ.get('spark_executor_cores')
spark_executor_memory = os.environ.get('spark_executor_memory')

def create_emr_python_wordcount_step(additional_args):
    """Generate a python test step
aws sns publish \
  --topic-arn \
  "arn:aws:sns:us-west-2:12345678910:emr-step-launcher-dev" \
  --message \
  "s3://yous3bucket/dev/moby_dick.txt,s3://yours3bucket/dev/moby_dick_output/"
    """
    step = {
        "Name": "python-wordcount-{}".format(env),
        "ActionOnFailure": "TERMINATE_JOB_FLOW",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "cluster",
                "--master",
                "yarn",
                "--conf",
                "spark.yarn.submit.waitAppCompletion=false",
                "--num-executors",
                "5",
                "--executor-memory",
                spark_executor_memory,
                "--executor-cores",
                spark_executor_cores,
                "https://gist.github.com/sepulworld/51fbd6757d3571df0ecb19cc0c1c7403"
            ]
        }
    }

    for i in additional_args:
        step['HadoopJarStep']['Args'].append(i)
        logger.info('Generated step: {}'.format(step))

    return step

def emr_launcher(event, context):
    """Launcer funtion for EMR on-demand cluster
sample event data
http://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-sns
The sns message should be a comma seperated string of args we can append to the
EMR step. This maybe s3 prefix location where input data is and where to output
ie "s3://silvermullet-data-bucket/input/,s3://silvermullet-data-bucket/output/"
    """

    client = boto3.client('emr')
    sns_event_message = event['Records'][0]['Sns']['Message']
    additional_args = [x for x in sns_event_message.split(',')]
    logger.info("Complete SNS event: {}".format(event))
    logger.info("Sns message received: {}".format(sns_event_message))
    logger.info("Parsed message into args: {}".format(additional_args))

    cluster = client.run_job_flow(
        Name=emr_name,
        ReleaseLabel=release_label,
        LogUri=emr_loguri,
        ServiceRole='EMR_DefaultRole',
        JobFlowRole='EMR_EC2_DefaultRole',
        VisibleToAllUsers=True,
        Instances={
            'InstanceFleets': [
                {
                    'Name': 'master-{0}-{1}'.format(emr_name, date_key),
                    'InstanceFleetType': 'MASTER',
                    'TargetSpotCapacity': 1,
                    'InstanceTypeConfigs': [
                        {
                            'InstanceType': master_instance_type,
                            'WeightedCapacity': 1,
                            'BidPriceAsPercentageOfOnDemandPrice': bid_percent
                        },
                    ],
                    'LaunchSpecifications': {
                        'SpotSpecification': {
                            'TimeoutDurationMinutes': 30,
                            'TimeoutAction': 'SWITCH_TO_ON_DEMAND'
                        }
                    }
                },
                {
                    'Name': 'core-{0}-{1}'.format(emr_name, date_key),
                    'InstanceFleetType': 'CORE',
                    'TargetSpotCapacity': core_instance_count,
                    'InstanceTypeConfigs': [
                        {
                            'InstanceType': core_instance_type,
                            'WeightedCapacity': core_instance_count,
                            'BidPriceAsPercentageOfOnDemandPrice': bid_percent
                        },
                        {
                            'InstanceType': core_instance_fallback_type,
                            'WeightedCapacity': core_instance_fallback_count,
                            'BidPriceAsPercentageOfOnDemandPrice': bid_percent
                        }
                    ],
                    'LaunchSpecifications': {
                        'SpotSpecification': {
                            'TimeoutDurationMinutes': 30,
                            'TimeoutAction': 'SWITCH_TO_ON_DEMAND'
                        }
                    }
                }
            ],
            'Ec2KeyName': key_name,
            },
        Steps=[create_emr_python_wordcount_step(additional_args)]
    )

    logger.info('EMR cluster launched: {}'.format(cluster))

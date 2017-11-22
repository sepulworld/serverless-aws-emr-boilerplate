import boto3
import datetime
import os
import time
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

master_instance_type = os.environ.get('master_instance_type')
core_instance_type = os.environ.get('core_instance_type')
core_instance_count = int(os.environ.get('core_instance_count'))
core_instance_fallback_type = os.environ.get('core_instance_fallback_type')
core_instance_fallback_count = int(
    os.environ.get('core_instance_fallback_count'))
key_name = os.environ.get('key_name')
release_label = os.environ.get('release_label')
emr_name = os.environ.get('emr_name')
bid_percent = int(os.environ.get('bid_percent'))
date_key = (datetime.date.today()).strftime('%Y%m%d')
env = os.environ.get('env')
python_spark_script = os.environ.get('python_spark_script')
spark_executor_cores = os.environ.get('spark_executor_cores')
spark_executor_memory = os.environ.get('spark_executor_memory')

def create_emr_python_wordcount_step():
    """Generate a python test step
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
                python_spark_script
            ]
        }
    }

    return step

def emr_launcher(event, context):
    """Launcher function for EMR on-demand cluster
sample event API gatway GET query with 'input' and 'output' query parameters
https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-api-gateway-request

curl --header 'X-Api-Key: YOUR_API_KEY_SERVERLESS_CREATES \
  https://serverlessendpoint.aws.com/launch_emr_wordcount?input=s3://silvermullet-data-bucket/input/?output=s3://silvermullet-data-bucket/output/

We expect and input and output query parameter and will append to the EMR step
"""

    client = boto3.client('emr')
    step = create_emr_python_wordcount_step()
    step['HadoopJarStep']['Args'].append(
        event['queryStringParameters']['input'])
    step['HadoopJarStep']['Args'].append(
        event['queryStringParameters']['output'])
    logger.info("Step to run: {}".format(step))
    logger.info("API Gateway message received: {}".format(event))

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
        Steps=[create_emr_python_wordcount_step()]
    )

    logger.info('EMR cluster launched: {}'.format(cluster))

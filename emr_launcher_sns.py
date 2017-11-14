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

def emr_launcher(event, context):
    """Launcer funtion for EMR on-demand cluster
    """

    client = boto3.client('emr')

    cluster = client.run_job_flow(
        Name=emr_name
        ReleaseLabel=release_label
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
                            'TimeoutDurationMintues': 30,
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
                            'TimeoutDurationMintues': 30,
                            'TimeoutAction': 'SWITCH_TO_ON_DEMAND'
                        }
                    }
                }
            ],
            'Ec2KeyName': key_name
            }
        )

logger.info('EMR cluster launched: {}'.format(cluster))

### Serverless AWS EMR Boilerplate

This is an serverless configured EMR on-demand example using AWS Lambda to launch
an EMR cluster and run 1 EMR Step via an SNS message that contains the location in s3
of the code to run and parameters to pass in

### EMR config

The EMR job flow in this example will leverage [EMR Instance Fleet](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html)

### Requirements

[Serverless.com framework](https://www.npmjs.com/package/serverless)

Replace <your_code_bucket> in serverless.yml with your s3 bucket

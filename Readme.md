### Serverless AWS EMR Boilerplate

This is a [Serverless](https://www.npmjs.com/package/serverless) boilerplate setup meant to demo multiple ways in which you can provision [AWS EMR](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html) on-demand through the following triggers:

* [AWS SNS](https://serverless.com/framework/docs/providers/aws/events/sns/)
* [AWS S3](https://serverless.com/framework/docs/providers/aws/events/s3/)
* [AWS API Gateway](https://serverless.com/framework/docs/providers/aws/events/apigateway/)

#### AWS SNS

function code to reference: emr_launcher_sns.py

SNS message body contains the [EMR Step(s)](https://docs.aws.amazon.com/emr/latest/DeveloperGuide//emr-steps.html) to run

* Message body with Steps will be run on the EMR cluster launched
```json
   {
        "Name": "MySparkJob-SilverMullet-step1",
        "ActionOnFailure": "TERMINATE_JOB_FLOW",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "cluster",
                "--class",
                "com.zane.silvermullet.batch.jobs.DataProcessor",
                "--executor-memory",
                "20G",
                "--executor-cores",
                "100",
                "s3://silvermullet-code-bucket/source/latest/spark.jar"
            ]
        }
    },
    {
        "Name": "MySparkJob-SilverMullet-step2",
        "ActionOnFailure": "TERMINATE_JOB_FLOW",
        "HadoopJarStep": {
            "Jar": "command-runner.jar",
            "Args": [
                "spark-submit",
                "--deploy-mode",
                "cluster",
                "--class",
                "com.zane.silvermullet.batch.jobs.DataProcessor2",
                "--executor-memory",
                "20G",
                "--executor-cores",
                "100",
                "s3://silvermullet-code-bucket/source/latest/spark.jar"
            ]
        }
    }
```

![messaging_amazonsns](https://user-images.githubusercontent.com/538171/32766496-0a0ee9a0-c8c4-11e7-927e-165336a46310.png) ->
![compute_awslambda_lambdafunction](https://user-images.githubusercontent.com/538171/32766526-3cc3a228-c8c4-11e7-949d-c08d9e7e9719.png) -> ![analytics_amazonemr_cluster](https://user-images.githubusercontent.com/538171/32766582-89f244fa-c8c4-11e7-8099-7373c944949e.png)



#### EMR configuration notes

The EMR job flow in this example will leverage [EMR Instance Fleet](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html)

#### Requirements

[Serverless.com framework](https://www.npmjs.com/package/serverless)

serverless.yml.exmaple contains items that will need to be updated to match your use case
Replace <your_code_bucket> in serverless.yml with your s3 bucket for example.

This serverless.yml.example is a boilerplate example and is meant to provide a central place for use cases.

# Serverless AWS EMR Boilerplate

This is a [Serverless](https://www.npmjs.com/package/serverless) boilerplate setup meant to demo multiple ways in which you can provision [AWS EMR](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html) on-demand through the following triggers:

* [AWS SNS Event in Serverless](https://serverless.com/framework/docs/providers/aws/events/sns/)
* [AWS S3 Event in Serverless](https://serverless.com/framework/docs/providers/aws/events/s3/)
* [AWS API Gateway HTTP Event in Serverless](https://serverless.com/framework/docs/providers/aws/events/apigateway/)

### [AWS SNS Event Trigger EMR](https://github.com/sepulworld/serverless-aws-emr-boilerplate/tree/master/launch_emr_via_sns)

##
![sns_to_emr](https://user-images.githubusercontent.com/538171/33153928-a7a92f50-cf99-11e7-9374-1384217cd32b.png)

SNS message body contains the input and output data parameters for [EMR Step](https://docs.aws.amazon.com/emr/latest/DeveloperGuide//emr-steps.html) to run

* Message body of SNS to contain comma separated string of args to pass to EMR Step
```json
"s3://silvermullet-data-bucket/input/,s3://silvermullet-data-bucket/output/"
```

See launch_emr_via_sns folder


### [AWS API Gateway Proxy Event Trigger EMR](https://github.com/sepulworld/serverless-aws-emr-boilerplate/tree/master/launch_emr_via_api_gateway)

##
![api_gateway_to_emr](https://user-images.githubusercontent.com/538171/33154005-33fbb996-cf9a-11e7-9e20-64144484d276.png)

Event driven by API gateway GET query with 'input' and 'output' query parameters for EMR step to work with.
https://docs.aws.amazon.com/lambda/latest/dg/eventsources.html#eventsources-api-gateway-request

```bash
curl --header 'X-Api-Key: YOUR_API_KEY_SERVERLESS_CREATES' \
https://serverlessendpoint.aws.com/launch_emr_wordcount?input=s3://silvermullet-data-bucket/input/?output=s3://silvermullet-data-bucket/output/
```

See launch_emr_via_api_gateway folder


#### EMR configuration notes

The EMR job flow in this example will leverage [EMR Instance Fleet](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-instance-fleet.html)

#### Requirements

[Serverless.com framework](https://www.npmjs.com/package/serverless)

serverless.yml.exmaple contains items that will need to be updated to match your use case
Replace <your_code_bucket> in serverless.yml with your s3 bucket for example.

This serverless.yml.example is a boilerplate example and is meant to provide a central place for use cases.

# Serverless AWS EMR Boilerplate

This is a [Serverless](https://www.npmjs.com/package/serverless) boilerplate setup meant to demo multiple ways in which you can provision [AWS EMR](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-what-is-emr.html) on-demand through the following triggers:

* [AWS SNS Event in Serverless](https://serverless.com/framework/docs/providers/aws/events/sns/)
* [AWS S3 Event in Serverless](https://serverless.com/framework/docs/providers/aws/events/s3/)
* [AWS API Gateway HTTP Event in Serverless](https://serverless.com/framework/docs/providers/aws/events/apigateway/)

### AWS SNS Event Trigger EMR

##
![messaging_amazonsns](https://user-images.githubusercontent.com/538171/32766496-0a0ee9a0-c8c4-11e7-927e-165336a46310.png) ---> ![compute_awslambda_lambdafunction](https://user-images.githubusercontent.com/538171/32766526-3cc3a228-c8c4-11e7-949d-c08d9e7e9719.png) ---> ![analytics_amazonemr_cluster](https://user-images.githubusercontent.com/538171/32766582-89f244fa-c8c4-11e7-8099-7373c944949e.png)

SNS message body contains the input and output data parameters for [EMR Step](https://docs.aws.amazon.com/emr/latest/DeveloperGuide//emr-steps.html) to run

* Message body of SNS to contain comma separated string of args to pass to EMR Step
```json
"s3://silvermullet-data-bucket/input/,s3://silvermullet-data-bucket/output/"
```

See launch_emr_via_sns folder


### AWS API Gateway Proxy Event Trigger EMR

##
![mobileservices_amazonapigateway](https://user-images.githubusercontent.com/538171/33153525-1c471212-cf97-11e7-9c46-7297a2f95b4b.png) --->
![compute_awslambda_lambdafunction](https://user-images.githubusercontent.com/538171/32766526-3cc3a228-c8c4-11e7-949d-c08d9e7e9719.png) ---> ![analytics_amazonemr_cluster](https://user-images.githubusercontent.com/538171/32766582-89f244fa-c8c4-11e7-8099-7373c944949e.png)

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

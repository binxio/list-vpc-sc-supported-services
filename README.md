# Google List VPC SC supported services

Scrapes the web page https://cloud.google.com/vpc-service-controls/docs/supported-products. This page
describes which Google Cloud Platform services support VPC SC and at which support level: ga, beta or preview.


The utility prints out a Terraform style dictionary of string lists. The key is the status of the service in lowercase, the value
an array of service names in that status. For example:

```shell
list-vpc-sc-supported-services

{
  beta = [
    "adsdatahub.googleapis.com",
    "cloudbuild.googleapis.com",
    ...
    "lifesciences.googleapis.com",
    "transcoder.googleapis.com",
  ]
  ga = [
    "accessapproval.googleapis.com",
    "aiplatform.googleapis.com",
    ...
    "vpcaccess.googleapis.com",
  ]
  preview = [
    "networkmanagement.googleapis.com",
    ...
  ]
}
```

## updating Hashicorp template
You can programmatically update this template. If you have a variable `vpc_sc_services` in HCL:

```hcl
locals {
  vpc_sc_services = {}
}
```
install [hcledit](https://github.com/minamijoyo/hcledit) and type:
```
         hcledit attributes set locals.vpc_sc_services \
         "$(list-vpc-sc-supported-services)" \
         --file locals.tf \
         --update
```


## Caveats
- It is a scraper, so your milage may vary. We are looking forward to a proper API.

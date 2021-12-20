from unittest import TestCase
from list_vpc_sc_supported_services import (
    scrape_vpc_service_controls_supported_products,
)
from list_vpc_sc_supported_services import remove_mixed_status
from list_vpc_sc_supported_services import generate_tf_variable

in_ga = set(
    [
        "accessapproval.googleapis.com",
        "aiplatform.googleapis.com",
        "apigee.googleapis.com",
        "apigeeconnect.googleapis.com",
        "artifactregistry.googleapis.com",
        "automl.googleapis.com",
        "bigquery.googleapis.com",
        "bigquerydatatransfer.googleapis.com",
        "bigtable.googleapis.com",
        "bigtableadmin.googleapis.com",
        "binaryauthorization.googleapis.com",
        "cloudasset.googleapis.com",
        "cloudfunctions.googleapis.com",
        "cloudkms.googleapis.com",
        "cloudprofiler.googleapis.com",
        "cloudsearch.googleapis.com",
        "cloudtrace.googleapis.com",
        "composer.googleapis.com",
        "compute.googleapis.com",
        "connectgateway.googleapis.com",
        "contactcenterinsights.googleapis.com",
        "container.googleapis.com",
        "containeranalysis.googleapis.com",
        "containerregistry.googleapis.com",
        "datacatalog.googleapis.com",
        "dataflow.googleapis.com",
        "datafusion.googleapis.com",
        "dataproc.googleapis.com",
        "dialogflow.googleapis.com",
        "dlp.googleapis.com",
        "dns.googleapis.com",
        "documentai.googleapis.com",
        "eu-automl.googleapis.com",
        "eventarc.googleapis.com",
        "file.googleapis.com",
        "gameservices.googleapis.com",
        "gkeconnect.googleapis.com",
        "gkehub.googleapis.com",
        "healthcare.googleapis.com",
        "iaptunnel.googleapis.com",
        "language.googleapis.com",
        "logging.googleapis.com",
        "managedidentities.googleapis.com",
        "memcache.googleapis.com",
        "meshca.googleapis.com",
        "metastore.googleapis.com",
        "ml.googleapis.com",
        "monitoring.googleapis.com",
        "networkconnectivity.googleapis.com",
        "notebooks.googleapis.com",
        "osconfig.googleapis.com",
        "oslogin.googleapis.com",
        "privateca.googleapis.com",
        "pubsub.googleapis.com",
        "pubsublite.googleapis.com",
        "recaptchaenterprise.googleapis.com",
        "recommender.googleapis.com",
        "redis.googleapis.com",
        "run.googleapis.com",
        "secretmanager.googleapis.com",
        "servicecontrol.googleapis.com",
        "servicedirectory.googleapis.com",
        "spanner.googleapis.com",
        "speech.googleapis.com",
        "sqladmin.googleapis.com",
        "storage.googleapis.com",
        "storagetransfer.googleapis.com",
        "sts.googleapis.com",
        "texttospeech.googleapis.com",
        "tpu.googleapis.com",
        "trafficdirector.googleapis.com",
        "translate.googleapis.com",
        "videointelligence.googleapis.com",
        "vision.googleapis.com",
        "vpcaccess.googleapis.com",
    ]
)


class Test(TestCase):
    def test_scrape_vpc_service_controls_supported_products(self):
        s = scrape_vpc_service_controls_supported_products()
        self.assertTrue("GA" in s)
        self.assertTrue(len(s["GA"]) > 0)
        for service in in_ga:
            self.assertTrue(service in s["GA"], f"{service} not in GA")

        self.assertEqual(
            len(set(s.keys()).difference(set(["GA", "Preview", "Beta"]))), 0
        )

    def test_remove_mixed_status(self):
        input = {
            "GA": set(["A", "B", "P"]),
            "Preview": set(["P", "P2"]),
            "Beta": set(["B"]),
        }
        expect = {
            "GA": set(["A", "B", "P"]),
            "Preview": set(["P2"]),
            "Beta": set(),
        }

        remove_mixed_status(input)
        self.assertEqual(input, expect)

    def test_generate_tf_variable(self):
        s = {
            "GA": set(["A", "B", "P"]),
            "Preview": set(["P2"]),
            "Beta": set(),
        }
        r = generate_tf_variable(s)
        expect = """{
  beta = [
  ]
  ga = [
    "A",
    "B",
    "P",
  ]
  preview = [
    "P2",
  ]
}
"""
        self.assertEqual(expect, r)

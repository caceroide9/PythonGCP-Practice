#!/usr/bin/env python

# Copyright 2019 Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_disable_requester_pays]
from google.cloud import storage


def disable_requester_pays(bucket_name):
    """Disable a bucket's requesterpays metadata"""
    # bucket_name = "my-bucket"

    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)
    bucket.requester_pays = False
    bucket.patch()

    print(f"Requester Pays has been disabled for {bucket_name}")


# [END storage_disable_requester_pays]


if __name__ == "__main__":
    disable_requester_pays(bucket_name=sys.argv[1])

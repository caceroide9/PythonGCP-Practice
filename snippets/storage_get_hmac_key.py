#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys

# [START storage_get_hmac_key]
from google.cloud import storage


def get_key(access_id, project_id):
    """
    Retrieve the HMACKeyMetadata with the given access id.
    """
    # project_id = "Your Google Cloud project ID"
    # access_id = "ID of an HMAC key"

    storage_client = storage.Client(project=project_id)

    hmac_key = storage_client.get_hmac_key_metadata(
        access_id, project_id=project_id
    )

    print("The HMAC key metadata is:")
    print(f"Service Account Email: {hmac_key.service_account_email}")
    print(f"Key ID: {hmac_key.id}")
    print(f"Access ID: {hmac_key.access_id}")
    print(f"Project ID: {hmac_key.project}")
    print(f"State: {hmac_key.state}")
    print(f"Created At: {hmac_key.time_created}")
    print(f"Updated At: {hmac_key.updated}")
    print(f"Etag: {hmac_key.etag}")
    return hmac_key


# [END storage_get_hmac_key]

if __name__ == "__main__":
    get_key(access_id=sys.argv[1], project_id=sys.argv[2])

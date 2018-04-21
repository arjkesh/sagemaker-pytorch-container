# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import pytest
import torch
from test.integration import data_dir, dist_operations_path, mnist_script
from test.utils import local_mode


def test_dist_operations_path_cpu(docker_image, opt_ml, dist_cpu_backend):
    local_mode.train(dist_operations_path, data_dir, docker_image, opt_ml, cluster_size=3,
                     hyperparameters={'backend': dist_cpu_backend})

    assert local_mode.file_exists(opt_ml, 'model/success'), 'Script success file was not created'
    assert local_mode.file_exists(opt_ml, 'output/success'), 'Success file was not created'
    assert not local_mode.file_exists(opt_ml, 'output/failure'), 'Failure happened'


@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda is not available")
def test_dist_operations_path_gpu(docker_image, opt_ml, dist_gpu_backend):
    local_mode.train(dist_operations_path, data_dir, docker_image, opt_ml, cluster_size=3,
                     use_gpu=True, hyperparameters={'backend': dist_gpu_backend})

    assert local_mode.file_exists(opt_ml, 'model/success'), 'Script success file was not created'
    assert local_mode.file_exists(opt_ml, 'output/success'), 'Success file was not created'
    assert not local_mode.file_exists(opt_ml, 'output/failure'), 'Failure happened'


def test_mnist_cpu(docker_image, opt_ml, dist_cpu_backend):
    local_mode.train(mnist_script, data_dir, docker_image, opt_ml, cluster_size=2,
                     hyperparameters={'backend': dist_cpu_backend})

    assert local_mode.file_exists(opt_ml, 'model/model'), 'Model file was not created'
    assert local_mode.file_exists(opt_ml, 'output/success'), 'Success file was not created'
    assert not local_mode.file_exists(opt_ml, 'output/failure'), 'Failure happened'


@pytest.mark.skipif(not torch.cuda.is_available(), reason="cuda is not available")
def test_mnist_gpu(docker_image, opt_ml, dist_gpu_backend):
    local_mode.train(mnist_script, data_dir, docker_image, opt_ml, cluster_size=2,
                     use_gpu=True, hyperparameters={'backend': dist_gpu_backend})

    assert local_mode.file_exists(opt_ml, 'model/model'), 'Model file was not created'
    assert local_mode.file_exists(opt_ml, 'output/success'), 'Success file was not created'
    assert not local_mode.file_exists(opt_ml, 'output/failure'), 'Failure happened'

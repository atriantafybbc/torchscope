import inspect
import pdb
import pytest

from sys import stdout

import scipy
import torch
import torchvision
import torchvision.models as models

from torchscope.saliency import Backprop


def test_set_model_to_eval_mode(mocker):
    mocked_models = mocker.spy(torchvision, 'models')
    model = mocked_models.vgg19()
    Backprop(model)

    model.eval.assert_called_once()


def test_find_first_conv_layer_from_torchvision_models(mocker):
    available_models = inspect.getmembers(models, inspect.isfunction)

    print()
    for name, func in available_models:
        print(f'Finding the first conv layer in model: {name}', end='\r')
        stdout.write('\x1b[2K')

        model = func()
        mocker.spy(model, 'eval')
        backprop = Backprop(model)

        target_layer = backprop.find_target_layer()

        assert type(target_layer) == torch.nn.modules.conv.Conv2d
        assert target_layer.in_channels == 3
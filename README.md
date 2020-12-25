# tf2show

## Install
```bash
pip install tf2show
```

## Example
```python
import tensorflow as tf
from tf2show import tf2show

model = tf.keras.applications.ResNet50()
tf2show(model)	# show model structure
tf2show(model,"model.xlsx")    # save model structure as excel file
```

## Description

tf2show prints tensorflow2's keras model pretty.

Below is the result of `summary` function provided in tensorflow2.

It's not pretty. In addition, some output has been omitted.

```
Model: "mobilenet_1.00_256"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
input_1 (InputLayer)         [(None, 256, 256, 3)]     0         
_________________________________________________________________
conv1_pad (ZeroPadding2D)    (None, 257, 257, 3)       0         
_________________________________________________________________
conv1 (Conv2D)               (None, 128, 128, 32)      864       
_________________________________________________________________
conv1_bn (BatchNormalization (None, 128, 128, 32)      128       
_________________________________________________________________
conv1_relu (ReLU)            (None, 128, 128, 32)      0         
_________________________________________________________________
conv_dw_1 (DepthwiseConv2D)  (None, 128, 128, 32)      288       
_________________________________________________________________
.
.
.
_________________________________________________________________
reshape_2 (Reshape)          (None, 1000)              0         
_________________________________________________________________
predictions (Activation)     (None, 1000)              0         
=================================================================
Total params: 4,253,864
Trainable params: 4,231,976
Non-trainable params: 21,888
_________________________________________________________________
```

Below is the output using tf2show.

It's pretty. All names are printed.

```
----------------------------------------------------------------------------------------------------
| LAYER                  | NAME                     | C    | H   | W    | INPUTS                   |
----------------------------------------------------------------------------------------------------
| InputLayer             | input_1                  | 3    | 256 | 256  | input_1:0                |
| ZeroPadding2D          | conv1_pad                | 3    | 257 | 257  | input_1:0                |
| Conv2D                 | conv1                    | 32   | 128 | 128  | conv1_pad                |
| BatchNormalization     | conv1_bn                 | 32   | 128 | 128  | conv1                    |
| ReLU                   | conv1_relu               | 32   | 128 | 128  | conv1_bn                 |
| DepthwiseConv2D        | conv_dw_1                | 32   | 128 | 128  | conv1_relu               |
| BatchNormalization     | conv_dw_1_bn             | 32   | 128 | 128  | conv_dw_1                |
| ReLU                   | conv_dw_1_relu           | 32   | 128 | 128  | conv_dw_1_bn             |
| Conv2D                 | conv_pw_1                | 64   | 128 | 128  | conv_dw_1_relu           |
| BatchNormalization     | conv_pw_1_bn             | 64   | 128 | 128  | conv_pw_1                |
| ReLU                   | conv_pw_1_relu           | 64   | 128 | 128  | conv_pw_1_bn             |
| ZeroPadding2D          | conv_pad_2               | 64   | 129 | 129  | conv_pw_1_relu           |
| DepthwiseConv2D        | conv_dw_2                | 64   | 64  | 64   | conv_pad_2               |
.
.
.
| Reshape                | reshape_2                |      |     | 1000 | conv_preds               |
| Activation             | predictions              |      |     | 1000 | reshape_2                |
----------------------------------------------------------------------------------------------------
```


It also supports saving to Excel.

This function can be useful when analyzing models.
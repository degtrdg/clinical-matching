import VAEClass
from VAEClass import VAE
import numpy as np
import pandas as pd

params = VAEClass.open_file("/work/08560/danyang/xNet1/cancernet_hyperparams.pickle")


dxNet = VAE(
    params["encoder"],
    params["latent"],
    params["decoder"],
    [100, 6],
    params["loss_weights"],
)

dxNet.build_multimodel()

dxNet.xnet.load_weights("/work/08560/danyang/DXNet/inference/rare6class.h5")
# dxNet.xnet.load_weights("/work/08560/danyang/DXNet/inference/newrareweights.h5")

x_v = VAEClass.open_file("/work/08560/danyang/DXNet/data/GEOData/x_train_od.csv")
x_v = np.asarray(x_v)
# x_v = x_v.transpose()

output = dxNet.xnet.predict(x_v)

print(output)
print(type(output))

out = np.asarray(output[1])
# out = pd.DataFrame(out)

# print(out.head())


print("--------------------------------------------------------------------------")

print("----------------------------- STATS --------------------------------------")


def make_categorical(y_score):
    from keras.utils import to_categorical

    classes = y_score.shape[1]
    y_classes = y_score.argmax(axis=1)
    Y = to_categorical(y_classes, num_classes=classes)
    return Y


predicted = make_categorical(out)

predicted = pd.DataFrame(predicted)
print(predicted)
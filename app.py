import gradio as gr
from CancerNET.VAEClass import open_file
from CancerNET.VAEClass import VAE
import numpy as np
import pandas as pd
from keras.utils import to_categorical


params = open_file(r"./CancerNET/cancernet_hyperparams.pickle")


dxNet = VAE(
    params["encoder"],
    params["latent"],
    params["decoder"],
    [100, 34],
    params["loss_weights"],
)

dxNet.build_multimodel()

dxNet.xnet.load_weights(r"./CancerNET/34_class_CancerNet_weights.h5")

inp = gr.DataFrame()
label = gr.Label()


def test_inp(inp):
    inp = np.asarray(inp)
    inp = inp.flatten()
    inp = inp.reshape(1,-1)
    print(inp)
    output = dxNet.xnet.predict(inp)
    out = np.asarray(output[1])
    print(out)
    # predicted = make_categorical(out)

    # print(predicted)
    result = {"output": out[0].tolist()}
    return result

def make_categorical(y_score):

    classes = y_score.shape[1]
    y_classes = y_score.argmax(axis=1)
    Y = to_categorical(y_classes, num_classes=classes)
    return Y


interface = gr.Interface(fn=test_inp, inputs=inp, outputs=gr.JSON())
interface.launch(inline=False)
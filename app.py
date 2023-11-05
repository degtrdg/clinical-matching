import gradio as gr
from CancerNET.VAEClass import open_file
from CancerNET.VAEClass import VAE
import numpy as np
import pandas as pd

params = open_file(r"./CancerNET/cancernet_hyperparams.pickle")


dxNet = VAE(
    params["encoder"],
    params["latent"],
    params["decoder"],
    [100, 6],
    params["loss_weights"],
)

dxNet.build_multimodel()

dxNet.xnet.load_weights(r"./CancerNET/rare6class.h5")

inp = gr.DataFrame
label = gr.output.label()

def test_inp(inp):
    print(inp)
    inp = np.asarray(inp)
    print(inp)
    output = dxNet.xnet.predict(inp)
    out = np.asarray(output[1])
    return out

inp = gr.dataFrame()

interface = gr.Interface(fn=test_inp, inputs=inp, outputs=label)
interface.launch(inline=False)
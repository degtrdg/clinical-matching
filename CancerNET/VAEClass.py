import tensorflow as tf
import keras
#from keras.models import Model
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, Layer
from tensorflow.keras.metrics import categorical_crossentropy, binary_crossentropy      # loss_value = tf.keras.backend.sparse_categorical_crossentropy(labels, logits) 
from tensorflow.keras.optimizers import RMSprop, Adam
import keras.backend as K
import pandas as pd
import io
import requests
import numpy as np
import pickle
import time

class topic_layer(Layer):
    '''As defined in 
       "On Completeness-aware Concept-Based Explanations in Deep Neural Networks" section 3 "Defining Completeness of Concepts"
       Here, vc(xt) and vc(x) are calculated as topic prob_n and topic_prob_nn, respectively
       additionally a component of the final model loss is output as an additional tensor that uses the normalized weights, this is l
    '''   
    '''this layer needs a list of inputs [tensor, int] that is the input tensor and the number of concepts'''
    def __init__(self, units=32):
        super(topic_layer, self).__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(
            shape=(input_shape[-1], self.units),
            initializer="random_normal",
            trainable=True,
        )

    def call(self, inputs):
        input_norm = K.l2_normalize(inputs, axis  = -1)
        w_norm = K.l2_normalize(self.w)
        topic_prob = K.dot(inputs, w_norm)
        topic_prob_n = K.dot(input_norm, w_norm)
        topic_prob_mask = K.cast(K.greater(topic_prob_n, 0.2), 'float32')
        topic_prob_a = topic_prob * topic_prob_mask
        topic_prob_sum = K.sum(topic_prob_a, axis = -1, keepdims = True) + 1e-3
        topic_prob_nn = topic_prob_a/topic_prob_sum
        l = K.dot(K.transpose(w_norm), w_norm) - np.eye(self.units)
        return [topic_prob_nn, topic_prob_n, l]
        
class Sampling(Layer):
    """Defines probablistic layer of VAE latent layer
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    #def get_config(self):
        #return {"a": None}
    #@classmethod	
    def get_config(self):
        config = super(Sampling, self).get_config()
        config.update()
        return config	

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.random.normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

def vae_loss(z_mean, z_log_sigma, b_value):
    def loss_calc(y_true, y_pred, sample_weights = None):
        xent_loss = tf.cast(tf.shape(y_true)[1], tf.float32) * tf.keras.metrics.binary_crossentropy(y_true, y_pred)
        #xent_loss = tf.cast(tf.shape(y_true)[1], tf.float32) * tf.keras.metrics.categorical_crossentropy(y_true, y_pred)  #changed
        kl_loss = - b_value * tf.math.reduce_mean(1 + z_log_sigma - tf.math.square(z_mean) - tf.math.exp(z_log_sigma), axis=1)
        return xent_loss + kl_loss
    return loss_calc
    
def topic_loss_toy(topic_prob_n, topic_vector_n, n_concept, loss1, topk = 32, para = 0.1):
  """creates loss for topic model
  NOTE: the topk variable must be >= to the batch size or this will throw an error
  the input topic_prob_n must be the second output of the topic_layer
  the input topic_vector is the last output of the topic_layer
  para can be tuned, it is set to the value used in the 
  """
  def loss(y_true, y_pred):
    return (1.0*tf.reduce_mean(input_tensor=loss1(y_true, y_pred))\
            - para*tf.reduce_mean(input_tensor=(tf.nn.top_k(K.transpose(K.reshape(topic_prob_n,(-1,n_concept))),k=topk,sorted=True).values))
            + para*tf.reduce_mean(input_tensor=topic_vector_n)
            )
  return loss
  
  
def open_file(filename, sep = ",", header = 0, index_col = None, rename = None):
    '''opens a file.
    Capable of opening pickle, csv or txt formats
    for csvs or txt the separator must be indicated
    if a specific index should be used as the column names then index_col may be used and must be the index number
    if index number is unknown but index name is then rename will take the index name and do the same thing as index_col
    '''
   # 

    filetype = filename.split(".")[-1]
    assert filetype == "pickle" or filetype == "csv" or filetype == "txt", "filetype must be 'pickle', txt' or 'csv'"
    if filetype == "pickle":
        
        with open(filename, 'rb') as handle:
            data = pickle.load(handle)
        
    if filetype == "csv":
        #assert type(data) == pd.DataFrame, "to open a 'csv' please ensure the data is a pandas DataFrame"
        data = pd.read_csv(filename, sep = sep, header = header, index_col = index_col)
        
    if filetype == "txt":
        data = pd.read_csv(filename, sep = sep, header = header, index_col = index_col)
        
        if rename != None:
                    data = rename_cols(data, row_name)
    return data   
	
class VAE:
    """
    creates a VAE model of the depth and dimensions defined by user
    Inputs:
        encoder_dims: list of ints with the length of the encoder depth. First entry is size of input
        latent_dim: int, defines the size of the probablistic layer
        decoder_dims: list of ints with the length of the decoder depth
        classifier_dims: list of ints with the length of the classifier depth including the output class layer
                         IF classifier_dims is [None] no classifier will be added to the model and it will train as a VAE
        output_weights: a list of ints of length 2 where the first entry is the weight of the generative loss and the second is the weight of the classification loss
        beta_value
    Call build function to build the vae.
    """
    def __init__(self, encoder_dims, latent_dim, decoder_dims, classifier_dims = None, output_weights = None, e_reg=None, c_reg = None, d_reg = None, extra_latent = False, b_value = 1):
        
        assert type(encoder_dims) == list, "encoder_dims must be a list"
        assert type(latent_dim) == int, "latent_dim must be a an int"
        assert latent_dim > 0, "latent_dim must be non-zero"
        assert type(decoder_dims) == list, "decoder_dims must be a list"
        #assert type(classifier_dims) == list or None, "classifier_dims must be a list"
        #assert len(output_weights) == 2 or None, "output_weights must be of length 2"
        #assert type(output_weights) == list or None, "output_weights must be a list"
        assert type(b_value) == int, "Beta Value must be an Int"
       
        self.output_weights = output_weights
        self.encoder_dims = encoder_dims
        self.latent_dim = latent_dim
        self.decoder_dims = decoder_dims
        self.classifier_dims = classifier_dims
        self.b_value = b_value

        self.e_reg = e_reg
        self.d_reg = d_reg
        self.c_reg = c_reg
        self.extra_latent = extra_latent
    def vae_loss(self, y_true, y_pred):
	    xent_loss = tf.cast(tf.shape(y_true), tf.float32) * tf.keras.metrics.binary_crossentropy(y_true, y_pred)
        #xent_loss = tf.cast(tf.shape(y_true)[1], tf.float32) * tf.keras.metrics.categorical_crossentropy(y_true, y_pred)  #changed
	    kl_loss = - self.b_value * tf.math.reduce_mean(1 + self.z_log_sigma - tf.math.square(self.z_mean) - tf.math.exp(self.z_log_sigma), axis=1)
	    loss_calc = xent_loss + kl_loss
	    return loss_calc

    def make_encoder(self):
        """
        Generates encoder with depth = len(encoder_dims)-1
        """
        self.inputs = Input(shape = (self.encoder_dims[0],), name = 'Input')
        self.e = [self.inputs]
        for i in self.encoder_dims[1:]:
            self.e.append(Dense(i, activation = 'relu', activity_regularizer = self.e_reg)(self.e[-1]))
        self.z_mean = (Dense(self.latent_dim, name = 'z_mean')(self.e[-1]))
        self.z_log_sigma = (Dense(self.latent_dim, name = 'z_log_sigma')(self.e[-1]))
        self.latent= Sampling(name = 'Sampling_layer')([self.z_mean, self.z_log_sigma])
        if self.extra_latent:
            self.latent = Dense(self.latent_dim, activation = 'relu', name = 'latent_layer')(self.latent)
        #return Model(e[0], latent, name = 'encoder')
    def make_encoder_multi(self):
        inputs = Input(shape = (self.encoder_dims[0],), name = 'Input')
        self.e = [inputs]
        for i in self.encoder_dims[1:]:
            self.e.append(Dense(i, activation = 'relu', activity_regularizer = self.e_reg)(self.e[-1]))
        self.z_mean = (Dense(self.latent_dim, name = 'z_mean')(self.e[-1]))
        self.z_log_sigma = (Dense(self.latent_dim, name = 'z_log_sigma')(self.e[-1]))
        self.latent= Sampling(name = 'Sampling_layer')([self.z_mean, self.z_log_sigma])
        return Model(self.e[0], self.latent, name = 'encoder')
    def make_decoder(self):
        """
        Generates decoder with depth = len(decoder_dims) + output layer
        last layer is a sigmoid layer
        """
       # d =[Input(shape = (self.latent_dim,), name = 'decoder_input')]
        for i in self.decoder_dims:
            self.e.append(Dense(i, activation = 'relu', activity_regularizer = self.d_reg)(self.latent))
        self.decoder_out = (Dense(self.encoder_dims[0], activation = 'sigmoid', name = 'decoder_out')(self.e[-1]))
       # return  Model(d[0],d[-1], name = 'decoder')
    def make_decoder_multi(self):
        inputs = Input(shape = (self.latent_dim,), name = 'decoder_input')
        self.d = [inputs]
        for i in self.decoder_dims[:-1]:
            self.d.append(Dense(i, activation = 'relu', activity_regularizer = self.d_reg)(self.d[-1]))
        self.d.append(Dense(self.encoder_dims[1], activation = 'sigmoid', name = 'decoder_out')(self.d[-1]))
        return Model(self.d[0], self.d[-1], name = 'decoder')    
    def make_classifier(self):
        """
        Generates classifier with depth = len(classifier_dims)
        """
        #c =[Input(shape = (self.latent_dim,), name = 'decoder_input')]
        for i in self.classifier_dims[:-1]:
            self.e.append(Dense(i, activation = 'relu', activity_regularizer = self.c_reg)(self.latent))
        self.e.append(Dense(self.classifier_dims[-1], activation = 'softmax', name = 'classifier_out')(self.e[-1]))
        #return  Model(c[0],c[-1], name = 'classifier')
    def make_classifier_multi(self):
        inputs = Input(shape = (self.latent_dim,), name = 'classifier_input')
        self.c = [inputs]
        for i in self.classifier_dims[:-1]:
            self.c.append(Dense(i, activation = 'relu', activity_regularizer = self.c_reg)(self.c[-1]))
        self.c.append(Dense(self.classifier_dims[-1], activation = 'softmax', name = 'classifier_out')(self.c[-1]))
        return Model(self.c[0], self.c[-1], name = 'classifier') 
    def build_flat(self, class_loss = categorical_crossentropy, e = False):
        '''
        builds VAE but without using multiple model
	class_loss can be any loss or can be VAE loss, use "VAE" for vae loss
	default of class loss is "categorical_crossentropy"
        '''
        self.class_loss = class_loss
        #self.outputs = [self.decoder(self.encoder(self.inputs)), self.classifier(self.encoder(self.inputs))]
        self.encoder = self.make_encoder()
        self.decoder = self.make_decoder()
        if self.classifier_dims != None:
            self.classifier = self.make_classifier()
            self.full_vae = Model(self.inputs, [self.e[-1], self.decoder_out], name = 'VAE_w_classifier')
            if class_loss == "VAE":
                self.full_vae.compile(optimizer = 'RMSprop', loss = [self.vae_loss, self.vae_loss], loss_weights = self.output_weights)
            else:
                if e:
                    print('yep')
                    self.full_vae.compile(optimizer = 'RMSprop', loss = [vae_loss(self.z_mean, self.z_log_sigma, b_value = 1), self.class_loss], loss_weights = self.output_weights)
                else:
                    self.full_vae.compile(optimizer = 'RMSprop', loss = [self.class_loss, self.vae_loss], loss_weights = self.output_weights)
        else:
            self.full_vae = Model(self.inputs, self.decoder_out)
            self.full_vae.compile(optimizer = 'RMSprop', loss = self.vae_loss)

        self.full_vae.summary()
	
    def build_multimodel(self, class_loss = categorical_crossentropy):
        '''
		Builds a multimodel VAE composed of an encoder, decoder and classifier model.
		Does not support VAE only or multi-VAE loss
		''' 
        self.class_loss = class_loss
        #self.outputs = [self.decoder(self.encoder(self.inputs)), self.classifier(self.encoder(self.inputs))]
        self.encoder = self.make_encoder_multi()
        self.decoder = self.make_decoder_multi()
        self.classifier = self.make_classifier_multi()
        self.xnet = Model(self.e[0], [self.decoder(self.encoder(self.e[0])), self.classifier(self.encoder(self.e[0]))])
        self.xnet.compile(optimizer = 'RMSprop', loss = [self.class_loss, vae_loss(self.z_mean, self.z_log_sigma, b_value = 1)], loss_weights = self.output_weights)

    def latent_model(self):
        '''split model at latent layer'''
        self.lat_model = Model(self.full_vae.layers[0].input, self.full_vae.get_layer('Sampling_layer').output)
    def class_model(self):
        '''gets classifier only'''
        self.classifier_model = Model(self.full_vae.get_layer('dense_3'), self.full_vae.get_layer('classifier_out').output)
    def generator_model(self):
        '''gets generator only'''
        self.gen_model = Model(self.full_vae.get_layer('dense_2').input, self.full_vae.get_layer('decoder_out').output)
        
    def make_topic_model(self,lat_embed_train, y_train, lat_embed_val, y_val, n_conc, pretrain = False, filename = 'topic_model_' + time.strftime("%Y%m%d-%H%M%S")+'.h5', topk = 32, para = 1.0):
        """
        Generates topic model as described in Jon D Mcauliffe and David M Blei. Supervised topic models. In NIPS, 2008 and 
        Yeh, Chih-Kuan, et al. "On completeness-aware concept-based explanations in deep neural networks." Advances in Neural Information Processing Systems 33 (2020): 20554-20565.
        Topic layer is Vc() of Yeh, et. al. 
        rec1 and rec2 comprise g() of Yeh, et. al. 
        finally the classifier is h()
        so we implement h(gf(vc(x))) we input x as the latent embeddings, this is classifier(rec_layers(topic_layer(latent_embeddings))) = classifier_output
        """
        self.topk = topk
        self.t = []
        self.t.append(Input(self.latent_dim))
        t_layer, self.t_n, l = topic_layer(n_conc)(self.t[-1])
        self.t.append(t_layer)
        self.t.append(Dense(n_conc*10, activation = 'relu', use_bias = False, name = 'rec_1')(self.t[-1]))
        self.t.append(Dense(self.latent_dim, activation = None, use_bias = False, name = 'rec_2')(self.t[-1]))
        #now append the classifier layers of diseasenet 
        #easiest way is to just make new layers and load the weights of the layers in. since dnet is already loaded this should be simple
        for i in self.classifier_dims[:-1]:
            self.t.append(Dense(i, activation = 'relu', activity_regularizer = self.c_reg)(self.t[-1]))
        self.t.append(Dense(self.classifier_dims[-1], activation = 'softmax', name = 'classifier_out')(self.t[-1]))
        self.topic_model = Model(self.t[0], self.t[-1], name = 'Topic_Model')
        self.topic_model.compile(loss=topic_loss_toy(self.t_n, l, n_conc, loss1=self.class_loss, para = para), metrics = ['accuracy'], optimizer= Adam(lr=0.001))
        #reassign classifier weights
        self.topic_model.summary()
        layer_dict = {'dense_3': -2,'classifier_out': -1}
        for k in layer_dict.keys():
            self.topic_model.layers[layer_dict[k]].set_weights(self.full_vae.get_layer(k).get_weights())
        if pretrain:
            self.topic_model.load_weights(filename)
        else:
            self.topic_model.layers[-2].trainable = False
            self.topic_model.layers[-1].trainable = False
            self.topic_model.compile(loss=topic_loss_toy(self.t_n, l, n_conc, loss1=self.class_loss, para = para, topk = self.topk), metrics = ['accuracy'], optimizer= Adam(lr=0.001))
            self.topic_model.summary(show_trainable = True)
            callback_early = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=100, verbose = 1)

            checkpoint_callback=tf.keras.callbacks.ModelCheckpoint(filepath= filename,
                                                       monitor='loss',
                                                       save_best_only=True,
                                                       save_weights_only=True,
                                                       mode='auto',
                                                       verbose = 1)
            CheckNaN = keras.callbacks.TerminateOnNaN()

            self.topic_model.fit(lat_embed_train, y_train, validation_data= (lat_embed_val, y_val), callbacks=[callback_early, checkpoint_callback, CheckNaN], batch_size = 7, epochs = 100000, verbose =2) 




import os
import json
import numpy as np
import pandas as pd
import tensorflow as tf
# from tensorflow import keras
import keras
from sklearn.preprocessing import RobustScaler, MinMaxScaler


@tf.function
def vae_loss(model, x):
    z_mean, z_log_var, z = model.encoder(x)
    reconstruction = model.decoder(z)
    reconstruction_loss = x.shape[1] * keras.metrics.binary_crossentropy(x, reconstruction)
    kl_loss = - 0.5 * tf.reduce_sum(1 + z_log_var - tf.square(z_mean) - 
                            tf.exp(z_log_var), axis=-1)
    total_loss = reconstruction_loss + kl_loss
    return total_loss, reconstruction_loss, kl_loss

class VAEBetaLoss:
    def __init__(self, beta):
        self.beta = beta

    def loss(self, model, x):
        z_mean, z_log_var, z = model.encoder(x)
        reconstruction = model.decoder(z)
        reconstruction_loss = x.shape[1] * keras.metrics.binary_crossentropy(x, reconstruction)
        kl_loss = - 0.5 * tf.reduce_sum(1 + z_log_var - tf.square(z_mean) - 
                                tf.exp(z_log_var), axis=-1)
        total_loss = reconstruction_loss + (self.beta * kl_loss)
        return total_loss, reconstruction_loss, kl_loss

@keras.saving.register_keras_serializable(package="netvae")
class Sampling(keras.layers.Layer):
    """Uses (z_mean, z_log_var) to sample z"""

    def call(self, inputs):
        z_mean, z_log_var = inputs
        batch = tf.shape(z_mean)[0]
        dim = tf.shape(z_mean)[1]
        epsilon = tf.random.normal(shape=(batch, dim))
        return z_mean + tf.exp(0.5 * z_log_var) * epsilon

class VAE(keras.Model):
    def __init__(self,features, encoder, decoder, loss=vae_loss, **kwargs):
        super().__init__(**kwargs)
        self.encoder = encoder
        self.decoder = decoder
        self.features = features
        self.loss = loss
        self.total_loss_tracker = keras.metrics.Mean(name="total_loss")
        self.reconstruction_loss_tracker = keras.metrics.Mean(
            name="reconstruction_loss"
        )
        self.kl_loss_tracker = keras.metrics.Mean(name="kl_loss")

    @property
    def metrics(self):
        return [
            self.total_loss_tracker,
            self.reconstruction_loss_tracker,
            self.kl_loss_tracker,
        ]

    def train_step(self, data):
        """VAE training step"""
        with tf.GradientTape() as tape:
            total_loss, reconstruction_loss, kl_loss = self.loss(self, data)

        grads = tape.gradient(total_loss, self.trainable_weights)
        self.optimizer.apply_gradients(zip(grads, self.trainable_weights))
        self.total_loss_tracker.update_state(total_loss)
        self.reconstruction_loss_tracker.update_state(reconstruction_loss)
        self.kl_loss_tracker.update_state(kl_loss)
        return {
            "loss": self.total_loss_tracker.result(),
            "reconstruction_loss": self.reconstruction_loss_tracker.result(),
            "kl_loss": self.kl_loss_tracker.result(),
        }
    
    def save(self, path):
        """Save model elements (encoder and decoder) with features index"""
        if not os.path.exists(path):
            os.makedirs(path)

        self.encoder.save( os.path.join(path, "model.enc.keras") )
        self.decoder.save( os.path.join(path, "model.dec.keras") )

        with open( os.path.join(path, "index"), "wt", encoding="ascii") as handle:
            handle.write(json.dumps( list(self.features) ))


class NetVae:
    def __init__(self, features, encoder=None, decoder=None):
        self.features = features
        self.encoder = encoder
        self.decoder = decoder
        self.latent_groups = None
        self.latent_index = None
        self.history = None
        self.normal_stats = None

    def run_train(self, df, latent_index,
                latent_groups=None,
                learning_rate=0.001, batch_size=128,
                phases = None, epochs=80
             ):
        feature_dim = len(df.columns)
        latent_dim = len(latent_index)
                
        constraint = NetworkConstraint(list(df.columns), latent_index, latent_groups)
        constraint.set_active(False)

        encoder = build_encoder(feature_dim, latent_dim, constraint)
        decoder = build_decoder(feature_dim, latent_dim)
        
        vae = VAE(self.features, encoder, decoder)

        vae.compile(optimizer=keras.optimizers.Adam(learning_rate=learning_rate))

        if phases is not None:
            epochs = sum(phases)    
            nc = NetTrainingCallback(constraint, phases)
            history = vae.fit(df, 
                        epochs=epochs, batch_size=batch_size, shuffle=True,
                        callbacks=[nc]
            )
        else:
            history = vae.fit(df, epochs=epochs, batch_size=batch_size, shuffle=True)

        self.latent_groups = latent_groups
        self.latent_index = latent_index
        self.decoder = decoder
        self.encoder = encoder
        self.history = history

        normal_pred = pd.DataFrame( 
            self.decoder.predict(self.encoder.predict(df)[0]), index=df.index, columns=df.columns)
        self.normal_stats = pd.DataFrame( 
            {"mean": (normal_pred - df).mean(), "std" : (normal_pred - df).std()}
        )

    def save(self, path, normal_df=None):
        """Save VAE model with associted elements"""
        if not os.path.exists(path):
            os.makedirs(path)

        self.encoder.save( os.path.join(path, "model.enc.keras") )
        self.decoder.save( os.path.join(path, "model.dec.keras") )

        with open( os.path.join(path, "index"), "wt", encoding="ascii") as handle:
            handle.write(json.dumps( list(self.features) ))

        with open( os.path.join(path,"net.groups.tsv"), "wt", encoding="ascii") as handle:
            for g in self.latent_index:
                n = self.latent_groups[g]
                handle.write("\t".join( [str(g), *n] ))
                handle.write("\n")

        with open( os.path.join(path, "stats.json"), "wt", encoding="ascii") as handle:
            handle.write(
                json.dumps({
                "loss_history" : self.history.history["loss"]
            }))

        if normal_df is not None:
            self.normal_stats.to_csv(os.path.join(path, "training.stats.tsv"), sep="\t")


def Open(path):
    """open VAE model directories"""
    enc = keras.models.load_model(os.path.join(path, "model.enc.keras"), 
                                  custom_objects={"NetworkConstraint":NetworkConstraint})
    dec = keras.models.load_model(os.path.join(path, "model.dec.keras"), 
                                  custom_objects={"NetworkConstraint":NetworkConstraint})

    with open(os.path.join(path, "index"), "rt", encoding="ascii") as handle:
        index = json.load(handle)

    netfile = os.path.join(path,"net.groups.tsv")
    if os.path.exists( netfile ):
        out = NetVae(index, encoder=enc, decoder=dec)
        out.normal_stats = pd.read_csv(os.path.join(path, "training.stats.tsv"), sep="\t", index_col=0)
        with open( netfile, "rt", encoding="ascii") as handle:
            groups = {}
            group_index = []
            for line in handle:
                row = line.rstrip().split("\t")
                group_index.append(row[0])
                groups[row[0]] = row[1:]
            out.latent_groups = groups
            out.latent_index = group_index
    else: 
        out = VAE(index, enc, dec)

    return out



class NetTrainingCallback(tf.keras.callbacks.Callback):
    def __init__(self, netConstraint, phases):
        super().__init__()
        self.netConstraint = netConstraint
        self.phaseEnds = []
        self.nodeGroups = []
        self.nodeDFs = []
        s = 0
        for i in phases:
            s += i
            self.phaseEnds.append(s)
            
    def calc_netgroups(self):
        path_weights = pd.DataFrame(self.model.encoder.weights[0], index=subDF.columns)
        scoreDF = pd.DataFrame(softmax(path_weights.abs(), axis=1), index=path_weights.index, columns=path_weights.columns)
    
        nodeDF = groupNodes(scoreDF, G)
        nodeGroup = {}
        for i in nodeDF:
            nodeGroup[i] = list(nodeDF.index[ nodeDF[i] == 1.0 ])
        return nodeDF, nodeGroup

    def on_epoch_begin(self, epoch, logs):
        for i,j in enumerate(self.phaseEnds):
            if j == epoch:
                if (i%2) == 0:
                    print("Start constraint phase")
                    nodeDF, nodeGroup = self.calc_netgroups()
                    self.nodeGroups.append(nodeGroup)
                    self.nodeDFs.append(nodeDF)
                    self.netConstraint.update_membership(nodeGroup)
                    self.netConstraint.set_active(True)
                else:
                    print("Start unconstrained phase")
                    nonZeroCount = len( np.nonzero( self.model.encoder.weights[0] )[0] )
                    print("non-zeros: %d" % (nonZeroCount))
                    self.netConstraint.set_active(False)

#@keras.saving.register_keras_serializable(package="netvae")
class NetworkConstraint(tf.keras.constraints.Constraint):
    def __init__(self, feature_index, latent_index, latent_membership):
        self.feature_index = feature_index
        self.latent_index = latent_index
        self.latent_membership = latent_membership
        self.active = True
        self.mask = tf.Variable( np.zeros([len(self.feature_index),len(self.latent_index)]).astype("float32") )
        self.update()
        
    def update_membership(self, latent_membership):
        self.latent_membership = latent_membership
        self.update()
    
    def set_active(self, a):
        self.active = a
        
    def update(self):
        if self.latent_membership is not None:
            print("Updating mask")
            f = np.zeros([len(self.feature_index),len(self.latent_index)]).astype("float32")
            gi = pd.Index(self.latent_index)
            for pi, p in enumerate(self.latent_index):
                for g in self.latent_membership[p]:
                    if g in gi:
                        f[gi.get_loc(g)][pi] = 1
            print("changing mask to custom")
            self.mask.assign( f )
        else:
            print("changing mask to ones")
            self.mask.assign( np.ones([len(self.feature_index),len(self.latent_index)]).astype("float32")  )

    def __call__(self, w):
        return w * self.mask

    def get_config(self):
        #print("config", self.gene_index, self.pathway_index, self.latent_membership)
        return {'feature_index': self.feature_index, "latent_index" : self.latent_index, "latent_membership" : self.latent_membership}


def build_encoder(feature_dim, latent_dim, constraint=None, batch_norm=False):
    encoder_inputs = keras.Input(shape=(feature_dim,), name="input_1")
    ei = encoder_inputs
    if batch_norm:
        ei = keras.layers.BatchNormalization(encoder_inputs)
    activation = "relu" # "sigmoid"
    pathway_layer = keras.layers.Dense(
        latent_dim,
        activation=activation,
        kernel_initializer='glorot_uniform',
        kernel_constraint=constraint,
        name="pathway_layer")(ei)
    x = pathway_layer
    x = keras.layers.BatchNormalization(name="batchnorm")(x)
    z_mean = keras.layers.Dense(latent_dim, name="z_mean")(x)
    z_log_var = keras.layers.Dense(latent_dim, name="z_log_var")(x)
    z = Sampling()([z_mean, z_log_var])
    encoder = keras.Model(encoder_inputs, [z_mean, z_log_var, z], name="encoder")
    
    print(encoder.summary())
    return encoder


def build_decoder(feature_dim, latent_dim):
    latent_inputs = keras.Input(shape=(latent_dim,))
    activation = "relu" # "sigmoid"
    x = keras.layers.Dense(
        feature_dim, kernel_initializer='glorot_uniform', 
        activation=activation, name="decoder_input")(latent_inputs)
    decoder_outputs = x
    decoder = keras.Model(latent_inputs, decoder_outputs, name="decoder")
    print(decoder.summary())
    return decoder

def extract_pathway_interactions(sif_path, relation='controls-expression-of'):
    pc = pd.read_csv(sif_path, sep="\t", 
                     header=None, names=["from", "relation", "to"])
    pc = pc[ ~(pc['from'].map(lambda x:"CHEBI" in x) | pc['to'].map(lambda x:"CHEBI" in x)) ]
    return pc[ pc["relation"] == relation ]




######
# Tools
######


def procrustes(X, Y):
    """
    Computes the Procrustes transformation between two matrices.

    Args:
        X: The first matrix.
        Y: The second matrix.

    Returns:
        Rotation matrix
    """
    # Ensure matrices have the same dimensions
    assert X.shape == Y.shape
    # Compute the singular value decomposition (SVD)
    U, S, Vt = np.linalg.svd(np.dot(X.T, Y))
    # Determine the rotation matrix
    R = np.dot(Vt.T, U.T)
    return R.T

def quantileMaxNorm(df, quantile_max=0.9):
    normDF = (df.transpose() / df.quantile(quantile_max, axis=1)).transpose().clip(upper=1.0, lower=0.0).fillna(0.0)
    return normDF

def expMaxNorm(df):
    t = np.log2(df+1)
    return (t.transpose() / t.max(axis=1)).transpose()

class ExpMinMaxScaler(MinMaxScaler):
    def fit(self, X):
        return MinMaxScaler.fit(self, np.log2(X+1))
    def transform(self, X):
        return MinMaxScaler.transform(self, np.log2(X+1))
    def inverse_transform(self, X):
        return np.exp2(MinMaxScaler.inverse_transform(self, X))-1

def calcRmsd(array1, array2):
    if len(array1) != len(array2):
        raise ValueError("Arrays must be of the same length")

    diff = array1 - array2
    squared_diff = diff ** 2
    mean_squared_diff = np.mean(squared_diff)
    rmsd = np.sqrt(mean_squared_diff)

    return rmsd
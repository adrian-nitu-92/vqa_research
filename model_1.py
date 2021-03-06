from keras.layers import Dense, Dropout, LSTM, Activation
from keras.layers import merge, Input
from keras.models import Model
from keras import regularizers


# Define our model
def text_model(text_input, dropout_rate, regularization_rate):
    print("Creating text model...")
    model = Activation('tanh')(text_input)
    model = LSTM(units=1024, return_sequences=True)(model)
    model = Dropout(dropout_rate)(model)
    model = LSTM(units=1024)(model)
    model = Dropout(dropout_rate)(model)
    model = Dense(1024, activation='tanh', kernel_regularizer=regularizers.l2(regularization_rate))(model)
    return model


def img_model(img_input, regularization_rate):
    print("Creating image model...")
    model = Dense(1024, activation='tanh', kernel_regularizer=regularizers.l2(regularization_rate))(img_input)
    return model


def model_1(embedding_dim, dropout_rate, regularization_rate, num_classes):
    img_input = Input(shape=(2048,))
    text_input = Input(shape=(None, embedding_dim))

    vgg_model = img_model(img_input, regularization_rate)
    lstm_model = text_model(text_input, dropout_rate, regularization_rate)
    print("Merging final model...")
    fc_model = merge([vgg_model, lstm_model], mode='mul')
    fc_model = Dropout(dropout_rate)(fc_model)
    fc_model = Dense(1000, activation='tanh', kernel_regularizer=regularizers.l2(regularization_rate))(fc_model)
    fc_model = Dropout(dropout_rate)(fc_model)
    fc_model = Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l2(regularization_rate))(fc_model)
    model = Model(inputs=[img_input, text_input], outputs=fc_model)
    model.compile(optimizer='rmsprop', loss='categorical_crossentropy',
                     metrics=['accuracy'])
    print (model.summary())
    return model

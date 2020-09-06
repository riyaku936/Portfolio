from pyimagesearch.models import SudokuNet
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.datasets import mnist
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
import argparse

# we get the path to save the model in from the command line when the python command is made 
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="path to output model after training")
args = vars(ap.parse_args())

# setting the hyperparameters (found after researching and testing)
INIT_LR = 1e-3
EPOCHS = 10
BS = 128

# we need to get the MNIST dataset that we will use to train the model 
((train, train_labels), (test, test_labels)) = mnist.load_data()


train = train.reshape((train.shape[0], 28, 28, 1))
test = test.reshape((test.shape[0], 28, 28, 1))


train = train.astype("float32") / 255.0
test = test.astype("float32") / 255.0

# One-hot encode labels and convert the labels from integers to vectors
le = LabelBinarizer()
trainLabel_l = le.fit_transform(trainLabel_l)
test_labels = le.transform(test_labels)


# initialize the optimizer and model
print("[INFO] compiling model...")
opt = Adam(lr=INIT_LR)
model = SudokuNet.build(width=28, height=28, depth=1, classes=10)
model.compile(loss="categorical_crossentropy", optimizer=opt,
	metrics=["accuracy"])



# training network
training = model.fit(
	train, trainLabel_l,
	validation_data=(test, test_labels),
	batch_size=BS,
	epochs=EPOCHS,
	verbose=1)


# evaluate the network using test data 
predictions = model.predict(test)

# print a classification report
print(classification_report(
	test_labels.argmax(axis=1),
	predictions.argmax(axis=1),
	target_names=[str(x) for x in le.classes_]))

# save model to disk 
print("[INFO] serializing digit model...")
model.save(args["model"], save_format="h5")



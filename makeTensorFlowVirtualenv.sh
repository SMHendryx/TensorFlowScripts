# Makes TensorFlow virtualenv for Python 3 following https://www.tensorflow.org/install/install_mac
# Also installs Keras into environment
# Should be run interactively

sudo easy_install pip
pip install --upgrade virtualenv 
targetDirectory=~/virtualenvs/TensorFlow
virtualenv --system-site-packages -p python3 $targetDirectory

cd $targetDirectory
source ./bin/activate  

#Ensure pip ≥8.1 is installed:
easy_install -U pip

pip3 install --upgrade tensorflow

python
import tensorflow as tf
hello = tf.constant('Hello, TensorFlow!')
sess = tf.Session()
print(sess.run(hello))
exit()


pip install keras

#Test:
python
import keras
exit()

deactivate



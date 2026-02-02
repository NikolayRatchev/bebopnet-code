import pickle

p='training_results/transformer/model'
print("train songs:", len(pickle.load(open(p+'/train.pkl','rb'))))
print("val songs:", len(pickle.load(open(p+'/val.pkl','rb'))))
pickle.load(open(p+'/converter_and_duration.pkl','rb'))
print("converter OK")


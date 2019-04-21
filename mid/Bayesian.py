import math

#Posterior(class_1)=P(class_1)*P(attr1)*P(attr2)*P(attr3)/evidence

#evidence=所有 Posterior(class_1) 上面相加

mean=0
var=1
test_attr=-1
p = (1 / math.sqrt(2 * math.pi * var)) * math.exp( (math.pow((test_attr - mean), 2) / (-2 * var))) #Naïve Bayesian classifier
print(p)
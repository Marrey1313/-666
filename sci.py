X=[0,1,2,3,4,5,6,7]
y=[6,5,5,2,7,2,5,2]
import numpy as np
X=np.array(X).reshape(-1,1)
y=np.array(y)
from sklearn.linear_model import LinearRegression
model=LinearRegression()
model.fit(X,y)
print(model.coef_,model.intercept_)
y_p=model.predict(X)
#print(y_p[:4])
from sklearn import metrics
print(metrics.root_mean_squared_error(y, y_p), y.mean())
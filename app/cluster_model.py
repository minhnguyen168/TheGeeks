# Import libraries
import numpy as np
import pandas as pd
import datetime
import matplotlib
from datetime import datetime
from matplotlib import colors
import plotly.express as px
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from matplotlib.colors import ListedColormap
from sklearn import metrics
import warnings
import sys
from datetime import date
from app import db
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)

# resultslist=[]
#     for result in df:
#         resulttemp=[]
#         for indiv in result:
#             resulttemp.append(indiv)
#         resultslist.append(resulttemp)
class clustering:
    def AC_cluster(df):
        def age(birthdate):
            today = date.today()
            hi = today.year - datetime.strptime(birthdate, '%Y/%m/%d').year - ((today.month, today.day) < (datetime.strptime(birthdate, '%Y/%m/%d').month, datetime.strptime(birthdate, '%Y/%m/%d').day))
            return hi
        df['age']=0
        for n in range(0,df.shape[0]):
            df['age'][n]=age(df['dateofbirth'][n])
        LE=LabelEncoder()
        obj=['city','investmentgoal','dropvalue','prioritiesofinvestment']
        for i in obj:
            df[i]=df[[i]].apply(LE.fit_transform)
        new_df = df.drop(['dateofbirth'],axis=1)
        scaler = StandardScaler()
        scaler.fit(new_df)
        scaled_features = pd.DataFrame(scaler.transform(new_df),columns= new_df.columns )
        pca = PCA(n_components=3)
        pca.fit(scaled_features)
        PCA_df = pd.DataFrame(pca.transform(scaled_features), columns=(["col1","col2", "col3"]))
        from sklearn.cluster import KMeans
        from sklearn.datasets import make_blobs
        from yellowbrick.cluster import KElbowVisualizer
        Elbow_M = KElbowVisualizer(KMeans(), k=10)
        Elbow_M.fit(PCA_df)
        Elbow_M.show()
        k_value=Elbow_M.elbow_value_
        #Initiating the Agglomerative Clustering model 
        AC = AgglomerativeClustering(n_clusters=k_value)
        # fit model and predict clusters
        AC_df = AC.fit_predict(PCA_df)
        PCA_df["Clusters"] = AC_df
        #Adding the Clusters feature to the orignal dataframe.
        df["Clusters_AC"]= AC_df
        attributes=['annualincome','estimatednetworth','endgoal','valueofcurrentinvestment','age']
        for i in attributes:
            plt.figure()
            pl=sns.swarmplot(x=df['Clusters_AC'], y=df[i], color= "#CBEDDD", alpha=0.5 )
            pl=sns.boxenplot(x=df['Clusters_AC'], y=df[i])
            plt.savefig(f'app/static/images/AC_cluster_{i}.png')
        return df


    

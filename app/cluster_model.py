# Import libraries
import numpy as np
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors
import plotly.express as px
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt, numpy as np
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from matplotlib.colors import ListedColormap
from sklearn import metrics
import warnings
import sys
if not sys.warnoptions:
    warnings.simplefilter("ignore")
np.random.seed(42)

# df=db.session.execute('SELECT c.client_id, u.dateofbirth, u.city, f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.age, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue FROM User u, Client c, FinancialGoal f WHERE u.banker=0 AND u.id =c.userid AND c.client_id=f.client_id')
# resultslist=[]
#     for result in df:
#         resulttemp=[]
#         for indiv in result:
#             resulttemp.append(indiv)
#         resultslist.append(resulttemp)

import sqlite3
import pandas as pd

cnx = sqlite3.connect('site.db')

df = pd.read_sql_query("SELECT c.client_id, u.dateofbirth, u.city, f.investmentgoal, f.yeartorealisegoal, f.endgoal, f.age, f.annualincome, f.estimatednetworth, f.topupamountmonthly, f.valueofcurrentinvestment, f.equity, f.fixedincome, f.forexcommodities, f.mutualfund, f.crypto, f.realestate, f.otherinvestment, f.prioritiesofinvestment, f.riskappetite, f.dropvalue FROM User u, Client c, FinancialGoal f WHERE u.banker=0 AND u.id =c.userid AND c.client_id=f.client_id", cnx)
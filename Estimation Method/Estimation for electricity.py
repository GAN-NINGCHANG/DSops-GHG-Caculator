# %%
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# %% [markdown]
# **Date preprocessing**

# %%
df = pd.read_excel('../data/Listing of Building Energy Performance Data for 2020.xlsx').iloc[:,3:] # Delete the first three columns about name and address of the building
df.columns = ['main function','size','beginning year','green mark rating','green mark year',
                'green mark type','GFA','AC percent','monthly occupation rate','number of hotel rooms',
                'AC type','age of chiller','AC efficiency','last chiller check year','LED percent',
                'Use of PV','2017EUI','2018EUI','2019EUI','2020EUI']
df.head()
# df.shape # (566,20)

# %%
# Checking missing values
df.isna().sum()

# %%
df2 = df.copy()
df2.dropna(subset=['main function'], inplace=True)
df2.isna().sum()

# %%
# df2[df2['size].isna()] # Main function and GFA of the building are known, try to change the value based on the rule
## Large Size Commercial Buildings: 
# i) Hotel - GFA ≥ 7,000 m²
# ii) Office; Hotel; Retail - GFA ≥ 15,000 m²
# Small Size Commercial Buildings: 
# i) Hotel - GFA < 7,000 m²
# ii) Office; Hotel; Retail - GFA < 15,000 m²
## Encoding 'lagre' as 1 and 'small' as 0
def size_category(row):
    if row['main function'] == 'Hotel':
        return 1 if row['GFA'] >= 7000 else 0
    else:
        return 1 if row['GFA'] >= 15000 else 0
df2['size']= df2.apply(size_category,axis=1)
df2['size'].value_counts()

# %%
df2.shape

# %%
df2.isna().sum()

# %%
# df['green mark rating'].value_counts() # Platinum, 126; Gold, 83; GoldPlus, 60; Certified, 26; Legislated, 22
df2 = pd.get_dummies(df2, columns=['main function'])
df2['green mark rating'] = df2['green mark rating'].fillna('Unknown')
df2 = pd.get_dummies(df2, columns=['green mark rating','green mark type'])
del df2['green mark year']
df2['number of hotel rooms'] = df2['number of hotel rooms'].fillna(0)
del df2['last chiller check year']
df2['Use of PV'] = df2['Use of PV'].map({'Y': 1, 'N': 0})
df2.isna().sum()

# %%
df2.dropna(subset=['age of chiller'], inplace=True)
df2[df2['AC efficiency'].isna()]['AC type'].value_counts()

# %%
df2['AC efficiency'] = df2['AC efficiency'].fillna(df2.groupby('AC type')['AC efficiency'].transform('mean'))
df2 = pd.get_dummies(df2, columns=['AC type'])
df2.isna().sum()

# %% [markdown]
# **Model Construction**

# %%
X = df2.drop(['2017EUI','2018EUI','2019EUI','2020EUI'],axis=1)
y = df2['2020EUI']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')

cv_mse = -cv_scores.mean()
print(f"MSE: {cv_mse}")

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"MSE: {mse}")

r2 = r2_score(y_test, y_pred)
print(f"r2:{r2}")

# %%
X = df2.drop(['2017EUI','2018EUI','2019EUI','2020EUI'],axis=1)
y = df2['2020EUI']*df2['GFA']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_model = RandomForestRegressor(n_estimators=100, random_state=42)

cv_scores = cross_val_score(rf_model, X_train, y_train, cv=5, scoring='neg_mean_squared_error')

cv_mse = -cv_scores.mean()
print(f"MSE: {cv_mse}")

rf_model.fit(X_train, y_train)

y_pred = rf_model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
print(f"MSE: {mse}")

r2 = r2_score(y_test, y_pred)
print(f"r2:{r2}")

# %%
from imblearn.over_sampling import SMOTE

# 假设只对类别和二进制特征进行增强
X = df.drop(columns=['2020EUI'])  # 将目标列去掉
y = df['2020EUI']  # 假设 2020EUI 是一个标签列，用于分类

smote = SMOTE()
X_resampled, y_resampled = smote.fit_resample(X, y)

# 生成新的DataFrame
df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
df_resampled['2020EUI'] = y_resampled
df_resampled.to_csv('synthetic_data.csv', index=False)

# %%
df2.to_csv('df2.csv',index=False)

# %% [markdown]
# **Synthesize Data**

# %%
import torch
import torch.nn as nn


# 假设现有数据集 df
data = df3.values  # 转换为 numpy array 格式

# 定义生成器
class Generator(nn.Module):
    def __init__(self, input_dim, output_dim):
        super(Generator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, output_dim)
        )

    def forward(self, x):
        return self.model(x)

# 定义判别器
class Discriminator(nn.Module):
    def __init__(self, input_dim):
        super(Discriminator, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, 128),
            nn.LeakyReLU(0.2),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )

    def forward(self, x):
        return self.model(x)

# 参数设置
input_dim = 10  # 随机噪声的维度，可以根据需求调整
output_dim = data.shape[1]  # 输出维度与数据特征维度相同
num_epochs = 10000
batch_size = 64
learning_rate = 0.0002

# 初始化生成器和判别器
generator = Generator(input_dim=input_dim, output_dim=output_dim)
discriminator = Discriminator(input_dim=output_dim)

# 定义损失函数和优化器
criterion = nn.BCELoss()
optimizer_G = torch.optim.Adam(generator.parameters(), lr=learning_rate)
optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=learning_rate)

# 开始训练
for epoch in range(num_epochs):
    # 训练判别器
    real_data = torch.tensor(data[np.random.randint(0, data.shape[0], batch_size)], dtype=torch.float32)
    fake_data = generator(torch.randn(batch_size, input_dim))

    real_labels = torch.ones(batch_size, 1)
    fake_labels = torch.zeros(batch_size, 1)

    # 判别器的损失
    outputs = discriminator(real_data)
    d_loss_real = criterion(outputs, real_labels)
    outputs = discriminator(fake_data.detach())
    d_loss_fake = criterion(outputs, fake_labels)
    d_loss = d_loss_real + d_loss_fake

    optimizer_D.zero_grad()
    d_loss.backward()
    optimizer_D.step()

    # 训练生成器
    fake_data = generator(torch.randn(batch_size, input_dim))
    outputs = discriminator(fake_data)
    g_loss = criterion(outputs, real_labels)

    optimizer_G.zero_grad()
    g_loss.backward()
    optimizer_G.step()

    # 打印损失
    if epoch % 1000 == 0:
        print(f"Epoch [{epoch}/{num_epochs}], d_loss: {d_loss.item()}, g_loss: {g_loss.item()}")

# 生成新的合成数据
num_samples = 100  # 想生成的数据样本数
latent_samples = torch.randn(num_samples, input_dim)
generated_data = generator(latent_samples).detach().numpy()

# 转换为 DataFrame 格式
df_generated = pd.DataFrame(generated_data, columns=df.columns)
# df_generated.to_csv('synthetic_data.csv', index=False)



# %%
df3 = df2.astype({col: 'int' for col in df2.select_dtypes('bool').columns})
df3.dtypes



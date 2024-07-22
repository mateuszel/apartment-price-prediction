# Apartments Price Preditction - Results
### Goal
My goal was to build a model capable of predicting prices of apartments in Warsaw.

### Data Source
The data I will be using comes from Otodom website and I got it using my own [webscraper](https://github.com/mateuszel/otodom-datascraper).

### Data Cleaning and EDA (eda.ipynb)
#### Formatting and cleaning the data
Most of the data included non-numeric characters, so I had to format it. This allowed me to find the amount of missing values in each column.
| Column | Missing Values |
| --- | ---: |
|total_price  |     2376|
|price_per_sqm  |   2376|
|area         |        0|
|rooms         |       0|
|finished      |   26232|
|floor         |     440|
|rent          |   16246|
|elevator      |    3892|
|built         |    7063|
|b_type        |    8209|
|link          |       0|
|max_floor     |    1260|
|balcony       |    8565|
|terrace       |    8565|
|garden        |    8565|
|street        |    7618|
|district      |     313|
|subdistrict   |     786|
|nbhood        |   19279|

#### Imputing missing values

Columns that had the most *NaN* values were entirely dropped and all rows with missing values in my target variable column were dropped aswell.

Methods of imputing missing values in selected columns:

* Values in column **rent** are strongly connected to 
both **area* and *district**, so I imputed missing values by calculating mean **rent_per_sqm** for each **district** and multiplying it by apartments **area**.
* For columns **balcony**, **terrace** and **garden** I was able to eliminate some incorrect data after plotting it:
![Image 1](img/bal_ter_gar.png)
After that I imputed missing values by calculating the probability of apartment having a **balcony** / **garden** / **terrace** base on its **district** and **floor**. 
* Plotting the relation between **b_type** and **built** allowed me to easily impute missing values based on corresponding **b_type** / **built** column since they are heavily related(as shown below).
![Image 2](img/btyp.png)
* In **elevator** column after plotting the data I noticed some incorrext values. I've overriden the previous data by choosing what % of buildings of each height should have an elevator.
![Image 3](img/elev.png)

#### Feature Engineering
Initially I converted **location** column into four new ones: **district**, **subdistrct**, **nbhood**, **street** using ``Geopy``. According to my research, a column **distance** containing distances from apartments to city center is very useful. Because there was too many missing values in **nbood** and **street** I calculated the distances based on subdistrict*. Using ``Google GeoCoding API`` I extracted coordinates of each **subdistrict's** center, then for each apartment I set **distance** to Euclidean distance between its **subdistrict** center and city center + noise.

#### Outliers and incorrect values
My last step was handling outliers and looking for incorrect data. There weren't many outliers, some of them I handled one by one, some of them were dropped. The same goes for incorrect data. After that my dataset was ready for modelling. 

### Training, testing and evaluating different models

#### Small updates to dataset
After preprocessing I was left with a dataset consisting of 13 features and just a little bit less than 30000 rows. \
My initial attempts at training models are described in ``model.ipynb``, however the results were not very good because of outliers, even though there weren't many of them. \
Getting more data to make models more accurate with outliers would be very time consuming, so I decided to drop 500 rows containing outliers. My work based on this dataset is described in ``model_no_outliers.ipynb``.

#### Algoritms used
Because of the small size of the dataset I was able to test multiple ML models in ``sklearn``:
* Linear Regression
* Ridge Regression
* Lasso Regression
* ElasticNet
* Polynomial Regression with:
    * Linear Regression
    * Ridge Regression
    * Lasso Regression
    * ElasticNet
* Gradient Boosting
* Regression Tree
* Random Forest

#### Encoding categorical features and scaling values
For features: **b_type** and **district** I used ``OneHotEncoding``.
For **rooms**, **floor**, **built**, **max_floor** I used ``OrdinalEncoding``, because values there can be 'ranked' and also because it doesn't increase dimensionality. \
Numerical features were scaled using ``StandardScaler``.

#### Linear Regression | Ridge Regression | Lasso Regression | ElasticNet with GridSearch

All these models performed very similarly, so I will only show results from Linear Regression.

| Metric  | Value                |
|---------|----------------------|
| MAE     | 213704.82419916763   |
| MSE     | 124225930474.904     |
| RMSE    | 352456.9909576259    |
| R²      | 0.7489847425925041   |

As we can see the model doesn't perform perfectly with RMSE being very high. However R² score implies that the model is reasonably well fit.
![Image 3](img/linreg.png)
After inspecting these plots we can see that the model clearly has trouble with predicting apartments that have bigger value. \
Additionally we can see that the model generalises pretty well, but it's too simple to learn all paterns in data(slow growth of validation curve). 
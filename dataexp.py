#PREPROCESSING ON A REAL DATASET SUCKS!!

def clear_numerical(data, column, null_strat='drop', cast='integer'):
    #cast values
    data = data.withColumn(column, col(column).cast(cast))

    #calculate the median of the column and round
    median = int(round(data.approxQuantile(column, [0.5], 0.25)[0]))

    #replace non-numerical and null values with the rounded median
    return data.withColumn(
        column,
        F.when((col(column).isNotNull()), col(column)).otherwise(median)
    )

def clear_boolean(data, column):
    #clear up the boolean categories without disturbing distribution
    #calculate the distribution of valid 1s and 0s in the column
    distribution = data.groupBy(column).count().collect()
    valid_0_count = next(item for item in distribution if item[column] == 0)['count']
    valid_1_count = next(item for item in distribution if item[column] == 1)['count']

    #calculate probabilities for setting invalid values to 0 or 1
    prob_0 = valid_0_count / (valid_0_count + valid_1_count)
    prob_1 = valid_1_count / (valid_0_count + valid_1_count)

    #replace non-boolean and null values with 0 or 1 based on distribution
    return data.withColumn(
        column,
        when(
            col(column).cast("boolean").isNotNull(),
            col(column)
        ).otherwise(
            when(
                (col(column) == "invalid") | col(column).isNull(),
                when(col(column) == "invalid", prob_1).otherwise(prob_0)
            )
        )
    )

'''
    'id' drop duplicates
    'region_url' drop anything not starting with https and then apply strindexer and maybe one-hot
    'type' needs indexing
    'price' cast to integer
    'sqfeet' cast to integer
    'beds' drop strs and nulls = median, cast to integer
    'baths' drop strs and nulls = median, cast to float
    'cats_allowed' keep the booleans and set nulls stratified-randomly
    'dogs_allowed' keep the booleans and set nulls stratified-randomly
    'smoking_allowed' keep the booleans, null the strs and set nulls stratified-randomly
    'wheelchair access' keep the booleans, set strs to 1 and set nulls stratified-randomly
    'electric_vehicle_charge' just cast as boolean and set nulls to 0
    'comes_furnished' keep the booleans, set strs to 1 and set nulls stratified-randomly
    'laudry_options' strindexer and null goes to 'no laundry on site'
    'parking' strindexer and null goes to 'no parking'
    'state' ignore for now

'''
#DATA CLEARING

#drop unwanted columns
data = data.drop('description', 'url', 'image_url', 'lat', 'long', 'region', 'state')


#drop duplicate ids
n = data.count()
data = data.dropDuplicates(['id'])
print('droped duplicates', n-data.count())

#dispose of id col
#data = data.drop('id')

#remove any region_url not starting with https
data = data.filter(col('region_url').startswith('https'))
#index the region_url


#fix datatypes
for c in ['price', 'sqfeet']:
    data = data.withColumn(c, col(c).cast('integer'))

for c in ['cats_allowed', 'dogs_allowed', 'smoking_allowed', 'wheelchair_access', 'electric_vehicle_charge', 'comes_furnished']:
    data = data.withColumn(c, col(c).cast('boolean'))

#clear up beds column
data = clear_numerical(data, 'beds', null_strat='median', cast='integer')

#clear up baths column
data = clear_numerical(data, 'baths', null_strat='median', cast='float')

inputCols = [
    'sqfeet', 'beds', 'baths', 'cats_allowed', 'dogs_allowed', 'smoking_allowed', 'wheelchair_access', 
    'electric_vehicle_charge','comes_furnished', 'region_url_idx', 'type_idx', 'laundry_options_idx', 'parking_options_idx'
]
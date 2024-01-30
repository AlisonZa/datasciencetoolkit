
# Function to check the unique values in each collumns
def check_unique_values (dataframe_list):
  counter = 0
  for df in dataframe_list:
    print(f'For the Data Frame number {counter} the unique values')
    print('**'*30)
    for a in df.columns:
      print(a)
      print(df[a].unique())
    print('**'*30)
    counter = counter + 1

# Function to check the shape
def check_shape (dataframe_list):
  counter = 0
  for df in dataframe_list:
    print(f'For the Data Frame number {counter} the shape is: {df.shape}')
    print('**'*30)
    counter = counter + 1

# Function to check the existence of null values in each collumns
def check_null_values (dataframe_list):
  counter = 0
  for z in dataframe_list:
    print(f'For the dataFrame number {counter} the null values are:')
    print(z.isnull().sum())
    print(f'For the dataFrame number {counter} the NaaN values are:')
    print(z.isna().sum())
    counter = counter + 1

# Function to check the collumns
def check_collumns_names (dataframe_list):
  counter = 0
  for df in dataframe_list:
    print(f'For the Data Frame number {counter} the name of the collumns are:')
    for a in df.columns:
      print(a)
    print('*'*30)
    counter = counter + 1

# Function to exclude the useless columns
def exclude_columns (dataframe_list, columns_to_exclude):
  for z in dataframe_list:
    for a in columns_to_exclude:
      z.drop(columns = a, inplace = True)


'''
Handling with the numerical missing data, the function replace with the mean
'''
def fill_numericals_mean(dataframe_list, columns):
  for df in dataframe_list:
    for clm in columns:
      mean_value = df[clm].mean()
      df[clm].fillna(mean_value, inplace=True)

def apply_change_booleans(dataframe_list, boolean_columns, change_dict):
    for df in dataframe_list:
        for column in boolean_columns:
            if column in df.columns:
                df[column] = df[column].map(change_dict)

# Handling the boolean null values for the test DataFrame
def fill_mode(dataframe_list, columns):
    for df in dataframe_list:
        for clm in columns:
            mode_value = df[clm].mode()
            if not mode_value.empty:
                df[clm].fillna(mode_value.iloc[0], inplace=True)

# Lista de classificadores a serem testados
def classifiers_accuracy_evaluation_cv(X_train,y_train, classifiers_list):
  # classifiers = [
  #     LogisticRegression(),
  #     SVC(),
  #     DecisionTreeClassifier(),
  #     RandomForestClassifier()
  # ]
  classifiers = classifiers_list

  # Treinando e avaliando cada classificador
  for classifier in classifiers:
    results = cross_validate(classifier, X_train, y_train, cv = skf, return_train_score=False)
    media = results['test_score'].mean()
    desvio_padrao = results['test_score'].std()
    print(f'Classifier {classifier}, Acuracy_score_médio {media}, +- 2 desvios padrões: {(media - 2 * desvio_padrao)*100}, {(media + 2 * desvio_padrao)*100}')


# HyperParamater RFC tunning
def HyperParamTuning(paramgrid, X_train, y_train, model):

  search = GridSearchCV(model(),
                      paramgrid,
                      cv = KFold(n_splits = 3, shuffle=True))
  search.fit(X_train, y_train)
  resultados = pd.DataFrame(search.cv_results_)
  resultados.head()

  scores = cross_val_score(search, X_train, y_train, cv = KFold(n_splits=3, shuffle=True))
  scores

  def imprime_score(scores):
    mean = scores.mean() * 100
    std = scores.std() * 100
    print("Accuracy médio %.2f" % mean)
    print("Intervalo [%.2f, %.2f]" % (mean - 2 * std, mean + 2 * std))

  imprime_score(scores)

  melhor = search.best_estimator_
  print(melhor)


def save_unique_values_to_excel(list_of_dataframes, file_name):
    # Create an Excel writer
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')

    # Iterate over each dataframe in the list
    for i, df in enumerate(list_of_dataframes):
        # Initialize an empty dataframe to store unique values
        df_unique_values = pd.DataFrame(columns=['Column', 'Unique Value'])

        # Iterate over each column in the dataframe
        for column in df.columns:
            # Get the unique values from the column
            unique_values = df[column].unique()

            # Add the unique values to the dataframe
            df_temp = pd.DataFrame({'Column': [column] * len(unique_values),
                                    'Unique Value': unique_values})

            # Add to the final dataframe
            df_unique_values = pd.concat([df_unique_values, df_temp], ignore_index=True)

        # Save the final dataframe as a sheet in the Excel file
        df_unique_values.to_excel(writer, sheet_name=f'Dataframe_{i+1}', index=False)

    # Save the Excel file
    writer.save()
    print(f'Unique values saved to {file_name}')

"""# Images"""

# Viewing a Sampling of Images
def plot_sample_images(dataset, num_images=10, num_rows=2, num_cols=5):
    fig, axes = plt.subplots(num_rows, num_cols, figsize=(15, 6))
    for images, _ in dataset.take(1):
        for i in range(num_rows):
            for j in range(num_cols):
                image = images[i * num_cols + j].numpy().astype("uint8")

                # Plot the image
                axes[i, j].imshow(image, cmap='gray')
                axes[i, j].axis('off')

    plt.tight_layout()
    plt.show()

# Convert images to numpy arrays
def images_in_directory_to_np_arrays(directory_path, size=(64, 64), color_mode='L'):
    full_mat = None

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)

        # Open and resize the image using PIL
        current_image = Image.open(filepath).resize(size)

        # Convert image to a matrix
        img_np = np.array(current_image.convert(color_mode))
        # Flatten the image into a vector / 1D array
        img_np = img_np.ravel()

        try:
            # Concatenate different images
            full_mat = np.concatenate((full_mat, [img_np]))
        except (UnboundLocalError, ValueError):
            # If not assigned yet or if concatenation fails, assign one
            full_mat = np.array([img_np])

    return full_mat

# Create average image
def find_mean_img(full_mat, title, size = (64, 64)):
    # calculate the average
    mean_img = np.mean(full_mat, axis = 0)
    # reshape it back to a matrix
    mean_img = mean_img.reshape(size)
    plt.imshow(mean_img, vmin=0, vmax=255, cmap='Greys_r')
    plt.title(f'Average {title}')
    plt.axis('off')
    plt.show()
    return mean_img

# Eigenimages
def eigenimages(full_mat, title, n_comp = 0.7, size = (64, 64)):
    pca = PCA(n_components = n_comp, whiten = True)
    pca.fit(full_mat)
    print('Number of PC: ', pca.n_components_)
    return pca

# Plot eigenimages in a grid
def plot_pca(pca, size = (64, 64)):

    n = pca.n_components_
    fig = plt.figure(figsize=(8, 8))
    r = int(n**.5)
    c = ceil(n/ r)
    for i in range(n):
        ax = fig.add_subplot(r, c, i + 1, xticks = [], yticks = [])
        ax.imshow(pca.components_[i].reshape(size),
                  cmap='Greys_r')
    plt.axis('off')
    plt.show()
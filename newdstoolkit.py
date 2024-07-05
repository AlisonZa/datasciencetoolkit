# -*- coding: utf-8 -*-
"""NewDsToolKit.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LSOw8jDtrF2jxLiqLEi6rjFCXEfRZpsK
"""

#TODO Implementar função que receba os datasets itere sobre eles, e sobre as features (categórica, numérica, discreta continua....),
# E plote gráficos afim de entender se os datasets (train dev e test) têm distribuições similares

# TODO Implementar Random Forest Imputation

# TODO Implementar função a fim de mensurar o tempo de predição time.time e os caceta
"""# 3. Explore the data to gain insights.

## 1. DataView
"""

# For Tabular Data

# Plot Numerical Features Distribution
def plot_numerical_features(df, features, save_path):
    numericals = features
    for feature in numericals:
        plt.figure(figsize=(8, 6))
        sns.histplot(df[feature], kde=True)
        plt.title(f'Distribution of {feature}')
        plt.xlabel(feature)
        plt.ylabel('Frequency')

        # Adjust the y-axis scale based on min and max values
        plt.ylim(0, df[feature].value_counts().max())

        plt.savefig(f'{save_path}/{feature}_distribution.png')
        plt.close()

# Plot
def mixed_feature_plot(df, quant_features, qual_features, save_path):
    # Pair plot for quantitative features
    if quant_features:
        quant_df = df[quant_features]
        plt.figure(figsize=(12, 8))
        sns.pairplot(quant_df)
        plt.suptitle('Pair Plot for Quantitative Features')
        plt.savefig(f'{save_path}/pair_plot_quantitative.png')
        plt.close()

    # Count plots for both qualitative and boolean features
    all_qual_features = qual_features + [col for col in df.columns if df[col].dtype == bool]

    if all_qual_features:
        plt.figure(figsize=(15, 10))
        for i, feature in enumerate(all_qual_features, start=1):
            plt.subplot(2, len(all_qual_features)//2, i)
            sns.countplot(x=feature, data=df, palette='viridis')
            plt.title(f'Count of {feature}')
            plt.xlabel(feature)
            plt.ylabel('Count')

        plt.tight_layout()
        plt.suptitle('Count Plots for Qualitative Features')
        plt.subplots_adjust(top=0.9)
        plt.savefig(f'{save_path}/count_plots_qualitative.png')
        plt.close()

# Provide insight into the target feature
def target_insight_graphics(df, numerical_features, boolean_features, target_features, save_path):
    # Ensure the save path exists
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    for target_feature in target_features:
        # Pair plot for numerical features
        if numerical_features:
            num_numerical_features = len(numerical_features)
            num_subplots = min(12, num_numerical_features)  # Limit to 12 subplots

            plt.figure(figsize=(15, 12))
            sns.pairplot(df[numerical_features + [target_feature]], hue=target_feature, palette='husl', height=2.5)
            plt.suptitle(f'Pair Plot for Numerical Features by {target_feature}', y=1.02)
            plt.savefig(os.path.join(save_path, f'pair_plot_numerical_{target_feature}.png'))
            plt.close()

        # Count plots for boolean features
        if boolean_features:
            num_boolean_features = len(boolean_features)
            num_subplots = min(12, num_boolean_features)  # Limit to 12 subplots

            plt.figure(figsize=(15, 10))
            num_rows = (num_subplots + 3) // 4  # Dynamically calculate the number of rows

            for i, feature in enumerate(boolean_features[:num_subplots], start=1):
                plt.subplot(num_rows, min(num_subplots, 4), i)
                sns.countplot(x=feature, hue=target_feature, data=df, palette='coolwarm')
                plt.title(f'Count of {feature} by {target_feature}')
                plt.xlabel(feature)
                plt.ylabel('Count')

            plt.tight_layout()
            plt.suptitle(f'Count Plots for Boolean Features by {target_feature}', y=1.02)
            plt.subplots_adjust(top=0.9)
            plt.savefig(os.path.join(save_path, f'count_plots_boolean_{target_feature}.png'))
            plt.close()

## For Images:

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

# Outlier Detection

"""## 3. Study each attribute and its characteristics:

"""

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

"""## 8. Identify the promising transformations you may want to apply

## 9. Identify extra data that would be useful (go back to “Get the Data”).

## 10. Document what you have learned.

# 4. Prepare the data to better expose the underlying data patterns to machine learning algorithms.

---

## 1. Clean the data:

### Fill in missing values (e.g., with zero, mean, median…) or drop their rows (or columns).
"""

# Handling the boolean null values for the test DataFrame
def fill_mode(dataframe_list, columns):
    for df in dataframe_list:
        for clm in columns:
            mode_value = df[clm].mode()
            if not mode_value.empty:
                df[clm].fillna(mode_value.iloc[0], inplace=True)

# Function to exclude the useless columns
def exclude_columns (dataframe_list, columns_to_exclude):
  for z in dataframe_list:
    for a in columns_to_exclude:
      z.drop(columns = a, inplace = True)

def apply_change_booleans(dataframe_list, boolean_columns, change_dict):
    for df in dataframe_list:
        for column in boolean_columns:
            if column in df.columns:
                df[column] = df[column].map(change_dict)

"""## 2. Perform feature selection (optional):

Drop the attributes that provide no useful information for the task,

Also use the correlation map

## 3. Perform feature engineering, where appropriate:

### Discretize continuous features.

### Decompose features (e.g., categorical, date/time, etc.).

### Add promising transformations of features (e.g., log(x), sqrt(x), x ,etc.).

### Aggregate features into promising new features.

## 4. Perform feature scaling:

# 5. Explore many different models and shortlist the best ones

### If the data is huge, you may want to sample smaller training sets so you can train many different models in a reasonable time (be aware that this penalizes complex models such as large neural nets or random forests).

### Once again, try to automate these steps as much as possible.

## 1. Train many quick-and-dirty models from different categories(e.g., linear, naive Bayes, SVM, random forest, neural net, etc.) using standard parameters
"""

def train_classifiers(X_train, y_train, classifiers_list, save_path):
    """
    Train a list of classifiers and return they assesments and confusion matrix for the training process.
    The assesment functionality is aimed to understand if the model underfits

    Parameters:
    - X_train (pd.DataFrame, or Np Array): Training features.
    - y_train (pd.Series, or Np Array): Training labels.
    - classifiers_list (list): List of classifier instances.
    - save_path (list): Path to save the report of the training.

    Returns:
    - results_df (Excel Spreadsheet): Spreadsheet with the assesment of the models, saved to the gave path.
    - trained_models (list): List of trained classifier models.
    """
    save_path = save_path + '/training_logs.xlsx'
    trained_models, results = [], []

    # Train the models
    for classifier in classifiers_list:
        clf = classifier.fit(X_train, y_train)
        trained_models.append(clf)

        # Predict the labels an assess the model on the training
        y_pred = model.predict(X_train)
        cm = confusion_matrix(y_train, y_pred)
        accuracy = accuracy_score(y_train, y_pred)
        precision = precision_score(y_train, y_pred)
        recall = recall_score(y_train, y_pred)
        f1 = f1_score(y_train, y_pred)

        # Append the results
        results.append({
            'Model': model.__class__.__name__,
            'True Negatives': cm[0, 0],
            'False Positives': cm[0, 1],
            'False Negatives': cm[1, 0],
            'True Positives': cm[1, 1],
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1
        })

    results_df = pd.DataFrame(results)
    results_df.to_excel(, index=False)
    print(f"Models trained, assesment saved to: {save_dir}")

    return  trained_models

# Model training and selection with cross validation
def train_cross_validation(X_train, y_train, classifiers_list, save_path, folds=5, scoring=None, n_jobs=-1, verbose=False):
    """
    Train a list of classifiers using cross-validation and return their assessments, including confusion matrices for the training process.
    The assessment functionality is aimed to understand if the model underfits.

    Parameters:
    - X_train (pd.DataFrame, or np.array): Training features.
    - y_train (pd.Series, or np.array): Training labels.
    - classifiers_list (list): List of classifier instances.
    - save_path (str): Path to save the report of the training.
    - folds (int): Number of cross-validation folds.
    - scoring (dict): Scoring metrics for evaluation.
    - n_jobs (int): Number of jobs to run in parallel. -1 means using all processors.
    - verbose (bool): If True, print progress messages.

    Returns:
    - results_df (Excel Spreadsheet): Spreadsheet with the assessment of the models, saved to the given path.
    - trained_models (list): List of trained classifier models.
    """
    if scoring is None:
        scoring = {
            'accuracy': 'accuracy',
            'precision': 'precision_macro',
            'recall': 'recall_macro',
            'f1': 'f1_macro'
        }

    logging.basicConfig(level=logging.INFO if verbose else logging.WARNING)
    logger = logging.getLogger(__name__)

    save_path = save_path + '/assessment_logs_cross_validation.xlsx'
    trained_models, results_list = [], []

    # Using StratifiedKFold for classification tasks
    skf = StratifiedKFold(n_splits=folds, shuffle=True)

    # Function to process each classifier
    def process_classifier(classifier):
        # Perform cross-validated evaluation
        results = cross_validate(classifier, X_train, y_train, cv=skf, scoring=scoring, return_train_score=False, n_jobs=n_jobs)
        accuracy_mean = results['test_accuracy'].mean()
        accuracy_std = results['test_accuracy'].std()
        recall_mean = results['test_recall'].mean()
        recall_std = results['test_recall'].std()
        precision_mean = results['test_precision'].mean()
        precision_std = results['test_precision'].std()
        f1_mean = results['test_f1'].mean()
        f1_std = results['test_f1'].std()

        # Fit the classifier on the entire training set
        clf = classifier.fit(X_train, y_train)

        # Predict the labels and assess the model on the entire training set
        y_pred = clf.predict(X_train)
        cm = confusion_matrix(y_train, y_pred)
        accuracy = accuracy_score(y_train, y_pred)
        precision = precision_score(y_train, y_pred, average='macro')
        recall = recall_score(y_train, y_pred, average='macro')
        f1 = f1_score(y_train, y_pred, average='macro')

        # Append the results
        results_list.append({
            'Classifier': classifier.__class__.__name__,
            'Average Accuracy': accuracy_mean,
            'Accuracy Std': accuracy_std,
            'Average Recall': recall_mean,
            'Recall Std': recall_std,
            'Average Precision': precision_mean,
            'Precision Std': precision_std,
            'Average F1': f1_mean,
            'F1 Std': f1_std,
            'True Negatives': cm[0, 0] if cm.shape == (2, 2) else 'N/A',
            'False Positives': cm[0, 1] if cm.shape == (2, 2) else 'N/A',
            'False Negatives': cm[1, 0] if cm.shape == (2, 2) else 'N/A',
            'True Positives': cm[1, 1] if cm.shape == (2, 2) else 'N/A',
            'Overall Accuracy': accuracy,
            'Overall Precision': precision,
            'Overall Recall': recall,
            'Overall F1': f1
        })

        trained_models.append(clf)

        logger.info(f"Classifier {classifier.__class__.__name__} processed.")

    # Process classifiers in parallel
    Parallel(n_jobs=n_jobs)(delayed(process_classifier)(classifier) for classifier in classifiers_list)

    results_df = pd.DataFrame(results_list)
    results_df.to_excel(save_path, index=False)
    print(f"Models trained, assessment saved to: {save_path}")

    return trained_models









"""## 3. Analyze the most significant variables for each algorithm.

## 4. Analyze the types of errors the models make
"""

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, format(cm[i, j], fmt), horizontalalignment="center", color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

# Directory to save the plots
save_dir = "/content/drive/MyDrive/CDC Diabetes Health Indicators/Confusion Matrices"
os.makedirs(save_dir, exist_ok=True)

# # Example usage
# for i, model in enumerate(trained_models):
#     y_pred = model.predict(X_val)
#     cm = confusion_matrix(y_val, y_pred)
#     plt.figure()
#     plot_confusion_matrix(cm, classes=[0, 1], title=f'Confusion matrix for {model.__class__.__name__}')
#     plt.savefig(os.path.join(save_dir, f"confusion_matrix_{model.__class__.__name__}.png"))
#     plt.close()  # Close the current plot to free memory

def classifier_assessment_valsplit(models, X_val, y_val, save_path):
    """
    Test models on validation dataset and save confusion matrix results to an Excel spreadsheet.

    Parameters:
    - models (list): List of trained models.
    - X_val (pd.DataFrame): Validation features.
    - y_val (pd.Series): Validation labels.
    - save_path (str): Path to save the Excel spreadsheet.
    """
    results = []
    for model in models:
        y_pred = model.predict(X_val)
        cm = confusion_matrix(y_val, y_pred)
        accuracy = accuracy_score(y_val, y_pred)
        precision = precision_score(y_val, y_pred)
        recall = recall_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred)

        results.append({
            'Model': model.__class__.__name__,
            'True Negatives': cm[0, 0],
            'False Positives': cm[0, 1],
            'False Negatives': cm[1, 0],
            'True Positives': cm[1, 1],
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1 Score': f1
        })

    results_df = pd.DataFrame(results)
    results_df.to_excel(save_path, index=False)
    print(f"Confusion matrix results saved to {save_dir}")





"""## 5. Perform a quick round of feature selection and engineering

## 6. Perform one or two more quick iterations of the five previous steps.

## 7. Shortlist the top three to five most promising models, preferring models that make different types of errors.

# 6. Fine-tune your models and combine them into a great solution.

### Notes:


> You will want to use as much data as possible for this step, especially as you move toward the end of fine-tuning.

> As always, automate what you can

## 1. Fine-tune the hyperparameters using cross-validation:
"""

# HyperParamater tunning only
def HyperParamTuningCV(paramgrid, X_train, y_train, model):

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



# Post Prunning for Decision Treees
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier

def post_pruning_decision_tree(
    save_path: str,
    metrics: list,
    X_train, y_train,
    X_val, y_val
):
    """
    Perform post-pruning on a Decision Tree classifier using cost complexity pruning.

    Parameters:
    save_path (str): The path to save the plots.
    metrics (list): List of metrics to evaluate the models.
    X_train: Training feature data.
    y_train: Training target data.
    X_val: Validation feature data.
    y_val: Validation target data.

    Returns:
    List of ccp alphas and plots of the specified metrics.
    """

    # Identify the alphas and the impurities
    clf = DecisionTreeClassifier()
    path = clf.cost_complexity_pruning_path(X_train, y_train)
    ccp_alphas, impurities = path.ccp_alphas, path.impurities

    # Train a decision tree for every ccp_alpha
    clfs = []
    for ccp_alpha in ccp_alphas:
        clf = DecisionTreeClassifier( ccp_alpha=ccp_alpha)
        clf.fit(X_train, y_train)
        clfs.append(clf)

    # Print the number of nodes in the last tree
    print("Number of nodes in the last tree is: {} with ccp_alpha: {}".format(
          clfs[-1].tree_.node_count, ccp_alphas[-1]))

    # Plotting Accuracy vs alpha for training and validation sets
    train_scores = [clf.score(X_train, y_train) for clf in clfs]
    val_scores = [clf.score(X_val, y_val) for clf in clfs]

    fig, ax = plt.subplots()
    ax.set_xlabel("alpha")
    ax.set_ylabel("accuracy")
    ax.set_title("Accuracy vs alpha for training and validation sets")
    ax.plot(ccp_alphas, train_scores, marker='o', label="train", drawstyle="steps-post")
    ax.plot(ccp_alphas, val_scores, marker='o', label="validation", drawstyle="steps-post")
    ax.legend()
    plt.savefig(f"{save_path}/accuracy_vs_alpha.png")
    plt.show()

    # Plot additional metrics if provided
    for metric in metrics:
        train_metric_scores = [metric(y_train, clf.predict(X_train)) for clf in clfs]
        val_metric_scores = [metric(y_val, clf.predict(X_val)) for clf in clfs]

        fig, ax = plt.subplots()
        ax.set_xlabel("alpha")
        ax.set_ylabel(metric.__name__)
        ax.set_title(f"{metric.__name__.capitalize()} vs alpha for training and validation sets")
        ax.plot(ccp_alphas, train_metric_scores, marker='o', label="train", drawstyle="steps-post")
        ax.plot(ccp_alphas, val_metric_scores, marker='o', label="validation", drawstyle="steps-post")
        ax.legend()
        plt.savefig(f"{save_path}/{metric.__name__}_vs_alpha.png")
        plt.show()

    return ccp_alphas

# Example usage
# from sklearn.metrics import f1_score, precision_score, recall_score
# ccp_alphas = post_pruning_decision_tree("path/to/save/plots", [f1_score, precision_score, recall_score], X_train, y_train, X_val, y_val)

### Para modelos de classificação podemos ajustar um treshold ideal
# Tenho que melhorar este modelo, e o entendimento do conceito por detrás

def find_optimal_threshold_binary_clf(classifiers, classifier_names, X_train, y_train, X_val, y_val):
    """
    Finds and visualizes the optimal threshold for a list of classifiers.

    Parameters:
    classifiers (list): List of classifier objects.
    classifier_names (list): List of classifier names corresponding to the classifiers.
    X_train (numpy array or pandas DataFrame): Training data features.
    y_train (numpy array or pandas Series): Training data labels.
    X_val (numpy array or pandas DataFrame): Validation data features.
    y_val (numpy array or pandas Series): Validation data labels.

    Returns:
    dict: A dictionary containing the optimal threshold for each classifier.
    """
    optimal_thresholds = {}

    plt.figure(figsize=(15, 10))

    for clf, name in zip(classifiers, classifier_names):
        # Train the classifier
        clf.fit(X_train, y_train)

        # Predict probabilities on the validation set
        y_val_pred_proba = clf.predict_proba(X_val)[:, 1]

        # Compute ROC curve
        fpr, tpr, thresholds = roc_curve(y_val, y_val_pred_proba)

        # Find the optimal threshold
        optimal_idx = np.argmax(tpr - fpr)
        optimal_threshold = thresholds[optimal_idx]
        optimal_thresholds[name] = optimal_threshold

        # Plot the ROC curve
        plt.plot(fpr, tpr, marker='.', label=f'{name} (AUC = {roc_auc_score(y_val, y_val_pred_proba):.2f})')
        plt.scatter(fpr[optimal_idx], tpr[optimal_idx], marker='o', color='red', label=f'Optimal Threshold for {name}')

        print(f'{name} - Optimal Threshold: {optimal_threshold}')

    # Customize the plot
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve and Optimal Thresholds')
    plt.legend()
    plt.show()

    return optimal_thresholds

# Example usage:
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

# Create a list of classifiers
classifiers = [
    RandomForestClassifier(),
    LogisticRegression(),
    AdaBoostClassifier(),
    KNeighborsClassifier()
]

# # Create a list of classifier names
# classifier_names = [
#     'RandomForest',
#     'LogisticRegression',
#     'AdaBoost',
#     'KNeighbors'
# ]

# # Generate a synthetic dataset
# from sklearn.datasets import make_classification
# from sklearn.model_selection import train_test_split

# X, y = make_classification(n_samples=2000, n_classes=2, weights=[1, 1], random_state=1)
# X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=1)
# X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=1)

# # Find optimal thresholds
# optimal_thresholds = find_optimal_threshold(classifiers, classifier_names, X_train, y_train, X_val, y_val)
# print(optimal_thresholds)

"""### Treat your data transformation choices as hyperparameters, especially when you are not sure about them (e.g., if you’re not sure whether to replace missing values with zeros or with the median value, or to just drop the rows).

### Unless there are very few hyperparameter values to explore, prefer random search over grid search. If training is very long, you may prefer a Bayesian optimization approach (e.g., using Gaussian process priors, as described by Jasper Snoek et al. )

## 2. Try ensemble methods. Combining your best models will often produce better performance than running them individually.

## 3. Once you are confident about your final model, measure its performance on the test set to estimate the generalization error.

# 7. Present your solution

## 1. Document what you have done.

## 2. Create a nice presentation:

### Make sure you highlight the big picture first.

## 3. Explain why your solution achieves the business objective.

## 4. Don’t forget to present interesting points you noticed along the way:

Describe what worked and what did not.

### List your assumptions and your system’s limitations.

## 5. Ensure your key findings are communicated through beautiful visualizations or easy-to-remember statements (e.g., “the median income is the number-one predictor of housing prices”)

# 8. Launch, monitor, and maintain your system

## 1. Get your solution ready for production (plug into production data inputs, write unit tests, etc.).

## 2. Write monitoring code to check your system’s live performance at regular intervals and trigger alerts when it drops:

### Beware of slow degradation: models tend to “rot” as data evolves.

### Measuring performance may require a human pipeline (e.g., via a crowdsourcing service).

### Also monitor your inputs’ quality (e.g., a malfunctioning sensor sending random values, or another team’s output becoming stale). This is particularly important for online learning systems.

##3. Retrain your models on a regular basis on fresh data (automate as much as possible).
"""

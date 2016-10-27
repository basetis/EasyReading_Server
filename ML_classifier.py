import text_batch_process as tbp
import utilities as u

ML_path = "ML/"

Algorithms_path = "ML/Algorithms/"

name_naive_bayes = "NB_classifier"
name_SVM = "SVM_classifier"
name_decision_tree = "decision_tree_classifier"
name_random_forest = "random_forest_classifier"
name_adaBoost = "AdaBoost_classifier"

def split_data(x, y):
	"""
		Given some features and tags, it splits them into a training and a testing sets
		
		Args:
			x:	features
			y:	tags
			
		Returns:
			x_train:	features to train the classifier
			x_test:		features to test the classifier
			y_train:	tags to train the classifier
			y_test:		tags to test the classifier
	"""
	
	from sklearn.cross_validation import train_test_split
	x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=47)

	from data_analisis import show_difficulties_distribution
	print "\nDATA DISTRIBUTION:"
	show_difficulties_distribution(y)

	import numpy as np
	print "\nTRAINING SET:"
	show_difficulties_distribution(y_train)
	print np.r_[y_train]

	print "\nTESTING SET:"
	show_difficulties_distribution(y_test)
	print np.r_[y_test]
		
	return x_train, x_test, y_train, y_test

	
def train_classifier(name, x_train, y_train):
	"""
		Using the caracteristics and the labels it will train the classifier
		and save it as a pickle file
		
		Args:
			name:		name of the classifier
			x_train:	metrics to train the classifier
			y_train:	labels to train the classifier
			
		Returns:
			the classifier
	"""
	
	"""
		Classifiers info: http://scikit-learn.org/stable/auto_examples/classification/plot_classifier_comparison.html
	"""
	
	timer = u.Timer()

	print "\nTraining", name
	
	from sklearn.preprocessing import StandardScaler
	scaler = StandardScaler(copy=True, with_mean=True, with_std=True)

	from sklearn.feature_selection import SelectKBest
	select = SelectKBest()
	
	list_k = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]

	### This functions allows to try other classifiers
	def declare_NB():
		from sklearn.naive_bayes import GaussianNB
		naive_bayes = GaussianNB()
		
		steps = [("scaler", scaler), ('feature_selection', select), ('naive_bayes', naive_bayes)]
		
		parameters = dict(feature_selection__k = list_k)
		
		return steps, parameters
		
	def declare_SVM():
		from sklearn.svm import SVC
		SVM = SVC()
		
		steps = [("scaler", scaler), ('feature_selection', select),	('SVM', SVM)]
	
		list_C = [1, 2, 3, 4, 5, 10, 100, 1000, 10000]
	
		parameters = dict(feature_selection__k = list_k, SVM__kernel=["rbf"], SVM__C = list_C)
		
		return steps, parameters, list_C

	def declare_adaboost():
		from sklearn.ensemble import AdaBoostClassifier
		adaboost = AdaBoostClassifier()

		steps = [("scaler", scaler), ('feature_selection', select), ('adaboost', adaboost)]
		
		parameters = dict(feature_selection__k = list_k)
		
		return steps, parameters

	def declare_Decision_tree():
		from sklearn import tree
		decision_tree = tree.DecisionTreeClassifier()

		steps = [("scaler", scaler), ('feature_selection', select), ('decision_tree', decision_tree)]

		min_samp_list = [20, 15, 10, 8, 6, 4]
		
		parameters = dict(feature_selection__k = list_k, decision_tree__min_samples_split = min_samp_list)
		
		return steps, parameters, min_samp_list

	def declare_Random_forest():
		from sklearn.ensemble import RandomForestClassifier
		random_forest = RandomForestClassifier()

		steps = [("scaler", scaler), ('feature_selection', select), ('random_forest', random_forest)]

		min_samp_list = [20, 15, 10, 8, 6, 4]
		
		parameters = dict(feature_selection__k = list_k, random_forest__min_samples_split = min_samp_list)
		
		return steps, parameters, min_samp_list


	#Use the apropiate algorithm
	if name == name_naive_bayes:
		steps, parameters = declare_NB()

	elif name == name_SVM:
		steps, parameters, list_C = declare_SVM()

	elif name == name_adaBoost:
		steps, parameters = declare_adaboost()

	elif name == name_decision_tree:
		steps, parameters, min_samp_list = declare_Decision_tree()

	elif name == name_random_forest:
		steps, parameters, min_samp_list = declare_Random_forest()

		
	from sklearn.cross_validation import ShuffleSplit
	cv = ShuffleSplit(len(x_train), n_iter=10, test_size=0.1, random_state=0)


	from sklearn.pipeline import Pipeline

	pipeline = Pipeline(steps)
	
	from sklearn.grid_search import GridSearchCV
	#Scoring options:
	#	accuracy, f1_weighted, r2, average_precision
	clf = GridSearchCV(pipeline, cv = cv, param_grid = parameters) #, scoring="f1_weighted")
	
	clf.fit(x_train, y_train)
	
	def report_NB():
		import data_analisis
	
		list_mean = []
	
		for param, mean_score, cv_scores in clf.grid_scores_:
			list_mean.append(mean_score)
		
		data_analisis.scatter_plot_from_lists(list_k, list_mean, "NB accuracy by K variables", Algorithms_path, xlabel="Num variables", ylabel="Accuracy")
	
	def report_Adaboost():
		import data_analisis
	
		list_mean = []
	
		for param, mean_score, cv_scores in clf.grid_scores_:
			list_mean.append(mean_score)
		
		data_analisis.scatter_plot_from_lists(list_k, list_mean, "Adaboost accuracy by K variables", Algorithms_path, xlabel="Num variables", ylabel="Accuracy")
	

	def report_SVM():
	
		size_k = len(list_k)
		size_c = len(list_C)
		
		print "k=", size_k, "c=", size_c
		
		matrix = [[0 for x in range(size_c)] for y in range(size_k)] 
		i = 0
		j = 0
		
		last_value_C = list_C[0]
		
		for param, mean_score, cv_scores in clf.grid_scores_:
			
			if param["SVM__C"] != last_value_C:
				i += 1
				j = 0
				last_value_C = param["SVM__C"]
			
			#print param, "mean=", mean_score, "i=", i, "j=", j
			
			matrix[j][i] = mean_score
			
			j += 1
			
		import numpy as np
		
		header = [""] + list_C
		matrix = np.c_[list_k, matrix]
		
		u.save_to_csv("SVM.csv", Algorithms_path, matrix, header)
		u.change_decimal_separator("SVM.csv", Algorithms_path)

	def report_decision_tree():
	
		size_k = len(list_k)
		size_min_samp = len(min_samp_list)
		
		print "k=", size_k, "min_samples=", size_min_samp
		
		matrix = [[0 for x in range(size_min_samp)] for y in range(size_k)] 
		i = 0
		j = 0
		
		last_value_min_samples = min_samp_list[0]
		
		for param, mean_score, cv_scores in clf.grid_scores_:
			
			if param["decision_tree__min_samples_split"] != last_value_min_samples:
				i += 1
				j = 0
				last_value_min_samples = param["decision_tree__min_samples_split"]
			
			#print param, "mean=", mean_score, "i=", i, "j=", j
			
			matrix[j][i] = mean_score
			
			j += 1
			
		import numpy as np
		
		header = [""] + min_samp_list
		matrix = np.c_[list_k, matrix]
		
		u.save_to_csv("DecisionTree.csv", Algorithms_path, matrix, header)
		u.change_decimal_separator("DecisionTree.csv", Algorithms_path)

	def report_random_forest():
	
		size_k = len(list_k)
		size_min_samp = len(min_samp_list)
		
		print "k=", size_k, "min_samples=", size_min_samp
		
		matrix = [[0 for x in range(size_min_samp)] for y in range(size_k)] 
		i = 0
		j = 0
		
		last_value_min_samples = list_k[0]
		
		for param, mean_score, cv_scores in clf.grid_scores_:
			
			if param["feature_selection__k"] != last_value_min_samples:
				i += 1
				j = 0
				last_value_min_samples = param["feature_selection__k"]
			
			#print param, "mean=", mean_score, "i=", i, "j=", j
			
			matrix[i][j] = mean_score
			
			j += 1
			
		import numpy as np
		
		header = [""] + min_samp_list
		matrix = np.c_[list_k, matrix]
		
		u.save_to_csv("RandomForest.csv", Algorithms_path, matrix, header)
		u.change_decimal_separator("RandomForest.csv", Algorithms_path)
		
	#Use the apropiate algorithm
	if name == name_naive_bayes:
		report_NB()

	elif name == name_SVM:
		report_SVM()

	elif name == name_adaBoost:
		report_Adaboost()

	elif name == name_decision_tree:
		report_decision_tree()

	elif name == name_random_forest:
		report_random_forest()

	print "\n\nBest estimator", clf.best_estimator_

	print "\n\nBest score", clf.best_score_
		
	print "Trained in", timer.get_time()

	from process_text import get_metrics_header
	final_feature_indices = clf.best_estimator_.named_steps["feature_selection"].get_support(indices=True)

	final_feature_list = [get_metrics_header()[i] for i in final_feature_indices]

	print "Selected vars:", final_feature_list
	
	u.save_pickle(clf, name, path = ML_path)
	
	return clf
	
def get_classifier(name, x_train=None, y_train=None, train=False):
	"""
		It will load the specified classifier. If it's not possible it will train if it has x_train and y_train
		
		Args:
			name:		name of the classifier
			x_train:	metrics to train the classifier
			y_train:	labels to train the classifier
			train:		if true, it will force to train the classifier without loading it
			
		Returns:
			the classifier
	"""

	#if asked by user, train anyway
	if train:
		clf = train_classifier(name, x_train, y_train)
		
	#if not, try to load previously processed data
	else:
		try:
			clf = u.load_pickle(name, path = ML_path)
			
		#if not found, try to train it
		except IOError:		
			print "Pickle object not found, starting to train the classifier"
			
			#Check if it is possible to train the classifier
			if x_train is None or y_train is None:
				print "\n\nNot possible to train the classifier without x_train and y_train\n\n"
				
			else:
				clf = train_classifier(name, x_train, y_train)
	
	return clf
	
def test_a_classifier_from_data(name, x_train, x_test, y_train, y_test):
	"""
		It will test the specified classifier showing the accuracy of both test and train data.
		It will also show the predictions and a report.
		
		Args:
			name:		name of the classifier
			x_train:	features to train the classifier
			x_test:		features to test the classifier
			y_train:	tags to train the classifier
			y_test:		tags to test the classifier
	"""
		
	#clf = get_classifier(name, x_train, y_train)
	clf = get_classifier(name, x_train, y_train, True)
	
	accuracy = clf.score(x_train, y_train)
	print "\nAccuracy train: %0.4f" % accuracy
	
	accuracy = clf.score(x_test, y_test)
	print "Accuracy test: %0.4f \n" % accuracy
	
	y_pred = clf.predict(x_test)

	print "\nPREDICTIONS:\n", y_pred
	
	from sklearn.metrics import classification_report
	report = classification_report( y_test, y_pred )

	print(report)
	
def test_a_classifier(name, calculate=False):
	"""
		It will test the specified classifier.
		
		Args:
			name:		name of the classifier
			calculate:	if true, it will force to process all the data and recalculate X and Y
	"""
	
	x, y = tbp.load_ML_variables(calculate)
	
	x_train, x_test, y_train, y_test = split_data(x, y)
	
	test_a_classifier_from_data(name, x_train, x_test, y_train, y_test)
	
def classify_new_text(text):
	"""
		Given a text it returns all the metrics
	"""

	name_classifier = "Classifier"

	timer = u.Timer()

	print "\nStarting to classify text with", len(text), "characters"

	from process_text import process_text_from_string
	
	clf = get_classifier(name_classifier)
	
	x_pred = process_text_from_string(text)
	
	#check if the text was processed correctly
	if x_pred is not None:
		
		y_pred = clf.predict([x_pred])
	
		tag = str(y_pred[0])
	
	#if its not correctly processed, return tag Z
	else:
		tag = "Z"

	print "\nText processed in", timer.get_time()
	print "It is difficulty", tag

	return tag	
	
def full_ML_process(calculate=False, plot=False):
	"""
		It allows to do all the processes. 
		It will process the texts (if asked), train a classifier and test it. 
		It will also plot all the possible combinations of the input variables of the ML part (if asked)

		Args:
			calculate:	if true, it will force to process all the data and recalculate X and Y
			plot:		if true, it will save all the possible scaterplots of the input varaibles (X)
	"""
	
	#name_actual_classifier = name_adaBoost
	name_actual_classifier = name_SVM
	#name_actual_classifier = name_naive_bayes
	#name_actual_classifier = name_decision_tree
	#name_actual_classifier = name_random_forest

	timer = u.Timer()
		
	test_a_classifier(name_actual_classifier, calculate=calculate)
	#classify_new_text(name_actual_classifier, "Me gusta saltar piedras")
	
	import data_analisis

	if plot:
		data_analisis.plot_all()

	data_analisis.get_correlation_matrix()

	print "\nAll the processes done in", timer.get_time()


	
if __name__ == '__main__':
	full_ML_process(calculate=False, plot=False)
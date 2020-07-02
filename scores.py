from sciunit.scores.complete import *
import scipy.stats as st
import statsmodels.stats.power as pw
import numpy

class StudentsTestScore(Score):
    """A Student's t-test score.

    A float indicating the difference between two means of two independent samples normalized by their standard deviations and the 
    two sample sizes
    Contains also in the related_data dictionnary:
    the p value, which evaluates the significativity of this difference
    the statistical power of the test
    the degrees of freedom
    """

    _description = ("The t statistic between the prediction and the observation")

    @classmethod
    def compute(cls, observation, prediction):
        """Compute a t statistic and a p_value from an observation and a prediction."""
        
	p_mean = prediction['mean'] 
       	p_std = prediction['std']
       	p_n = prediction['n']
        p_var= p_std**2
	
	#2 samples t-test
	if isinstance(observation, dict):
		o_mean = observation['mean']
        	o_std = observation['std']
        	o_n = observation['n']
		o_var=o_std**2 
     
		#If the 2 variances are too different, perform a Welch t-test 	
		if p_var/o_var > 2 or o_var/p_var > 2: 
			value, p_val = st.ttest_ind_from_stats(p_mean,p_std,p_n,o_mean,o_std,o_n,equal_var=False)
			vnp=p_var/p_n
			vno=o_var/o_n
			#Welch-Satherwaite equation to compute the degrees of freedom
			dof=(vnp+vno)**2/(vnp**2/(p_n-1) + vno**2/(o_n-1)) 
		#If the 2 variances are similar, perform a 2 sample independant Student t-test
		else:
	        	value, p_val = st.ttest_ind_from_stats(p_mean,p_std,p_n,o_mean,o_std,o_n,equal_var=True)
			dof=o_n+p_n-2
		
		#Compute the statistical power of the test
		power=pw.TTestIndPower().power(effect_size=CohenDScore.compute(observation,prediction).score,nobs1=p_n,ratio=float(o_n)/p_n,alpha=0.05)
	
	#1 sample t-test
	else:
		value, p_val= st.ttest_ind_from_stats(p_mean, p_std, p_n, observation, std2=0, nobs2=2, equal_var=False)	
		#Compute the statistical power of the test
                power=pw.TTestPower().power(effect_size=CohenDScore.compute({"mean":observation,"std":0},prediction).score,nobs=p_n,alpha=0.05)
		o_mean=observation
		dof=p_n-1		
	return StudentsTestScore(value,related_data={"dof": dof, "p_value": p_val,"power": power,"diffmean":p_mean-o_mean})
	
    def __str__(self):
	if self.test.sheets:
                return 't = %.2f, degrees of freedom: %2f, p=%.6f, power=%.6f, difference of mean=%.6f for sheet(s) %s' % (self.score, self.related_data["dof"], self.related_data["p_value"], self.related_data["power"], self.related_data["diffmean"],self.test.sheets)
        else:
	        return 't = %.2f, p=%.6f' % (self.score, self.related_data["p_value"])


class StudentsPairedTestScore(Score):
    """A Student's paired t-test score.
    A float indicating the difference between two means of two dependent samples normalized by the two standard deviations and the  
    two sample sizes
    Contains also in the related_data dictionnary:
    the p value, which evaluates the significativity of this difference
    the statistical power of the test
    the degrees of freedom
    """

    _description = ("The t statistic between the prediction and the observation")

    @classmethod
    def compute(cls, observation, prediction):
        """Compute a t statistic and a p_value from an observation and a prediction."""

        value, p_val = st.ttest_rel(prediction,observation)
        power=pw.TTestPower().power(effect_size=value/len(observation)**0.5,nobs=len(observation),alpha=0.05)
	diffmean=numpy.mean(prediction)-numpy.mean(observation)
        return StudentsPairedTestScore(value,related_data={"dof": len(observation)-1, "p_value": p_val,"power": power,"diffmean":diffmean})

    def __str__(self):
        if self.test.sheets:
                return 't = %.2f, degrees of freedom: %2f, p=%.6f, power=%.6f, difference of mean=%.2f for sheet(s) %s' % (self.score, self.related_data["dof"], self.related_data["p_value"], self.related_data["power"], self.related_data["diffmean"],self.test.sheets)
        else:
                return 't = %.2f, p=%.6f' % (self.score, self.related_data["p_value"])


class ShapiroTestScore(Score):
    """A Shapiro-Wilk test score.

    A float indicating the difference between the distribution of the prediction and the one indicated in the observation string 
    Contains also the p value, which evaluates the significativity of this difference
    """

    _description = ("The Shapiro's W between the two distributions")

    @classmethod
    def compute(cls, observation, prediction):
        """Compute a Shapiro's W from an observation and a prediction."""

	if observation == "normal":
	        value, p_val = st.shapiro(prediction)
	
	elif observation== "lognormal":
		logPredictions=[]
		for p in prediction:
			if p > 0:
				logPrediction=numpy.log(p)
			#If the prediction is equal or inferior to 0, replace the value by log(0.000000001)
			else:
				logPrediction=numpy.log(0.000000001)
			logPredictions.append(logPrediction)		
		value, p_val = st.shapiro(logPredictions)
	
        return ShapiroTestScore(value,related_data={"p_value": p_val})

    def __str__(self):
        if self.test.sheets:
		return 'W = %.2f, p=%.6f for sheet(s) %s' % (self.score, self.related_data["p_value"],self.test.sheets)
	else:
		return 'W = %.2f, p=%.6f' % (self.score, self.related_data["p_value"])

import sciunit
import capabilities as cap
import scores
import numpy as np 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

#===============================================================================


class Test(sciunit.Test):
    """ Extension of sciunit.nest by adding the parameter sheets """


    def __init__(self,
                 observation = None,
                 sheets = None,
                 name = "Test"):

        self.sheets=sheets
        sciunit.Test.__init__(self, observation, name)


class AverageFiringRate(Test):
    """Test the if the distribution of the sheets average firing rates is significatively different than a predefined value
    or distribution"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = "Test if the sheets average firing rate is different than a predifined value or distribution"

    def __init__(self,
                 observation = None,
		 sheets = None,
                 name = "Average Firing Rate Test"):
	
	self.required_capabilities += (cap.StatsSheetsFiringRate,)
        Test.__init__(self,observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))
	
    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction=model.stats_sheets_firing_rate(self.sheets)
        if type(prediction).__module__=="numpy":
		prediction=prediction.item()


	self.distribution=model.sheet_firing_rate(self.sheets)

        return prediction

    #----------------------------------------------------------------------
    def compute_score(self, observation, prediction):
	score = scores.StudentsTestScore.compute(observation, prediction)

	plt.hist(self.distribution,20,color='w',rwidth=0.8,ec='black')
	if isinstance(observation, int) or isinstance(observation, float):
		plt.xlim(min(min(self.distribution),observation-0.2),max(max(self.distribution),observation+0.2))
		plt.axvline(x=observation,ls='--',lw=1,color='r')
		plt.xticks(np.arange(0,max(max(self.distribution),observation+0.2),0.2))
		plt.savefig(self.sheets.replace('/','')+"_"+ "AverageFiringRateTest"+".png")
	else:
                plt.xlim(min(min(self.distribution),observation["mean"]-0.2),max(max(self.distribution),observation["mean"]+0.2))
                plt.axvline(x=observation["mean"],ls='--',lw=1,color='r')
                plt.xticks(np.arange(0,max(max(self.distribution),observation["mean"]+0.2),0.2))
		plt.savefig(self.sheets.replace('/','')+"_"+ "AverageFiringRateTestComparison"+".png")

	plt.close()
	plt.xlabel("Firing Rate")
	plt.ylabel("Number of neurons")
     	return score


class DistributionAverageFiringRate(Test):
    """Test the if the sheet average firing rates distributions is significatively different 
    than a specific distribution"""

    score_type = scores.ShapiroTestScore
    """specifies the type of score returned by the test"""

    description = """Test if the sheet average firing rates distributions is significatively different 
    than a specific distribution""" 

    def __init__(self,
                 observation = None,
                 sheets = None,
                 name = "Distribution Average Firing Rate Test"):

        self.required_capabilities += (cap.SheetFiringRate,)
        Test.__init__(self, observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        try:
            assert isinstance(observation, str)
        except Exception:
            raise sciunit.errors.ObservationError(
                ("Observation should be a string containing the name of the distribution the average firing rates should be compared to, either: 'normal' or 'lognormal'"))
    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction=model.sheet_firing_rate(self.sheets)
        return prediction

    #----------------------------------------------------------------------
    def compute_score(self, observation, prediction):
        score = scores.ShapiroTestScore.compute(observation, prediction)
        return score


class CoefficientVariationISI(Test):
    """Test the if the sheets distribution of the coefficient of variation of the Inter-Spike-Interval is significatively greater than a predefined value or distribution"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = "Test if the sheets coefficient of variation of the Inter-Spike-Interval is significatively greater than a predefined value"

    def __init__(self,
                 observation = None,
                 sheets = None,
                 name = "Coefficient of Variation of Inter-Spike-Interval Test"):

        if type(observation).__module__=="numpy":
                observation=observation.item()

        self.required_capabilities += (cap.SheetsCVISI,)
        Test.__init__(self, observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)): 
	    try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))
    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction=model.sheets_cv_isi(self.sheets)
        if type(prediction).__module__=="numpy":
                prediction=prediction.item()
        return prediction

    #----------------------------------------------------------------------
    def compute_score(self, observation, prediction):
        score = scores.StudentsTestScore.compute(observation, prediction)
	score.description="If p<0.05 and t>0, then the test is passed"
        return score


class CorrelationCoefficient(Test):
    """Test the if the sheets distribution correlation coefficient is significatively greater than a predefined distribution"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = "Test if the sheets correlation coefficient is greater than a predefined value"

    def __init__(self,
                 observation = None,
                 sheets = None,
                 name = "Correlation Coefficient Test"):

        if type(observation).__module__=="numpy":
                observation=observation.item()

        self.required_capabilities += (cap.SheetsCorrelationCoefficient,)
        Test.__init__(self, observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))
    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction=model.sheets_correlation_coefficient(self.sheets)
        if type(prediction).__module__=="numpy":
                prediction=prediction.item()
        return prediction

    #----------------------------------------------------------------------
    def compute_score(self, observation, prediction):
        score = scores.StudentsTestScore.compute(observation, prediction)
        return score






class RestingPotential(Test):
    """Test the sheets' average resting membrane potential"""

    #score_type = sciunit.scores.CohenDScore
    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = ("Test the sheets' average resting membrane potential")

    def __init__(self,
                 observation,
		 sheets, 
                 name ="Sheets Resting Membrane Potential Test"):
        self.required_capabilities += (cap.SheetsMembranePotential,)
	Test.__init__(self, observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))
    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.sheets_membrane_potential(self.sheets)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        observation["std"] = observation["std"] * (float(observation["n"])/(observation["n"]-1))**0.5 #Bessel's correction for unbiased variance	
	score = scores.StudentsTestScore.compute(observation, prediction)
        return score



class ExcitatorySynapticConductance(Test):
    """Test the sheets' average excitatory synaptic conductance"""

    score_type = scores.StudentsTestScore 
    """specifies the type of score returned by the test"""

    description = ("Test the sheets' average excitatory synaptic conductance")

    def __init__(self,
                 observation,
                 sheets,
                 name ="Sheets Excitatory Synaptic Conductance Test"):
        self.required_capabilities += (cap.SheetsExcitatorySynapticConductance,)
        Test.__init__(self, observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.sheets_excitatory_synaptic_conductance(self.sheets)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        observation["std"] = observation["std"]*(float(observation["n"])/(observation["n"]-1))**0.5 #Bessel's correction for unbiased variance
	score = scores.StudentsTestScore.compute(observation, prediction)
        return score

class InhibitorySynapticConductance(Test):
    """Test the sheets' average inhibitory synaptic conductance"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = ("Test the sheets' average inhibitory synaptic conductance")

    def __init__(self,
                 observation,
                 sheets,
                 name ="Sheets Inhibitory Synaptic Conductance Test"):
        self.required_capabilities += (cap.SheetsInhibitorySynapticConductance,)
        Test.__init__(self, observation, sheets, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.sheets_inhibitory_synaptic_conductance(self.sheets)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        observation["std"] = observation["std"]*(float(observation["n"])/(observation["n"]-1))**0.5 #Bessel's correction for unbiased variance
        score = scores.StudentsTestScore.compute(observation, prediction)
        return score




class SinusoidalGratingsTest(Test):
    """ Extension of Test by adding the parameter contrast """


    def __init__(self,
                 observation = None,
                 sheets = None,
                 contrast = 100, 
		 name = "Test"):

        self.sheets=sheets
	self.contrast=contrast
        Test.__init__(self, observation, sheets, name)

class HWHH(SinusoidalGratingsTest):
    """Test if the sheets' tuning curves Half-Width at Half-Height are significantly different than a predifine distribution"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = ("Test the sheets' if the sheets' tuning curves Half-Width at Half-Height are significantly different than a predifined distribution")

    def __init__(self,
                 observation,
                 sheets,
		 contrast,
                 name ="Half-Width at Half-Height Test"):
        self.required_capabilities += (cap.StatsSheetsHWHH,)
        SinusoidalGratingsTest.__init__(self, observation, sheets, contrast, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.stats_sheets_hwhh(self.sheets, self.contrast)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        observation["std"] = observation["std"]*(float(observation["n"])/(observation["n"]-1))**0.5 #Bessel's correction for unbiased variance
        score = scores.StudentsTestScore.compute(observation, prediction)
        return score

class HWHHContrastComparison(SinusoidalGratingsTest):
    """Test if the sheets' Half-Width at Half-Height values at a certain contrast are significantly different than the values 
	observed with another contrast"""

    score_type = scores.StudentsPairedTestScore
    """specifies the type of score returned by the test"""

    description = ("Test the sheets' if the sheets' Half-Width at Half-Height values at a certain contrast are significantly different than the values observed with another contrast")

    def __init__(self,
                 observation,
                 sheets,
                 contrast,
                 name ="Half-Width at Half-Height Contrast Comparison Test"):
        self.required_capabilities += (cap.SheetsHWHH,)
        SinusoidalGratingsTest.__init__(self, observation, sheets, contrast, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, list)):
   		raise sciunit.errors.ObservationError(
                    ("Observation must return a list of values"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.sheets_hwhh(self.sheets, self.contrast)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        score = scores.StudentsPairedTestScore.compute(observation, prediction)
        return score




class RURA(SinusoidalGratingsTest):
    """Test if the sheets' Relative Unselective Response Amplitude are significantly different than a predifined distribution"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = ("Test the sheets' if the sheets' tuning curves Relative Unselective Response Amplitude are significantly different than a predifined distribution")

    def __init__(self,
                 observation,
                 sheets,
                 contrast,
                 name ="Relative Unselective Response Amplitude Test"):
        self.required_capabilities += (cap.StatsSheetsRURA,)
        SinusoidalGratingsTest.__init__(self, observation, sheets, contrast, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.stats_sheets_rura(self.sheets, self.contrast)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        observation["std"] = observation["std"]*(float(observation["n"])/(observation["n"]-1))**0.5 #Bessel's correction for unbiased variance
        score = scores.StudentsTestScore.compute(observation, prediction)
        return score



class RURAContrastComparison(SinusoidalGratingsTest):
    """Test if the sheets' Relative Unselective Response Amplitude values at a certain contrast are significantly different than the 
	values observed with another contrast"""

    score_type = scores.StudentsPairedTestScore
    """specifies the type of score returned by the test"""

    description = ("Test if the sheets' Relative Unselective Response Amplitude values at a certain contrast are significantly different than the values observed with another contrast")

    def __init__(self,
                 observation,
                 sheets,
                 contrast,
                 name ="Relative Unselective Response Amplitude Contrast Comparison Test"):
        self.required_capabilities += (cap.SheetsRURA,)
        SinusoidalGratingsTest.__init__(self, observation, sheets, contrast, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, list)):
                raise sciunit.errors.ObservationError(
                    ("Observation must return a list of values"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.sheets_rura(self.sheets, self.contrast)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        score = scores.StudentsPairedTestScore.compute(observation, prediction)
        return score


class ModulationRatio(SinusoidalGratingsTest):
    """Test if the sheets' modulation ratios are significantly different than a predifined distribution"""

    score_type = scores.StudentsTestScore
    """specifies the type of score returned by the test"""

    description = ("Test if the sheets' modulation ratios are significantly different than a predifined distribution")

    def __init__(self,
                 observation,
                 sheets,
                 contrast,
                 name ="Modulation Ratio test"):
        self.required_capabilities += (cap.StatsSheetsModulationRatio,)
        SinusoidalGratingsTest.__init__(self, observation, sheets, contrast, name)

    #----------------------------------------------------------------------

    def validate_observation(self, observation):
        if not (isinstance(observation, int) or isinstance(observation, float)):
            try:
                assert len(observation.keys()) == 3
                for key, val in observation.items():
                    assert key in ["mean", "std","n"]
                    if key =="n":
                        assert (isinstance(val, int))
                    else:
                        assert (isinstance(val, int) or isinstance(val, float))
            except Exception:
                raise sciunit.errors.ObservationError(
                    ("Observation must return a integer, a float, or a dictionary of the form:"
                     "{'mean': NUM1, 'std': NUM2, 'n' : NUM3}"))

    #----------------------------------------------------------------------

    def generate_prediction(self, model):
        prediction = model.stats_modulation_ratio(self.sheets, self.contrast)
        return prediction

    #----------------------------------------------------------------------

    def compute_score(self, observation, prediction):
        observation["std"] = observation["std"]*(float(observation["n"])/(observation["n"]-1))**0.5 #Bessel's correction for unbiased variance
        score = scores.StudentsTestScore.compute(observation, prediction)
        return score


import sciunit
from capabilities import * # One of many potential model capabilities.
from mozaik.analysis.analysis import *
from mozaik.analysis.vision import *
from mozaik.storage.queries import *
from mozaik.storage.datastore import PickledDataStore
from mozaik.tools.mozaik_parametrized import MozaikParametrized
import random

class ModelV1Spont(sciunit.Model, StatsSheetsFiringRate, SheetFiringRate, SheetsMembranePotential, SheetsExcitatorySynapticConductance, SheetsInhibitorySynapticConductance, SheetsCorrelationCoefficient, SheetsCVISI):
	"""A model of spontaneous activity of V1."""

	def __init__(self, path, name="Spontaneous activity of V1"):
		""" path should be a string containing  the path of the files containing the results of the simulation of the model
		"""
		self.data_store=PickledDataStore(load=True,parameters=ParameterSet({'root_directory': path,'store_stimuli' : False}),replace=True)

		self.data_store_spont = param_filter_query(self.data_store,st_direct_stimulation_name=None,st_name="InternalStimulus")
		super(ModelV1Spont, self).__init__(name=name)


	def sheet_firing_rate(self, sheet):
		"""Get the average firing rates of the sheet
                sheet should be a string containing the name of the sheet
                """
		try:
                        assert (isinstance(sheet, str))
                except Exception:
                        raise sciunit.errors.Error("Parameter sheet must be a string")

                return param_filter_query(self.data_store_spont, value_name='Firing rate', identifier='PerNeuronValue', sheet_name=sheet, analysis_algorithm='TrialAveragedFiringRate',ads_unique=True).get_analysis_result()[0].values

	

	def stats_sheets_firing_rate(self, sheets):
		"""Get descriptive statistics about the average firing rates of the sheets
		sheets should be a string containing the name of the sheet, or a list of strings containing the names of the sheets
		"""	

                ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
                population=[]
                mean=[]
                std=[]

                if isinstance(sheets, str):
			FR=self.sheet_firing_rate(sheets)
                        mean_FR, std_FR = ms(FR)
                        n=len(FR)

                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")
				FR=self.sheet_firing_rate(s)
                                population.append(len(FR))
                                mean.append(numpy.mean(FR))
                                std.append(numpy.std(FR, ddof=1))

                        mean_FR=numpy.average(mean,weights=population)
			
			#Computation of the pooled standard deviation
                        std_FR=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)

                return {"mean": mean_FR, "std": std_FR, "n": n}



	def sheets_cv_isi(self, sheets):
                """Get the coefficient of variation of the inter-spike-interval of the sheets
                sheets should be a string containing the name of the sheet, or a list of strings containing the names of the sheets
                """

                ms = lambda a: (numpy.mean(a),numpy.std(a, ddof=1))
                population=[]
                mean=[]
                std=[]

                if isinstance(sheets, str):
			cv_isi=param_filter_query(self.data_store_spont, value_name='CV of ISI squared', identifier='PerNeuronValue', sheet_name=sheets, analysis_algorithm='Irregularity',ads_unique=True).get_analysis_result()[0].values

                        mean_cv_isi, std_cv_isi = ms(cv_isi)
                        n=len(cv_isi)

                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")
                        	cv_isi=param_filter_query(self.data_store_spont, value_name='CV of ISI squared', identifier='PerNeuronValue', sheet_name=s, analysis_algorithm='Irregularity',ads_unique=True).get_analysis_result()[0].values
				population.append(len(cv_isi))
                                mean.append(numpy.mean(cv_isi))
                                std.append(numpy.std(cv_isi, ddof=1))

                        mean_cv_isi=numpy.average(mean,weights=population)
			
			#Computation of the pooled standard deviation
                        std_cv_isi=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)
		
                return {"mean": mean_cv_isi, "std": std_cv_isi, "n": n}

	
	def sheets_correlation_coefficient(self, sheets):
		"""Get the correlation coefficient of the sheets
                sheets should be a string containing the name of the sheet, or a list of strings containing the names of the sheets
                """

                ms = lambda a: (numpy.mean(a),numpy.std(a))
                population=[]
                mean=[]
                std=[]

                if isinstance(sheets, str):
			
			CC=param_filter_query(self.data_store_spont, value_name='Correlation coefficient(psth (bin=10.0))', identifier='PerNeuronValue', sheet_name=sheets, analysis_algorithm='NeuronToNeuronAnalogSignalCorrelations',ads_unique=True).get_analysis_result()[0].values
                        mean_CC, std_CC = ms(CC)
                        n=len(CC)

                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

				CC=param_filter_query(self.data_store_spont, value_name='Correlation coefficient(psth (bin=10.0))', identifier='PerNeuronValue', sheet_name=s, analysis_algorithm='NeuronToNeuronAnalogSignalCorrelations',ads_unique=True).get_analysis_result()[0].values
                                population.append(len(CC))
                                mean.append(numpy.mean(CC))
                                std.append(numpy.std(CC, ddof=1))

                        mean_CC=numpy.average(mean,weights=population)
			
			#Computation of the pooled standard deviation
                        std_CC=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)
		
		return {"mean": mean_CC, "std": std_CC, "n": n}


	def sheets_membrane_potential(self, sheets):
		"""Get the average resting membrane potential of the sheets"""
	
		ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
		population=[]
		mean=[]
		std=[]

		if type(sheets)== str:
			mean_VM, std_VM = ms(param_filter_query(self.data_store_spont,sheet_name=sheets,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(VM)',ads_unique=True).get_analysis_result()[0].values)
			n=len(param_filter_query(self.data_store_spont, sheet_name=s).get_segments()[0].get_stored_vm_ids())
	
		else:
			try:
		                assert (isinstance(sheets, list))
        		except Exception:
            			raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

			for s in sheets:
				try: 
	                                assert (isinstance(s, str))
	                        except Exception:
	                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")
				population.append(len(param_filter_query(self.data_store_spont, sheet_name=s).get_segments()[0].get_stored_vm_ids()))
                                mean.append(numpy.mean(param_filter_query(self.data_store_spont,sheet_name=s,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(VM)',ads_unique=True).get_analysis_result()[0].values))
                                std.append(numpy.std(param_filter_query(self.data_store_spont,sheet_name=s,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(VM)',ads_unique=True).get_analysis_result()[0].values, ddof=1))
	
			mean_VM=numpy.average(mean,weights=population)
			
			#Computation of the pooled standard deviation
			std_VM=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
			n=sum(population)

		return {"mean": mean_VM, "std": std_VM, "n": n}




	def sheets_excitatory_synaptic_conductance(self, sheets):
		"""Get the average excitatory synaptic conductance of the sheets"""
               
		ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
                population=[]
                mean=[]
                std=[]

                if type(sheets)== str:
                        mean_ECond, std_ECond = ms(param_filter_query(self.data_store_spont,sheet_name=sheets,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(ECond)',ads_unique=True).get_analysis_result()[0].values)
                        n=len(param_filter_query(self.data_store_spont, sheet_name=s).get_segments()[0].get_stored_esyn_ids())
                        
                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")
                                population.append(len(param_filter_query(self.data_store_spont, sheet_name=s).get_segments()[0].get_stored_esyn_ids()))
                                mean.append(numpy.mean(param_filter_query(self.data_store_spont,sheet_name=s,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(ECond)',ads_unique=True).get_analysis_result()[0].values))
                                std.append(numpy.std(param_filter_query(self.data_store_spont,sheet_name=s,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(ECond)',ads_unique=True).get_analysis_result()[0].values, ddof=1))
                        
                        mean_ECond=numpy.average(mean,weights=population)
			
			#Computation of the pooled standard deviation
                        std_ECond=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)

		return {"mean": mean_ECond, "std": std_ECond, "n": n}
	



	def sheets_inhibitory_synaptic_conductance(self, sheets):
		"""Get the average inhibitory synaptic conductance of the sheets"""
	
                ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
                population=[]
                mean=[]
                std=[]

                if type(sheets)== str:
                        mean_ICond, std_ICond = ms(param_filter_query(self.data_store_spont,sheet_name=sheets,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(ICond)',ads_unique=True).get_analysis_result()[0].values)
                        n=len(param_filter_query(self.data_store_spont, sheet_name=s).get_segments()[0].get_stored_isyn_ids())
                        
                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                                population.append(len(param_filter_query(self.data_store_spont, sheet_name=s).get_segments()[0].get_stored_isyn_ids()))
                                mean.append(numpy.mean(param_filter_query(self.data_store_spont,sheet_name=s,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(ICond)',ads_unique=True).get_analysis_result()[0].values))
                                std.append(numpy.std(param_filter_query(self.data_store_spont,sheet_name=s,analysis_algorithm='Analog_MeanSTDAndFanoFactor',value_name='Mean(ICond)',ads_unique=True).get_analysis_result()[0].values, ddof=1))
                        
                        mean_ICond=numpy.average(mean,weights=population)

			#Computation of the pooled standard deviation
                        std_ICond=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)

		return {"mean": mean_ICond, "std": std_ICond, "n": n}


class ModelV1(ModelV1Spont, SheetsHWHH, SheetsRURA, StatsSheetsRURA, StatsSheetsHWHH):
        """A model of spontaneous activity of V1."""

        def __init__(self, path, name="Spontaneous activity of V1"):
                """ path should be a string containing  the path of the files containing the results of the simulation of the model
                """
		super(ModelV1, self).__init__(path=path, name=name)
                self.data_store_drift = param_filter_query(self.data_store,st_direct_stimulation_name=None,st_name="FullfieldDriftingSinusoidalGrating")

        def sheets_hwhh(self, sheets, contrast):
                """Get the Half-Width at Half-Height of all neurons of the sheets
                sheets should be a string specifying the name of the sheet
                contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
                A list of contrast can be used instead if the excluding of neurons for should be based on their values for more than
                one contrast. e.g. when wanting to compare the results for 2 values of contrast. Only the first value of the list
                will be used for the computation of the HWHH
                """

                if not isinstance(contrast,list):
                        contrast=[contrast]
                elif len(contrast) != 2:
                        raise sciunit.errors.Error("Parameter contrast must be an integer or a list of 2 integers")

                ids=param_filter_query(self.data_store_drift,sheet_name=sheets).get_segments()[0].get_stored_spike_train_ids()

                for c in contrast:
                	base = queries.param_filter_query(self.data_store_drift,sheet_name=sheets,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=c,value_name='orientation baseline of Firing rate',ads_unique=True).get_analysis_result()[0].get_value_by_id(ids)
                        ids=numpy.array(ids)[numpy.array(base) > 0.]
                        base = queries.param_filter_query(self.data_store_drift,sheet_name=sheets,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=c,value_name='orientation baseline of Firing rate',ads_unique=True).get_analysis_result()[0].get_value_by_id(ids)                        
			mmax = queries.param_filter_query(self.data_store_drift,sheet_name=sheets,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=c,value_name='orientation max of Firing rate',ads_unique=True).get_analysis_result()[0].get_value_by_id(ids)
                        ids = numpy.array(ids)[numpy.array(base)+numpy.array(mmax) > 1.0]
                        errors = queries.param_filter_query(self.data_store_drift,value_name=['orientation fitting error of Firing rate'],sheet_name=sheets,st_contrast=c, ads_unique=True).get_analysis_result()[0]
                        ids=numpy.array(ids)[numpy.array(errors.get_value_by_id(ids))<0.3]

                return param_filter_query(self.data_store_drift,sheet_name=sheets,st_contrast=contrast[0],value_name='orientation HWHH of Firing rate',ads_unique=True).get_analysis_result()[0].get_value_by_id(ids)


        def stats_sheets_hwhh(self, sheets, contrast):
        	"""Get the mean and standard error of Half-Width at Half-Height of all neurons of the sheets
            	sheets should be a string specifying the name of the sheet
            	contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
                A list of contrast can be used instead if the excluding of neurons for should be based on their values for more than
                one contrast. e.g. when wanting to compare the results for 2 values of contrast. Only the first value of the list 
		will be used for the computation of the HWHH  
		"""
                ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
                population=[]
                mean=[]
                std=[]
																															
                if type(sheets)== str:
                                
                        HWHH=self.sheets_hwhh(sheets,contrast)

                        mean_HWHH, std_HWHH = ms(HWHH)
                        n=len(HWHH)

                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        	HWHH=self.sheets_hwhh(s,contrast)
                                population.append(len(HWHH))
                                mean.append(numpy.mean(HWHH))
                                std.append(numpy.std(HWHH, ddof=1))
                        mean_HWHH=numpy.average(mean,weights=population)

			#Computation of the pooled standard deviation 
                        std_HWHH=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)
                return {"mean": mean_HWHH, "std": std_HWHH, "n": n}


	def sheets_rura(self, sheets, contrast):
                """Get the Relative Unselective Response Amplitude of all neurons of the sheets
                sheets should be a string specifying the name of the sheet
                contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
                A list of contrast can be used instead if the excluding of neurons for should be based on their values for more than                 one contrast. e.g. when wanting to compare the results for 2 values of contrast. Only the first value of the list
                will be used for the computation of the RURA
                """


                if not isinstance(contrast,list):
                        contrast=[contrast]
                elif len(contrast) != 2:
                        raise sciunit.errors.Error("Parameter contrast must be an integer or a list of 2 integers")
			
                ids=param_filter_query(self.data_store_spont,sheet_name=sheets).get_segments()[0].get_stored_spike_train_ids()
			
                for i in range(len(contrast)):
                	b = queries.param_filter_query(self.data_store_drift,sheet_name=sheets,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=contrast[i],value_name='orientation baseline of Firing rate',ads_unique=True).get_analysis_result()[0]
                        if i ==0:
                                base=b
                	ids=numpy.array(ids)[numpy.array(b.get_value_by_id(ids)) > 0.]
                        m = queries.param_filter_query(self.data_store_drift,sheet_name=sheets,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=contrast[i],value_name='orientation max of Firing rate',ads_unique=True).get_analysis_result()[0]
                        if i ==0:
                                mmax=m
                	b = queries.param_filter_query(self.data_store_drift,sheet_name=sheets,st_name='FullfieldDriftingSinusoidalGrating',st_contrast=contrast[i],value_name='orientation baseline of Firing rate',ads_unique=True).get_analysis_result()[0]
		        ids = numpy.array(ids)[numpy.array(b.get_value_by_id(ids))+numpy.array(m.get_value_by_id(ids)) > 1.0]
                        errors = queries.param_filter_query(self.data_store_drift,value_name=['orientation fitting error of Firing rate'],sheet_name=sheets,st_contrast=contrast[i], ads_unique=True).get_analysis_result()[0]
                        ids=numpy.array(ids)[numpy.array(errors.get_value_by_id(ids))<0.3]

		return [100*base.get_value_by_id(i)/(mmax.get_value_by_id(i)+base.get_value_by_id(i)) for i in ids] 

        def stats_sheets_rura(self, sheets, contrast):
                """Get the mean and standard error of Relative Unselective Response Amplitude of all neurons of the sheets
                sheets should be a string specifying the name of the sheet
                contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
                A list of contrast can be used instead if the excluding of neurons for should be based on their values for more than                 one contrast. e.g. when wanting to compare the results for 2 values of contrast. Only the first value of the list 
                will be used for the computation of the RURA  
		"""

                ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
                population=[]
                mean=[]
                std=[]

                if type(sheets)== str:
			
			RURA=self.sheets_rura(sheets,contrast)
			
                        mean_RURA, std_RURA = ms(RURA)
                        n=len(RURA)

                else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")
                        
			for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        	RURA=self.sheets_rura(s,contrast)
                                population.append(len(RURA))
                                mean.append(numpy.mean(RURA))
                                std.append(numpy.std(RURA, ddof=1))
                        mean_RURA=numpy.average(mean,weights=population)

			#Computation of the pooled standard deviation 
                        std_RURA=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)
			print(mean_RURA)
			print(std_RURA)
			print(n)
                return {"mean": mean_RURA, "std": std_RURA, "n": n}


        def stats_sheets_modulation_ratio(self, sheets, contrast):
                """Get the mean and standard error of the modulation ratio of all neurons of the sheets
                sheets should be a string specifying the name of the sheet
                contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
                """

                ms = lambda a: (numpy.mean(a),numpy.std(a,ddof=1))
                population=[]
                mean=[]
                std=[]


                if type(sheets)== str:

			mr = param_filter_query(self.data_store_drift,sheet_name=sheets,st_contrast=contrast,value_name='Modulation ratio(time)',ads_unique=True).get_analysis_result()[0].values

                        mean_mr, std_mr = ms(mr)
                        n=len(mr)
                
		else:
                        try:
                                assert (isinstance(sheets, list))
                        except Exception:
                                raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                        for s in sheets:
                                try:
                                        assert (isinstance(s, str))
                                except Exception:
                                        raise sciunit.errors.Error("Parameter sheets must be a string or a list of string")

                                mr = param_filter_query(self.data_store_drift,sheet_name=sheets,st_contrast=contrast,value_name='Modulation ratio(time)',ads_unique=True).get_analysis_result()[0].values
				population.append(len(mr))
                                mean.append(numpy.mean(mr))
                                std.append(numpy.std(mr, ddof=1))
                        mean_mr=numpy.average(mean,weights=population)

			#Computation of the pooled standard deviation 
                        std_mr=(sum([(p-1)*st**2 for (st,p) in zip(std,population)])/(sum(population)-len(population)))**0.5
                        n=sum(population)

                return {"mean": mean_mr, "std": std_mr, "n": n}


import sciunit

#==============================================================================

class SheetFiringRate(sciunit.Capability):
    """Get the average firing rate of the sheet"""

    def sheet_firing_rate(self, sheet):
        """Model should implement this method such as to retrieve the average firing rate of its sheet of neurons passed in input 
	   sheet should be a string specifying the name of the sheet
        """
        raise NotImplementedError()


class StatsSheetsFiringRate(SheetFiringRate):
    """ Get descriptibe statistics about the distribution of the average firing rates of the sheets """

    def stats_sheets_firing_rate(self, sheets):
        """Model should implement this method such as to retrieve descriptive statistics about the distribution of 
	the average firing rates of its sheets of neurons passed in input 
	   sheet should be a string specifying the name of the sheet
	"""
	raise NotImplementedError()

class SheetsMembranePotential(sciunit.Capability):
    """Get the average resting membrane potential of the sheets"""

    def sheets_membrane_potential(self, sheets):
        """Model should implement this method such as to retrieve the resting membrane potential 
	   of its sheets of neurons passed in input 
	   sheets should be a string or a list of strings specifying the name of the sheets
        """
        raise NotImplementedError()

class SheetsExcitatorySynapticConductance(sciunit.Capability):
    """Get the average excitatory synaptic conductance of the sheets"""

    def sheets_excitatory_synaptic_conductance(self, sheets):
        """Model should implement this method such as to retrieve the excitatory synaptic conductance 
	   of its sheets of neurons passed in input 
	   sheets should be a string or a list of strings specifying the name of the sheets
        """
        raise NotImplementedError()

class SheetsInhibitorySynapticConductance(sciunit.Capability):
    """Get the average inhibitory synaptic conductance of the sheets"""

    def sheets_inhibitory_synaptic_conductance(self, sheets):
        """Model should implement this method such as to retrieve the inhibitory synaptic conductance
	   of its sheets of neurons passed in input 
	   sheets should be a string or a list of strings specifying the name of the sheet
        """
        raise NotImplementedError()


class SheetsCVISI(sciunit.Capability):
    """Get the average coefficient of variation of the inter-spike-interval of all neurons of the sheets"""

    def sheets_cv_isi(self, sheets):
        """ Model should implement this method such as to retrieve the coefficient of variation of the inter-spike-interval 
            of its sheets of neurons passed in input
            sheets should be a string specifying the name of the sheet
        """


class SheetsCorrelationCoefficient(sciunit.Capability):
    """Get the average correlation coefficient between the PSTH of all pair of neurons of the sheets"""

    def sheets_correlation_coefficient(self, sheets):
	""" Model should implement this method such as to retrieve the correlation coefficient
	    of its sheets of neurons passed in input
	    sheets should be a string specifying the name of the sheet
	"""
	raise NotImplementedError()


class SheetsHWHH(sciunit.Capability):
    """Get the list of Half-Width at Half-Height of all neurons of the sheet"""

    def sheets_hwhh(self, sheets, contrast):
        """ Model should implement this method such as to retrieve the Half-Width at Half-Height
            of its sheets of neurons passed in input
            sheets should be a string specifying the name of the sheet
            contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
        """
        raise NotImplementedError()

class StatsSheetsHWHH(sciunit.Capability):
    """Get the mean and standard deviation of Half-Width at Half-Height of all neurons of the sheets"""

    def stats_sheets_hwhh(self, sheets, contrast):
        """ Model should implement this method such as to retrieve the mean and standard deviation of the Half-Width at Half-Height 
            of its sheets of neurons passed in input
            sheets should be a string specifying the name of the sheet
	    contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
        """
        raise NotImplementedError()

class SheetsRURA(sciunit.Capability):
    """Get Relative Unselective Response amplitude of all neurons of the sheets"""

    def sheets_rura(self, sheets, contrast):
        """ Model should implement this method such as to retrieve the Relative Unselective Response amplitude of all neurons 
            of its sheets passed in input
            sheets should be a string specifying the name of the sheet
            contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
        """
        raise NotImplementedError()

class StatsSheetsRURA(sciunit.Capability):
    """Get the mean and standard deviation of the Relative Unselective Response amplitude of all neurons of the sheets"""

    def stats_sheets_rura(self, sheets, contrast):
        """ Model should implement this method such as to retrieve the mean and the standard deviation of the Relative Unselective
	    Response Amplitude of its sheets of neurons passed in input
            sheets should be a string specifying the name of the sheet
        """
        raise NotImplementedError()

class SheetsModulationRatio(sciunit.Capability):
    """Get the mean and standard deviation of the modulation ratio of all neurons of the sheets"""

    def stats_modulation_ratio(self, sheets, contrast):
        """ Model should implement this method such as to retrieve the mean and the standard deviation of the modulation ratio
	 of its sheets of neurons passed in input
            sheets should be a string specifying the name of the sheet
            contrast should be an integer or a float specifying the contrast of the sinusoidal grating stimulus
        """
        raise NotImplementedError()


import sys
from models import *
from tests import *

newModel=ModelV1(sys.argv[1])

newTest=RURA({"mean": 2.5, "std": 8.5, "n": 58},["V1_Exc_L4","V1_Exc_L2/3"],100)
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=RURA({"mean": 18.1, "std": 25.7, "n": 19},["V1_Inh_L4","V1_Inh_L2/3"],100)
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=RURAContrastComparison(newModel.sheets_rura("V1_Exc_L4",[30,100]),"V1_Exc_L4",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=RURAContrastComparison(newModel.sheets_rura("V1_Inh_L4",[30,100]),"V1_Inh_L4",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=RURAContrastComparison(newModel.sheets_rura("V1_Exc_L2/3",[30,100]),"V1_Exc_L2/3",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=RURAContrastComparison(newModel.sheets_rura("V1_Inh_L2/3",[30,100]),"V1_Inh_L2/3",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=HWHH({"mean": 23.4, "std": 9.2, "n": 58},["V1_Exc_L4","V1_Exc_L2/3"],100)
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=HWHH({"mean": 31.9, "std": 11.3, "n": 19},["V1_Inh_L4","V1_Inh_L2/3"],100)
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=HWHHContrastComparison(newModel.sheets_hwhh("V1_Exc_L4",[30,100]),"V1_Exc_L4",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=HWHHContrastComparison(newModel.sheets_hwhh("V1_Inh_L4",[30,100]),"V1_Inh_L4",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=HWHHContrastComparison(newModel.sheets_hwhh("V1_Exc_L2/3",[30,100]),"V1_Exc_L2/3",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=HWHHContrastComparison(newModel.sheets_hwhh("V1_Inh_L2/3",[30,100]),"V1_Inh_L2/3",[100,30])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=AverageFiringRate(2,"V1_Exc_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=AverageFiringRate(newModel.stats_sheets_firing_rate("V1_Exc_L4"),"V1_Inh_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=AverageFiringRate(2,"V1_Exc_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=AverageFiringRate(newModel.stats_sheets_firing_rate("V1_Exc_L2/3"),"V1_Inh_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=DistributionAverageFiringRate("lognormal","V1_Exc_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=DistributionAverageFiringRate("lognormal","V1_Inh_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=DistributionAverageFiringRate("lognormal","V1_Exc_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=DistributionAverageFiringRate("lognormal","V1_Inh_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=CoefficientVariationISI(0.8,"V1_Exc_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=CoefficientVariationISI(0.8,"V1_Exc_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=CoefficientVariationISI(0.8,"V1_Inh_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=CoefficientVariationISI(0.8,"V1_Inh_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=CorrelationCoefficient(newModel.sheets_correlation_coefficient("V1_Exc_L4"),"V1_Inh_L4")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=CorrelationCoefficient(newModel.sheets_correlation_coefficient("V1_Exc_L2/3"),"V1_Inh_L2/3")
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=RestingPotential({"mean": -72.3, "std": 5, "n": 217},["V1_Exc_L4", "V1_Inh_L4", "V1_Exc_L2/3", "V1_Inh_L2/3"])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=ExcitatorySynapticConductance({"mean": 0.001, "std": 0.0009, "n": 22},["V1_Exc_L4", "V1_Inh_L4", "V1_Exc_L2/3", "V1_Inh_L2/3"])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

newTest=InhibitorySynapticConductance({"mean": 0.0049, "std": 0.0036, "n": 22},["V1_Exc_L4", "V1_Inh_L4", "V1_Exc_L2/3", "V1_Inh_L2/3"])
score= newTest.judge(newModel, deep_error=True)
score.summarize()

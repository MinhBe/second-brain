sensors
Article
CTTGAN: Traffic Data Synthesizing Scheme Based on
Conditional GAN
JiayuWang1,2 ,XuehuYan1,2,* ,LintaoLiu1,2,LonglongLi1,2 andYongqiangYu1,2
1 CollegeofElectronicEngineering,NationalUniversityofDefenseTechnology,Hefei230037,China;
wangjiayu@nudt.edu.cn(J.W.);lintao89@nudt.edu.cn(L.L.);lilongs@nudt.edu.cn(L.L.);
publicmouse@126.com(Y.Y.)
2 AnhuiProvinceKeyLaboratoryofCyberspaceSecuritySituationAwarenessandEvaluation,
Hefei230037,China
* Correspondence:publictiger@126.com
Abstract:Mostmachinelearningalgorithmsonlyhaveagoodrecognitionrateonbalanceddatasets.
However,inthefieldofmalicioustrafficidentification,benigntrafficonthenetworkisfargreater
thanmalicioustraffic,andthenetworktrafficdatasetisimbalanced,whichmakesthealgorithm
havealowidentificationrateforsmallcategoriesofmalicioustrafficsamples.Thispaperpresents
a traffic sample synthesizing model named Conditional Tabular Traffic Generative Adversarial
Network(CTTGAN),whichusesaConditionalTabularGenerativeAdversarialNetwork(CTGAN)
algorithmtoexpandthesmallcategorytrafficsamplesandbalancethedatasetinordertoimprove
themalicioustrafficidentificationrate.TheCTTGANmodelexpandsandrecognizesfeaturedata,
whichmeetstherequirementsofamachinelearningalgorithmfortrainingandpredictiondata.The
contributionsofthispaperareasfollows:first,thesmallcategorysamplesareexpandedandthetraffic
datasetisbalanced;second,thestoragecostandcomputationalcomplexityarereducedcomparedto
modelsusingimagedata;third,discretevariablesandcontinuousvariablesintrafficfeaturedata
(cid:1)(cid:2)(cid:3)(cid:1)(cid:4)(cid:5)(cid:6)(cid:7)(cid:8)(cid:1)
(cid:1)(cid:2)(cid:3)(cid:4)(cid:5)(cid:6)(cid:7) areprocessedatthesametime,andthedatadistributionisdescribedwell.Theexperimentalresults
Citation:Wang,J.;Yan,X.;Liu,L.;Li, showthattherecognitionrateoftheexpandedsamplesismorethan0.99inMLP,KNNandSVM
L.;Yu,Y.CTTGAN:TrafficData algorithms. Inaddition, therecognitionrateoftheproposedCTTGANmodelisbetterthanthe
SynthesizingSchemeBasedon oversamplingandundersamplingschemes.
ConditionalGAN.Sensors2022,22,
5243. https://doi.org/10.3390/ Keywords:malicioustrafficidentification;conditionalGAN;samplesynthesis;databalancing
s22145243
AcademicEditors:ZhongyunHua
andYushuZhang
1. Introduction
Received:6June2022
Therapiddevelopmentofnetworktechnologybringsconveniencetopeople.However,
Accepted:11July2022
itisalsoaccompaniedbysecurityproblems.Manydevicesthatmeettechnicalrequirements
Published:13July2022
canaccesstheInternet,includingsoftwarewithmaliciousbehaviors,suchasinvadingusers’
Publisher’sNote:MDPIstaysneutral hosts,stealinginformation,destroyingequipment,etc.,bringinggreathiddendangersto
withregardtojurisdictionalclaimsin users’privacyandtothesecurityoftheirproperty. Thesecureprotectionofinformation
publishedmapsandinstitutionalaffil- andpropertyonthenetworkisakeyproblemtobesolved,andtheaccurateidentification
iations.
oftrafficplaysanimportantroleinsolvingthisproblem.
Themethodsofmalicioustrafficidentificationmainlyincludeport-based[1],payload-
based [2,3] and machine learning algorithms. The port based identification method is
nolongersuitableforthecurrentnetworkenvironmentbecausemanynetworkattacks
Copyright: © 2022 by the authors.
nolongerusefixedandconventionalports. However,identificationmethodsbasedon
Licensee MDPI, Basel, Switzerland.
payloads cannot identify the encrypted traffic, and at present, traffic encryption in the
This article is an open access article
networkhasbecomeagradualtrend. Inordertosolvetheproblemofencryptedmalicious
distributed under the terms and
trafficidentification,peoplebegantostudytheidentificationmethodbasedonmachine
conditionsoftheCreativeCommons
Attribution(CCBY)license(https:// learningalgorithms.
creativecommons.org/licenses/by/ Lucia et al. [4] used Convolutional Neural Networks (CNN) and Support Vector
4.0/). Machine(SVM)algorithmstoidentifytraffic,andtherecognitioneffectofSVMalgorithm
Sensors2022,22,5243.https://doi.org/10.3390/s22145243 https://www.mdpi.com/journal/sensors

Sensors2022,22,5243 2of17
was better than the CNN. Shekhawat et al. [5] used three machine learning algorithms
(SVM,XGBoost,RandomForest)toidentifytrafficrespectively,andfurtheranalyzedthe
extractedfeatures. Theysuggestedthatfeatureselectionbasedonthemodelitself(domain
free method) may be better than selecting features based on human expertise. Some
researchersusedeeplearningalgorithmstoautomaticallyextractfeaturesandthenidentify
traffic[6–8].Heetal.[9]proposedamalicioustrafficdetectionmethodbasedonaCNNand
Auto-Encoders(AE).Theencoderistrainedwithbenigntraffictolearnitsreconstruction
ability.Whenmalicioustrafficisinputintotheencoder,thereconstructionratecannotreach
thethreshold;thatis,thetrafficisjudgedasamaliciousone. Zhongetal.[10]proposed
aheterogeneousensemble-learningtrafficdetectionframeworkbasedonmultipledeep
learningmodels.
Manymachinelearningalgorithmsworkwellonbalanceddatasetsbutnotonimbal-
anceddatasets. Intherealnetworkenvironment,benigntraffichasalargeamountofdata
andiseasytocollect,whilemalicioustraffichasasmallamountofdataandisdifficultto
collect. Inmanynetworktrafficdatasets,benigntrafficisfarmorethanmalicioustraffic.
Similarsituationsexistinpracticalapplications. Weneedtoaccuratelyidentifymalicious
traffic in a large number of benign traffic. Data imbalance leads to the low recognition
accuracyofmanymachinelearningmodels. Peoplehaveconductedalotofresearchto
solvethisproblem. Fromtheperspectiveofmodelimprovement,Telikanietal.[11]pro-
posedacost-sensitivedeeplearningmodel,whichdeterminesthecostfunctionaccording
tothecostmatrixofdata,soastoreducetheimpactofdatasetimbalance. Heetal.[9]only
usedthelargeamountofbenigntrafficdatatotraintheAEandjudgewhetherthetraffic
isbenignormaliciousthroughthereconstructionrateoftheAE.However,thesekindsof
modelsarecomplexandhavepooradaptabilitytodifferenttrafficdata.
Fromtheperspectiveofdatabalancing,thetraditionalmethodsmainlyincludeover-
sampling[12]andundersampling[13]techniques. Oversamplingtechnologymaycause
overfittingproblem,andundersamplingtechnologywillleadtoinsufficientlearningofthe
data.SyntheticMinorityOversamplingTechnique(SMOTE)[14]technologyisanimproved
algorithmbasedonoversampling. Insteadofcopyingsamples,itaddsasmallamountof
noisetothesamplestoobtaindifferentdata. Qianetal.[15],Yanetal.[16]balancedthe
trafficdatasetswiththeSMOTEalgorithmandidentifiedtrafficonnewdatasets. However,
SMOTEtechnologydoesnotaddnewinformationtothesamples. Goodfellow[17]first
proposedgeneratingsampledatausingtheGenerativeAdversarialNetwork(GAN)in
2014. Differentfromtheabovemethods,thedatageneratedusingtheGANcontaindata
samplescompletelydifferentfromtheoriginaldata.
Vuetal.[18]usedanAuxiliaryClassifierGenericAdvantageousNetwork(ACGAN)[19]to
expandtrafficsamples,balanceSSHandnon-SSHdata,andthenidentifiedtraffic.Dongetal.[8]
usedtheWassersteinGAN(WGAN)[20]tobalancethetrafficdatasetandclassifyit.Thereare
alsostudiesthatusetheGANanditsderivativealgorithmstogeneratetrafficdata[12,21,22],
mixedwithrealdataandtrainmodelsandimprovingtheperformanceofIDSandmalware
detectionsystems.IntheresearchofusingGANanditsderivativealgorithmstoexpandtraffic
datasets,manyofthestudiesusetheoriginaltrafficdataandconvertitintoimages,andthen
expandthedatasetsandidentifythetraffic.However,thedatausedbymanymachinelearning
algorithmstotrainmodelsandpredictcategoriesarefeaturedata.Ifwesynthesizeoriginaldata
orimages,wealsoneedtoextractfeatureslater.Moreover,thestorageandoperationofimages
needalargecost.
Intheresearchonthesynthesisofthefeaturedataoftrafficdata,Merinoetal.[23]
usedaGANtogenerateattacktrafficintheNSLKDD99datasetandbalancedthedataset.
Shahriaretal.[24]proposedaGAN-basedIntrusionDetectionSystem(G-IDS),whichuses
aGANtogenerateimbalancedandmissingdataandimprovethedetectionabilityofthe
intrusiondetectionsystem. TheirexperimentswerealsotrainedandtestedontheNSL
KDD99dataset. However,theNSLKDD99datasetistoooutdated,andthecharacteristics
ofnetworktrafficarerelativelysimpleandregular. Itisnolongersuitableforthecurrent
complex network environment. Huang et al. [25] proposed an Imbalanced Generative

Sensors2022,22,5243 3of17
AdversarialNetworkIntrusionDetectionSystem(IGAN-IDS)toperformdatabalancing
andtrafficcategoryrecognitiononNSLKDD99,UNSW-NB15andCIC-IDS2017datasets.
Therecognitionaccuracywasimprovedcomparedwithothermachinelearningalgorithms.
However,theiralgorithmdidnotfullyconsiderthefeatureattributesoftrafficdataand
cannotfullyreflectthefeaturedistributionoftrafficdata.
IntheresearchontrafficdataexpansionusingtheGANanditsderivativealgorithms,
therearemainlytwoapproaches: expandingoriginaltrafficdataandexpandingfeature
data. Theexpansionschemesoforiginaltrafficdataneedtostorethesyntheticsamples
afterexpansionandthenextractandfilterthefeatures,soastoidentifymalicioustraffic.
Theseschemesrequirealotofstoragecosts,andthecalculationofimagesalsorequiresa
highcost. Asfortheexpansionschemesoffeaturedata,manydatasetsusedintheschemes
areoutdatedandhavelimitedreferencesignificance. Moreover,theexistingresearchon
thedistributionofflowdatafeaturesisinsufficient.
Themotivationofthispaperistousefeaturedataforexpansion,whichmeetsthere-
quirementsofmachinelearningalgorithmtrainingandprediction. Inthisway,onlyfeature
dataneedtobesavedduringstorage,whilePcapdataandimagesdonot,whichgreatly
reducesthestoragecost. Inthesubsequentmodeltrainingprocess,featureextractionis
notrequiredagain,whichreducesthecalculationcost. Whatismore,inordertobetter
dealwiththediscreteandcontinuousvariablesinthefeaturesoftrafficdata,weusethe
CTGAN[26]modeltogeneratedata.
IntheproposedCTTGANscheme,afterobtainingtheoriginaltrafficdata,weextract
andfilterthedatatogetcharacteristers,andthenexpandsmallclasssamplesofdatawith
the CTGAN algorithm. Considering the need of practical application, we only use the
amplifieddataasthetrainingsetandtherealdataasthetestset. Themaincontributionsof
thispaperareasfollows:
1. WeproposedtheCTTGANschemetoexpandthesmallcategorysamplesinthetraffic
datasets. Aftertheexpansion,alltheindicatorshavebeenimproved,andtheeffect
isstable.
2. In the field of traffic data synthesizing, our research focuses on one-dimensional
tabularfeaturedataratherthanimagedata,whichareapplicabletomachinelearning
modelsandgreatlyreducethestorageandcomputingcosts.
3. TheschemeusestheCTGANmodel,whichcanobtainbetterresultswhenprocessing
discretevariablesandcontinuousvariablesintrafficdataatthesametime.
The structure of this paper is arranged as follows. In Section 2, we introduce the
principleofGAN,especiallythederivativealgorithmsofGANintabulardatageneration.
In Section 3, we introduce the proposed Conditional Tabular Traffic GAN (CTTGAN)
scheme in detail and present the scheme’s flow chart and algorithm. In Section 4, the
experimentalresultsandacomparativeanalysisaregiven. Finally,conclusionsaredrawn
inSection5.
2. Preliminaries
UsingGANtoexpandsamplescangeneratenewsamplesthatdidnotexistbefore,
whichwillnotcauseover-fittingproblemsandcanreflectthecharacteristicsofsamples
well. ManyGAN-derivedalgorithmshavebeenproposedaccordingtotheirproperties
inthefieldsofimages[27],music[28],naturallanguagegeneration[29]andsoon. The
schemeproposedinthispaperaimstoexpandtrafficfeaturedatatobalancethedataset,
thatis,toexpandthetabulardata.
Inthissection,weintroducetheimplementationprincipleofGANanditsderivative
algorithmsinthefieldoftabulardatageneration.
2.1. GANandConditionalGAN
ThebasicideaofGAN[17]istomakethegeneratoranddiscriminatorconfronteach
othertoimprovetheirperformance. TheschematicdiagramisshowninFigure1.

Sensors2022,22,5243 4of17
True Data
Judge True Data
Discriminator Or
Synthetic Data
Noise Generator
Synthetic Data
Figure1.SchematicdiagramoftheGAN.
LetG(z)bethegenerator,andtheinputnoisez ∼ p(z)betheoutputofsyntheticdata
through G(z). Therealdataandthesyntheticdataareinputtothediscriminator D(x),
andthediscriminatoroutputsthediscriminationresult. TheresultofDisfedbacktoG,
andGimprovesthegenerationalgorithmtomakethesyntheticdataclosertotherealdata.
WhenmoresimilarsyntheticdataandrealdataareinputtoD,Dalsoneedstoimproveits
discriminationabilitytoaccuratelydistinguishthesyntheticdatafromtherealdata. The
aboveprocessisrepeatedcontinuously,andthegenerationanddiscriminationabilityofG
andDarecontinuouslyimproveduntilthenetworkreachesaNashequilibrium. Itcanbe
consideredthatthedatageneratedbythenetworkareclosetotherealdata. Theobjective
functionoftheGANisshowninEquation(1):
minmaxV(D,G) = E [logD(x)]+E [log(1−D(G(z)))] (1)
x∼p (x) z∼P(z)
G D data
Mirza et al. [30] proposed that the GAN has the disadvantage that the modeling
processistoofree,whichmaymakethetrainingprocessdifficulttocontrol. Inorderto
solve this problem, they proposed the Conditional GAN (CGAN). The idea of CGAN
model is to add additional information variable y to the modeling of generator G and
discriminatorDtoguidethegenerationofdata. TheobjectivefunctionofCGANisshown
inEquation(2):
minmaxV(D,G) = E [logD(x|y)]+E [log(1−D(G(z|y)))] (2)
x∼p (x) z∼P(z)
G D data
2.2. GANinGeneratingTabularData
ManystudieshavebeenconductedonthegenerationoftabulardatausingtheGAN.
Yahietal.[31]studiedtheuseoftheGANtogeneratecontinuouslaboratorytimeseriesdata
andproposedthatitmaybebeneficialtocombinetherepresentationlearningofthetraining
queuebeforetrainingtheGANmodel. Yuetal.[32]showedthatitisdifficulttopassthe
gradient update from the discriminator to the generator when using GAN to generate
discretetokens. TheyproposedtheSeqGANmodel,modelingthegeneratorasstochastic,
anddirectlyupdatingthegradientofthegenerator. Choietal.[33]proposedmedGAN
to generate realistic patient records. They focus on the generation of high-dimensional
discrete variables (binary and count features). Lederrey et al. [34] proposed DATGAN
modeltogeneratepopulationdata. Theycombinedexpertiseanddeeplearningmethods
anduseddirectedacyclicgraphtoidentifytherelationshipsbetweenvariables.
2.3. ConditionalTabularGAN(CTGAN)
IntheresearchofusingGANtogeneratetabulardata,mostofthemarefordiscrete
variables or continuous variables. When there are discrete variables and continuous
variablesintherealdataatthesametime,thealgorithmswillhavedifficultygenerating
data with the same distribution as the real data. To solve this problem, Xu et al. [26]
proposed the CTGAN model. They designed a conditional generator to resample the

Sensors2022,22,5243 5of17
imbalanceddiscretecolumns. Thereconstructeddistributionoftherealdataisshownin
Equation(3),inwhichk∗ representsthei∗thdiscretecolumnD i∗ value:
P(row) = ∑ P G (row | D i∗ = k ∗)P(D i∗ = k) (3)
k∈D i∗
3. ProposedScheme
3.1. DesignConcept
Thenetworktrafficcharacteristicsincludediscretevariablessuchasthenumberof
forwardpackets,thenumberofbackwardpackets,thelengthofforwardpackets,thelength
ofbackwardpackets,etc.,andcontinuousvariablessuchasthenumberofforwardpackets
persecond,thenumberofbackwardpacketspersecond,andtheaveragepacketlength,
etc. WeproposetheConditionalTabularTrafficGAN(CTTGAN)scheme. Inthestageof
trafficsampleexpansion,theCTGANmodelisusedtoexpandeachtypeofsmallsampleto
obtainthesynthetictrafficdata. IntheCTGANmodel,twofullyconnectedhiddenlayers
areusedinboththegeneratoranddiscriminator. Thereluactivationfunctionisusedinthe
generatorandtheleakyrelufunctionisusedinthegenerator.
3.2. SchemeProcess
The scheme flow chart is shown in Figure 2. First, preprocess the original traffic
datasetstoobtainthecharacteristicdata. Next,expandeachsmalltrafficcategorytoobtain
thesyntheticsamples. Finally,traintheidentificationmodelonthebalanceddatasetand
makepredictions.
Traffic Data Expansion
CTGAN Model
Traffic Data True Data
Preprocessing
Network ex F t e r a a t c u ti r o e n Feature cle D a a n t i a n g Clean Synthetic Synthetic
Data data
Traffic and data data
screening
Generator Discriminator
True or Synthetic
Training
set
Test Predict Trained Model Train model
set MLP, KNN, SVM
BENIGN DoS Port ... Heart
Hulk Scan bleed
Traffic Identification
Figure2.CTTGANschemeflowchart.

Sensors2022,22,5243 6of17
3.3. SchemeSteps
Inthedatapreprocessingsection,firstextracteffectivefeaturesoftrafficdata. Then,
filterthefeaturesandremoveunpracticalones,suchasthetimestamp,destinationhostand
sourcehostIPaddress. Thesefeatureswillmakethetrafficflowhaveobviousattributes;
however,suchfeaturesdonotexistinpracticalapplications. Next,wecleanupthedata,
thatis,removedatawithmissingtermsandinfinityvalues. Inthesmallcategorytraffic
dataexpansionsection,theCTGANmodelisusedtoexpandeachsmallsampletoobtain
synthetic traffic data. Finally, the identification model is trained for traffic prediction.
Considering the actual application demand, the traffic to be predicted shall be the real
traffic. Therefore, we randomly selected part of the real traffic data as the test set, and
mixtheremainingrealtrafficdataandsynthetictrafficdataasthetrainingsettotrainthe
model. Aftertheidentificationmodelisobtained,wepredictthetestsetandobtainthe
results. ThestepsareshowninAlgorithm1andFigure3.
Raw Traffic Data
Extract Features
Feature Data
Select Features
Selected Features
Clean the Data
Clean Data
Yes Small No
Categories
Expand the Data
Using CTGAN Algorithm
Synthetic Data Select Randomly
Select Randomly
Training Set
Train the Model
Test Set
Trained Model
Predict
Identification Results
Figure3.CTTGANstepflowchart.

Sensors2022,22,5243 7of17
Algorithm1:TheProposedCTTGAN
Input: RawNetworkTrafficData(X,Y)
Output: TrafficIdentificationResults(y_pred)
(X(cid:48),Y(cid:48)) = Preprocess(X,Y);
ifsmallcategory=Truethen
z ∼ p ;
z
forkstepsdo
Min(loss(G(z)));
Min(loss(D(x)));
end
Gen=G(z);
end
S = Random(X(cid:48),Y(cid:48));
test
S = Random((X(cid:48),Y(cid:48)),Gen);
training
MLP/KNN/SVM.fit(S );
training
y_pred = MLP/KNN/SVM.predict(S );
test
returny_pred;
4. ExperimentalResults
Inthissection,wefirstintroducethedataset,evaluationindicatorsandexperimentalplat-
formconfiguration,andthenshowtheexperimentalresultsandconductcomparativeanalysis.
4.1. DatasetDescription
WeusedCIC-IDS2017datasetintheexperiment,whichwaspublishedbyCanadian
InstituteofNetworkSecurity. Thedatasetcollectednetworktrafficdatafrom9a.m. on
3July2017to5p.m. on7July2017,includingbenigntrafficand14attacktrafficevents.
Thedatasetisopenandtypical,andthetrafficdataarerelativelynew,whichisconsistent
with the current network environment. The traffic category and quantity are shown in
Tables1and2. ItcanbeseenfromTable2thatthetrafficdatacategoriesareimbalanced.
The dataset contains original network traffic data (PCAPs) and feature data (CSV)
obtainedbyflowfeatureextractiontoolCICFlowMeter. Thefeaturedatainclude78fea-
turessuchasflowduration,maximumpacketlength,minimumpacketlength,number
of forward packets, number of reverse packets, etc. (the original feature data contains
79features,inwhichthefeature“forwardpacketheaderlength”repeatedtwiceandwe
deletedonce). Thefollowingexperimentswereconductedwithfeaturedata.
ItcanbeseenfromTable2thatthebenigntrafficaccountsformorethan80percent,
farmorethanthesumof14typesofmalicioustraffic. Amongthe14typesofmalicious
traffic,11typesoftrafficsamples,suchasDoSGoldenEyeandFTP-Patator,accountfor
lessthan1percent,andthreetypesoftrafficsamples,Infiltration,WebAttackSqlInjection
andHeartbleed,accountforlessthan0.001percent. Thatis,thetrafficdatasetisseriously
imbalanced,whichwillmakethemachinelearningalgorithmbiasedtowardsthelarger
categorysamples,andtherecognitionrateofthesmallerofcategorysampleswillbelow.
Table1.OverviewofdatasetCIC-IDS2017.
Date TrafficCategory
Monday BENIGN
Tuesday BENIGN,FTP-Parator,SSH-Parator
BENIGN,DoSHulk,DoSGoldenEye,DoSslowloris,DoSslowhttptest,
Wednesday
Heartbleed
BENIGN,WebAttackBruteForce,WebAttackXSS,WebAttackSql
Thursday
Injection,Infiltration
Friday BENIGN,PortScan,DDoS,Bot

Sensors2022,22,5243 8of17
Table2.ThecategoriesandquantitiesofdatasetCIC-IDS2017.
TrafficCategory Quantity Proportion
BENIGN 2,260,360 80.33%
DoSHulk 229,198 8.15%
PortScan 157,703 5.60%
DDoS 127,082 4.52%
DoSGoldenEye 10,289 0.37%
FTP-Patator 7894 0.28%
SSH-Patator 5861 0.21%
DoSslowloris 5771 0.21%
DoSslowhttptest 5485 0.19%
Bot 1943 0.07%
WebAttackBruteForce 1497 0.05%
WebAttackXSS 648 0.02%
Infiltration 34 0.0012%
WebAttackSqlInjection 21 0.0007%
Heartbleed 11 0.0004%
4.2. EvaluationIndicators
We use three classical evaluation indicators, Recall, Precision and F1-score, in the
experiment. Thespecificmeaningsareasfollows:
TP(TruePositive)indicatesthenumberofpositivecasesrecognizedaspositive,FP
(FalsePositive)indicatesthenumberofnegativecasesrecognizedaspositive,FN(False
Negative) indicates the number of positive cases recognized as negative and TN (True
Negative) indicates the number of negative cases recognized as negative. In the case
ofmulti-classificationproblems, whenevaluatingtheclassificationofonecategory, the
samples of this category are recorded as positive cases, and all the other samples are
recordedasnegativecases.
TP
Recall = (4)
TP+FN
TP
Precision = (5)
TP+FP
2× Recall × Precision
F1-score= (6)
Recall + Precision
Recall reflects the ratio that a certain type of data are correctly detected; Precision
reflectstheratioofalldatadetectedasacertaintypeofdata; F1-scoretakesbothrecall
andprecisionintoaccount. Foragoodtrafficdetectionmodel,itshouldhavehighRecall,
PrecisionandF1-score.
4.3. ExperimentalPlatformConfiguration
TheexperimentswereconductedonWindows1164-bitOSand16GBofRAM.The
codewaswritteninPython3.8usingthesklearn0.24.1,sdv0.14.0,pandas1.2.4,numpy
1.20.1andmatplotlib3.5.1libraries. Wecalledsomealgorithmsinthesklearnlibraryto
segmentthetrainingsetandtestset,drawtheconfusionmatrixandtraintheMLP,KNN
andSVMmodels;theSdvlibrarywasusedtotraintheCTGANmodelandgeneratedata;
thepandasandnumpylibrarieswereusedtopreprocessdata;andtheMatplotliblibrary
wasusedtodrawandsavepictures. Thedownloadwebsite,briefintroductionandused
functionsofthelibrariesareshowninTable3. TheIDEusedintheexperimentispycharm,
version2020.3x64.

Sensors2022,22,5243 9of17
Table3.Thedownloadwebsite,descriptionandusedfunctionsofthelibraries(allweblinksaccessed
on5June2022).
Library DownloadWebsite Description UsedFunction
confusion_matrix,
train_test_split,
sklearn https://scikit-learn.org Toolsforpredictivedataanalysis preprocessing,
MLPClassifier,
KNeighborsClassifier,SVC
sdv https://github.com/sdv-dev/SDV Asyntheticdatagenerationecosystem CTGAN,evaluate
read_csv,factorize,
pandas https://pandas.pydata.org Adataanalysisandmanipulationtool
DataFrame
numpy https://numpy.org Ascientificcomputingpackage diag,sum,mean
matplotlib https://matplotlib.org Acomprehensivevisualizationlibrary pyplot
4.4. ExperimentalResultsandAnalysis
4.4.1. IdentificationResultsofRawData
InExperiment1,weextractedthecategorieswithdataquantitiesgreaterthan10,000.
ForDDoS,DOSHulk,PortScanandDoSGoldenEye(dataquantitiesbetween10,000and
1,000,000), we extracted 10,000 pieces of data. Subsequent experiments can verify that
10,000piecesofdataareenoughtostabilizethemodelrecognitionrate. ForBENIGNdata
(withadataquantityofmorethan1,000,000),consideringthatthenormalnetworksamples
containmanytypesoftraffic,suchasaccessingnormalwebpages,sendingandreceiving
emails,downloadingdata,etc.,inordertofullycharacterizebenigntraffic,100,000samples
were selected for experiments. The quantity of the data used in the experiment one is
showninTable4.
Table4.Dataquantityinexperimentone.
TrafficCategory Quantity
BENIGN 100,000
DoSHulk 10,000
PortScan 10,000
DDoS 10,000
DoSGoldenEye 10,000
FTP-Patator 7894
SSH-Patator 5861
DoSslowloris 5771
DoSslowhttptest 5485
Bot 1943
WebAttackBruteForce 1497
WebAttackXSS 648
Infiltration 34
WebAttackSqlInjection 21
Heartbleed 11
WeuseMLP,KNNandSVMmachinelearningalgorithmstoclassifytherawimbal-
anceddata. Forthe14categoriesofmalicioustraffic,weincreasethenumberoftraining
samplesstepbystep,andobtainthegrowthcurveoftheRecallindicatorwiththenumber
ofsamples,asshowninFigure4. InordertoreflecttherelationshipbetweentheRecall
indicatorofeachtrafficcategoryanddataquantity,experimentsarecarriedoutforeach
trafficcategory;thatis,foreachcategory,thenumberofsamplesisincreasedstepbystep,
thedataofothercategoriesarekeptunchangedandthechangeintheRecallvalueofthis
categoryisrecorded.

Sensors2022,22,5243 10of17
1.0
0.8
0.6
0.4
0.2
0.0
0 2000 4000 6000 8000 10000
Number of Samples
llaceR
MLP
1.0
DoS Hulk 0.8
PortScan
DDoS
DoS GoldenEye 0.6
FTP-Parator
SSH-Parator
DoS slowloris
0.4
DoS slowhttptest
Bot
Web Attack Brute Force
Web Attack XSS 0.2
Infiltration
Web Attack Sql Injection
Heartbleed 0.0
0 2000 4000 6000 8000 10000
Number of Samples
(a)
llaceR
KNN
DoS Hulk
PortScan
DDoS
DoS GoldenEye
FTP-Parator
SSH-Parator
DoS slowloris
DoS slowhttptest
Bot
Web Attack Brute Force
Web Attack XSS
Infiltration
Web Attack Sql Injection
Heartbleed
(b)
1.0
0.8
0.6
0.4
0.2
0.0
0 2000 4000 6000 8000 10000
Number of Samples
llaceR
SVM
DoS Hulk
PortScan
DDoS
DoS GoldenEye
FTP-Parator
SSH-Parator
DoS slowloris
DoS slowhttptest
Bot
Web Attack Brute Force
Web Attack XSS
Infiltration
Web Attack Sql Injection
Heartbleed
(c)
Figure 4. Growth curve of Recallindicator with number oftraffic samples using three machine
learningalgorithms.(a)MLP;(b)KNN;(c)SVM.
There are 14 curves in Figure 4a–c representing the change in the Recall values of
14trafficcategorieswiththenumberofsamples. Inthethreefigures,therearesixtraffic
categoriesinwhichtheRecallvaluesarenotstable. TheyareBot,WebAttackBruteForce,
WebAttackXSS,Infiltration,WebAttackSqlInjectionandHeartbleed. Theexperimental
resultsshowthatindifferentmachinelearningalgorithms,allkindsoftrafficsamplesneed
toreachacertainamountofdatatomakethetrainedmodelstable.
Asfortheselectionofdatavolume,wegivesomesupplementaryexplanations. The
quantity of the extracted data is related to many factors, such as the complexity of the
dataitself,thenumberofextractedfeatures,thesignificanceofthefeatures,whetherthe
extracted features are reasonable and so on. In addition, the selection of data volume
is also closely related to the architecture and implementation functions of the machine
learningmodel. Itcanbeseenfromtheexperimentalresultsthatwhenthesamplesize
oftheoriginaltrafficdataissufficient,5000piecesofdatacanbeusedtotraindifferent
machinelearningmodelstoachievestability. Thisdatavolumemaybeofgreatreference
valuefordatasetssimilartotheCIC-IDS2017dataset(78featuresand14trafficcategories).

Sensors2022,22,5243 11of17
4.4.2. IdentificationResultsafterCTTGANExpansion
Forthesixtrafficcategorieswithinsufficientdatainexperimentone,weconsiderthe
quantityofWebAttackXSS,Infiltration,WebAttackSqlInjectionandHeartbleedaretoo
smalltofullyreflectthecharacteristicsofthesamples,sothesefourtrafficcategorieswill
notbeconsideredinsubsequentstudies. ForBotandWebAttackBruteForce,weusethe
CTGANalgorithmtoexpandthemandconductidentificationexperiments. Thefollowing
experiments use MLP algorithm for identification. The values of Recall, Precision and
F1-scoreareobtainedasshowninFigure5.
1.0
0.8
0.6
0.4
0.2
0.0
0 500 1000 1500 2000 2500 3000 3500
Number of Training Samples
llaceR
1.00
0.95
0.90
Bot
0.85
0.80
0.75
Web Attack Brute Force
0.70
raw data
new data
0.65
0 500 1000 1500 2000 2500 3000 3500
Number of Training Samples
(a)
noisicerP
Bot
Web Attack Brute Force
raw data
new data
(b)
1.0
0.8
0.6
0.4
0.2
0.0
0 500 1000 1500 2000 2500 3000 3500
Number of Training Samples
erocs-1F
Bot
Web Attack Brute Force
raw data
new data
(c)
Figure5.ExperimentalresultsofBotandWebAttackBruteForceinMLPidentificationalgorithm.
(a)Recall;(b)Precision;(c)F1-score.
Bluecurvesinthefiguresrepresenttheoriginaldata,andredcurvesrepresentsyn-
theticdata. Consideringtheneedsofpracticalapplication,intheexperimentsofsynthetic
data,500piecesofrealtrafficdataarerandomlyselectedasthetestset,andanother500real
trafficdataarerandomlyselectedandaremixedwithsyntheticdataasthetrainingset.
Thecontrolvariablemethodisusedintheexperiment;thatis,whenchangingthequantity
of Bot traffic data, the other categories of data are kept unchanged, and we record the
indicatorsofBotdata. ThesameoperationisperformedonWebAttackBruteForcedata. It
canbeseenfromtheexperimentalresultsthattheindicatorsofBotandWebAttackBrute
Forcehaveimprovedafterexpansionandfinallyreachstability.

Sensors2022,22,5243 12of17
Toverifytheeffectivenessoftheproposedscheme,weselectedtrafficcategorieswith
sufficientsamplesizestoperformaverificationwith. DDoS,DoSGoldenEye,FTP-Patator
andSSH-Patatorareselected,andtheresultsareshowninFigure6.
1.00
0.99
0.98
0.97
0.96
0.95
0 2000 4000 6000 8000 10000
Number of Training Samples
llaceR
DDoS
1.00
0.98
0.96
0.94
0.92
raw data
new data 0.90
0 2000 4000 6000 8000 10000
Number of Training Samples
(a)
llaceR
DoS GoldenEye
raw data
new data
(b)
1.00
0.99
0.98
0.97
0.96
0.95
0 1000 2000 3000 4000 5000 6000 7000 8000
Number of Training Samples
llaceR
FTP-Patator
1.000
0.975
0.950
0.925
0.900
0.875
0.850
0.825
raw data
new data 0.800
0 1000 2000 3000 4000 5000 6000
Number of Training Samples
(c)
llaceR
SSH-Patator
raw data
new data
(d)
Figure 6. Experimental results of four traffic categories with sufficient sample sizes in the MLP
identificationalgorithm.(a)DDoS;(b)DoSGoldenEye;(c)FTP-Patator;(d)SSH-Patator.
Theexperimentalresultsshowthatthesyntheticsampleshaveasimilarfluctuation
trendwiththeoriginalsamples,whichindicatesthatthesyntheticsamplescanreflectthe
characteristicsoftheoriginaldatawell. Inaddition,inordertoverifytheeffectivenessof
theproposedscheme,weusetheMLP,KNNandSVMalgorithmstoidentifythetraffic
oftheexpandeddataset. TheresultsareshowninTable5. ForBotandWebAttackBrute
Force,500realsamplesarerandomlyselectedasthetestset,and4500generatedsamples
areusedasthetrainingset. Thedatavolumeofothertrafficcategoriesisthesameasthat
ofExperiment1.
IntherecognitionresultsobtainedbytheKNN,SVMandMLPalgorithms,therecog-
nitionrecallindexofBotandWebAttackBruteForceallreachesmorethan0.99,andall
trainingsetsarerealsamples. Theresultsshowthattheproposedschemeiseffective.

Sensors2022,22,5243 13of17
Table5.Identificationresultsoftheexpandeddataset.
Recall
DataCategory
MLP KNN SVM
BENIGN 0.9904 0.9881 0.9682
DoSHulk 0.9980 0.9925 0.9015
PortScan 0.9990 0.9590 0.9910
DDoS 0.9980 0.9940 0.9350
DoSGoldenEye 0.9980 0.9975 0.9730
FTP-Patator 0.9968 0.9987 0.9899
SSH-Patator 0.9981 0.9949 0.9889
DoSslowloris 0.9913 0.9931 0.9671
DoSslowhttptest 0.9909 0.9918 0.9854
Bot 0.9980 0.9960 0.9980
WebAttackBruteForce 0.9960 0.9960 1.0000
Note:RedindicatestheRecallindexofsmallcategorysamplesinCTTGANscheme,allofwhichareabove0.99.
4.4.3. ComparativeExperiments
The above experiments verify the effectiveness of the proposed scheme. Next, we
furthercomparetheCTTGANschemewithoversamplingandundersampling,thetwo
most common schemes used to balance datasets in machine learning algorithms [35].
Oversamplingreferstotherepeatedsamplingofafewsamples,andundersamplingrefers
tothediscardingofsomelargesamplestoachieveabalancebetweenthedata. Theresults
oftheMLPalgorithmareshowninTable6. Thequantityofdataforthetrafficcategoriesis
showninbrackets. TheRecallvaluesofthesmalltrafficcategoriesintheCTTGANscheme
reachmorethan0.99,whicharemarkedinred. Theconfusionmatrixoftheexperimental
resultsisshowninFigure7.
Table6.Experimentalresultsofthecomparativeexperiment.
Recall
DataCategory RawData OverSampling UnderSampling CTTGAN
(Amount) (Amount) (Amount) (Amount)
BENIGN 0.9864(100,000) 0.9829(100,000) 0.9433(1500) 0.9904(100,000)
DoSHulk 1.0000(10,000) 0.9925(10,000) 1.0000(1500) 0.9980(10,000)
PortScan 0.9990(10,000) 0.9990(10,000) 1.0000(1500) 0.9990(10,000)
DDoS 0.9975(10,000) 0.9985(10,000) 1.0000(1500) 0.9980(10,000)
DoSGoldenEye 0.9990(10,000) 0.9995(10,000) 0.9967(1500) 0.9980(10,000)
FTP-Patator 0.9975(7894) 0.9981(7894) 0.9867(1500) 0.9968(7894)
SSH-Patator 0.9906(5861) 0.9915(5861) 0.9933(1500) 0.9881(5861)
DoSslowloris 0.9922(5771) 0.9931(5771) 0.9900(1500) 0.9913(5771)
DoSslowhttptest 0.9909(5485) 0.9918(5485) 0.9967(1500) 0.9909(5485)
Bot 0.7918(1943) 0.9720(5000) 0.9967(1500) 0.9980(5000)
WebAttackBruteForce 0.9431(1497) 0.9530(5000) 0.9467(1497) 0.9960(5000)
Note:RedindicatestheRecallindexofsmallcategorysamplesintheCTTGANscheme,allofwhichareabove0.99.
In Experiments 1 and 2, it can be concluded that both real samples and synthetic
samplesarestablewhenthequantityreaches5000. Therefore,intheoversamplingexper-
iment,werepeatedlysampledBotandWebattackbruteforcesamplesto5000,andthe
dataofothertrafficcategoriesremainunchanged. Intheundersamplingexperiment,the
quantityofWebattackbruteforceis1497,andwerandomlyselected1500piecesofdata
forothertrafficcategoriestobalancethedata. IntheCTTGANexperiment,theBotand
Webattackbruteforcesampleswereexpandedto5000. Thedataofothertrafficcategories
remainedunchanged.

Sensors2022,22,5243 14of17
NGINEB toB SoDD eyEnedloG
SoD
kluH
SoD
tsetptthwolS
SoD
sirolwols
SoD
rotataP-PTF nacStroP rotataP-HSS ecroF
eturB
kcattA
beW
BENIGN
Bot
DDoS
DoS GoldenEye
DoS Hulk
DoS Slowhttptest
DoS slowloris
FTP-Patator
PortScan
SSH-Patator
Web Attack Brute Force
Predicted label
lebal
eurT
Confusion Matrix
1.0
0.98640.00210.00010.00010.00680.0004 0.00020.00050.00020.0031
0.20820.7918
0.8
0.0020 0.99750.0005
0.0005 0.9990 0.0005
1.0000 0.6
0.0046 0.0009 0.99090.0027 0.0009
0.0009 0.0009 0.00430.9922 0.0017 0.4
0.0013 0.9975 0.0013
0.0010 0.9990
0.2
0.0034 0.00340.0017 0.0009 0.9906
0.0134 0.04350.9431
0.0
(a)
NGINEB toB SoDD eyEnedloG
SoD
kluH
SoD
tsetptthwolS
SoD
sirolwols
SoD
rotataP-PTF nacStroP rotataP-HSS ecroF
eturB
kcattA
beW
BENIGN
Bot
DDoS
DoS GoldenEye
DoS Hulk
DoS Slowhttptest
DoS slowloris
FTP-Patator
PortScan
SSH-Patator
Web Attack Brute Force
Predicted label
lebal
eurT
Confusion Matrix
0.98290.00650.00010.00040.00510.00030.0001 0.00110.00020.0030
0.02800.9720
0.8
0.0015 0.9985
0.0005 0.9995
0.0075 0.9925 0.6
0.0018 0.99180.0055 0.0009
0.0017 0.00430.9931 0.0009 0.4
0.0006 0.9981 0.00060.0006
0.0010 0.9990
0.2
0.0017 0.00170.0017 0.00090.0026 0.9915
0.0030 0.04400.9530
0.0
(b)
NGINEB toB SoDD eyEnedloG
SoD
kluH
SoD
tsetptthwolS
SoD
sirolwols
SoD
rotataP-PTF nacStroP rotataP-HSS ecroF
eturB
kcattA
beW
BENIGN
Bot
DDoS
DoS GoldenEye
DoS Hulk
DoS Slowhttptest
DoS slowloris
FTP-Patator
PortScan
SSH-Patator
Web Attack Brute Force
Predicted label
lebal
eurT
Confusion Matrix
1.0
0.94330.0233 0.00330.0067 0.00330.01000.0100
0.00330.9967
0.8
1.0000
0.9967 0.0033
1.0000 0.6
0.0033 0.9967
0.0033 0.00670.9900 0.4
0.0067 0.9867 0.0067
1.0000
0.2
0.0033 0.0033 0.9933
0.0033 0.05000.9467
0.0
(c)
NGINEB toB SoDD eyEnedloG
SoD
kluH
SoD
tsetptthwolS
SoD
sirolwols
SoD
rotataP-PTF nacStroP rotataP-HSS ecroF
eturB
kcattA
beW
BENIGN
Bot
DDoS
DoS GoldenEye
DoS Hulk
DoS Slowhttptest
DoS slowloris
FTP-Patator
PortScan
SSH-Patator
Web Attack Brute Force
Predicted label
lebal
eurT
Confusion Matrix
0.9904 0.00010.00040.00750.0003 0.00030.0007
0.00200.9980
0.8
0.0015 0.99800.0005
0.0015 0.9980 0.0005
0.0015 0.00050.9980 0.6
0.0036 0.0018 0.99090.0036
0.0017 0.00610.9913 0.0009 0.4
0.0006 0.00190.9968 0.0006
0.0010 0.9990
0.2
0.0068 0.00430.0009 0.9881
0.0040 0.9960
0.0
(d)
Figure7.Confusionmatrixofcomparativeexperiment.(a)Originaldata;(b)Oversampling;(c)Un-
dersampling;(d)CTTGAN.
The results show that the recognition rate of the Bot and Web Attack Brute Force
samplesislowintheoriginalcase. Intheoversamplingexperiment,therecognitionrateof
Bothasbeengreatlyimproved,andtherecognitionrateofWebAttackBruteForcehasbeen
slightlyimproved. Intheundersamplingexperiment,therecognitionrateofBotreaches
morethan0.99,therecognitionrateofWebAttackBruteForceisalmostunchangedand
theBENIGNrecognitionratedecreases. IntheCTTGANexperiment,therecognitionrate
ofeachcategoryishigh.
4.4.4. DiscussionandAnalysis
Intheexperiments,wesynthesizefeaturedataofnetworktraffic,ratherthanoriginal
dataorimage. Thesyntheticdatacanbedirectlyinputtomachinelearningalgorithms,
saving storage costs and computing costs. In addition, it may be more reasonable to
calculateandprocessthefeaturedataintheCTTGANmodel. Insomeschemesthatconvert
networktrafficintoimages,thefirstnbytesoftheoriginalnetworktrafficareconverted
intograyimages. ThesebytescontainthedestinationIP,sourceIPandotherinformation,
whichisunreasonabletobeusedtoidentifythetrafficcategory. Suchproblemscanbe
solvedintheCTTGAN.

Sensors2022,22,5243 15of17
Thenetworktrafficfeaturesincludebothcontinuousvariablesanddiscretevariables.
WeusetheCTGANalgorithmtogeneratetwotypesofdataatthesametime. Thesynthetic
datahavesimilardistributionstotheoriginaldata. First,weconductexperimentstoverify
thatindifferentidentificationalgorithms,thetrafficdataneedtoreachacertainquantity
tomakethemodelachieveastablerecognitionrate. Secondly, weverifythatforsmall
categorytrafficsamples,thesyntheticdatacanimprovetheperformanceofthemodel. For
largecategorysamples,thesyntheticdatahavesimilarfluctuationtrendstotheoriginal
one. TheseexperimentalresultsprovethatthedatageneratedbytheCTTGANschemeare
closetotherealdata,andthegenerateddatacanbeusedasasupplementtotheinsufficient
samples. Whatismore,weperformtrafficrecognitionforallcategories. IntheMLP,KNN
andSVMalgorithms,therecognitionrateoftheexpandedsamplesreachesmorethan0.99.
Finally,wecomparetheCTTGANmodelwithoversamplingandundersamplingschemes.
The performance of the CTTGAN is better than the oversampling and undersampling
schemesonthewhole,whichprovesthattheproposedCTTGANschemeiseffectiveand
haspracticalsignificance.
In the experiments, all test sets are composed of real data, which proves that the
synthetic data can be used as a supplement in the training of the model to improve its
performanceinrealdetectionscenarios.
5. Conclusions
Inthispaper,weproposetheCTTGANmodeltoexpandnetworktrafficsamplesto
balancethedatasetinordertoimprovetherecognitionrateofmachinelearningalgorithms.
Differentfrommosttrafficdataexpansionmodels,theCTTGANmodeldoesnotconvert
networktrafficdataintoimages,butextractsitseffectivefeaturesandthenexpandsthe
featuredata.Inthisway,thesyntheticfeaturedataconformtothedatastructureofmachine
learningalgorithms,andwedonotneedtoextractfeaturesafterdataexpansion. Thisre-
ducesstoragecostsandcomputationalcomplexityandspeedsupcomputing. Experiments
showthattherecognitionrateoftrafficcategorieswithlessdataislow,andtherecognition
rateincreasesandreachesastablelevelwhenthereissufficientdata. Afterexpandingthe
smallcategorysampleswiththeCTTGANmodel,therecognitionratereachesmorethan
0.99,andthemodelhasgoodstability. WealsousetheCTTGANtosynthesizethelarge
categorysamplestoverifythatthefluctuationtrendissimilartotherealdata. Therefore,
theproposedCTTGANmodeliseffective. Moreover,therecognitionrateoftheCTTGAN
modelishigherthanthatoftheoversamplingandundersamplingschemes,whichproves
thattheCTTGANmodelhasgoodexperimentalresultsandpracticalvalue.
Infuturework,wewillfurtherstudytheexpansionofcategorieswithtoofewsamples,
suchasWebAttackXSS,Infiltration,WebAttackSqlInjectionandHeartbleed. Wewill
studyhowtofullyminethecharacteristicsofthesecategoriesofdata,reflecttheoverall
distributionandthenrealizereasonableexpansionofthesedatatoachieveeffectiveiden-
tification. Inaddition,weconsiderthestudyofinstantidentificationofmalicioustraffic,
whichisofgreatsignificanceforpracticalapplications.
Author Contributions: Conceptualization, J.W. and L.L. (Lintao Liu); methodology, J.W.,
L.L.(LonglongLi) and Y.Y.; validation, L.L. (Lintao Liu) and Y.Y.; writing—original draft prepa-
ration, J.W.; writing—reviewandediting, L.L.(LonglongLi)andX.Y.; supervision, X.Y.; project
administration,X.Y.Allauthorshavereadandagreedtothepublishedversionofthemanuscript.
Funding: ThisresearchwasfundedbytheNationalNaturalScienceFoundationofChinagrant
number61602491.
InstitutionalReviewBoardStatement:Notapplicable.
InformedConsentStatement:Notapplicable.
DataAvailabilityStatement: ThenetworktrafficdatasetCIC-IDS2017canbedownloadedfrom
website:https://www.unb.ca/cic/datasets/ids-2017.html(accessedon5June2022).
ConflictsofInterest:Theauthorsdeclarenoconflictofinterest.

Sensors2022,22,5243 16of17
References
1. Zhang,J.;Xiao,C.;Yang,X.;Zhou,W.;Jie,W. RobustNetworkTrafficClassification. IEEE/ACMTrans.Netw.2015,23,1257–1270.
[CrossRef]
2. Park, J.S.; Yoon, S.H.; Kim, M.S. Performance improvement of payload signature-based traffic classification system using
application traffic temporal locality. In Proceedings of the 2013 15th Asia-Pacific Network Operations and Management
Symposium(APNOMS),Hiroshima,Japan,25–27September2013.
3. Lee,S.H.;Park,J.S.;Yoon,S.H.;Kim,M.S. Highperformancepayloadsignature-basedInternettrafficclassificationsystem.
InProceedingsofthe201517thAsia-PacificNetworkOperationsandManagementSymposium(APNOMS),Busan,Korea,
19–21August2015.
4. deLucia,M.J.;Cotton,C. DetectionofEncryptedMaliciousNetworkTrafficusingMachineLearning. InProceedingsofthe
MILCOM2019—2019IEEEMilitaryCommunicationsConference(MILCOM),Norfolk,VA,USA,12–14November2019;pp.1–6.
[CrossRef]
5. Shekhawat,A.S.;Troia,F.D.;Stamp,M. FeatureAnalysisofEncryptedMaliciousTraffic. ExpertSyst.Appl.2019,125,130–141.
[CrossRef]
6. Ma,R.;Qin,S.Identificationofunknownprotocoltrafficbasedondeeplearning. InProceedingsofthe20173rdIEEEInternational
ConferenceonComputerandCommunications(ICCC),Chengdu,China,13–16December2017.
7. Liu,Z.;Li,S.;Zhang,Y.;Yun,X.;Cheng,Z. EfficientMalwareOriginatedTrafficClassificationbyUsingGenerativeAdver-
sarialNetworks. InProceedingsofthe2020IEEESymposiumonComputersandCommunications(ISCC),Rennes,France,
7–10July2020.
8. Dong, S.; Xia, Y.; Peng, T. Trafficidentificationmodelbasedongenerativeadversarialdeepconvolutionalnetwork. Ann.
Telecommun.2021.[CrossRef]
9. He,M.;Wang,X.;Zhou,J.;Xi,Y.;Wang,X. Deep-Feature-BasedAutoencoderNetworkforFew-ShotMaliciousTrafficDetection.
Secur.Commun.Netw.2021,2021,6659022.[CrossRef]
10. Zhong,Y.;Chen,W.;Wang,Z.;Chen,Y.;Li,K. HELAD:Anovelnetworkanomalydetectionmodelbasedonheterogeneous
ensemblelearning. Comput.Netw.2019,169,107049.[CrossRef]
11. Telikani, A.; Gandomi, A.H.; Choo, K.K.R.; Shen, J. A Cost-Sensitive Deep Learning-Based Approach for Network Traffic
Classification. IEEETrans.Netw.Serv.Manag.2022,19,661–670. [CrossRef]
12. Gu,X.;Angelov,P.P.;Soares,E. ASelf-AdaptiveSyntheticOver-SamplingTechniqueforImbalancedClassification.Int.J.Intell.
Syst.2019,35,923–943.[CrossRef]
13. Peng,M.;Qi,Z.;Xing,X.;Tao,G.;Huang,X. TrainableUndersamplingforClass-ImbalanceLearning. Proc.AAAIConf.Artif.
Intell.2019,33,4707–4714.[CrossRef]
14. Chawla,N.V.;Bowyer,K.W.;Hall,L.O.;Kegelmeyer,W.P. SMOTE:SyntheticMinorityOver-samplingTechnique. J.Artif.Intell.
Res.2002,16,321–357.[CrossRef]
15. Qian,Y.;Min,Z. P2PTrafficIdentificationBasedOver-SamplingTechnique. Telecommun.Sci.2014,30,109–113.
16. Yan,B.H.;Han,G.D.;Huang,Y.J.;Yu,X.L. DPCS2017+41+ANoveltrafficClassificationMethodBasedonImbalancedData.
J.Comput.Appl.2017.
17. Goodfellow,I.;Pouget-Abadie,J.;Mirza,M.;Xu,B.;Warde-Farley,D.;Ozair,S.;Courville,A.;Bengio,Y. GenerativeAdversarial
Nets. NeuralInf.Process.Syst.2014,27,1–9.
18. Vu, L.; Bui, C.T.; Nguyen, Q.U. A Deep Learning Based Method for Handling Imbalanced Problem in Network Traffic
Classification. InProceedingsoftheEighthInternationalSymposiumonInformation&CommunicationTechnology,NhaTrang,
Vietnam,7–8December2017;pp.333–339.
19. Odena,A.;Olah,C.;Shlens,J. ConditionalImageSynthesisWithAuxiliaryClassifierGANs.InProceedingsoftheInternational
ConferenceonMachineLearning,NewYork,NY,USA,20–22June2016.
20. Arjovsky,M.;Chintala,S.;Bottou,L. WassersteinGAN.arXiv2017,arXiv:1701.07875.
21. Kim,J.Y.; Bu,S.J.; Cho,S.B. Zero-daymalwaredetectionusingtransferredgenerativeadversarialnetworksbasedondeep
autoencoders. Inf.Sci.2018,460,83–102.[CrossRef]
22. Lin,Z.;Shi,Y.;Xue,Z. IDSGAN:GenerativeAdversarialNetworksforAttackGenerationagainstIntrusionDetection.arXiv2018,
arXiv:1809.02077.
23. Merino, T.; Stillwell, M.; Steele, M.; Coplan, M.; Patton, J.; Stoyanov, A.; Deng, L., Expansion of Cyber Attack Data from
UnbalancedDatasetsUsingGenerativeAdversarialNetworks. InSoftwareEngineeringResearch,ManagementandApplications;Lee,
R.,Ed.;Springer:Cham,Switzerland,2020;pp.131–145. [CrossRef]
24. Shahriar,M.H.;Haque,N.I.;Rahman,M.A.;Alonso,J.M. G-IDS:GenerativeAdversarialNetworksAssistedIntrusionDetection
System.InProceedingsofthe2020IEEE44thAnnualComputers,Software,andApplicationsConference(COMPSAC),Madrid,
Spain,13–17July2020.
25. Huang,S.;Lei,K. IGAN-IDS:AnImbalancedGenerativeAdversarialNetworktowardsIntrusionDetectionSysteminAd-hoc
Networks. AdHocNetw.2020,105,102177.[CrossRef]
26. Xu,L.;Skoularidou,M.;Cuesta-Infante,A.;Veeramachaneni,K. ModelingTabulardatausingConditionalGAN. InAdvances
inNeuralInformationProcessingSystems;Wallach,H.,Larochelle,H.,Beygelzimer,A.,d'Alché-Buc,F.,Fox,E.,Garnett,R.,Eds.;
CurranAssociates,Inc.:RedHook,NY,USA,2019;Volume32.

Sensors2022,22,5243 17of17
27. Huang,H.;Yu,P.S.;Wang,C.AnIntroductiontoImageSynthesiswithGenerativeAdversarialNets. arXiv2018,arXiv:1803.04469.
28. Jhamtani,H.;Berg-Kirkpatrick,T. ModelingSelf-RepetitioninMusicGenerationusingGenerativeAdversarialNetworks.In
ProceedingsoftheMachineLearningforMusicDiscoveryWorkshop,ICML,LongBeach,CA,USA,15June2019.
29. Rajeswar, S.; Subramanian, S.; Dutil, F.; Pal, C.; Courville, A. Adversarial Generation of Natural Language. arXiv 2017,
arXiv:1705.10929.
30. Mirza,M.;Osindero,S. ConditionalGenerativeAdversarialNets. Comput.Sci.2014,2672–2680.
31. Yahi,A.;Vanguri,R.;Elhadad,N.;Tatonetti,N.P. GenerativeAdversarialNetworksforElectronicHealthRecords:AFramework
forExploringandEvaluatingMethodsforPredictingDrug-InducedLaboratoryTestTrajectories.arXiv2017,arXiv:1712.00164.
32. Yu,L.;Zhang,W.;Wang,J.;Yong,Y. SeqGAN:SequenceGenerativeAdversarialNetswithPolicyGradient.InProceedingsofthe
AAAIConferenceonArtificialIntelligence,Phoenix,AZ,USA,12–17February2016.
33. Choi,E.;Biswal,S.;Malin,B.;Duke,J.;Sun,J. GeneratingMulti-labelDiscretePatientRecordsusingGenerativeAdversarial
Networks.InProceedingsoftheMachineLearningforHealthcareConference,Boston,MA,USA,18–19August2017.
34. Lederrey,G.;Hillel,T.;Bierlaire,M. DATGAN:Integratingexpertknowledgeintodeeplearningforsynthetictabulardata.arXiv
2022,arXiv:2203.03489.
35. Drummond,C.;Holte,R.C4.5,ClassImbalance,andCostSensitivity:WhyUnder-SamplingbeatsOver-Sampling.InProceedings
oftheWorkshoponLearningfromImbalancedDatasetsII,Washington,DC,USA,21August2003.
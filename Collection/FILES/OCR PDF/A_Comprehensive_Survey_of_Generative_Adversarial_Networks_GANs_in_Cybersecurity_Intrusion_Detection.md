Received27June2023,accepted14July2023,dateofpublication19July2023,dateofcurrentversion27July2023.
DigitalObjectIdentifier10.1109/ACCESS.2023.3296707
A Comprehensive Survey of Generative
Adversarial Networks (GANs) in
Cybersecurity Intrusion Detection
AERYNDUNMORE 1,(GraduateStudentMember,IEEE),JULIANJANG-JACCARD 1,
FARIZASABRINA 2,(Member,IEEE),ANDJINKWAK3
1CybersecurityLaboratory,DepartmentofComputerScience,MasseyUniversity,Auckland0653,NewZealand
2SchoolofEngineeringandTechnology,CentralQueenslandUniversity,Sydney,NSW4701,Australia
3DepartmentofCyberSecurity,AjouUniversity,Suwon,Gyeonggi-do206KRSouthKorea
Correspondingauthor:AerynDunmore(a.dunmore@massey.ac.nz)
ThisworkwassupportedbytheMinistryofBusiness,Innovation,andEmployment(MBIE)fromtheNewZealandGovernmentunder
GrantMAUX1912.
ABSTRACT GenerativeAdversarialNetworks(GANs)haveseensignificantinterestsincetheirintroduction
in 2014. While originally focused primarily on image-based tasks, their capacity for generating new,
synthetic data has brought them into many different fields of Machine Learning research. Their use in
cybersecurityhasgrownswiftly,especiallyintaskswhichrequiretrainingonunbalanceddatasetsofattack
classes.InthispaperweexaminetheuseofGANsinIntrusionDetectionSystems(IDS)andhowtheyare
currentlybeingemployedinthisareaofresearch.GANsarecurrentlyinuseforthecreationofadversarial
examples,editingthesemanticinformationofdata,creatingpolymorphicsamplesofmalware,augmenting
data for rare classes, and much more. We have endeavored to create a paper that may act as a primer for
cybersecurityspecialistsandmachinelearningresearchersalike.ThispaperdetailswhatGANsareandhow
theywork,thecurrenttypesofGANinuseinthearea,datasetsusedinthisresearch,metricsforevaluation,
currentareasofuseinintrusiondetection,andwhenandhowtheyarebestused.
INDEX TERMS Generative adversarial networks (GAN), machine learning, research survey, attack
modeling, threat detection, intrusion detection systems, data augmentation, zero-day attacks, adversarial
examples.
I. INTRODUCTION GooglehasusedprogramslikereCAPTCHA1tocreatelarge
TheGenerativeAdversarialModel,orGAN,isamethodpro- labeled datasets for computer vision [4], most do not have
posed by Goodfellowetal.[1] in 2014 as a new alternative a similar opportunity to leverage the average citizen for
to Variational Autoencoders (VAE) [2] for generating large creating datasets. As a result of this lack of data, models
amountsofsynthesizedbutrealisticdata.Thepowerbehind like GAN or VAE are looked at to help train new machine
the GAN model and the research it has spurred on, is the learningsystems.Insecurity,GANmodelscanbeveryuseful
abilitytoaugmentandevencreatedatasets,atalentgreatlyin atgeneratingsamplesofmaliciouscode,traffic,orbehavior.
demandduetotheever-risingtideofmachinelearning-driven As a result, these models are being employed with great
technology. Training machine learning models requires a success in research towards new or improved Intrusion
substantialdataset,necessitatinghumancollatedandlabeled DetectionSystems.Ouraimwiththispaperistosurveythe
datasetswhichareexpensiveinbothcostandintime.While currentstateoftheartinutilizingGANmodelsforIntrusion
Detection Systems challenges and research. We endeavor
to present both breadth of topics and depth of knowledge,
The associate editor coordinating the review of this manuscript and 1Alphabet,Google’sparentcompany,confirmstheuseofyouranswers
approvingitforpublicationwasJemalH.Abawajy . forpurposesotherthanverificationofyourstatusasahuman[3].
VOLUME11,2023 ThisworkislicensedunderaCreativeCommonsAttribution4.0License.Formoreinformation,seehttps://creativecommons.org/licenses/by/4.0/ 76071

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
that we might offer a contribution which is of use to both very unsuccessful, as they are primarily random noise, but
the experienced machine learning researcher as an update as more and more feedback propagates backwards from the
on current research and methods, and also as a primer to Discriminator,theGeneratorslowlyimprovesthequalityof
thoseenteringintoGANresearchforcybersecurity.Wehave itssamples,bringingthemclosertothegenuinesamplesthe
alsodoneourutmosttocoverthesetopicsfromthepointof training set contains. The Generator is also the part of the
viewofbothcybersecurityandmachinelearningresearchers. modelthatisgenerallykeptafterconvergenceisachievedor
We have offered a comprehensive review of not just the thefullnumberoftrainingepochshasrun[5].Oncetraining
currentresearch,butthedatasetsusedfortesting,themethods is complete and the Generator is capable of synthesizing
anddesignsoftheGANmodelsusedinexperimentation,and samplesthatareallbutgenuine,itisreadytobeusedforthe
themetricsusedtoevaluateboth. purposeforwhichitwasbuilt.Insomecases,theGenerator
The remainder of our paper is structured as follows: failstowinagainsttheDiscriminator,whichinsteadbecomes
Section II introduces the reader to the basic structure a highly effective classifier. Some research scenarios utilize
of the original Generative Adversarial Networks proposed theDiscriminatorforthispurpose,ratherthandiscardingit.
in [1], as well as defining Intrusion Detection Systems and
2) DISCRIMINATORS
maliciousoperatorsforthepurposeofoursurvey.SectionIII
As discussed above, the Discriminator of the model is
will explain the other survey papers in the area, and show
not usually kept after the Generator has been successfully
how we have filled a knowledge gap in the specificity of
trained [6]. The essence of the Discriminator is to look
subject and depth of knowledge, while Section IV details
at samples provided by the Generator, both genuine and
the metrics by which researchers evaluate their schemes.
synthesized, and successfully categorize them. As the
Section V explains the datasets on which the models have
Generator gets the feedback and slowly alters its weights
been trained and tested. Section VI goes into detail about
for more accurate sample generation, the Discriminator is
the different variants and models of GANs that have been
supposed to slowly become less and less effective, until it
proposed in the papers we have surveyed. Section VII
is little more than a computerized coin toss. In some cases,
investigates the uses that are current hot topics in research,
the opposite occurs, with the Generator unable to model
and then Section VIII discusses the research applications in
the provided samples accurately. In the original proposed
detail.Finally,SectionIXgoesintothepotentialavenuesfor
modelhowever,theGeneratorwinsthegame.Atthispoint,
futureresearch,andSectionXconcludesoursurvey.
the Discriminator is no longer necessary, as it has fulfilled
the purpose for which it was built - training the Generator
II. EXPLANATIONS,TERMS,ANDTHEGANMODEL
to synthesize exceptionally realistic samples. As mentioned
A. WHATISGAN?
earlier,sometimestheDiscriminatordoeswinthegameand,
The basic Generative Adversarial Network model, as pro-
depending on the type of GAN model, this can result in a
posedbyGoodfellowetal.[1],isatwo-network,two-player
usefulandaccurateclassifier.Insomemodels,theGenerator
game, with a zero-sum target based in Game Theory. The
iscreatinglabeledsamplesofdifferentclasses,meaningthe
Generator, which is trained on a dataset of real samples,
Discriminatoriscarefullytrainedtoknowwhateachclassof
triestogenerateconvincingsampleswhichcanfooltheDis-
samplesshouldlooklike.
criminator,suchthattheDiscriminatorbelievesthesamples
are genuine. They are considered semi-supervised learning,
3) CONVERGENCE
andtheweightsareadjustedthroughback-propagation.The
InEquation1,wehaveprovidedtheminmaxgamethatsits
game is over when the Discriminator can only tell the
at the heart of the GAN model. The p (z) input contains
z
real samples from the generated ones with an accuracy of
the z variable, the seed data for the Generator, while the
50%, effectively making a binary guess or a coin toss. p function plots a noise distribution. V(D,G) provides the
The generation of new samples that are all-but-real makes
value function in which G is the Generator, with the value
GAN models very desirable. In order to be able to train functionofG(z;θ )andDisthediscriminator.Theresultof
g
Intrusion Detection Systems, Antivirus, and other defensive theDiscriminator’sfunctionD(x;θ )istheprobabilityvalue
D
technologies,todetectwhenacommunication,file,oraction,
(asinglescalarvalue),whichsuggestswhethertheinput,x,
is malicious, large sets of classes and data types with many
came from the training set or from the Generator. Because
samples are needed. It is simple to see how this can give
both networks are being trained concurrently, the goal is to
GANmodelsasignificantplaceinresearchinsecuritygoing minimizethelog(1−G(z))fortrainingtheGenerator,while
forwards.
alsominimizinglog(D(x))fortheDiscriminator[7].Oncethe
probabilityvalue-theoutputscalarfromthevaluefunction
1) GENERATORS
oftheDiscriminator-flattensinto0.5,thegameisoverand
TheGeneratorNetworkinthemodelisthemorecomplicated
convergencehasbeenachieved.
of the two. It starts, in training a ‘‘vanilla’’ GAN (the
original,Goodfellowmodel),witharandomseed,sometimes
referredtoasanoisesample,andthentheGeneratorbegins
m
G
inm
D
axV(D,G)=E x∼pdata(x) [logD(x)] (1)
generating samples immediately. These early attempts are +E z∼pz(z) [log(1−D(G(z)))] (2)
76072 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
B. INTRUSIONDETECTIONSYSTEMS Arora and Shantanu [13] reviewed uses for Generative
The central tenants of cybersecurity are Confidentiality, AdversarialNetworksinthecybersecuritydomain.Thissur-
Integrity and Availability (CIA). An Intrusion Detection veydoesdelveintothetypesofGANmodels,explainingthe
System(IDS)is,atheart,amethodforensuringthestrongest differenttypesofmodelsandgivinggraphicalrepresentation
possible version of the CIA requirements for its host or of these models, as seen in Figure 3. The paper also places
user [8]. IDS models are not new - in 1988, Smaha [9] a lot of emphasis on a case study of anomaly detection
proposedanIDScalledHaystack.Knowingiftherehasbeen and generation using the KDD-NSL dataset. While it offers
anattemptonyourdevice,successfulornot,isaparticularly a good overview of some of the different GAN models,
important part of keeping yourself safe, be you a person on it lacks in both depth and breadth of applications, with a
the street with a smartphone, or a giant corporation with its specificfocusonnetworkintrusion,andsomeexplorationon
own server farm. IDS models are meant to enforce the CIA steganographyandpasswordguessing.Thoughthispaperis
protocolsthatarethecoreofcybersecuritytraining.AnIDS timelyandimportant,wedonotbelieveitnegatestheneedfor
modelisbuilttodetectunauthorizeduserbehavior,and/orto ourpaper,astheauthorssurveyonlyasmallnumberofGAN
detect behavior from authorized users that falls outside the models - vanilla GAN, DCGAN, BiGAN, and CycleGANs.
purviewoftheirauthorization[10].Insimplestterms,anIDS The paper looks at the types of datasets in use, and more
shouldbeabletotelliftrafficismaliciousorlegitimate[11]. specificallytheindividualdomainsofcybersecurityinwhich
Anintrusion,forthepurposeofthispaperandresearch,isan GANmodelscanbeused.Becausethatpaperissocompact,
effort or instance of attempting to circumvent or cause a itdoesnothavetheopportunitytogointodepthintheway
failureinCIA[8].ModernIDSmodelsareeitherNetwork- wedointhissurvey.
based(inthattheymonitorthepacketsexchanged)orHost- Duttaetal.[14]didanextensivesurveypaperthatexplores
based(inthattheymonitorloggedbehavioronadevice)[12]. many different types of algorithms using the GAN model,
An extension of IDS is the Intrusion Prevention System, forsecuritypurposes.Itshowsbothdefensiveandoffensive
orIPS,whichtakesthebehaviorofanIDSonestepfurther algorithms,tobalancethepaperwiththewaysGANscanbe
as an attempt to shield the host from unauthorized access appliedinthesecuritydomain.
attempts.Giventhis,itisnotsurprisingthatmachinelearning In [14], the authors are careful to extend a wide range of
for IDS models has taken off with such gusto. Of course, spacesinwhichGANscouldbeusedtoimprovethesecurity
theenduringproblemwithmachinelearningmodelsistheir of sensitive information. Amongst other areas, healthcare
trainingphaseandtheexpanseofdatarequiredtocreatethe and banks. The authors also discuss ethics and possible
necessarytrainingandtestingdatasets.AccordingtoThakkar misuse of technology. Overall, this paper does raise some
and Lohiya [11], there are a number of dangers in network veryinterestingstudies,andthesurveycoversawiderange
traffic to consider at this point in the evolution of internet of topics. However, it is quite a short survey, and one thing
usage.Theseinclude: noticeablyabsentinmostsectionsisanytypeofmetricforthe
• Attemptstoobtainpersonalandprivatedata studyinquestion.Wefoundthisunusualforasurveypaper
• Ransomware whichdiscussesthesignificanceandsuccessesoftheuseof
• AdversarialAI GANinthecybersecuritydomain.
• IoT-focusedattacks Caietal.[15]havecreatedahighlydetailedandin-depth
Machine learning techniques for IDS models belong to the surveyoftheelementsofsecurityandprivacywhereinGAN
category of Anomaly-based Detection. Traditional methods can be applied. This paper is very insistent on showing
ofIDSsystemsalsoincludeSignatureandStatefulProtocol both sides of GAN research. Cases wherein the generator
Analysis detection methods [8]. IDS models can also be is an attacker against the defending classifier (such as [16],
divided along the type of classification provided - a binary [17], [18], [19]), as well as those wherein the generator
classifierwillassignaclassofeitherattackorbenign,while is defending itself against the attacking discriminator (such
amulticlassclassifiermayoffermoredetailedclassification, as [20], [21], [22], [23], [24]) are examined. The latter
suchasthetypeofattack.Rareclassesortypesofattackshave includeGANmodelssuchasGenerativeAdversarialPrivacy
fewsamples,whilebenevolentornormaltrafficisplentiful. (GAP), Privacy Preserving Adversarial Networks (PPANs),
AlongsidethisistheproblemoftestingyourIDSagainstan CompressiveAdversarialPrivacy(CAP),andReconstructive
enemyactor.Thesearejustsomeofthewaysresearchersare Adversarial Network. A point of interest in the paper is
using Generative Adversarial Networks for the building of thesectionsurveying‘‘model’’privacy.‘‘Amodel’sprivacy
IDSmodels. breaches if an adversary can use the model’s output to
infer the private attributes used to train the model.’’ (pp.
III. RELATEDWORK 132:13,[15])Wehavefoundthatothersurveysdonotinclude
This section attempts to create a general overview of the this as standard in the sections of their papers on security.
surveysonGenerativeAdversarialNetworksincybersecurity The importance of model privacy seems to normally be an
andwithregardstointrusiondetection.Webrieflydetailthe overlookedone.Thispapertakesthetimetolookatit,with
paperandthetopicsdiscussed,aswellaswherewefeelour a definition based on [25]. While it is an intriguing area of
surveyfitswithinthecurrentresearchlandscape. research for security and privacy, we do not believe that it
VOLUME11,2023 76073

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
is necessary to go into the same level of detail in our own c: RECALL
survey. The recall, also called the True Positive Ratio, or the
We believe our survey has found a space within these sensitivity, of the model, is classified as the number of true
existing surveys to fill gaps with regards to how Generative positives predicted by the model, over the number of true
Adversarial Networks are used in building an effective IDS predictionsoverall,bothpositiveandnegative.
model. We have done this while focusing on creating an
overview that will be of use to researchers in machine R= TP (5)
learning and Intrusion Detection, new and experienced. TP+TN
The survey papers’ topics and specific GAN models are
d: HARMONICMEAN
summarizedinTable1.
The Harmonic Mean, also known as the F1-Score, is the
method by which the performance of a model is measured
IV. MEASURINGPERFORMANCE
withregardstoitsminorityclass.Thisisespeciallyimportant
The used performance metrics for evaluating Machine
in cases such as those involving classification and neural
Learningareaveryselectandoft-repeatedset.Here,wetry
networks. The ability to accurately classify the class which
toensurethatourreaderisasfamiliarwiththesemetrics.
occurs the least in the training set, that is the rarest of the
samples,isbothextremelyimportantandextremelydifficult.
1) TRUEPOSITIVE
Thisiscalculatedasthetrade-offbetweenPrecision(P)and
A true positive (TP) occurs when the model correctly
Recall(R),asshownbelow.
identifiesabenignsampleasbenign.
(cid:18) (cid:19)
PR
2) FALSEPOSITIVE F 1 =2 P+R (6)
A false positive (FP) occurs when a model classifies a
malicioussampleasbenign.
e: THEINCEPTIONSCORE
The Inception Score is one of the less common methods of
3) TRUENEGATIVE measuring the performance of a model. It determines the
A true negative (TN) occurs when the model classifies a distributionofthemodel’spredictionsandclassificationsas
malicioussampleasmalicious. thedistributionofprobabilitiesovertwosetsofdistributions,
(cid:127) and (cid:127) [26]. When g is classed as the Generator, and
X Y
4) FALSENEGATIVE welabeld astheDiscriminator,wehavethedistributionof
A false negative (FN) occurs when the model incorrectly the generator as p , and the Discriminator function can be
g
classifiesabenignsampleasmalicious. determinedasp : (cid:127) → M((cid:127) ).Weclassifyeachimage
Y x Y
Using TP, FP, TN, FN metrics is only a small part of as some x, and each label as some y. We have the set of
measuring the performance of the machine.We will now all possible distributions M((cid:127) ), over the set (cid:127) . We can
Y Y
introduce some methods of measuring performance that go thengoontosaythatwritingp (y|x)iswritingthefunction
d
slightly deeper. Some papers do not press much farther that gives the probability that a given x has the label y. The
than the above, however the best methods for determining InceptionScorewasoriginallydevelopedforcomputervision
a particular model’s success may be different to those of tasks - the equation offers as an output a value in the range
another. [1,1000], with the higher values meaning a higher level of
quality or detail in an image [27]. It came to use in CNN
a: ACCURACY modelsin[28].
Theaccuracyofamodelistheoverallmeanofthepredictions
made by the model, both correct and incorrect. It measures f: MODESCORE
thetotalcorrectpredictionsagainstthetotalpredictionsboth A modified version of the Inception Score, the Mode
correctandincorrect. Score[29]isdesignedtoignorethedistributionoftheoriginal
TP+TN setofprobabilities.Introducedin[30],theModeScorewas
acc= (3)
TP+TN +FP+FN designed to deal with ‘‘missing modes’’, or areas in which
thegeneratorwasundertakingverylittlesamplingandwhere
b: PRECISION thediscriminatorthereforetookprecedence.Themodescore
The Precision or Positive Predicted Value (PPV) is the wasalsodesignedinordertoofferawaytoevaluatesample
measurement of all the true positive predictions, against all qualitywithoutahumanannotator.
thepredictionsofapositiveclass,bothTPandFP.Inthisway,
itevaluatetheoverallwaysinwhichthemodelsuccessfully
g: FRÉCHETINCEPTIONDISTANCE
orunsuccessfullyclassesthepositivevalues.
Another evaluative metric designed originally for use in
TP computer vision tasks [28], the FID, as a version of the
P= (4)
TP+FP originalInceptionScore,isdesignedasanattempttocombat
76074 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
TABLE1. TypesofGANresearchinrelatedworks.
overfitting2 withinthedata.TheFIDcalculatedforanytwo TABLE2. Metricsinmachinelearningclassifiers.
distributions,µandν,overthesetofrealnumbers,RN:
Z
!1/2
d (µ,ν):= inf ∥x−y∥2 dγ(x,y)
F
γ∈(cid:48)(µ,ν) Rn×Rn
(7)
as r - and
N(µ′,P′
), and this is therefore calculated as in
When we examine this equation it is of importance and Equation8.
interest to note that the set, Gamma(µ,ν) is also called the FID(r,g)=∥µ −µ ∥2 +Tr( X + X −2( XX )1/2)
2-Wasserstein distance. It is possible to calculate the FID r g 2
r g r g
usingasecondmethod-butonlyunderthespecificinstance
(8)
in which the variable distributions are two Gaussian, multi-
dimensional distributions,
N(µ,P
) - symbolized below
V. DATASET
2Overfittingoccurswhenthedatagivenistoospecializedandthemodel
This section briefly discusses the datasets used in the
fitsitselftoospecificallytothegivendata,meaningthatthegeneralizability
ofthemodelislost,asistheabilitytouseitwithfuturedata. surveyedpapers,theircontents,type,andorigins.Whilewe
VOLUME11,2023 76075

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
didnotwanttodevotetoomuchtimetowardsthedatasetsas TABLE3. ThedistributionofclasstypesovertherawCICIDS-2018
opposedtothemodels,wefeltitimportanttoensurethatthe dataset.Theimbalanceshowsclearlytheneedforpreprocessingand
dataaugmentationmethodsbeforeusingittotrainmachinelearning
readerhadasolidfoundationastowhichdatasetwasbeing classifiers[36].
referredtoandwhyitwasappropriateforuse.
A. NSL-KDD
In1999,theKDDdatasetwasreleasedaspartofachampi-
onshipgame,TheThirdInternationalKnowledgeDiscovery
and Data Mining Tools Competition. The original purpose
of the dataset and the competition was to have competitors
buildingtheirownNetworkIntrusionDetectionSystem[31].
Thisdatasetwaslaterrefinedandtheproblematicissuesdealt
with-thefirstissuewasalargenumberofduplicaterecords dataformachinelearningasanefforttoshowingreaterdetail
which required removal from the set; the second issue was the effect this pre-processing data had on the training of a
thewaythedatawasstructured,causinganyIDSalgorithm system.
toachievea86%accuracyrateatminimum[32].Theseissues
wereassessedandamendedin[32],andtheresultingdataset 2) CICIDS-18
wasdubbedtheNSL-KDDdataset.Thisdatasetofintrusion Like the CICIDS-17 dataset, the 2018 updated version of
detectioninformationhasfourcategories:DoS,UsertoRoot the dataset contains real-time traffic files for analysis. The
(U2R),RemotetoLocal(R2L),ProbingAttacks.Thetraining work done by [34] takes steps to examine the biases and
setcontains1,074,992uniquerecords:812,814areofbenign imbalancesofthedataset(aswellastheearlier2017dataset).
traffic,and262,178arefromthefourclassesofattackslisted Theassessmentshowedtheskewofdifferentdatatypes,with
above.ThenewandimprovedNSL-KDDtestsetcontained theBenigndatashowntobesignificantlygreaterinnumbers
77,289uniquerecords.Theupdateddatasetcanbefoundon than any other type, and some data types so small that the
the website for the Canadian Institute for Cybersecurity at trainingofMLalgorithmsontherawandfulldatasetwould
UNB,andisopenaccessforresearchers[33]. notcreateabalancedandeffectiveIDSscheme.Thiscanbe
seen in Figure 3, a table of the distribution of data types,
orclasses,inthe2018editionofthedataset.
B. CIC-IDS
The CIC-IDS datasets are large sets of network traffic
data. They include Benign data, multiple types of DoS C. DARPA
(denial of service), DDoS (distributed denial of service), The DARPA datasets date back to 1998 and 1999 respec-
infiltration, SQL-injection, bots, port scans, and brute force tively. They were considered early pioneers of data classes
attacks. Like the NSL-KDD dataset, the CIC-IDS datasets showingnetworkattacks.Thedatasetswereputtogetherby
areavailabletoresearchersasanopensourceresourcefrom MIT’sLincolnLaboratory,publishedin[37],withpermission
the UNB Canadian Institute for Cybersecurity. It can also and involvement from the US government and Air Force.
be found in numerous other locations across the web, as it The full datasets can be found in places like Papers with
is a popular dataset for training machine learning and IDS Code[38],aswellasonMIT’sLincolnLaboratoryResearch
schemes. The name CIC-IDS is an acronym for Catalonia and Development website [37]. Similarly to the CICIDS
IndependenceCorpusIntrusionDetectionSystem.Therehas datasets, the DARPA datasets contain the real-time traffic
beenasignificantbodyofresearchintothedatasetsfromboth data,andanofflineevaluationandassessmentofthecollected
2017and2018,includingasurveyandtaxonomyundertaken information. The DARPA datasets were collected based on
in[34]. attacksanddailytrafficforanAirForcebase.Theyinclude
a large number of attack types. The data is separated as
follows[37],
1) CICIDS-17
TheCICIDS-17isthedatasetcreatedin2017,usingthedata • Outsidesniffingdata(TCPdumpformat)
typesandattacksmostprevalentatthetime.Itcontainsreal- • Insidesniffingdata(TCPdumpformat)
timePCAPfilesofnetworktrafficoverthecourseofawork • BSMauditdata(fromPascal)
week - Monday 9am to Friday 5pm. In addition to the raw • NTauditdata(fromHume)
trafficflowfiles,itcontainsevaluationsofthetrafficdata,and • Long listings of directory trees (from Pascal, Marx,
Zeno,andHume)
labeledandclassifiedpackets,withCSVfilestodealwiththe
networkanalysisinformationaspartofthedataset. • Dumpsofselecteddirectories(fromPascal,Marx,Zeno,
andHume)
The dataset’s popularity has resulted in significant anal-
ysis. In [35], a thorough examination of the dataset was • Areportoffilesysteminodeinformation(fromPascal)
undertaken, with Feature Selection used to examine the Interestingly,inspiteofthefactthatthedatasetsareovertwo
77 features in the dataset. They also utilized the processed decadesold,somerecentpapershavevoicedtheirsupportof
76076 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
theDARPAdatasetsoverthemorerecent(butstilladecade entries,andhasbeenusedforbrute-forcedictionaryattacks
old)NSL-KDDdatasets[39]. as well as for checking proposed passwords against. It is
alsousedtotrainmachinelearningtoolslikePassGAN[48],
D. CTU-13 whichreplacesthetraditionalpasswordrequirementswhich
TheCTU-13datasetisprimarilyusedfortrainingclassifiers are chosen by a person, and creates its own requirements.
torecognizebotnetattacks.Itcontainsreal-timebotnettraffic PassGAN uses a Generative Adversarial Network to check
of13differentclasses,andisoneofthepremierdatasetsfor and learn password distribution and such, and was trained
trainingMLIDSalgorithmstorecognizebotnettraffic[40]. on the RockYou dataset. It has also been used to train
DuetotheimbalanceofclassesintheCTU13dataset,there a Variational Autoencoder model for password guessing,
isasubsetcalledtheQuasi-BalancedCTU-13dataset[41], in [49]. The dataset can be found in multiple locations,
whichpreservestherareclasseswhilebalancingthenumber including Kaggle,3 IEEE Data Port,4 and TensorFlow,5
of instances with more heavily represented classes. The amongothers.
dataset has been used to validate results of training ML
algorithms as in [42] and [43]. In both of the mentioned G. ADFA
cases,theCTU13datasetwasusedtovalidatetheresultsof The Australian Defence Force Academy (ADFA) Intrusion
trainingontheNSL-KDDdatasetdiscussedinSectionV-A. DetectionSystemdatasethastwoversions-aLinuxversion
Thedatasetcontainsthefollowing15featuresaspartofthe (ADFA-LD) and a Windows version (ADFA-WD). These
trafficflowcapturedforthedataset[40]: can be downloaded directly from the UNSW Sydney6
universitywebsite.Thedatasetwasgeneratedandcompiled
• Starttime
by Creech et al. over the course of three research papers,
• Duration
one of which was a doctoral thesis [50], [51], [52]. The
• Protocol
dataset was originally developed to be used in research on
• SourceanddestinationIPaddresses
Virtual Kernel Theory and capturing process calls, but has
• Direction
sincebeenusedfordevelopingIntrusionDetectionSystems
• Sourceanddestinationports
(asin[53]),andinusingk-nearestneighborclassificationfor
• State
cybersecurity(asin[40]).
• Typeofservice(ToS)
• Totalpackets
• Totalbytes H. UNSWNB15
• Timecomparison This dataset from the University of New South Wales
• Averagebyterate (UNSW) is an amalgamation of real traffic and generated
• Averagepacketrate attack data [54]. An intrusion detection dataset, it contains
• Pingbyte generated data from an IXIA traffic generator environment
• Maliciousport setup,ThedatasetisavailableontheUNSW’swebsite,7 as
well as Papers with Code.8 The dataset contains 2,540,044
instances,bothbenignandmalicious[55],andwasintended
E. DGArchive
The DGArchiveis aset ofdomains, of43 families,classes, to be a successor to the NSL-KDD (’98 and ’99 versions)
or variants, with more than 20 million domains as of and the DARPA IDS datasets [56]. Attacks are set in the
2015 [44]. These domains are from models in Domain following categories: Analysis, Backdoor, DoS, Exploits,
Generating Algorithms which create domains for Control Fuzzers, Generic, Reconnaissance, Shellcode and Worms.
and Command centers. The database of malicious botnet ThebreakdownofinstancesperclasscanbeseeninFigure4.
C&C domains allows for machine learning classifiers to be
trained on how to detect domain name malware. This data VI. TYPESOFGANMODELS
is extremely important in creating new machine learning Wehavesurveyedpaperscontainingawiderangeofmodels
methods for identifying botnet C&C centers (as in [45]). ofGANschemes.FromthebaseGoodfellow(or‘‘Vanilla’’)
The compilation of this information into such a large and GANschemetomorecomplexversionliketheWasserstein
comprehensive database is an important research tool. The or the Conditional Deep Convolutional GAN (cDCGAN),
DGArchivedatasetisalsousedtocreateadversarialmachine thesepapersusemodelswhicharebestsuitedtotheirneeds.
learning models, such as MaldomDetector [46], which Asaprimer,orrefresherforthemoreexperiencedresearcher,
undertake the generation of malicious domain names itself,
and allows researchers to test defensive machine learning 3https://www.kaggle.com/datasets/wjburns/common-password-list-
algorithmsonanadversary. rockyoutxt
4https://ieee-dataport.org/documents/rockyou
5https://www.tensorflow.org/datasets/catalog/rock_you
F. RockYou
6https://research.unsw.edu.au/projects/adfa-ids-datasets
The RockYou dataset [47] is a comprehensive list of 7https://research.unsw.edu.au/projects/unsw-nb15-dataset
commonly used passwords, with more than 14 million 8https://paperswithcode.com/dataset/unsw-nb15
VOLUME11,2023 76077

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
Z
TABLE4. AbreakdownoftheinstancesperclassintheUNSWNB15 V(G,D)= p (x)log(D(x))dx (12)
data
dataset[55].
x
+p (x)log(1−D(x))dx (13)
g
B. cGAN
cGAN, or Conditional GANs, as proposed in [7] by Mirza
andOsindero,suggestamethodforcreatingcontrolsonthe
outputofaGANmodel,inordertocreatedatasampleswith
afocusonparticularaspects.MirzaandOsinderodiscussthe
benefitsofbeingableto‘‘direct’’theprocessofGANsample
creation.Forexample,beingabletofocusthesamplesonthe
we have compiled the different types of GAN used in this
classlabelingmaybeofuseinsomeinstances.Inothers,the
literaturefortheeaseofuseofourreaders.
focus could be on a certain feature in the samples. In this
way,thecGANmodelallowsforanelementofcontrolthatis
A. GOODFELLOWGAN
lackingintheGoodfellowGAN.In[60],theauthorsdiscuss
Thetraditional,orVanilla,GenerativeAdversarialNetwork,
the ability the cGAN model creates to allow the researcher
is that proposed in 2014 by Goodfellowetal.[1]. The
to employ different modes of operation for different tasks.
traditional GAN follows the template set out in Figure 1.
The ability to focus on contextual input is a feature heavily
Therearehowever,twoimportantpointstomakewithregards
discussed with respect to CGANs. While in a Vanilla GAN
tothismodel.
thestructureinFigure1,inacGAN,thenoisefunctionp (z)
z
is combined with the conditional data, represented by y as
1) MODECOLLAPSE inputtotheGenerator.ThisisshowninFigure2.
TheproblemofModeCollapse-essentiallyanoptimization
problem - in GAN models is inherent to the MinMax game
C. DCGAN
that is used to achieve optimal results. The model can
The Deep Convolutional Generative Network, or DCGAN,
fail because it has an inherently non-convex shape, making
is a model put forward in [61]. They modeled the DCGAN
maximalvaluesdifficulttofindwithconvexmethods.Other
architecture heavily on the original Convolutional Neural
models utilize different methods, for example the gradient
Networks that were used as building blocks for GANs.
descent-ascent(GDA)[57],toavoidtheModeCollapse.
The original DCGANs were, as most GAN models were,
originallyheavilyfocusedonimagegeneration,learning,and
2) CATASTROPHICFORGETTING classification tasks. These networks generalized well, and
TheproblemofCatastrophicForgettingisonewhichoccurs have since been successfully applied to security problems.
whentheinformationgainedinprioriterationsofthemodel Radford et al. incorporated multiple new techniques from
are lost or destroyed by the new task or iteration [58]. several sources into their new GAN model (see [62], [63],
This is obviously a distinct problem because it makes it [64]).Thesechangeshelpedmakeitsosuccessfulinitstasks.
all but impossible to optimize the model as necessary, One
of the outcomes of Catastrophic Forgetting is a failure to
D. WGAN
reach convergence. Both mode collapse and catastrophic
The Wasserstein GAN was proposed in a 2017 conference
forgettingareseparateandinterlinkedproblems-tofixone
paper [65]. The paper clearly lays out the two different
you need to fix the other [58]. There is discussion within
distributionsthatarepartoftheircontribution.Thedistance
the research community as to whether this issue is fixable
and divergences between our two separate distributions:
utilizingContinuousLearningmethods[59]. P ,P ∈Prog(X),inwhichProb(X)is‘‘spaceofprobability
r g
ThestructureoftheGoodfellowGANfollowsthatofthe
measuresdefinedonX’’[65,p.215].Thedistancebetween
general model sketched out in Section II. As such, we will
thetwodistributionsismeasuredbytheTotalVariation(TV)
not go into it deeply here. The Goodfellow model provided
distance,inEquation14.
the structure on which these other methods were built. The
optimal discriminator equation is shown in Equation 9, and δ(P ,P )= sup |P (A)−P (A)| (14)
r g r g
thetrainingfortheGoodfellowDiscriminatorandGenerator A∈P
areinEquation10.
Thedivergencesbetweenthedistributionsaremeasuredwith
D ∗ (x)= p data (x) (9) theKullback-Leibler(KL)divergence(Equation15),andthe
G p (x)+p (x) Jensen-Shannon(JS)divergence(Equation16).
data g
Z
V(G,D)= p data (x)log(D(x))dx (10) KL(P ∥P )= Z log( P r (x) )P (x)dµ(x) (15)
x r g P (x) r
Z g
+ p z (z)log(1−D(g(z)))dz (11) JS(P r ,P g )=KL(P r ∥P m )+KL(P g ∥P m ) (16)
x
76078 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
FIGURE1. ThesimplifiedstructureofaVanillaGAN,asproposedby[1].
FIGURE2. Thestructureofaconditionalgenerativeadversarialnetworkbasedonthatproposedby[7].
The central calculation to the WGAN is the Wasserstein ofcompromisinginfecteddevices[70].Whileonlyproposed
distance,whichisapartoftheEarth-Moverequation,orthe foruseinaugmentingdatasetsandincreasingtherobustness
EM-distance. This equation tracks the distance between the of Android antivirus software, it is functional. This is not
result/outcomeandtheintendedgoal,ratherthanjustabinary the only Android API malware creation to come out of
0/1 evaluation from the classifier. This equation for the the cascade of GAN development, and it shows the extent
EM-distanceisshowninEquation17 to which GAN can be used by an adversary for malicious
purposes. In [71] the authors found that they could disrupt
WD(P
r
,P
g
)= inf E (xr,xg)∼γ[d(xr,xg)] (17)
theaccuracyofAndroidantivirussoftwarebasedonmachine
γ∈(cid:48)(P r ,P g)
learningsystemsbychangingonly4featuresofthe315used
WGAN models have been widely adopted and used in for detection. They created a scheme to use this called
many fields. In cybersecurity, they have been the basis of TrickDroid,whichcreatedadversarialexamples.Thechange
IntrusionDetectionSystems,asin[66],inwhichtheauthors of only 4 features dropped the accuracy/detection of those
proposed a WGAN base for polymorphic adversarial cyber classifiers to 0%. This staggering piece of research showed
attacks, to train the IDS scheme against an ever-changing how important a truly robust and tested system is needed
enemy. in the realm of Android devices, and not just in traditional
computer antivirus schemes. The finding is also dependent
E. BiGAN on the use of classifiers built using machine learning – this
The Bi-directional Generative Adversarial Network was raises potential red flags about how ready these system are
proposed in 2017, by Donahue et al. [67]. The purpose of to be deployed and implemented for wide use. However,
BiGAN models was to create a method of inverse mapping once the authors flipped the script and created a system
of the information backwards into the latent space. This to generate code injection attacks (CIA), the result was
inversemappingofferedmorefeedbacktothenetwork.Italso that the classifiers achieved under 1% in evasion rates.
createdtheabilityforresearcherstosuperviselearningwith When they used their scheme, TrickDroid, to generate
differentfocuses.ThestructureoftheBiGANmodelcanbe AEs for augmenting the dataset, the classifiers tested had
seen at its most basic level in Figure 3. The major change their evasion rate dropped to 0.5% maximum across the
is the addition of the encoder to the two-party GAN model, board.
creating a three-party game instead. While BiGAN models
doexcelinchallengesinsecurity,theyalsogainedpopularity G. CycleGAN
in development for reading and generating diagnostic RNA The CycleGAN mechanism translates images from one
predictions for the bio-informatic infosphere [68]. Others domaintoanother[72].Thereismorethanjusttheonetypeof
havealreadybegunutilizingBiGANsinintrusiondetection, model - recent modifications include Mocycle-GAN, which
suchas[69]. translatesvideofromonespaceintoanother[73].Theaimsof
CycleGANmodelsaretobeabletotaketheinputimagefrom
F. GANG-MAMANDTrickDroid onedomainandtranslateitintoanotherdomainorproblem
The GAN used to create malicious Android apps, playfully spacebelongingtotheoutputsphere.Abasicoutlineofthe
namedGANG-MAM,createsactualAPIcallsforthepurpose CycleGANmodelisinFigure4.
VOLUME11,2023 76079

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
FIGURE3. ThestructureofthebasicBi-directionalGANmodelproposedin[67].
the creation of a ‘‘distributed hashcat’’ to harness these
abilities [77]. The authors of [48] found PassGAN to be
able to match 51-71% of passwords from the HashCat
program.Beingcapableofundertakingthislevelofpassword
generation anonymously is a difficult task. It also suggests
thattheuseofGANsforattackingthroughpasswordguessing
hasahighenoughsuccessratethatitwilllikelybeanareaof
interest in not only research, but also in the development of
newblackhattechniques.Asalways,thebalanceofresearch
and ethics is at play in situations such as this, and it is
important to consider the potential misuse of any openly
providedalgorithmsandhowtheyarebuilt.
FIGURE4. TheCycleGANmodelatitsbasestructurefortranslating
problemdomains.
J. ISGAN
The Identity Sensitive Generative Adversarial Network,
H. AC-GAN
introduced in [78], was proposed to generate sketches
The Auxiliary Classifier Generative Adversarial Network
based on photographs. The reasoning for this was that
wasproposedin[74].Itoperatesbyincreasingthestructural
the translation of the image often produced a great deal
requirementsofthelatentspaceofatraditional/vanillaGAN.
moredetailthanisnoticeableinaphotograph.Thesecurity
They also added a cost function which was specific to their
applicationsofthismodelinvolvetheabilitytoextractclearer
(imageresolutionbased)task.TheobjectiveofOdenaetal.,
imagesfromCCTVimagesfromcrimescenes,amongother
was to characterize ‘‘the structure of natural images’’ [74].
things. While a very specific use-case is involved, it still
The process involved down-sampling images to draw out
offersanintriguingmethodofimage-to-imagetranslationfor
the most necessary features. They utilized this to identify
detailextraction.
the point at which the ability to discriminate details within
an image becomes an exceptionally difficult task. In [75],
K. BEGAN
this model was moved into generating the more insidious
The Boundary Equilibrium Generative Adversarial Net-
malicious code attempting to attack the user system. They
work, or BEGAN, was proposed in a 2017 paper by
foundthismodeltobeparticularlyeffectiveatthistask.
Berthelotetal.[79].ThepurposeoftheBEGANmodelwas
I. PassGAN toemploythebestoftheWGANmodelandtheGANsthat
In a 2019 paper, Hitajetal.[48] proposed the GAN based usedtrainedautoencoders,whilealsochangingthewaythat
PassGAN. This ML scheme was focused on learning likely convergencewasreached,soastocreateamodelthatwasfast
password distributions from real lists, and creating its andsturdy.Thecontributionsdiscussedinthepaperinvolve
own password guesses. It was trained on the RockYou using a new equilibrium factor to balance the generator
dataset of passwords (see Section V-F). The authors used and discriminator networks; a method for sliding along the
the unique entries in the RockYou dataset for training scale between diversity and quality; and the novel measure
purposes.In2020,Biesneretal.[49]usedasimilarapproach for approximate convergence. The new MaxMin, optimized
with Variational Autoencoders to create password guessing objectiveequationisshowninEquation18.
software trained via deep learning using multiple datasets,  L =L(x)−k ·L(G(z )) forθ
including the RockYou dataset discussed in Section V-F.
 D t p D
L =L(G(z )) forθ
The PassGAN algorithm was trialed against HashCat [76], G G G
a system to process and classify hashtags which has since k t+1 =k t +λ k (γL(x)−L(G(x))) foreachtrainingstept
beenrepurposedformanyresearchareas,includingthrough (18)
76080 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
L. ProGAN P. InfoGAN
The Proximity Generative Adversarial Network was devel- The Information Maximising Generative Adversarial Net-
oped to preserve important semantic data - specifically, work, or InfoGAN, model was first proposed in Chen et al.
the proximity of data in the original space when down- in2016[84].InthepaperinwhichInfoGANwasintroduced,
sampling, such that the proximity is preserved when the theauthorsnotedtheabilityofInfoGAN’smodeltountangle
data is translated into a lower-dimensional space [80]. The images of handwritten characters. The model was tested
ProGAN model not only preserves, but creates a method and trained using the MNIST dataset. It was also utilized
to generate proximities in sample data. The aim was to on 3-dimensional images of faces, and on pictures of
use this generation of proximity data to discover different house street numbers. In performance, the InfoGAN model
semantic and characteristic traits in data with different adds ‘‘negligible’’ complexity to the vanilla GAN (see
proximities. SectionVI-A) model. The training itself was based on the
training done for a DCGAN (SectionVI-C), rather than a
M. MSG-GAN vanillaGAN.
Multi-ScaleGradientsforGenerativeAdversarialNetworks,
or Msg-GANs, are meant as an answer to the problems of Q. SeqGAN
domain transferability [81]. Because the gradients change A version of GAN developed for the purposes of gener-
specifically for the task at hand, taking an existing GAN ating data sequences, SeqGAN was proposed in 2016 by
model and modifying it for a new use is not a simple task. Yuetal.[85]. The SeqGAN model discards the generator
TheideaofMsg-GANsishavingmultiplescalesofgradients, differation problem and instead uses gradient policy the
whichcanpassfromthediscriminatortothegenerator.This way we see in the common WGAN derivative, WGAN-GP.
alsomakesthesystemmorestable. This was built from a need for a GAN model that could
deal with sequences of discrete values, and not just binary,
N. SAGAN ‘‘real-not-real’’, continuous data. Using Gradient Penalty
TheSelf-AttentionGenerativeAdversarialModel(SAGAN), (GP) means that the generator can be coaxed bit by bit
was proposed in a 2019 paper by Zhangetal.[82]. This towards the goal, along a gradient path. These small but
model was a variant with the specific distinction that the significantchangescanbehardtoundertakeinthetraditional
creatoroftheoriginal/vanillaGAN,IanGoodfellow,worked continuousGANmodel.Anotherreasonwhythisvarientisof
on the creation of SAGAN, for long-range image tasks. interestisthatthetraditionalGANoutputsatallyofreal/not-
SAGAN models were created to allow the generation of real, and therefore would find giving a partial sequence
details that come from a multitude of features, and a as output difficult. To deal with this, the authors decided
discriminatorwiththeabilitytocheckalltheseexceptionally to classify generation of these sequences as a sequential
detailedsamplesareconsistentwithoneanother.Theaddition decision-makingprocess[85].Aspartofusingsmallchanges
of a ‘‘self-attention’’ module to the model offers the ability along a gradient to alter the output of the generator, the
to calculate the full feature set and distances, returning authors propose a series of Monte Carlo calculations, and
a weighted sum with fairly little computational overhead thentrainthegeneratorusingthepolicygradientitself.The
cost. The main distinction of the SAGAN model is that objective equation for the SeqGAN with GP is shown in
it is essentially a convolutional GAN (see VI-B) with Equation20,
a self-attention module added. This module gives us the
opportunitytoaddanddefineveryfinedetailswithinimages
J(θ)=E[R
T
|s
0
,θ]= X Gθ(y
10
)·Q G
D
θ
φ
(s
0
,y
1
) (20)
y1 ∈γ
O. IW-GAN
R. TranGAN
Inferential Wasserstein generative adversarial networks,
TranGAN is the result of a transfer learning model whose
orIW-GANs,meldsAutoencodersandGenerativeAdversar-
purposeistoundertakesocialtieprediction[86].Thisisan
ial Networks together for greater functionality. Proposed in
important piece of the puzzle for social network analysis.
2022byChenetal.[83],theIW-GANemploysadistinctand
When tested against the traditional benchmark algorithms,
fast stopping criteria, and trains both the generator (G) and
TranGAN outperformed them and seems to have become a
thedeterministicautoencoder(Q : X → Z)simultaneously.
newstandardinsocialtieprediction.
The results of their paper show IW-GAN as being effective
at guarding against mode collapse. Rather than focusing
VII. AREASOFUSE
on the Kullback-Leibler distance, the IW-GAN employs
In the seminal paper introducing Generative Adversarial
the 1-Wasserstein distance as its main evaluation tool. The
Networks,IanGoodfellowstatesthatthemodels’generators
equationforthiscanbeseeninEquation19.
are‘‘analogoustoateamofcounterfeiters,tryingtoproduce
W 1 (P X ,P G(Z) )= inf E (X,Z)∼π ∥X −G(Z))∥ fake currency and use it without detection, while the
π∈(cid:53)(PX ,PZ) discriminative model is analogous to the police, trying to
(19) detectthecounterfeitcurrency’’[1].
VOLUME11,2023 76081

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
TABLE5. Taxonomyofpapersreviewed.
76082 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
TABLE5. (Continued.)Taxonomyofpapersreviewed.
ThisadversarialmodeliswhatmakesGANssoexcellent ofGenerativemodels,usingtheDeepConvolutionalGener-
in many areas. In this section, we will discuss the areas ativeAdversarialNetwork(DCGAN)andLongShort-Term
in which GAN models have been most successful, with a Memory (LSTM) methods to design an effective real-time
particular focus on those relevant to the creation, training, intrusion detection system for use in general devices. The
and maintenance of Intrusion Detection Systems. Intrusion DCGAN is specifically chosen to help balance out the
Detection Systems default into several main categories. positive and negative samples by generating new synthetic,
For the purposes of this paper, and the review of IDS rawdata.AsstatedinSectionVI-C,theDCGANisexcellent
experimentation with GANs, we have sorted them into at generalizing, and has been applied to multiple security
the following categories: Wired or general Network IDS; problems, including [61]. The LSTM then provides the
Wireless; IoT; Mobile; Sensor Networks; and Autonomous classification method. This proved highly effective, and
Vehicles. These are the main types of Network Intrusion when tested against the KDD and NSL-KDD datasets
Detection Systems, and the main focus of this paper. (seeV-A),wasabletoachieve99.73%and99.62%accuracy
Traditional IDS methods involve anomaly detection and respectively.In[90],theauthorsuseaGANschemetolearn
attack signatures, with specific definitions for what the the patterns in their traffic log data, training the model to
scheme should be looking for [87]. This section describes recognizethetypesoftraffic,andthenusingthistodetectany
thedifferentareasinwhichGenerativeAdversarialNetworks anomalies in the traffic patterns. This creates a GAN-based
are most useful in assisting a Network Intrusion Detection systemfordetectingmalicioustraffic.Theirmodelachieved
System.TheuseofGANmodelstotrainintrusiondetection an f1-score of over 94% when identifying the anomalous
systems,orIDS,isafundamentaluse-caseincybersecurity. traffic.
Between the ability to generate new examples, create SomeresearchershavebeenusingGANsincreativeways
adversarial application files or traffic, and highlight the to improve network security, for example, in [91], authors
important contextual clues and relationships, GAN models attempted to create a pair of GAN schemes - one to attack
havesignificantcontributionstomakeinthetrainingofnew and one to defend. They used a GAN-based IDS for the
IDSschemes[88]. detectionofattackdata,andtodefendagainstit.Whiletheir
overallaccuracynumberswerenotashighasonemighthope,
A. NETWORKINTRUSIONDETECTIONSYSTEMS theydidshowthatitispossibletouseGAN-basedschemes
IntraditionalNetworkIDSmachinelearningmodels,GANs to defend against the types of attacks leveraged against a
are used in multiple aspects to improve performance. For machinelearningordeeplearningbasedIDSmodel.Usinga
example,in[89]theauthorstakeadvantageofthestrengths GANtocreatetheadversarialexamplesandasecondGANto
VOLUME11,2023 76083

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
detectanddefendagainstsaidexamplesisacreativeapproach In[98],theauthorsproposeamethodtouseGANmodels
totwo-partysecuritymodels.Thisisanareaofresearchwith to train their IDS using RGB images of malware for classi-
greatpotential. fication purposes. The authors wanted a way to continually
There have been many interesting, suggested models update and train their antivirus software, after it had been
for GANs to run on, including one which suggested that released. Using GAN models offered the opportunity to
pulling the opcodes, the machine instructions, from the continue providing new formations of malware and unseen
program,withthepurposeofcomparingbytesequenceswith examples to train their software. This ‘‘update and retrain’’
known malware examples, may offer high level accuracy behavior, also called online learning, is present in [99],
in identifying the variant [92]. This approach offered some inwhichtheauthorsclaimthattheycanuseGANmodelsto
interesting possibilities. The scheme focused primarily on dealwiththeissuespresentedbythedeteriorationofmachine
the protection of high-security systems, like weapons or learning models over time. The authors used multiple GAN
defensive programs. This is an area of urgency when it models - DCGAN [61], ALI-GAN [100], CoRGAN, and
comestoaccuratedetectionofmalicioustrafficandsoftware. CoRaGAN.CoRGANandCoRaGAN(createdbytheauthors
The authors proposed that one might use opcode sentences, themselves), and DCGAN, ALI, and CoRGAN consistently
sequential strings of the machine instructions, for the clas- perform at the top of the different metrics and databases.
sification and the generation of new sentences. The scheme Thehighestscoresinprecision,recall,f1-score,andaccuracy
resulted in a significant improvement in detection accuracy, wereallinthehigh90%,andtheaugmenteddatasetimproved
jumpingfrom96.3%,to98%whentheGAN-augmenteddata thescoresacrosstheboard.
wasaddedtothetrainingset.Thiswaswithanexperimental In[101],theauthorsproposeacombinationnetworkwhich
setup with such limited data, the adversarial samples from utilizes both Convolutional Neural Networks and WGANs
theoriginaldatasetnumberedonly42.Furthertestsshowed to create an IDS system to detect and classify threats to the
the area under the curve (AUC) went from 79.2% to 98% system.TheuseofaWGAN(discussedinSectionVI-D)is
when the augmented dataset was applied to the training of primarilyaimedatimprovingmodelstabilityandminimizing
the model. This clearly displays the success that is possible the chances of mode collapse. While they achieved a high
when using GAN models to generate adversarial examples, rate of accuracy on the test set, there were also 17 classes
even on the rarest classes. In [93], similarly to [94], the of attacks which were not seen in the training set but were
authors implement a GAN in order to classify malware included in the test set. On these unseen attack samples
samples through translation to images for feeding into the the system achieved an impressive 67.5% accuracy rate
GAN scheme. The Mal-IAGAN model they propose also in classification. The accuracy in classifying the binary
trainsIDSmodelsusingtheclassifiedimages.Thesignificant experimentswas88.23%andtheaccuracyinclassifyingthe
contribution they make in this paper is the robustness of fivemainclasseswas80.80%.Theabilitytocorrectlyclassify
the solution. Even when the Mal-IAGAN is only trained unseen classes shows exactly how powerful these models
on 1% of the dataset, an amalgam of VirusShare APK can be. While 67.5% is certainly lower than one would
Android malware [95] and the BIG-2015 dataset [96], the expect to achieve on classes the model was trained on, it is
model had an accuracy rate of over 80%. This suggests the significantly higher than the expectation for classes that the
model has an excellent robustness with regards to unseen modelhasneverseen,whichinthiscasewouldhaveoffered
examples,andthatthemodelcangeneralizetoasignificant arandomchanceofatmost1/17.In[102],theauthorsutilize
degree. a WGAN derived method called DoS-WGAN, specifically
Reference[97]focusesspecificallyontheuseofAPIcalls togeneratenewsamplesoftraceevidencefromDoSattacks
within Windows executable files for the identification of forthepurposeoftrainingIDSschemestodetectthesetypes
maliciouscode.TheauthorsuseaGANmodeltotraintheir of attacks. The DoS-GAN allows the camouflage of attack
own classifiers, both of which achieve impressive results in traffic, while the Standardized Euclidean distance and the
identifying malware samples. The contextual and semantic informationentropyareusedtomeasureprogressintraining.
relationshipsareessentialtoidentifyingthemalwarethrough The authors are specifically focused on the importance of
the API calls it makes. The authors use a Long Short-Term examining how attackers are most likely to adapt to the
Memory (LSTM) model GAN, and as their classifiers they knowledgethatthesystemtheyaretryingtocompromiseis
utilize models they name LSTM-Attention and BiLSTM- utilizingamachinelearningbasedIDSdefensemechanism.
Attention.Theproposedmodelsaremeasuredagainstseveral Thisfocusisshowninthewaysthattheauthorsutilizetheir
existing machine learning classifiers for their performance DoS-GAN method to perturb and manipulate the malicious
as IDS models. All of them are trained using their GAN samples for detection evasion. This paper is specifically
scheme. The comparison of Convolutional Neural Network focusedontheattacksideoftheIDSresearchquestion,using
(CNN),LogisticRegression,DecisionTree,RandomForest, the DoS-GAN model to attack and evade existing ML IDS
SupportVectorMachines,andMulti-LayerPerceptronmod- models. Their success in this shows the ways GANs can
els show excellent performance, with 95.43% and 96.53% be used not only for, but against IDS models. In [103], the
accuracy on the LSTM-Attention and BiLSTM-Attention authorsfocusonthereconstructionerrorandtheWasserstein
respectively. distance while creating an AI based NIDS scheme which
76084 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
utilizes both GAN and autoencoder methodologies. Three comparison with the other two. They made note of the
machine-learningclassifierswereused:deepneuralnetworks importance of feature extraction in identifying malicious
(DNN); convolutional neural networks (CNN); and Long network traffic through an IDS. The use of an autoencoder
Short-Term Memory (LSTM) models. The experimental forthispurposeallowstheIDSmodeltocontinuallymodify
set up was tested on the NSL-KDD (both versions), itselfandadapttoenvironmentalchangeswithinthenetwork,
UNSW-NB15, IoT datasets, as well as a ‘‘real-world’’ using unsupervised learning. In the 2022 review paper on
dataset of normal/benign network traffic. A Support Vector AdversarialMachineLearningmethodsforsecuringwireless
Machine (SVM) and Decision Tree (DT) were employed and mobile networks, the authors [22] explored the current
as comparative models for the experiments. The proposed stateofGANresearchintheareaofwirelessnetworksandthe
GAN NIDS scheme achieved scores of 93.2% and 87% relevantintrusiondetectionsystems.Thisisaverythorough
on the NSL-KDD and UNSW-NB15 datasets respectively. survey of the state-of-the-art in the area, and the inclusion
In several categories on the IoT dataset the model achieved of GAN models makes it particularly relevant to the work
accuracyof100%.Thisrobustandcompetitiveperformance presentedhere.TheauthorsnotethatGANsgenerallyrequire
showcases the effectiveness of GAN based schemes for access to all the features, including the functional and non-
network intrusion detection systems. Similarly, in [104] the functional. This is because of the need to generate realistic
authorsemployGANandaRandomForestmodeltoexamine datathatapproximatesthegenuinearticleinallways,andis
anddetectattacksinnetworktraffic,onlyusingtheCICIDS thereforeacorerequirementoftheprocessoftrainingaGAN
2017dataset.TheuseofGANmethodsinconjunctionwith model. They also particularly highlight the use of GANs in
the Random Forest classifier resulted in high results across creatingadversarialexamples,bothforattackandfortraining
theboard,andtheywerecomparedtotheresultsofasingle purposes.
RF classifier, with the accuracy, precision, recall, f1-score
oftheGANRFmodelachieving99.83%,98.68%,92.76%, C. INTERNETOFTHINGINTRUSION
and 95.04% in comparison to the single RF model’s scores In [108], a method referred to as attackGAN is used
of 99.19%, 98.2%, 83.79%, and 87.79% respectively. This to build attacks that take advantage of the weakness of
againemphasizestheutilityandstrengthofGANmodelsin machine learning models. They use their model to attack
creatingrobustIDSschemes. the perturbation of data on IoT devices. This method
is utilized to demonstrate the deficiencies of the current
B. WIRELESSNETWORKINTRUSION methods and ways they can be improved. The attackGAN
IntrusionDetectionsystemsthatresideontheNetworklayer model is based on the previously discussed Wasserstein
ofcommunicationinfrastructurefordistributedschemesrely GAN model (SectionVI-D), with feedback from the IDS
onarobustsecurityleveltosecurecommunicationsbetween scheme used to improve later attacks. The authors also
devices. This is an essential part of securing any business made use of the NSL-KDD dataset for the development
or government network. Any connected system of devices of the GAN model (see SectionV-A for details on this
that uses internet connectivity relies on NIDS models to dataset). Using GANs for adversarial examples like this is
remain safe and to enforce the CIA principles of security. anexcellentoptionfortraininganIDStoreactappropriately
Onesuchexample,usingPCAPfilesfortrainingandtesting, to zero days or unseen classes of attacks. GANs offer more
called FlowGAN, sets about doing exactly this [105]. This generalization in augmented datasets, which helps prevent
method improves the accuracy of identifying malicious overfittingwhentrainingtheMLIDSmodel.IoTdevicescan
networktrafficsignificantly,andtheauthorsutilizeadataset be used in concert to create distributed systems. Ferdowsi
introduced in [106], called ‘‘ISCX VPN non-VPN traffic and Sand [109] do exactly this, in creating a distributed
dataset’’,fortheexperimentationportionoftheirstudy.The GAN-based IDS for IoT systems. Their model achieved an
Precision, Recall, and F1-Scores were increased by 13.2%, accuracy of up to 20% higher than a non-distributed IDS
17%, and 15.6% respectively, when run against the same method. Because they distribute the system over all the
algorithmsusingadatasetuneditedbytheFlowGANmodel, differentIoTdevices(IoTD)onthenetwork,thesystemalso
using a Multi-layer Perceptron model in both cases. The provides an option for creating more stable IDS methods in
abilitytousethemodelonbothencryptedandnon-encrypted networkswithresistancetothefailureofindividualdevices.
traffic shows its usefulness. Many businesses and other Each individual device is optimized for detection using the
connected groups rely on connections that run through valuefunctioninEq.21.
VPNs, meaning a model like FlowGAN being capable of V(D ¯ ,G ¯ )=−log(4)+s(p ||p ) (21)
operating over encrypted traffic is extremely useful in real-
i i i datai data
worldscenarios.In[107],theauthorsemployanAutoencoder In [110], the authors use the newly published IoT-23 [111]
Conditional GAN (AE-CGAN) model to improve intrusion datasetandmethodssuchasBi-directionalGAN,orBiGAN
detection on the network, using the CICIDS 2017 dataset (see Section VI-E), to train IDS models to detect attacks
(seeSectionV-B).Theauthorscomparedthismodelagainst like those from the Mirai botnet, which at its peak infected
two others - single RF, and AE-RF - and found that the more than 600,000 IoT devices [112]. The IoT-23 dataset
proposed AE-CGAN model showed improved accuracy in involves the network traffic records of devices such as
VOLUME11,2023 76085

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
smart-doorbells and Amazon’s Echo smart home hub, and variety of categories including entertainment, news, system
is composed of log files generated from .pcap files with tools, etc. The test set for the WGAN model found the
labelsgeneratedthroughuseofapythonscript,thusavoiding accuracy of detecting malicious network behavior to be
the time-intensive requirement of individually labeling the approximately 88%. When the author included generated
samplesbyhand.Theauthorswereabletousetheirmodels data in the sample set the accuracy improved to 96.89%,
to achieve an impressive F1-score of 99%. BiGAN models, demonstratingthataGANmodelcanevencreateapplication
as discussed earlier, are specifically for the purpose of filesthatareabletoactinplaceofgenuinesamplefiles.This
allowinginversemappingsandtheabilitytospecifyfocuses. isnotaninsignificantfinding.
Their BiGAN model for the detection of zero-day and In [117], the authors examine the research into newer
unseen attacks achieved an F1-score of between 85% and advancedmachinelearningmethodsandmobileandwireless
100% over the different classes of the data. In [113], the networks.TheytouchontheuseofGANsfordatageneration,
authors combined a Wasserstein GAN and an Autoencoder particularly for supervised learning tasks. While it does not
for the creation of an IoT network IDS scheme which also focus specifically on security measures, there is discussion
uses the Gradient Penalty scheme to improve performance. of the different ways in which GANs were in use for
They used the Bot-IoT dataset from the University of New mobile network analysis training and Mobile Traffic Super-
South Wales [114] for training and testing purposes, and Resolution. GANs are particularly successful at this task,
identifiedwithinthatdatasetoftrafficflows9mainfeatures withtheirinitialaimofimagegenerationbeingtranslatedinto
on which to base their training - 2 categorical features and adversarialexamplesinmanypapers.
7 statistical features. Categorical features are run through UtilizingGANmodelstodevelopasecuremobilenetwork,
one hot encoding systems to prepare for use, resulting in in [118], the authors combine a GAN model with Zipper
a dimensionality of 29. Features are also normalized prior Network(ZipNet).Thegoalinthispaperistocreateasystem
to their use, ensuring ranges are kept to [−1,1]. As part of that can deal with the large scale requirements of mobile
the experiments, the authors trained both a Global Model, trafficanalysiscitywide.Theirschemecaninferdetailswith
and a Distributed Model. The Global Model is a single upto100timesthegranularityofstandardprobingmethods.
instance of the scheme with access to all local samples and It was potentially the first time a system has employed
data. The Distributed Model, on the other hand, involves super-resolutionmethodologytomobiletrafficanalysis.The
givingeachlocalnetworkitsownlocalautoencoder,trained scheme results in between 65 and 78% smaller Normalized
only on the local data and samples, and not linked to the RootMeanSquareError,orNRMSE.Thereiscertainlyscope
other instances. The overall performance was compared toundergofurtherresearchinthisarea,asthesecurityofthe
using four different clustering methods: one-class support mobile network from intrusions and malicious traffic is of
vector machine, isolation forest, local outlier factor, and K- vitalimportancewiththeproliferationofmobiletechnology.
Meansclustering.Thetraditionalmetricsofprecision,recall,
accuracy, and F1-Score were used to measure the resulting E. SENSORNETWORKINTRUSION
performances. The overall best performer was the Global Sensor networks, like those in smart grids, are an aspect
Model, with accuracy, precision, recall, and F1-scores of of IoT devices large enough to require their own section
97.11%, 99.33%, 97.33%, and 98.31%, respectively. This in this paper. Given their use in areas such as public
shows there is a space to utilize GAN-based NIDS for transport, power plants, medical devices, and other areas of
distributed IoT systems with a high degree of confidence national infrastructure, the security of these devices is of
and a significant success rate. Further research in this area nationalimportance.In[119],theauthorsreviewthecurrent
is needed, and this is a potential research space with the (as of 2019) methods in use for machine learning based
opportunityforseriousreal-worldapplications. intrusiondetectionsystemsinwirelesssensornetworks.The
Software-Defined Wireless Sensor Networks, or SDWSN,
D. MOBILEINTRUSION areacombinationofSoftware-DefinedNetworksandWire-
Given the prevalence of mobile devices in the current lessSensorNetworks.Software-DefinedNetworksarefound
technological era, the ability to secure these devices is of acrossmedicalandindustrialdevices,aswellasintheuseand
exceptional importance. Mobile devices contain scores of guidanceofdronesandbombs.Assuch,theyarehigh-value
personallyidentifiableinformation(PII),aswellasbeingthe targets in need of robust IDS methods. The possibility of a
portalbywhichweseetheworld.Asstatedsimplyin[115], maliciousactorhijackingoneofthesedevicesornetworksis
‘‘themorewidelyatechnologyisused,themorelikelyitisto fartooseriousathreattoignore.Reviewingthestate-of-the-
becomethetargetofhackers’’.In[116],theauthoremploys artinprotectingthesedevicesandtheirnetworks,theauthors
a Wasserstein GAN model to develop a malware detection foundthatcombiningmachine-learningorAImethodswith
system for mobile systems. This scheme is specifically cryptographic schemes to be the most effective way of
for detecting suspicious behavior and communication on securing the SDWSNs. GANs were taken here as effective
the network layer of a mobile device and could therefore methods of augmenting and improving the datasets for
also be considered a form of Network IDS. They used training these ML/AI intrusion detection systems. In [120],
559 applications from the Android Play Store, from a large theauthorsdevelopedanewGANbasedintrusiondetection
76086 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
systemforSmartGridnetworks.Thescheme,calledARIES, AVs, the authors of [125] gave a comprehensive review of
utilizes3differentdetectionlayersformaximumprotection. cybersecurity for vehicles. They were careful to highlight
Itscansandcoversnetworkflows,Modbusandtransmission the important security flaws found by Keen Labs in Tesla
control systems, and the operational data. Utility grids and vehicles in 2017,9 followed by BMWs in 2019 [126], and
energycompaniesinmostWesterncountriesareconsidered the newer security risks posed by the popularization of
to be Critical National Infrastructure, and therefore require autonomousvehicles,whichdependheavilyontheabilityto
a high level of security [121]. Attacks against CNI can be reach and communicate with global servers for updates and
disastrous for the people within a country, and thus any information on routes, conditions, and traffic alerts. BMW
intrusion into the networks that control and maintain CNI was the target of security vulnerabilities in [126] where the
must be detected and dealt with as soon as is possible. authors described the exploits and attacks found using the
Smart Grids, a type of sensor network that deals in the Infomaticsystemsandthenetworkedentertainmentmodules.
maintenance and visibility of an energy grid, are highly Thesesystems-forwhichthevulnerabilitieswereaddressed
connected networks, and therefore require sophisticated by BMW prior to the publication of the paper (an example
cybersecurity systems. The ARIES GAN system involved ofthesuccessofresearchersensuringethicalpublicationof
the use of electrical signal increases from a power plant in security research) - allowed the researchers to access the
Greece to detect control commands and abnormalities, the on-board computing modules and deploy commands to the
first to do so. This information was collected as part of the vehicles. Researchers in [125] also found that the majority
operationaldatalayer.TheCSE-CIC-IDS2018dataset[122] oftheresearchsurveyeddisplayedatendencytowardsusing
was used for the testing and training of the network. This machinelearningandartificialintelligencemethodstosecure
dataset includes network flow statistics and other control thesenewvehicles.Thissecurityneedcreatedbytheriseof
data which was combined with data from the Greek power autonomousvehiclesisonethatmachinelearningresearchers
plant for specificity of information. Using a Decision Tree havebegunexploring,leavingopportunitiesforresearchinto
classifierresultedinthebestscoresinthefirstdetectionlayer the potential use of GAN models to create secure network
(IDM)foraccuracy,truepositiverate,falsepositiverate,and intrusiondetectionsystemsforthesevehicles.Oneexample
f1-score,being99.4%,98.2%,0.3%,and98.2%respectively. of this can be seen in [127], where the authors proposed a
Intheseconddetectionlayerthebestresultswerefoundwith GAN-based Intrusion Detection System they named GIDS.
an Isolation Forest classifier at 91.7%, 75.1%, 4.9%, and Thefocusofthissystemwasoneffectiveness,expandability,
75.1%, while the third detection layer was best served by andsecurity.Becausethetrainingwasexclusivelyperformed
the ARIES GAN system at 93%, 87.5%, 5.3%, and 85.3% onnormaldata,thesystemcoulddetectintrusionsandattacks
respectively.Theselevelsofaccuracyshowthepotentialfor withoutfocusingonaparticulartypeofattackdata.Theidea
an ML IDS to protect CNI sensor networks. As the use of of this type of training was that the IDS would be able to
smart sensors in CNI systems grows, so does the need for better detect unseen attacks this way. The authors exploited
truly secure IDS models. Therefore, there is a need for a the image-based excellence of GANs by converting CAN
concertedresearcheffortinthisarea,andGANmodelsseem messages into images for use in the system, in a process
likelytooffersignificantimprovements. referred to as ‘‘one hot-vector encoding’’. The network
usedtoclassifywasacombinationofConvolutionalNeural
F. AUTONOMOUSVEHICLEINTRUSION Network and Deep Neural Network. The authors tested the
Autonomousvehicles,likeSensorNetworks,aretechnically system with DoS, Fuzzy, and RPM/GEAR attacks, as well
an IoT subsection. However, they are similarly prevalent asbenignor‘‘normal’’data.Whilethelargersizedinputsdid
and serious enough to require their own addition in this decreaseoverallaccuracy(withthemostsignificantdipat80)
paper. Plenty of research in recent years has focused on theinputsizedefinedforthefinalexperimentswasfixedat
the development and use of autonomous vehicles, known 64.ThelowestdetectionrateforaninputdatatypewasRPM
colloquially as self-driving cars. Because these machines attacks, at 98.7%. It was able to operate in real time, as it
areusuallyinconstantcommunicationwiththecloud-based took 0.18 seconds to sort 1,954 CAN bus messages, and in
services that provide their data and instructions, it is of practicetheCANbussystemgeneratesapproximately1,954
extremeimportancetosecurethemagainstintrusion.Hack- messagespersecond.Thisveryeffectivelydemonstratedthe
ingcars,eventraditionalvehicles,hasbeenshowntobeboth potential impact of a GAN based system for creating an
possibleandeffective.Asearlyas2015,Wiredpublishedan effective IDS for vehicular systems, but there is still plenty
article describing the way two researchers remotely hacked ofresearchspaceinthisarea.
a Chrysler vehicle, prompting a massive recall of over In [128], a review of IoT NIDS and machine learning
1.4millionChryslervehicles[123],[124].Giventheincrease systems,theauthorsputforwardtheusecaseofautonomous
inconnectivityfromtraditionaltoautonomousvehicles,the vehicles and the vehicular edge network as the example
securityofthesedevicesisalife-or-deathsituation.Assuch,
researchers have begun to seriously examine the security
9KeenSecurityLabofTencent,https://keenlab.tencent.com/en/2017/07/
27/New-Car-Hacking-Research-2017-Remote-Attack-Tesla-Motors-
concerns of malicious intrusion into autonomous vehicles.
Again/New Car Hacking Research: 2017, Remote Attack Tesla Motors
When reviewing the current state of the art in security for Again,2017-07-27.
VOLUME11,2023 76087

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
of GAN and NIDS in networked devices. The processes The use of generated Adversarial Examples can offer an
undertakenaspartofthevehicularedgenetworkarecarried improvement on generalization and learning traits from
outontheMobileEdgeComputingserver,orMEC.Whena families of malicious code. It can also help protect against
vehicleneedstoundertakeaprocessthatcanbedonefaster overfitting, especially when only small numbers of samples
ontheMECserverthanonitsowncomputationalequipment, for a particular class are available for training a network.
thenetworkoffloadstheprocesstotheMEC.Thevehicular InthecaseofIDSmodels,havinganattack/defendscheme,
edgecomputingsystemresponsibleforthisdivisionoflabor, suchastheonediscussedin[91](seeSectionVII-A),offers
orVEC,isa5GnetworkconnectingthevehiclestotheMEC the ability to view real-time reactions from the defender
for secure communication. Of course, as with any external network in a controlled environment. Building an attack
network connection, it is vulnerable to attack. The security modellikethiscreatesopportunitiestotesttheIDSmodelina
system proposed by the authors suggests the embedding of controlledenvironmentinrealtime,whichcanbeinvaluable
the GAN based scheme at each of the nodes, monitoring indebuggingandstreamliningthesystem.
any traffic to or from the MEC server. The security scheme In an example like MalGAN [132], the GAN model
is monitored by each MEC node, meaning that the MEC is used to create malware for the purposes of training
servers themselves are able to detect and react to malicious and testing Intrusion Detection Systems which are based
activitywithintheirnetworksector,aswellasallowingthema on machine learning methods. This is a key point - IDS
globalviewofthenetworkanditssecurity.Whiletheauthors models built through machine learning methods can be a
werefairlynon-specificaboutthetypesofGANalgorithms goodcounterpointtouseGANattackmethodson.However,
employedtoworkontheMECservers,orthegeneralset-up traditionalIDSmodelsareunlikelytogainmuchthroughthe
and use, they did specify that they were able to achieve an useofaGANattackmodel.
accuracyrateofupto90%. Adversarial examples are of course, not the only area for
employingGANsforuseinIDSmodels.Generativemodels
VIII. DISCUSSION can be used for creation and classification in many ways.
The previous sections have primarily set the stage for this The discussed areas of Sensor Networks and Autonomous
discussion-why,how,andwhereisitappropriatetoemploy Vehiclesareperhapsthemostimportantoressentialareasof
a GAN model for the improvement of Intrusion Detection researchwhenitcomestomachinelearningIDSmodels,and
Systems? The importance of discussing where not to use thusareanareaforfocusingGANresearch.
GANisasimportantasdiscussingthewaysinwhichGAN
isbeingeffectivelyemployed. 2) HOWTOUSEGAN
Generative Adversarial Networks are highly useful models
A. WHYGAN? for many tasks, when implemented correctly. While this
Goodfellowassertsthatthetwo-playergame,withtheheavy paperisspecifictoIntrusionDetectionSystems,themethods
intervention of backpropagation methods, is what makes of implementing GANs are standard across many research
Generative Adversarial Networks so effective in their tasks. areas. However, the framework for using GAN models
Thederivativesusedforthatbackpropagationarecalculated requires researchers to decide on tasks with care, so as to
asseeninEquation22. implement GAN models when they will be most useful.
We have iterated some of the tasks in which GAN methods
σ li → m 0 ∇ x E ϵ∼N(0,σ2I f(x+ϵ)=∇ x f(x) (22) are most likely to provide useful output, with discussion of
howandwhytheyworkinthementionedtasks.
1) WHENTOUSEGAN
TheGenerativeAdversarialNetworkmodelhasspecifictraits a: DATAPRE-PROCESSING
which make it better at some specific tasks than others. GAN models are excellent at tasks that involve balancing
We have explained the ease with which GAN undertakes datasets or sampling rare data classes for training and
image-based tasks below (see Section VIII-A2). However, testing of other Machine Learning classifiers. These tasks
thisdoesnotmeanthattheuseofGANschemesisrestricted oftenbreakdownintoimage-basedsamples,andnon-image
to those which are naturally image-based. Many tasks can samples,becauseofGAN’seaseofuseintheimagedomain.
be translated into image domains, or can be fitted with the In the realm of ML based IDS models, balancing the rarer
data they have, like those we have seen use the opcode attack classes in datasets is an extremely important part of
sequences[71],orPDFfiles[129],[130],orevenAPKs[131] training an IDS method. In some datasets there are as few
and API calls. In the training of an Intrusion Detection asacoupleofdozensamplesofaspecificclass.Traditional
System, the generation of Adversarial Examples [132] is methods like SMOTE or ADASYN may not be able to
of exceptional importance. Creating samples to ‘‘attack’’ augmenttheseclasseswithoutcreatingoverfitting,whichis
the system to train it offers the ability to train it in a whatmakesGANssouseful.
semantic manner with contextual clues. This can offer 1) ImageSamples
strength when the IDS is faced with zero-day attacks, Image tasks are an area GAN models are extremely
as it relies not only on previously seen training samples. competent in, with computer vision, imaging, and
76088 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
other domains well-saturated with GAN based b: ADVERSARIALEXAMPLES,UNSEENATTACKS,AND
schemes [133]. One excellent example is Star- ZERO-DAYSAMPLES
GAN [134], which the authors trained to take facial ThroughoutSectionVII,wehavedemonstratedtheeffective-
images, using celebrities for training and testing, ness of GANs in creating attacks and adversarial examples.
and translate them into different hair colors, genders, For example, in [139], the authors present a GAN-based
emotions (such as happy, angry, and fearful), and method for continuously changing the attack profile of a
skin colors. GANs are regularly used in tasks system so that it remains undetected by the IDS. The focus
that involve image-to-image translation, text-to-photo of the paper is on polymorphic attacks, those which are
translation[135],andimagegeneration. constantlychanginginordertoremainundertheradar.Using
2) Non-ImageSamples GANstocreatepolymorphicattackdatashowstheversatility
GANs may work particularly well on image based with which these systems produce synthetic samples. They
tasks,buttheyarealsoofgreatuseintasksthatinvolve usedtheGANmodelstoswapdifferentfeaturesofthebenign
samplesfromnon-imagedomains.Whileitispossible datasampleswithfeaturesfromthemalwaresamplesitwas
totranslateanon-imagedatatypeintoanimageforease trained on, to introduce characteristics of the benign data
ofprocessing(seebelow),itisnotalwaysnecessary. into the adversarial examples. This type of attack method
3) ChangingtoanImageDomain is extremely difficult to counter, and offers a serious risk to
As we have seen throughout this paper, GAN models those developing traditional IDS models. Using a Random
can be trained on data that has been translated Forest classifier to test the effectiveness of their model, the
from a non-image sample to an image sample. The authors found that after 100 epochs and having swapped
translationoftrafficflow,PCAPfile,applicationfiles, features, they were able to achieve a detection rate as low
and executables into images allows IDS researchers as 3.89%. This achievement shows the impact that GANs
to take advantage of the strength of GANs’ image canhavewhenusedtocreateadversarialexamplestoevade
classificationabilities.Thereareanumberofmethods IDS models. It also opens the doors to more research
for translating data to image, such as [134], [136], into how best to counter these attacks when deployed in
and[137].Inparticular,thetranslationof.PCAPfiles, real-world scenarios. In [140], the authors implement an
applications, and other data types into an image for attack scheme called A3CMal using GANs, which creates
easeofoperationisquitecommonamongresearchers malware that is capable of being classified as benign by
in the cybersecurity domain, due to the general detection schemes. They split their attacks into two groups
successthatGANmodelshavewithimage-basedtasks. - targeted and non-targeted. In the targeted attacks, they
This enables security researchers to maximize the attemptedtoforcetheclassifiertolabelthemalwaresamples
performanceoftheirGANmodelforIDSwhileusing with a particular label, while the non-targeted attacks were
traditionalIDSdatasetswithnon-imagedata. simply to evade detection, and have the classifier put the
4) Non-ImageSampleTypes malware into a benign category. The existence of an attack
Inmorerecentyears,asGANmodelshaveproliferated such as this, wherein the attackers are able to make the
fromthecomputervisiondisciplineintocountlessother classifier believe the malicious data is something entirely
subject areas, including cybersecurity, researchers different, chosen from a specific category, is one with
have increasingly employed GAN methodology with seriouspotentialrepercussions.Twistingmaliciouscodefor
non-image data types. Within this paper we have a specific classification by an IDS is a very real possibility
explored research that dealt with opcodes [131], withthemisuseofGANsbymaliciousactors,andassuchis
APKs[138],networkflowtraffic[118],andmanyother aresearchproblemwhichrequiresaddressing.
data types. Papers such as [89] have used network
dataofattackssuchastheKDDandNSLdatasetsfor
training and testing purposes, showing how versatile B. WHYNOTGAN?
these methods are. For IDS researchers, the ability to 1) WHENNOTTOUSEGAN
use untranslated datasets saves significant time in the While GAN methods can work extremely well in some
pre-processingstage,as wellascomputationalpower. situations,therearealsosomeareasandsituationsinwhich
Generally, IDS datasets for research do not appear GAN models will not offer much (if any) improvement.
in an image format, so the ability to use a GAN In[141],severalopenquestionsintotheuseofGANmodels
withouttranslatingthedatatoanimagefirstisofgreat are posed. One of these is why one would use a GAN
importanceintrainingandtestingmodelsforintrusion model instead of Flow Models, or Autoregressive Models.
detection. It also enables more realistic opportunities Odena points out that there are three specific categories for
for real-time operation, as the time taken to translate evaluating which of the three to use. This can be seen in
incoming data to images in order to classify it could the Table 6, which highlights the three metrics proposed by
significantlyincreaseprocessingtime. Odena[141].
VOLUME11,2023 76089

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
TABLE6. ThreemetricsfordeterminingwhethertheGenerative deployed throughout Critical National Infrastructure (CNI),
AdversarialNetworkmodelisanappropriatemodelforaparticular andthepotentialhackingofautonomousvehiclescreatesthe
task[141].
possibilityof fataltrafficcollisions. IntheRusso-Ukrainian
War, we have seen the importance of CNI first hand. One
scholarargued,in[142],thattheemploymentofcyber-attacks
on the CNI of Ukraine by Russia contributed to a ‘‘thunder
strategy’’ which helped speed up the war effort. This is
an extreme example, which demonstrates the importance of
a: TRAININGTRADITIONALIDSMODELS
protectingsensornetworksandCNIfromsophisticatedcyber
WhentraininganIntrusionDetectionSystem,GANmodels
attacks.Thisisbothanareaforgrowth,andanareaofgreat
are of use because they can undertake tasks like generating
importance, making them an excellent place for researchers
adversarial examples (see Section VIII-A1), but they are of
tobeginexploringwaystoutilizethepowerofGANmodels
little to no use in training traditional Intrusion Detection
tostrengthenCNIagainstattack.
Systems,whichdonotimplementmachinelearningmethods.
TheemploymentofGANmodelsintheseareasallowsfor
the adaptation and augmentation of datasets which contain
b: UNSUITABLESAMPLES rare classes or which are smaller than may be typical for
The suitability of the samples in the dataset used is very training neural network models. In newer areas like these,
important in whether or not to use a GAN model. As in datasets are both rarer and smaller than those for a typical
Section VIII-A1, image-based samples are excellent, as are IDS model. As such, the ability to generate more samples
sequencesandsamplesthattranslateintotheimagedomain becomes an issue of more significance. For one example,
without too much computational cost. The most important in [143] the authors use the Kyoto University Benchmark
pointhereisthatiftheresearchinvolvedisn’tautomatically dataset[144]totrainandtesttheirautonomousvehicleIDS.
asuitabledatatype,thecostofpre-processingthatdatamay The Kyoto University Benchmark dataset was created in
becomputationallyexpensivetothepointthatitissimplerby 2006,andcontainsIDSdatatakenfromtraditionalcomputer
fartoutilizeadifferenttypeofgenerativemodel.Especially systems. As such, it is not the ideal dataset for autonomous
when a researcher is looking to create an IDS model which vehicles,butitisreadilyavailableandlargeenoughtotrain
canoperateinreal-time,thepre-processingrequirementsfor neural network models on. This shows the need for models
theuseofaGANmaysimplyoutweighthepotentialgainsof based on systems like GANs to augment datasets that offer
employingsuchamodel. moretargetedandvehiclespecificsamples.
The use of GAN models to create labeled data, as is
c: ONESAMPLE,MANYLABELS donein[145],offersanewmethodofgeneratinglarge-scale
WhileGANmodelsareexcellentatlearningcontextualclues datasets. The requirement for large amounts of labeled data
and semantic relationships, when it comes to output, they fortrainingandtestingofMLmodelsisoneofthedrawbacks
are best when there are only a limited number of output of utilizing these schemes in real-world applications. In a
‘‘labels’’. If a sample set has too many potential outcomes, regular scenario, human operators are required to label
or even has more than one outcome per sample (multilabel datasetsforuseinsupervisedmachinelearning.Thisisboth
classification), GAN models are unlikely to perform well. time-intensive and expensive. Thus, the ability to generate
In these situations it may be more effective and successful labels for existing samples in order to create datasets is a
to utilize a different generative model. This type of data highlyimportantanddesirableapplicationofGANmodels.
is less likely to be encountered amongst research into IDS The success in [145] shows the possibilities of GAN
models, but if a researcher is trying to use a GAN on for creating realistic data with embedded semantic infor-
datasetswithmanydifferentattackclasses,ratherthanmerely mation. This potential could be transferred to the domain
a Benign/Malicious classification task, the computational of Intrusion Detection, and offers a potential pathway
power and time requirements may make using a GAN to new datasets for training and testing. There are also
unfeasible. many other avenues for potential research. The methods
employed by the authors in [146] to avoid the popular
IX. EMERGINGTOPICS step of translating the dataset into sequences or images
Having discussed when and when not to use GAN models and instead working on the data directly using the n-gram
in general research, we now discuss when and where GAN feature extraction method is certainly an area worthy of
seemstobeofmosteffectiveuseinemergingIDSresearch. future research for more applications. Any improvements
The uses of GAN are many, as seen in Section VII. The for using GANs without requiring pre-processing data into
most recent areas of development for GANs in Intrusion imagesofferbenefitstodomainssuchasIDSmodels.While
DetectionSystemsinvolvemethodsforautonomousvehicles many different methods exist, there is always room for
(asin[125]amongothers)andwirelesssensornetworkarrays improving the quality and availability of the data, as well
(such as [119]). These are both critical areas of research as improving the time and computational requirements for
withreal-worldlife-or-deathoutcomes.Sensornetworksare processingit.
76090 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
When it comes to adversarial examples for IDS models, performance of these different IDS methods, and the suc-
theincrediblylowdetectionrateachievedby[147]showsjust cessesandfailurestheyhavefoundthroughdevelopmentand
howmuchfutureresearchisneededtocreateIDSmodelsthat exploration. There are several areas of developing research,
cansuccessfullyfendoffattacksfromGAN-basedsystems. andmanypromisingmethodsandimplementations.Wehope
Using a GAN attack model can create a situation in which oursummationofthecurrentresearchprovesofusetothose
it is possible to test an IDS model against an attacker in who are currently in the field of GAN or IDS research,
real-time,usingacontrolledenvironment.Thisoffersplenty aseitherarefresheroranintroductiontothetopicarea.
of scenarios for improving the performance of IDS models,
andespeciallytrainingthemtoreactappropriatelytounseen FUNDING
examples. Working on a pair of ML models as in [91] The authors would like to thank the Ministry of Business,
providesafullyfunctionalscenarioinwhichtheresearchers Innovation,andEmployment(MBIE)fromtheNewZealand
canviewthefullperformanceoftheirmodel. Governmenttosupportourworkwiththegrant(MAUX1912)
Overall, the opportunities created by technologies like whichmadeitpossibleforustoconducttheresearch.
autonomous vehicles rising to the forefront of public
consciousness provide future research directions for those REFERENCES
looking at the applications of GAN models in securing
[1] I. Goodfellow, J. Pouget-Abadie, M. Mirza, B. Xu, D. Warde-Farley,
network IDS schemes for future technologies. Work done S.Ozair,A.Courville,andY.Bengio,‘‘Generativeadversarialnets,’’in
on the vulnerabilities of autonomous vehicles, like that Proc.Adv.NeuralInf.Process.Syst.,vol.27,2014,pp.1–14.
[2] D.P.KingmaandM.Welling,‘‘Auto-encodingvariationalBayes,’’2013,
done by Keen Labs (see VII-F) or the examination of
arXiv:1312.6114.
vulnerabilities in BMW’s more recent autonomous vehicle [3] R.Maruzani,‘‘AreyouunwittinglyhelpingtotrainGoogle’sAImodels?
offerings (see [126]) shows the importance and urgency of HowGoogleisusingyourreCAPTCHAentriestotrainmachinelearning
models,’’Medium,‘TowardsDataSci.’,Tech.Rep.,Jan.2021.
research in this area. The prevalence of GAN models for
[4] C.Daly,‘‘‘I’mnotarobot’:Google’santi-robotreCAPTCHAtrainstheir
semanticimageeditingsuggeststhatthereisapossibilityof robotstosee,’’AIBus.,Tech.Rep.,2017.
utilizingGANmodelstoeditexistingdataandperhapscreate [5] A. Aggarwal, M. Mittal, and G. Battineni, ‘‘Generative adversarial
network:Anoverviewoftheoryandapplications,’’Int.J.Inf.Manage.
new attack files using benign traffic. There are significant
DataInsights,vol.1,no.1,Apr.2021,Art.no.100004.
possibilitiesforutilizingthehigh-levelsemanticinformation
[6] K.Wang,C.Gou,Y.Duan,Y.Lin,X.Zheng,andF.-Y.Wang,‘‘Generative
that GANs are capable of capturing in their latent space in adversarialnetworks:Introductionandoutlook,’’IEEE/CAAJ.Autom.
order to edit existing data and create new datasets. There Sinica,vol.4,no.4,pp.588–598,Sep.2017.
[7] M.MirzaandS.Osindero,‘‘Conditionalgenerativeadversarialnets,’’
are many areas of Network IDS research in GANs that are
2014,arXiv:1411.1784.
still developing apace, such as the rapidly expanding world [8] H.-J.Liao,C.-H.R.Lin,Y.-C.Lin,andK.-Y.Tung,‘‘Intrusiondetection
of IoT devices, which offer opportunities for researchers to system:Acomprehensivereview,’’J.Netw.Comput.Appl.,vol.36,no.1,
pp.16–24,2013.
exploretheusesofthesemachinelearningmodels.Research
[9] S. Smaha, ‘‘Haystack: An intrusion detection system,’’ in Proc. 4th
in Generative Adversarial Networks has exploded in recent Aerosp.Comput.Secur.Appl.,Dec.1988,pp.37–44.
years, as researchers have uncovered the many potential [10] B. Mukherjee, L. T. Heberlein, and K. N. Levitt, ‘‘Network intrusion
detection,’’IEEENetw.,vol.8,no.3,pp.26–41,May1994.
applicationsinnumerousfields.
[11] A. Thakkar and R. Lohiya, ‘‘A survey on intrusion detection system:
Therealmsofcybersecurityandintrusiondetectioncontain Featureselection,model,performancemeasures,applicationperspective,
many possible avenues for research when it comes to GAN challenges,andfutureresearchdirections,’’Artif.Intell.Rev.,vol.55,
algorithms, as has been illustrated in this paper. Our aim is no.1,pp.453–563,Jan.2022.
[12] M.AlkasassbehandS.A.-H.Baddar,‘‘Intrusiondetectionsystems:A
tohaveprovidedanexplanationofnotonlywhatGenerative
state-of-the-arttaxonomyandsurvey,’’ArabianJ.Sci.Eng.,pp.1–44,
Adversarial Networks are and how they are trained and Nov.2022,doi:10.1007/s13369-022-07412-1.
assessed, but also to have given an effective grounding in [13] A.Arora,‘‘AreviewonapplicationofGANsincybersecuritydomain,’’
IETETech.Rev.,vol.39,no.2,pp.433–441,Mar.2022.
theapplicationswithinintrusiondetectionwhichGANsmay
[14] I. K. Dutta, B. Ghosh, A. Carlson, M. Totaro, and M. Bayoumi,
workwith,bothinthecurrentliteratureandinanypotential ‘‘Generativeadversarialnetworksinsecurity:Asurvey,’’inProc.11th
futureresearch. IEEE Annu. Ubiquitous Comput., Electron. Mobile Commun. Conf.
(UEMCON),Oct.2020,pp.0399–0405.
[15] Z. Cai, Z. Xiong, H. Xu, P. Wang, W. Li, and Y. Pan, ‘‘Generative
X. CONCLUSION adversarialnetworks:Asurveytowardprivateandsecureapplications,’’
This paper explores the use of Generative Adversarial ACMComput.Surv.,vol.54,no.6,pp.1–38,Jul.2022.
[16] S.BalujaandI.Fischer,‘‘Adversarialtransformationnetworks:Learning
NetworksinresearchrelatingtoIntrusionDetectionSystems,
togenerateadversarialexamples,’’2017,arXiv:1703.09387.
andthepotentialforoptimizationtherein.Wehaveexplored
[17] Y.GaoandY.Pan,‘‘Improveddetectionofadversarialimagesusingdeep
the current models in favor of IDS research; the current neuralnetworks,’’2020,arXiv:2007.05573.
research into wired, wireless, mobile, IoT, sensor network, [18] B.Hitaj,G.Ateniese,andF.Perez-Cruz,‘‘DeepmodelsundertheGAN:
Informationleakagefromcollaborativedeeplearning,’’inProc.ACM
and autonomous vehicle systems; discussed where this
SIGSACConf.Comput.Commun.Secur.,Oct.2017,pp.603–618.
research is currently leading; and provided a detailed look [19] Z. Zhao, D. Dua, and S. Singh, ‘‘Generating natural adversarial
at the state-of-the-art as it is in GANs for Network IDS examples,’’2017,arXiv:1710.11342.
[20] X. Chen, P. Kairouz, and R. Rajagopal, ‘‘Understanding compressive
models. This overview of the area explores the ways in
adversarial privacy,’’ in Proc. IEEE Conf. Decis. Control (CDC),
which researchers arecurrently using GANs to improvethe Dec.2018,pp.6824–6831.
VOLUME11,2023 76091

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
[21] C.Huang,P.Kairouz,X.Chen,L.Sankar,andR.Rajagopal,‘‘Context- [46] A.O.Almashhadani,M.Kaiiali,D.Carlin,andS.Sezer,‘‘MaldomDetec-
awaregenerativeadversarialprivacy,’’Entropy,vol.19,no.12,p.656, tor:Asystemfordetectingalgorithmicallygenerateddomainnameswith
Dec.2017. machinelearning,’’Comput.Secur.,vol.93,Jun.2020,Art.no.101787.
[22] S. Liu, A. Shrivastava, J. Du, and L. Zhong, ‘‘Better accuracy with [47] R. Mutalik, D. Chheda, Z. Shaikh, and D. Toradmalle, ‘‘RockYou,’’
quantifiedprivacy:Representationslearnedviareconstructiveadversarial Dataset,SkullSecur.,Rapid7,2010.
network,’’2019,arXiv:1901.08730. [48] B.Hitaj,P.Gasti,G.Ateniese,andF.Perez-Cruz,‘‘PassGAN:Adeep
[23] A. Tripathy, Y. Wang, and P. Ishwar, ‘‘Privacy-preserving adversarial learningapproachforpasswordguessing,’’2017,arXiv:1709.00440.
networks,’’ in Proc. 57th Annu. Allerton Conf. Commun., Control, [49] D. Biesner, K. Cvejoski, B. Georgiev, R. Sifa, and E. Krupicka,
Comput.(Allerton),Sep.2019,pp.495–505. ‘‘Generativedeeplearningtechniquesforpasswordgeneration,’’2020,
[24] K. Alrawashdeh and S. Goldsmith, ‘‘Defending deep learning based arXiv:2012.05685.
anomalydetectionsystemsagainstwhite-boxadversarialexamplesand [50] G.CreechandJ.Hu,‘‘GenerationofanewIDStestdataset:Timeto
backdoor attacks,’’ in Proc. IEEE Int. Symp. Technol. Soc. (ISTAS), retiretheKDDcollection,’’inProc.IEEEWirelessCommun.Netw.Conf.
Nov.2020,pp.294–301. (WCNC),Apr.2013,pp.4487–4492.
[25] M. Fredrikson, E. Lantz, S. Jha, S. Lin, D. Page, and T. Ristenpart, [51] G.CreechandJ.Hu,‘‘Asemanticapproachtohost-basedintrusiondetec-
‘‘Privacyinpharmacogenetics:Anend-to-endcasestudyofpersonalized tionsystemsusingcontiguousanddiscontiguoussystemcallpatterns,’’
warfarindosing,’’inProc.23rdUSENIXSecur.Symp.(USENIXSecur.), IEEETrans.Comput.,vol.63,no.4,pp.807–819,Apr.2014.
2014,pp.17–32. [52] G. Creech, ‘‘Developing a high-accuracy cross platform host-based
[26] T. Salimans, I. Goodfellow, W. Zaremba, V. Cheung, A. Radford, intrusiondetectionsystemcapableofreliablydetectingzero-dayattacks,’’
and X. Chen, ‘‘Improved techniques for training GANs,’’ 2016, Ph.D.thesis,SchoolEng.Inf.Technol.,UNSWSydney,Sydney,NSW,
arXiv:1606.03498. Australia,2014.
[27] P.Salehi,A.Chalechale,andM.Taghizadeh,‘‘Generativeadversarial [53] T. Mouttaqi, T. Rachidi, and N. Assem, ‘‘Re-evaluation of combined
networks(GANs):Anoverviewoftheoreticalmodel,evaluationmetrics, Markov-bayesmodelsforhostintrusiondetectionontheADFAdataset,’’
andrecentdevelopments,’’2020,arXiv:2005.13178. inProc.Intell.Syst.Conf.(IntelliSys),Sep.2017,pp.1044–1052.
[28] C.Szegedy,V.Vanhoucke,S.Ioffe,J.Shlens,andZ.Wojna,‘‘Rethinking [54] R.A.KhamisandA.Matrawy,‘‘Evaluationofadversarialtrainingon
the inception architecture for computer vision,’’ in Proc. IEEE Conf. differenttypesofneuralnetworksindeeplearning-basedIDSs,’’inProc.
Comput.Vis.PatternRecognit.(CVPR),Jun.2016,pp.2818–2826. Int.Symp.Netw.,Comput.Commun.(ISNCC),Oct.2020,pp.1–6.
[29] A. Borji, ‘‘Pros and cons of GAN evaluation measures,’’ 2018, [55] Z. Zoghi and G. Serpen, ‘‘UNSW-NB15 computer security dataset:
arXiv:1802.03446. Analysisthroughvisualization,’’2021,arXiv:2101.05067.
[30] T.Che,Y.Li,A.P.Jacob,Y.Bengio,andW.Li,‘‘Moderegularized [56] N. Moustafa and J. Slay, ‘‘UNSW-NB15: A comprehensive data set
generativeadversarialnetworks,’’2017, arXiv:1612.02136. for network intrusion detection systems (UNSW-NB15 network data
[31] KDD Cup 1999 Data, Dataset, Canadian Univ. Cybersecur., Univ. set),’’ in Proc. Mil. Commun. Inf. Syst. Conf. (MilCIS), Nov. 2015,
NewBrunswick,1999. pp.1–6.
[32] M.Tavallaee,E.Bagheri,W.Lu,andA.A.Ghorbani,‘‘Adetailedanalysis [57] R.Durall,A.Chatzimichailidis,P.Labus,andJ.Keuper,‘‘Combating
oftheKDDCUP99dataset,’’inProc.IEEESymp.Comput.Intell.Secur. mode collapse in GAN training: An empirical analysis using Hessian
DefenseAppl.,Jul.2009,pp.1–6. eigenvalues,’’2020,arXiv:2012.09673.
[33] NSL-KDDDataset,CanadianInst.Cybersecur.|Univ.NewBrunswick, [58] H.Thanh-TungandT.Tran,‘‘Catastrophicforgettingandmodecollapse
Fredericton,NB,Canada,2009. inGANs,’’inProc.Int.JointConf.NeuralNetw.(IJCNN),Jul.2020,
[34] M.S.HaroonandH.M.Ali,‘‘Adversarialtrainingagainstadversarial pp.1–10.
attacksformachinelearning-basedintrusiondetectionsystems,’’Com- [59] A.Seff,A.Beatson,D.Suo,andH.Liu,‘‘Continuallearningingenerative
put.,Mater.Continua,vol.73,no.2,pp.3513–3527,2022. adversarialnets,’’2017,arXiv:1705.08395.
[35] D.Stiawan,M.Y.B.Idris,A.M.Bamhdi,andR.Budiarto,‘‘CICIDS- [60] J.Gauthier,‘‘Conditionalgenerativeadversarialnetsforconvolutional
2017 dataset feature analysis with information gain for anomaly face generation,’’ in Class Project for Stanford CS231N: Convo-
detection,’’IEEEAccess,vol.8,pp.132911–132921,2020. lutional Neural Networks for Visual Recognition, Winter Semester,
[36] S. S. Gopalan, D. Ravikumar, D. Linekar, A. Raza, and M. Hasib, vol. 2014, no. 5. San Francisco, CA, USA: Stanford Univ., 2014,
‘‘BalancingapproachestowardsMLforIDS:AsurveyfortheCSE-CIC p.2.
IDSdataset,’’inProc.Int.Conf.Commun.,SignalProcess.,TheirAppl. [61] A. Radford, L. Metz, and S. Chintala, ‘‘Unsupervised representation
(ICCSPA),Mar.2021,pp.1–6. learningwithdeepconvolutionalgenerativeadversarialnetworks,’’2015,
[37] Darpa Intrusion Detection Evaluation Dataset, Machine Learning in arXiv:1511.06434.
Laboratory,Cambridge,MA,USA,1999. [62] J.T.Springenberg,A.Dosovitskiy,T.Brox,andM.Riedmiller,‘‘Striving
[38] R.Robert,E.Marcin,A.Guillem,andS.Thomas,‘‘DARPAdataset| forsimplicity:Theallconvolutionalnet,’’2014,arXiv:1412.6806.
paperswithcode,’’Medium,‘TowardsDataSci.’,Tech.Rep.,Aug.2022. [63] A.Mordvintsev,C.Olah,andM.Tyka,‘‘Inceptionism:Goingdeeperinto
[39] M.M.Anjum,S.Iqbal,andB.Hamelin,‘‘Analyzingtheusefulnessofthe neuralnetworks,’’GoogleRes.Labs,Tech.Rep.,2015.
DARPAOpTCdatasetincyberthreatdetectionresearch,’’inProc.26th [64] S. Ioffe and C. Szegedy, ‘‘Batch normalization: Accelerating deep
ACMSymp.AccessControlModelsTechnol.,Jun.2021,pp.27–32. networktrainingbyreducinginternalcovariateshift,’’inProc.Int.Conf.
[40] O.YavanogluandM.Aydos,‘‘Areviewoncybersecuritydatasetsfor Mach.Learn.,2015,pp.448–456.
machinelearningalgorithms,’’inProc.IEEEInt.Conf.BigData(Big [65] M.Arjovsky,S.Chintala,andL.Bottou,‘‘Wassersteingenerativeadver-
Data),Dec.2017,pp.2186–2193. sarialnetworks,’’inProc.Int.Conf.Mach.Learn.,2017,pp.214–223.
[41] J.Velasco-Mata,V.González-Castro,E.F.Fernández,andE.Alegre, [66] R.Chauhan,U.Sabeel,A.Izaddoost,andS.S.Heydari,‘‘Polymorphic
‘‘Efficientdetectionofbotnettrafficbyfeaturesselectionanddecision adversarialcyberattacksusingWGAN,’’J.CybersecurityPrivacy,vol.1,
trees,’’IEEEAccess,vol.9,pp.120567–120579,2021. no.4,pp.767–792,Dec.2021.
[42] S.Chowdhury,M.Khanzadeh,R.Akula,F.Zhang,S.Zhang,H.Medal, [67] J.Donahue,P.Krähenbühl,andT.Darrell,‘‘Adversarialfeaturelearning,’’
M.Marufuzzaman,andL.Bian,‘‘Botnetdetectionusinggraph-based inProc.5thInt.Conf.Learn.Represent.,2017,pp.1–18.
featureclustering,’’J.BigData,vol.4,no.1,p.14,Dec.2017. [68] Q.YangandX.Li,‘‘BiGAN:LncRNA-diseaseassociationprediction
[43] A. Bansal and S. Mahapatra, ‘‘A comparative analysis of machine based on bidirectional generative adversarial network,’’ BMC Bioinf.,
learningtechniquesforbotnetdetection,’’inProc.10thInt.Conf.Secur. vol.22,no.1,p.357,Dec.2021.
Inf.Netw.,Oct.2017,pp.91–98. [69] W.Xu,J.Jang-Jaccard,T.Liu,andF.Sabrina,‘‘Trainingabidirectional
[44] D. Plohmann, ‘‘DGArchive A deep dive into domain generating GAN-basedone-classclassifierfornetworkintrusiondetection,’’2022,
malware,’’FraunhoferFKIE,Tech.Rep.,Dec.2015.[Online].Available: arXiv:2202.01332.
https://dgarchive.caad.fkie.fraunhofer.de/ [70] G.Renjith,S.Laudanna,S.Aji,C.Visaggio,andP.Vinod,‘‘GANG-
[45] C.Choudhary,R.Sivaguru,M.Pereira,B.Yu,A.C.Nascimento,and MAM:GANbasedenGineformodifyingAndroidmalware,’’SoftwareX,
M.DeCock,‘‘Algorithmicallygenerateddomaindetectionandmalware vol.18,Jun.2022,Art.no.100977.
familyclassification,’’inSecurityinComputingandCommunications: [71] H.Rafiq,N.Aslam,B.Issac,andR.H.Randhawa,‘‘Aninvestigationon
6thInternationalSymposium,SSCC2018,Bangalore,India,September fragilityofmachinelearningclassifiersinAndroidmalwaredetection,’’in
19–22, 2018, Revised Selected Papers 6. Singapore: Springer, 2019, Proc.IEEEINFOCOMConf.Comput.Commun.Workshops(INFOCOM
pp.640–655. WKSHPS),May2022,pp.1–6.
76092 VOLUME11,2023

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
[72] M.M.Zhu,S.Gong,Z.Qian,andL.Zhang,‘‘Abriefreviewoncycle [97] X. Peng, H. Xian, Q. Lu, and X. Lu, ‘‘Semantics aware adversarial
generative adversarial networks,’’ in Proc. 7th Int. Conf. Intell. Syst. malwareexamplesgenerationforblack-boxattacks,’’Appl.SoftComput.,
ImageProcess.,2019,pp.235–242. vol.109,Sep.2021,Art.no.107506.
[73] Y.Chen,Y.Pan,T.Yao,X.Tian,andT.Mei,‘‘Mocycle-GAN:Unpaired [98] V.S.BhaskaraandD.Bhattacharyya,‘‘Emulatingmalwareauthorsfor
video-to-videotranslation,’’inProc.27thACMInt.Conf.Multimedia, proactiveprotectionusingGANsoveradistributedimagevisualization
Oct.2019,pp.647–655. ofdynamicfilebehavior,’’2018,arXiv:1807.07525.
[74] A.Odena,C.Olah,andJ.Shlens,‘‘Conditionalimagesynthesiswith [99] W.L.TanandT.Truong-Huu,‘‘Enhancingrobustnessofmalwaredetec-
auxiliaryclassifierGANs,’’2016,arXiv:1610.09585. tion using synthetically-adversarial samples,’’ in Proc. GLOBECOM
[75] R. Nagaraju and M. Stamp, ‘‘Auxiliary-classifier GAN for malware IEEEGlobalCommun.Conf.,Dec.2020,pp.1–6.
analysis,’’2021,arXiv:2107.01620. [100] V. Dumoulin, I. Belghazi, B. Poole, O. Mastropietro, A. Lamb,
[76] S.Kausar,B.Tahir,andM.A.Mehmood,‘‘HashCat:Anovelapproach M.Arjovsky,andA.Courville,‘‘Adversariallylearnedinference,’’2016,
forthetopicclassificationofmultilingualTwittertrends,’’inProc.Int. arXiv:1606.00704.
Conf.FrontiersInf.Technol.(FIT),Dec.2021,pp.212–217. [101] J.-T. Wang and C.-H. Wang, ‘‘High performance WGAN-GP based
[77] R.Hranický,L.Zobal,O.Ryšavý,andD.Koláš,‘‘Distributedpassword multiple-categorynetworkanomalyclassificationsystem,’’inProc.Int.
crackingwithBOINCandhashcat,’’Digit.Invest.,vol.30,pp.161–172, Conf.CyberSecur.Emerg.Technol.(CSET),Oct.2019,pp.1–7.
Sep.2019. [102] Q. Yan, M. Wang, W. Huang, X. Luo, and F. R. Yu, ‘‘Automat-
[78] L.Yan,W.Zheng,C.Gou,andF.-Y.Wang,‘‘IsGAN:Identity-sensitive ically synthesizing DoS attack traces using generative adversarial
generativeadversarialnetworkforfacephoto-sketchsynthesis,’’Pattern networks,’’Int.J.Mach.Learn.Cybern.,vol.10,no.12,pp.3387–3396,
Recognit.,vol.119,Nov.2021,Art.no.108077. Dec.2019.
[79] D.Berthelot,T.Schumm,andL.Metz,‘‘BEGAN:Boundaryequilibrium [103] C.Park,J.Lee,Y.Kim,J.-G.Park,H.Kim,andD.Hong,‘‘Anenhanced
generativeadversarialnetworks,’’2017,arXiv:1703.10717. AI-basednetworkintrusiondetectionsystemusinggenerativeadversarial
[80] H. Gao, J. Pei, and H. Huang, ‘‘ProGAN: Network embedding via networks,’’ IEEE Internet Things J., vol. 10, no. 3, pp.2330–2345,
proximitygenerativeadversarialnetwork,’’inProc.25thACMSIGKDD Feb.2023.
Int.Conf.Knowl.DiscoveryDataMining,Jul.2019,pp.1308–1316. [104] J.LeeandK.Park,‘‘GAN-basedimbalanceddataintrusiondetection
[81] A. Karnewar and O. Wang, ‘‘MSG-GAN: Multi-scale gradients for system,’’ Pers. Ubiquitous Comput., vol. 25, no. 1, pp.121–128,
generativeadversarialnetworks,’’inProc.IEEE/CVFConf.Comput.Vis. Feb.2021.
PatternRecognit.(CVPR),Jun.2020,pp.7796–7805. [105] Z. Wang, P. Wang, X. Zhou, S. Li, and M. Zhang, ‘‘FLOWGAN:
[82] H. Zhang, I. Goodfellow, D. Metaxas, and A. Odena, ‘‘Self-attention Unbalanced network encrypted traffic identification method based
generativeadversarialnetworks,’’2018,arXiv:1805.08318. on GAN,’’ in Proc. IEEE Int. Conf Parallel Distrib. Process. With
[83] Y. Chen, Q. Gao, and X. Wang, ‘‘Inferential Wasserstein generative Appl., Big Data Cloud Comput., Sustain. Comput. Commun., Social
adversarialnetworks,’’J.Roy.Stat.Soc.Ser.B,Stat.Methodol.,vol.84, Comput. Netw. (ISPA/BDCloud/SocialCom/SustainCom), Dec. 2019,
no.1,pp.83–113,Feb.2022. pp.975–983.
[84] X.Chen,Y.Duan,R.Houthooft,J.Schulman,I.Sutskever,andP.Abbeel, [106] G.Draper-Gil,A.H.Lashkari,M.S.I.Mamun,andA.A.Ghorbani,
‘‘InfoGAN:Interpretablerepresentationlearningbyinformationmaxi- ‘‘Characterization of encrypted and VPN traffic using time-related
mizinggenerativeadversarialnets,’’2016,arXiv:1606.03657. features,’’ in Proc. 2nd Int. Conf. Inf. Syst. Secur. Privacy, 2016,
[85] L.Yu,W.Zhang,J.Wang,andY.Yu,‘‘SeqGAN:Sequencegenerative pp.407–414.
adversarialnetswithpolicygradient,’’2016,arXiv:1609.05473. [107] J. Lee and K. Park, ‘‘AE-CGAN model based high performance
[86] Y.Chen,Y.Xiong,B.Liu,andX.Yin,‘‘TranGAN:Generativeadversarial networkintrusiondetectionsystem,’’Appl.Sci.,vol.9,no.20,p.4221,
networkbasedtransferlearningforsocialtieprediction,’’inProc.IEEE Oct.2019.
Int.Conf.Commun.(ICC),May2019,pp.1–6. [108] S.Zhao,J.Li,J.Wang,Z.Zhang,L.Zhu,andY.Zhang,‘‘AttackGAN:
[87] M.Garuba,C.Liu,andD.Fraites,‘‘Intrusiontechniques:Comparative Adversarial attack against black-box IDS using generative adversarial
studyofnetworkintrusiondetectionsystems,’’inProc.5thInt.Conf.Inf. networks,’’Proc.Comput.Sci.,vol.187,pp.128–133,Jan.2021.
Technol.,NewGenerat.(itng),Apr.2008,pp.592–598. [109] A. Ferdowsi and W. Saad, ‘‘Generative adversarial networks for
[88] W. Xu, J. Jang-Jaccard, T. Liu, F. Sabrina, and J. Kwak, ‘‘Improved distributedintrusiondetectionintheInternetofThings,’’inProc.IEEE
bidirectional GAN-based approach for network intrusion detection GlobalCommun.Conf.(GLOBECOM),Dec.2019,pp.1–6.
using one-class classifier,’’ Computers, vol. 11, no. 6, p.85, [110] N.Abdalgawad,A.Sajun,Y.Kaddoura,I.A.Zualkernan,andF.Aloul,
May2022. ‘‘GenerativedeeplearningtodetectcyberattacksfortheIoT-23dataset,’’
[89] J.Yang,T.Li,G.Liang,W.He,andY.Zhao,‘‘Asimplerecurrentunit IEEEAccess,vol.10,pp.6430–6441,2022.
modelbasedintrusiondetectionsystemwithDCGAN,’’IEEEAccess, [111] S.Garcia,A.Parmisano,andM.J.Erquiaga,IoT-23:ALabeledDataset
vol.7,pp.83286–83296,2019. WithMaliciousandBenignIoTNetworkTraffic.Honolulu,HI,USA:
[90] S. P. Kulyadi, P. Mohandas, S. K. S. Kumar, M. J. S. Raman, and Zenodo,2020.
V.S.Vasan,‘‘Anomalydetectionusinggenerativeadversarialnetworks [112] M. Antonakakis, T. April, M. Bailey, M. Bernhard, E. Bursztein,
onfirewalllogmessagedata,’’inProc.13thInt.Conf.Electron.,Comput. J. Cochran, Z. Durumeric, J. A. Halderman, L. Invernizzi, and
Artif.Intell.(ECAI),Jul.2021,pp.1–6. M.Kallitsis,‘‘UnderstandingtheMiraibotnet,’’inProc.26th{USENIX}
[91] M. Usama, M. Asim, S. Latif, and J. Qadir, ‘‘Generative adversarial Secur.Symp.({USENIX}Secur.),2017,pp.1093–1110.
networks for launching and thwarting adversarial attacks on network [113] T.Zixu,K.S.K.Liyanage,andM.Gurusamy,‘‘Generativeadversarial
intrusiondetectionsystems,’’inProc.15thInt.WirelessCommun.Mobile network and auto encoder based anomaly detection in distributed
Comput.Conf.(IWCMC),Jun.2019,pp.78–83. IoT networks,’’ in Proc. GLOBECOM IEEE Global Commun. Conf.,
[92] C.Choi,S.Shin,andI.Lee,‘‘Opcodesequenceamplifierusingsequence Dec.2020,pp.1–7.
generative adversarial networks,’’ in Proc. Int. Conf. Inf. Commun. [114] N. Koroniotis, N. Moustafa, E. Sitnikova, and B. Turnbull, ‘‘Towards
Technol.Converg.(ICTC),Oct.2019,pp.968–970. thedevelopmentofrealisticbotnetdatasetintheInternetofThingsfor
[93] Y.Liu,J.Li,B.Liu,X.Gao,andX.Liu,‘‘Malwareidentificationmethod networkforensicanalytics:Bot-IoTdataset,’’2018,arXiv:1811.00701.
basedonimageanalysis,’’inProc.11thInt.Conf.Inf.Technol.Med. [115] N. Leavitt, ‘‘Mobile security: Finally a serious problem?’’ Computer,
Educ.(ITME),Nov.2021,pp.157–161. vol.44,no.6,pp.11–14,Jun.2011.
[94] S.Wang,Q.Wang,Z.Jiang,X.Wang,andR.Jing,‘‘Aweakcoupling [116] S.Wei,P.Jiang,Q.Yuan,andJ.Wang,‘‘Mobileapplicationnetwork
of semi-supervised learning with generative adversarial networks for behaviordetectionandevaluationwithWGANandbi-LSTM,’’inProc.
malware classification,’’ in Proc. 25th Int. Conf. Pattern Recognit. TENCONIEEERegionConf.,Oct.2018,pp.44–49.
(ICPR),Jan.2021,pp.3775–3782. [117] C. Zhang, P. Patras, and H. Haddadi, ‘‘Deep learning in mobile and
[95] C.Forensics,‘‘VirusShare–becausesharingiscaring,’’DatabaseReposi- wirelessnetworking:Asurvey,’’2018,arXiv:1803.04311.
tory,CorvusForensics,NewYork,NY,USA,Tech.Rep. [118] C. Zhang, X. Ouyang, and P. Patras, ‘‘ZipNet-GAN: Inferring fine-
[96] R. Ronen, M. Radu, C. Feuerstein, E. Yom-Tov, and M. Ahmadi, grained mobile traffic patterns via a generative adversarial neural
‘‘Microsoft malware classification challenge (BIG 2015),’’ Feb. 2018, network,’’inProc.13thInt.Conf.Emerg.Netw.Exp.Technol.,Nov.2017,
arXiv:1802.10135. pp.363–375.
VOLUME11,2023 76093

A.Dunmoreetal.:ComprehensiveSurveyofGANsinCybersecurityIntrusionDetection
[119] S. M. W. Umba, A. M. Abu-Mahfouz, T. D. Ramotsoela, and [144] J. Song, H. Takakura, and Y. Okabe, ‘‘Description of Kyoto Uni-
G.P.Hancke, ‘‘A review of artificial intelligence based intrusion versity benchmark data,’’ 2006. [Online]. Available: http://www.
detectionforsoftware-definedwirelesssensornetworks,’’inProc.IEEE takakura.com/Kyoto_data/BenchmarkData-Description-v5.pdf
28thInt.Symp.Ind.Electron.(ISIE),Jun.2019,pp.1277–1282. [145] L.Sixt,B.Wild,andT.Landgraf,‘‘RenderGAN:Generatingrealistic
[120] P.R.Grammatikis,P.Sarigiannidis,G.Efstathopoulos,andE.Panaousis, labeleddata,’’FrontiersRobot.AI,vol.5,p.66,Jun.2018.
‘‘ARIES:Anovelmultivariateintrusiondetectionsystemforsmartgrid,’’ [146] E. Zhu, J. Zhang, J. Yan, K. Chen, and C. Gao, ‘‘N-gram MalGAN:
Sensors,vol.20,no.18,p.5305,Sep.2020. Evadingmachinelearningdetectionviafeaturen-gram,’’Digit.Commun.
[121] M.Rudner,‘‘Cyber-threatstocriticalnationalinfrastructure:Anintelli- Netw.,vol.8,no.4,pp.485–491,Aug.2022.
gencechallenge,’’Int.J.Intell.CounterIntell.,vol.26,no.3,pp.453–481, [147] X. Li, K. Kong, S. Xu, P. Qin, and D. He, ‘‘Feature selection-based
Sep.2013. Androidmalwareadversarialsamplegenerationanddetectionmethod,’’
[122] I.Sharafaldin,A.H.Lashkari,andA.A.Ghorbani,‘‘Towardgenerating IETInf.Secur.,vol.15,no.6,pp.401–416,Nov.2021.
anewintrusiondetectiondatasetandintrusiontrafficcharacterization,’’
inProc.4thInt.Conf.Inf.Syst.Secur.Privacy,2018,pp.108–116.
[123] A.Greenberg,‘‘HackersremotelykillaJeeponthehighway—Withme
AERYNDUNMORE(GraduateStudentMember,
init,’’WIRED,Jul.21,2015.
IEEE)receivedthemaster’sdegreeincomputing
[124] D.Shepardson,‘‘Fiatchryslerwillrecallvehiclesoverhackingworries,’’
and information sciences from the Auckland
Reuters,2015.
UniversityofTechnology,in2017.Sheiscurrently
[125] K.Kim,J.S.Kim,S.Jeong,J.-H.Park,andH.K.Kim,‘‘Cybersecurityfor
pursuingthePh.D.degree.HerPh.D.dissertation
autonomousvehicles:Reviewofattacksanddefense,’’Comput.Secur.,
was on creating alternative encryption systems,
vol.103,Apr.2021,Art.no.102150.
titled‘‘UsingGraphicBasedSystemstoImprove
[126] Z.Cai,A.Wang,W.Zhang,M.Gruffke,andH.Schweppe,‘‘0-Days
&mitigations:RoadwaystoexploitandsecureconnectedBMWcars,’’ Cryptographic Algorithms.’’ She is a Research
BlackHatUSA,vol.2019,p.39,Aug.2019. AssistantwithMasseyUniversity.Shespecializes
[127] E. Seo, H. M. Song, and H. K. Kim, ‘‘GIDS: GAN based intrusion inneuralnetworksforcybersecurityandencryp-
detection system for in-vehicle network,’’ in Proc. 16th Annu. Conf. tion designs. She has studied at the University of Auckland and Oxford
Privacy,Secur.Trust(PST),Aug.2018,pp.1–6. University.
[128] H. Sedjelmaci, ‘‘Attacks detection and decision framework based
on generative adversarial network approach: Case of vehicular edge
computing network,’’ Trans. Emerg. Telecommun. Technol., vol. 33, JULIANJANG-JACCARDreceivedtheM.Sc.and
no.10,Oct.2022,Art.no.e4073. Ph.D. degrees from the University of Sydney,
[129] C.SmutzandA.Stavrou,‘‘MaliciousPDFdetectionusingmetadataand Australia.SheiscurrentlyanAssociateProfessor
structural features,’’ in Proc. 28th Annu. Comput. Secur. Appl. Conf., and the Head of the Cybersecurity Laboratory
Dec.2012,pp.239–248.
at Massey University, New Zealand. She has
[130] H.Bae,Y.Lee,Y.Kim,U.Hwang,S.Yoon,andY.Paek,‘‘Learn2Evade:
published more than 70 papers in leading con-
Learning-basedgenerativemodelforevadingPDFmalwareclassifiers,’’
ferencesandjournalvenues,includingIEEEand
IEEETrans.Artif.Intell.,vol.2,no.4,pp.299–313,Aug.2021.
ACM. Her research interests include cyberse-
[131] X.Zhang,J.Wang,M.Sun,andY.Feng,‘‘AndrOpGAN:AnopcodeGAN
curity, intrusion detection, anomaly detection,
for Android malware obfuscations,’’ in Proc. Int. Conf. Mach. Learn.
artificial intelligence, data anonymization, and
CyberSecur.,vol.12486,2020,pp.12–25.
privacy-preservationtechniques.Shewasarecipientofmanymulti-million
[132] W.HuandY.Tan,‘‘Generatingadversarialmalwareexamplesforblack-
boxattacksbasedonGAN,’’2017,arXiv:1702.05983. dollar research awards both from Australian and New Zealand gov-
[133] A.Creswell,T.White,V.Dumoulin,K.Arulkumaran,B.Sengupta,and ernments/industries while collaborating with the top international ICT
A.A.Bharath,‘‘Generativeadversarialnetworks:Anoverview,’’IEEE companiesanduniversitiesaroundtheworld.
SignalProcess.Mag.,vol.35,no.1,pp.53–65,Jan.2018.
[134] Y.Choi,M.Choi,M.Kim,J.-W.Ha,S.Kim,andJ.Choo,‘‘StarGAN:
Unified generative adversarial networks for multi-domain image-to- FARIZASABRINA(Member,IEEE)receivedthe
imagetranslation,’’2017,arXiv:1711.09020. M.E.degree(byresearch)inelectricalandinfor-
[135] H. Zhang, T. Xu, H. Li, S. Zhang, X. Wang, X. Huang, and mationengineeringfromtheUniversityofSydney,
D.Metaxas,‘‘StackGAN:Texttophoto-realisticimagesynthesiswith Australia, and the Ph.D. degree in computer
stackedgenerativeadversarialnetworks,’’2016,arXiv:1612.03242. science and engineering from the University of
[136] A. Cherepkov, A. Voynov, and A. Babenko, ‘‘Navigating the GAN NewSouthWales,Australia.Shehasmanyyears
parameterspaceforsemanticimageediting,’’2020,arXiv:2011.13786. ofresearch,teaching,andindustrialexperiencein
[137] T.Karras,S.Laine,andT.Aila,‘‘Astyle-basedgeneratorarchitecture informationandcommunicationtechnologies.She
forgenerativeadversarialnetworks,’’IEEETrans.PatternAnal.Mach.
iscurrentlyaSeniorLecturerandtheDiscipline
Intell.,vol.43,no.12,pp.4217–4228,Dec.2021.
Lead of Network and Information Security with
[138] M.Amin,B.Shah,A.Sharif,T.Ali,K.-I.Kim,andS.Anwar,‘‘Android
theSchoolofEngineeringandTechnology,CentralQueenslandUniversity,
malware detection through generative adversarial networks,’’ Trans.
Australia.Hercurrentresearchinterestsincludenetworkingandinformation
Emerg.Telecommun.Technol.,vol.33,no.2,Feb.2022,Art.no.e3675.
security,theInternetofThings(IoT),cybersecurity,blockchain,andartificial
[139] R.ChauhanandS.S.Heydari,‘‘PolymorphicadversarialDDoSattackon
intelligence.Sheservesasatechnicalprogramcommitteememberofvarious
IDSusingGAN,’’inProc.Int.Symp.Netw.,Comput.Commun.(ISNCC),
conferences.SheisamemberofACMandACS.
Oct.2020,pp.1–6.
[140] Z.Fang,J.Wang,J.Geng,Y.Zhou,andX.Kan,‘‘A3CMal:Generating
adversarialsamplestoforcetargetedmisclassificationbyreinforcement
learning,’’Appl.SoftComput.,vol.109,Sep.2021,Art.no.107505. JIN KWAK is a Professor and the Head of the
[141] A. Odena, ‘‘Open questions about generative adversarial networks,’’ DepartmentofCybersecurityatAjouUniversity,
Distill,vol.4,no.4,p.e18,Apr.2019. RepublicofKorea.Hehasmorethan150publi-
[142] G.Mueller,B.Jensen,B.Valeriano,R.Maness,andJ.Macias,‘‘Cyber cations in leading journals and conferences. His
operationsduringtheRusso–Ukrainianwar,’’CenterforStrategicInt. current research interests include authentication,
Studies,Washington,DC,USA,2023. informationsecurityandprivacy,appliedcryptog-
[143] K. M. A. Alheeti and K. McDonald-Maier, ‘‘Intelligent intrusion raphy,wirelesssecurity,anddataencryption.
detection in external communication systems for autonomous
vehicles,’’ Syst. Sci. Control Eng., vol. 6, no. 1, pp.48–56,
Jan.2018.
76094 VOLUME11,2023
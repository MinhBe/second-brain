Received1December2025,accepted17December2025,dateofpublication22December2025,dateofcurrentversion2January2026.
DigitalObjectIdentifier10.1109/ACCESS.2025.3646769
Architectural Selection Framework for
Synthetic Network Traffic: Quantifying
the Fidelity-Utility Trade-off
DUREADANAMMARA1,JIANGUODING1(SeniorMember,IEEE),andKurtTutschku1 (Member,
IEEE)
1BlekingeInstituteofTechnology,Karlskrona,37179Sweden
Correspondingauthor:DureAdanAmmara(dure.adan.ammara@bth.se).
ThisworkwassupportedbyEuropeanCeltic+andSwedishVinnovaProjectthroughCISSAN–CollectiveIntelligenceSupportedby
SecurityAwareNodesunderGrantC2022/1-3.
ABSTRACT The fidelity and utility of synthetic network traffic are critically compromised by
architectural mismatch across heterogeneous network datasets and prevalent scalability failure. This
study addresses this challenge by establishing an Architectural Selection Framework that empirically
quantifieshowdatastructurecompatibilitydictatestheoptimalfidelity-utilitytrade-off.Wesystematically
evaluate twelve generative architectures (both non-AI and AI) across two distinct data structure types:
categorical-heavy NSL-KDD and continuous-flow-heavy CIC-IDS2017. Fidelity is rigorously assessed
through three structural metrics (Data Structure, Correlation, and Probability Distribution Difference)
to confirm structural realism before evaluating downstream utility. Our results, confirmed over twenty
independentruns(N =20),demonstratethatGAN-basedmodels(CTGAN,CopulaGAN)exhibitsuperior
architectural robustness, consistently achieving the optimal balance of statistical fidelity and practical
utility. Conversely, the framework exposes critical failure modes, i.e., statistical methods compromise
structural fidelity for utility (Compromised fidelity), and modern iterative architectures, such as Diffusion
Models, face prohibitive computational barriers, rendering them impractical for large-scale security
deployment.Thiscontributionprovidessecuritypractitionerswithanevidence-basedguideformitigating
architectural failures, thereby setting a benchmark for reliable and scalable synthetic data deployment in
adaptive security solutions.
INDEXTERMS SyntheticDataGeneration,GenerativeAdversarialNetworks(GANs),NSL-KDD,CIC-
IDS, Network Traffic Analysis, Fidelity, Utility, Generative AI
I. INTRODUCTION A. NEEDFORHIGH-FIDELITYNETWORKDATA
The increasing reliance on data-driven decision-making in Synthetic data generation has emerged as a promising solu-
networking and cybersecurity has intensified the need for tiontoovercomethechallengesmentionedabove.Itenables
high-quality network traffic data. This data plays a fun- the creation of realistic yet privacy-preserving network data
damental role in various applications, including intrusion that can supplement or replace real traffic for research and
detection,threatanalysis,andthetrainingofartificialintelli- testing. The primary challenge synthetic data must address
gence(AI)modelsforadaptivesecuritysolutions[1].How- is the imbalance issue: real-world traffic datasets are highly
ever, collecting and utilizing real-world network traffic data skewed, with benign flows vastly outnumbering malicious
remains a significant challenge due to privacy restrictions, ones. This imbalance biases AI models against rare but
limited availability, and the high cost of manual labeling critical attack classes [3]. Moreover, regulatory constraints
[2]. These barriers hinder the development and evaluation (e.g.,GDPR)andorganizationalconfidentialityfurtherlimit
of robust AI-based security systems. access to comprehensive network traces [4]. Hence, gener-
ating high-fidelity and balanced synthetic traffic is essential
forscalable,ethical,andreproduciblecybersecurityresearch
VOLUME11,2023 1
6202
raM
31
]RC.sc[
3v62361.0142:viXra

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
[5]. Despite this potential, generating high-quality synthetic the data. For instance, datasets like NSL-KDD [12] are
network traffic data remains a technically complex task. dominated by discrete and categorical features (e.g., flags
Existing methods struggle with three core issues: and protocols), while comparatively modern datasets like
CIC-IDS2017 [13] are characterized by continuous, high-
1) Ensuring Realism (Fidelity): replicating the complex
dimensional network flow metrics (e.g., bytes per second).
statistical and temporal dependencies of real network
In summary, the challenges of fidelity, utility, and computa-
traffic [6].
tional complexity can be traced back to a common underly-
2) Variability and Generalization (Utility): avoiding
ing issue of architectural mismatch. When the generative
mode collapse to produce diverse traffic variations
model’s design does not align with the data’s structure,
effective for AI training [7]–[9].
fidelity deteriorates, utility declines, and scalability fails.
3) Computational Complexity: managing the resource
This study directly addresses this problem by introducing
demands of state-of-the-art models like Generative
an architectural selection framework that quantifies and
Adversarial Networks (GANs) and diffusion models
mitigates these mismatches, thereby improving generative
[10].
performance and computational efficiency.
These challenges are not independent; they are funda-
mentally influenced by the underlying architecture of the
D. RESEARCHQUESTIONS
generativemodel.Inparticular,amodel’sabilitytomaintain
To address this critical gap, this study systematically evalu-
fidelity,achieveutility,andmanagecomputationalcomplex-
atesgenerativemodelsbasedontheirarchitecturalcompati-
ity depends on how well its architecture aligns with the
bilitywith varyingnetwork datastructures. Thesequestions
data’s intrinsic structure.
directly address the three core challenges of fidelity, utility,
and computational scalability identified earlier. The follow-
B. MOTIVATION ing research questions guide our investigation:
Despite significant advances in generative modeling, the 1) Which generative models produce synthetic network
motivation for this study stems from a critical gap between trafficdatathatisbothrealistic(fidelity)andusefulfor
model innovation and model applicability: the lack of ar- downstreamtaskssuchasanomalydetection(utility)?
chitectural understanding that connects generative design to 2) How do dataset characteristics (e.g., categori-
data structure. While these challenges are well recognized, cal/discrete features in NSL KDD vs. continuous-
most existing studies focus on improving individual gener- heavy flows in CIC-IDS2017) influence the compara-
ative models rather than understanding why specific archi- tive model performance?
tectures succeed or fail across different network data struc- 3) Whatarethecomputationaltrade-offsassociatedwith
tures.Networktrafficdataisinherentlyheterogeneous;some these methods, and how do these factors govern their
datasets(e.g.,NSL-KDD)aredominatedbycategoricalfea- suitability for real-world security deployment?
tures, while others (e.g., CIC-IDS2017) are continuous and
high-dimensional. Without systematic guidance on aligning E. CONTRIBUTIONS
model architectures to these varying data characteristics, ThisstudyintroducesanArchitecturalSelectionFramework
syntheticdatagenerationremainsinconsistentinqualityand for generating synthetic network traffic, which fundamen-
scalability. Therefore, there is a clear need for an evidence- tally advances model selection beyond traditional bench-
based framework that empirically links generative architec- marking. Our key contributions explicitly address the per-
ture design with data structure to guide model selection for vasive challenges of architectural mismatch and scalability
cybersecurityapplications.Thisisparticularlyimportantfor failure, confirming the scientific impact of our empirical
cybersecurity research, where data-driven detection systems findings:
rely on consistent and realistic traffic generation to ensure 1) We propose and validate an evidence-based frame-
the trustworthiness of model evaluation. work that demonstrates the optimal generative model
choice is rigorously dependent on the underlying
C. LACKOFANARCHITECTURALSELECTION dataset structure. This contribution provides a sys-
FRAMEWORK tematic, architecturally informed guide for mitigating
Whilevariousmethodsexistforgeneratingsynthetictraffic, generative failures in cybersecurity applications.
rangingfromnon-AItoAIapproaches[11],asignificantsci- 2) Our empirical analysis reveals that GAN-based ar-
entificlimitationremains,i.e.,thelackofanevidence-based chitectures (CTGAN, CopulaGAN) exhibit superior
architecturalselectionframework.Priorcomparativestudies statistical robustness (low variance from N = 20
have often treated network traffic data as a homogenous runs), consistently achieving the most stable fidelity-
entity, focusing on general performance without accounting utility balance across heterogeneous network data
for the deep differences in underlying data structure. This structures. This finding is a validated benchmark for
studyarguesthatthesuccessorfailureofagenerativemodel reliable synthetic data generation.
is fundamentally connected to the architectural compatibil- 3) We provide the rigorous quantification of the high
ity between the model and the specific characteristics of computationalbarrierfor DiffusionModelsandProb-
2 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
abilistic Graphical Models on high-volume, tabular [22])attempttolearnmarginalorjointdistributions,buttyp-
network data. This conclusion asserts that the current icallyrelyonparametricassumptions(e.g.,Gaussianity)and
architectural design of these models is fundamentally cannot capture high-dimensional, non-linear traffic depen-
impractical for large-scale security simulation and dencies. For example, survey evidence shows non-AI meth-
deployment. ods often produce synthetic datasets with correct marginal
4) We present a unified benchmarking of twelve repre- statisticsyetpoorfidelityintemporal/flowstructure[14].In
sentativesyntheticdatagenerationmethods,including thecybersecuritytrafficdomain,thislimitationmanifestsas
the implementation of Fidelity Gatekeeper Metrics syntheticdatasetsthatmaybebalancedbutleadtodegraded
(DS/Corr). This foundation establishes a reproducible performance in downstream tasks (e.g., intrusion detection)
baseline for advancing generative modeling in cyber- due to weak structural realism [23]. To summarize, these
securityandexplicitlyvalidatesthestructuralintegrity methods offer scalability and improved class balance (util-
of synthetic data. ity),buttradeofffidelity,andareseldomarchitecture-aware
relative to heterogeneous data structures [24].
Thesourcecodeforthisstudyispubliclyavailableathttps:
//github.com/AdenRajput/Comparative_Analysis.git.
B. DEEPGENERATIVEARCHITECTURES(AI-BASED):
PURSUINGFIDELITYANDUTILITY(WITHSCALABILITY
F. PAPERORGANIZATION
TRADE-OFFS)
Theremainderofthispaperisstructuredasfollows.Section
Deep generative models (VAEs, GANs, diffusion) aim to
II reviews existing literature and outlines the architectural
generate data that better mimics the real traffic distribution,
gaps in current synthetic data research. Section III de-
thereby improving fidelity, while offering potential utility
tails the experimental methodology and generative model
gains. Nevertheless, they differ in how they handle com-
implementation. Section IV defines the evaluation metrics
putational scalability, and relatively few specifically target
used for fidelity and utility analysis. Section V presents
heterogeneous traffic dataset structures [17].
empirical results and the composite architectural trade-off
analysis. Section VI provides a technical discussion on
1) VariationalAutoencoders(VAEs)
architecture-guided model selection for IDS deployment.
Encoder–decoder frameworks, such as Tabular VAEs
Section VII outlines directions for future work, and Section
(TVAE), embed mixed-type data into a latent space and re-
VIII concludes the paper.
construct synthetic samples [16]. While they can generalize
and are often easier to train than GANs, empirical studies
II. RELATEDWORK
indicate VAEs struggle in high-dimensional network traffic
Thegenerationofsyntheticnetworktrafficdatahasevolved
contexts and fail to preserve rare/discrete patterns or tem-
significantly, moving from rule-based simulations to ad-
poral dependencies, resulting in reduced fidelity and some-
vanced deep generative models [14]. While many studies
times compromised utility. For example, synthetic network
aim to improve fidelity (the degree to which synthetic data
traffic generated via VAEs may lack subtle joint-feature
replicates real network traffic statistics and temporal pat-
correlations critical for anomaly detection [25]. However,
terns), fewer address the twin issues of utility (downstream
empirical evaluations of how VAE architectures align with
task performance, i.e., IDS) and computational scalability
heterogeneous traffic datasets (categorical vs. continuous)
(training cost, memory use, deployment feasibility) [15]–
remain limited [26], [27].
[17]. This section reviews prior efforts grouped by archi-
tecturalclass,highlightinghoweachaddresses(orneglects)
2) GenerativeAdversarialNetworks(GANs)
thesethreechallengesandidentifyingthegapsthatmotivate
GAN-based architectures, including Conditional Tabular
our architectural selection framework.
GAN (CTGAN) [28], Wasserstein GAN with Gradient
Penalty(WGAN-GP)[7],[29],andCascadedTabularGAN
A. STATISTICALANDRESAMPLINGARCHITECTURES (CasTGAN) [30], remain the dominant approaches for gen-
(NON-AIMETHODS):LIMITEDSTRUCTURALFIDELITY erating high-fidelity synthetic tabular data. They are excep-
Non-AI approaches primarily focus on class imbalance tionally prominent in synthetic network traffic research; for
(boosting/replecating rare attack classes) and simple proba- example, surveys of GANs for network traffic generation
bilistic modelling, offering utility or scalability benefits but highlight their ability to capture complex joint distributions
frequently falling short on structural fidelity [?], [11]. Re- and mixed feature types [31]. In network traffic contexts,
sampling techniques such as Random Oversampling (ROS) specialized GANs for simulating traffic at both flow level
[18],SyntheticMinorityOversamplingTechnique(SMOTE) and packet level, i.e., FlowGAN [32] and NetShare [33],
[19], and Adaptive Synthetic Sampling (ADASYN) [20] havedemonstratedimprovedfidelityanddownstreamutility
targetclassimbalanceandarecomputationallyinexpensive; [34], [35]. These models tend to deliver superior perfor-
however, they do not model complex feature dependencies mance for AI model training (anomaly detection, intrusion
or temporal correlations. Probabilistic models (e.g., Gaus- detection) when synthetic data is used as augmentation.
sian Mixture Models (GMM) [21] and Bayesian Networks GANs are associated with well-known issues, including
VOLUME11,2023 3

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
traininginstability,modecollapse,highcomputationalcosts, scalability). Our study aims to fill this gap by introducing
and sensitivity to architecture/hyperparameters. For large an evidence-based architectural selection framework that
network datasets, these costs become non-trivial. Although correlates dataset characteristics with model architecture,
many studies compare GAN performance, few analyze why empirically evaluates twelve representative methods across
specific GAN architectures succeed on particular traffic heterogeneous traffic datasets, and offers actionable guid-
datasettypes(e.g.,categoricalvs.continuous).Architectural ance for cybersecurity practitioners.
alignment is rarely discussed [28], [36].
III. EXPERIMENTALMETHODOLOGYANDGENERATIVE
3) DiffusionModels MODELIMPLEMENTATION
Diffusion models (e.g., TABDDPM [37], NetDiffus [38]) The objective of this methodology is to ensure the com-
represent the emerging models in synthetic traffic genera- parativeanalysisadherestoscientificrigorbystandardizing
tion.Forexample,NetDiffusdemonstratesa66.4%increase theexperimentalenvironmentandestablishingatransparent
in fidelity and 18.1% downstream task uplift compared rationaleformodelconfigurationandfeatureselection.This
to GAN-based methods [38]. These models can produce section describes the properties of the selected datasets, the
highlyrealistictraffic,includingtemporaldynamics,through precisefeatureselectionprocess,andthespecificimplemen-
iterativedenoising.Akeyissueiscomputationalscalability, tation choices made for each generative model architecture.
many time steps, heavy denoising networks, and large
memory footprints. Tabular, mixed-type network traffic ap- A. DATASETCHARACTERISTICSANDSELECTION
plicationsarestillintheirearlystage.Asurveyofdiffusion RATIONALE
for tabular data reports promising results but highlights To investigate Research Question 2 (Architectural Influ-
scalabilityandarchitecture/data-mismatchissues[39].Even ence), we selected two prominent network traffic datasets
fewer studies explicitly consider how diffusion architecture that represent fundamentally distinct data structures and
aligns with traffic data structure, especially in cybersecurity typesofattackprofiling,i.e.,NSL-KDDandCIC-IDS2017.
contexts [40], [41].
The preceding subsections highlight progress across var-
1) NSL-KDDDataset
ious generative families; however, these advances remain
NSL-KDD, a refined version of the original KDD Cup
largely fragmented. Despite improvements in fidelity and
1999 dataset, is widely used in cybersecurity to evaluate
utility,aunifyingperspectivethatrelatesarchitecturaldesign
IDS [12]. This dataset was selected as a representative
to dataset structure remains missing.
of older network security benchmarks, characterized by
a predominance of categorical and discrete features (e.g.,
C. ARCHITECTURALCOMPATIBILITY:ATRIPLETOF
flags, protocols, service types), which require specific ar-
FIDELITY,UTILITY&SCALABILITYGAPS
chitecturalhandlingviaencodingtomaintaindependencies.
Despite the escalation of methods, a recurring limitation in Forthisstudy,thetrainingportionoftheNSL-KDDdataset,
the literature is the absence of systematic investigation into originally consisting of 125,973 instances and 42 columns
howmodelarchitecturecohereswiththetrafficdatasetstruc- (41 features and 1 (binary) target), was used, and following
ture (e.g., categorical-heavy vs. continuous-flow-heavy) and pre-processing, it contained 26 encoded features (Table 1).
how this affects the triad of fidelity, utility, and scalability
[11], [40]. Specifically:
2) CIC-IDS2017Dataset
• Few studies analyze how architectural design choices This data is part of the Canadian Institute for Cybersecu-
(e.g., conditional generation in GANs vs. iterative de-
rity’s intrusion detection dataset collection, which is widely
noising in diffusion) affect the fidelity-utility trade-off
employed for evaluating cybersecurity systems [13]. This
across traffic dataset types [28], [38].
contemporarydatasetwaschosenbecauseitfocusesheavily
• There is a scarcity of standardized benchmarks that on modern, continuous flow-based features (e.g., Average
concurrentlyevaluatefidelity,utility,andcomputational
Packet Size, Flow Bytes/s, Packet Length Variance). This
scalability across generative model classes on hetero-
structure tests the models’ architectural robustness when
geneous network traffic datasets [42].
learning complex, high-dimensional dependencies inherent
• Practitioners lack a reliable architectural selection in modern flow-level network data. CIC-IDS2017 has one
framework that guides model choice based on dataset
week of captured network traffic data in eight comma-
structure, use case (e.g., intrusion detection), and de-
separatedfiles(CSV).Thesefilesaregeneratedbasedonthe
ployment constraints.
types of attacks. There are 2,830,743 instances of all eight
In summary, while existing research contributes valuable files and 79 columns (78 numerical features and one binary
insights into synthetic traffic generation, none provide target).Theinitialeightrawfileswereconcatenated,cleaned
a comprehensive, architecture-aware framework that links (null, infinity, and the duplicate "Fwd Header Length" col-
generative model design to dataset structure and addresses umn removed), resulting in 21 pre-selected features (Table
thethreecorechallenges(fidelity,utility,andcomputational 2)
4 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
TABLE1. Summaryof26EncodedselectedFeaturesfromNSL-KDDDataset[12]
S.No Feature Description
1 src_bytes Numberofdatabytesfromsourcetodestination
2 dst_bytes Numberofdatabytesfromdestinationtosource
3 same_srv_rate Percentageofconnectionstothesameservice
4 diff_srv_rate Percentageofconnectionstodifferentservices
5 flag_SF Connectionstatuswithanormalconnection(SF:"Normal")
6 dst_host_srv_count Numberofconnectionstothesameserviceasthecurrentconnection
inthepast100connections
7 dst_host_same_srv_rate Percentageofconnectionstothesameserviceforadestinationhost
8 logged_in 1ifsuccessfullyloggedin;0otherwise
9 dst_host_serror_rate Percentageofconnectionsthathave“SYN”errors
10 dst_host_diff_srv_rate Percentageofconnectionstodifferentservicesforadestinationhost
11 dst_host_srv_serror_rate Percentage of connections that have “SYN” errors for a destination
host
12 serror_rate Percentageofconnectionsthathave“SYN”errors
13 srv_serror_rate Percentageofconnectionsthathave“SYN”errorsforthesameservice
14 flag_S0 Connection status where no data packets were exchanged (S0: "No
DataExchange")
15 count Numberofconnectionstothesamehostasthecurrentconnectionin
thepast2seconds
16 service_http HTTPservice(1ifused,0otherwise)
17 dst_host_srv_diff_host_rate Percentageofconnectionstodifferenthostsonthesameservice
18 level Threatleveloftheconnection
19 dst_host_count Number of connections to the same destination host in the past 100
connections
20 dst_host_same_src_port_rate Percentageofconnectionswiththesamesourceporttothedestination
host
21 service_private Privatenetworkservice(1ifused,0otherwise)
22 srv_diff_host_rate Percentageofconnectionstodifferenthostsforthesameservice
23 srv_count Numberofconnectionstothesameserviceasthecurrentconnection
inthepast2seconds
24 dst_host_srv_rerror_rate Percentage of connections that have “REJ” errors for a destination
host
25 service_domain_u Domainnameservice(DNS)(1ifused,0otherwise)
26 target classlabelindicatingiftheconnectionisnormaloranattack
B. MUTUALINFORMATION While approaches like Information Gain (IG) have been
To ensure that the synthetic data generation models are used for feature selection, as demonstrated by one study
trainedonthemostimpactfulfeatures,weemployedMutual [46], Information Gain only measures the relationship be-
Information (MI) [43] for feature selection, rather than tween individual features and the target variable, overlook-
relying on simpler methods such as Pearson correlation ing interdependencies between features [47]. Mathemati-
[44] or opaque tree-based techniques [45]. Correlation was cally, it measures the reduction in entropy when a feature
the first and most obvious choice, mathematically defined X is used to predict the target variable Y.
as the Pearson correlation coefficient (equ: 1). However,
correlation only accounts for linear relationships [44]. In IG(Y,X)=H(Y)−H(Y|X) (2)
real-world scenarios, non-linear relationships often need to
where H(Y) is the entropy of the target variable Y,
be identified and quantified to select the optimal set of
and H(Y|X) is the conditional entropy of Y given X.
features.
Although Information Gain quantifies the relationship be-
Cov(X,Y)
Corr(X,Y)= (1) tween individual features and the target variable, it ignores
σ σ
X Y interdependencies among the features.
where Cov(X,Y) is the covariance between variables X Incontrast,MIcapturestherelationshipbetweenfeatures
andY,andσ X andσ Y arethestandarddeviationsofX and and the target and the dependencies among the features
Y, respectively. While correlation is effective for capturing themselves, providing a more holistic evaluation [48]. MI
linear relationships, it does not account for the non-linear is defined as:
relationships that often exist in real-world data, limiting
MI(X,Y)=H(X)+H(Y)−H(X,Y) (3)
its effectiveness for feature selection. The second option
was a tree-based AI technique, known for its robustness where H(X) and H(Y) are the entropies of variables X
and ability to identify essential features rigorously [45]. and Y, and H(X,Y) is their joint entropy. By capturing
However, tree-based methods suffer from the "black box" non-linear dependencies and interactions among features,
problem,offeringlittleinterpretabilityregardingwhycertain MI offers a more comprehensive framework for feature
features are selected. selection.
VOLUME11,2023 5

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
TABLE2. Summaryof21selectedFeaturesfromCIC-IDS2017Dataset[13]
S.No Feature Description
1 AveragePacketSize Averagesizeofthepacketsintheflow
2 PacketLengthStd Standarddeviationofthepacketlengthsintheflow
3 PacketLengthVariance Varianceofthepacketlengthsintheflow
4 PacketLengthMean Meanlengthofthepacketsintheflow
5 TotalLengthofBwdPackets Totalnumberofbytesinbackward(Bwd)packets
6 SubflowBwdBytes Numberofbytesinthebackwardsub-flow
7 DestinationPort Portnumberofthedestinationhost
8 AvgBwdSegmentSize Averagesizeofbackwardsegments
9 BwdPacketLengthMean Meanlengthofbackwardpackets
10 Init_Win_bytes_forward Initialwindowsizeinbytesforforwarddirection
11 SubflowFwdBytes Numberofbytesintheforwardsub-flow
12 TotalLengthofFwdPackets Totalnumberofbytesinforward(Fwd)packets
13 MaxPacketLength Maximumlengthofapacketintheflow
14 BwdPacketLengthMax Maximumlengthofabackwardpacket
15 Init_Win_bytes_backward Initialwindowsizeinbytesforbackwarddirection
16 FwdPacketLengthMax Maximumlengthofaforwardpacket
17 FwdPacketLengthMean Meanlengthofforwardpackets
18 AvgFwdSegmentSize Averagesizeofforwardsegments
19 FlowIATMax Maximumtimeintervalbetweenpacketsintheflow
20 FlowBytes/s Rateofflowinbytespersecond
21 target classlabelindicatingiftheflowisbenignormalicious
TABLE3. MutualInformationScoreofNSL-KDDFeatures TABLE4. MutualInformationScoreofCIC-IDS2017Features
Feature MutualInformationScore Feature MutualInformationScore
src_bytes 0.566864 AveragePacketSize 0.347112
dst_bytes 0.439281 PacketLengthStd 0.342188
same_srv_rate 0.369288 PacketLengthVariance 0.342019
diff_srv_rate 0.361895 PacketLengthMean 0.319635
flag_SF 0.341828 TotalLengthofBwdPackets 0.296955
dst_host_srv_count 0.335993 SubflowBwdBytes 0.296882
dst_host_same_srv_rate 0.309832 DestinationPort 0.291245
logged_in 0.292075 AvgBwdSegmentSize 0.287676
dst_host_serror_rate 0.286589 BwdPacketLengthMean 0.287483
dst_host_diff_srv_rate 0.283874 Init_Win_bytes_forward 0.287174
dst_host_srv_serror_rate 0.281332 SubflowFwdBytes 0.284528
serror_rate 0.278666 TotalLengthofFwdPackets 0.284264
srv_serror_rate 0.269186 MaxPacketLength 0.264060
flag_S0 0.263399 BwdPacketLengthMax 0.263210
count 0.262733 Init_Win_bytes_backward 0.250188
service_http 0.191343 FwdPacketLengthMax 0.246537
dst_host_srv_diff_host_rate 0.189822 FwdPacketLengthMean 0.213223
level 0.153819 AvgFwdSegmentSize 0.213065
dst_host_count 0.144479 FlowIATMax 0.212817
dst_host_same_src_port_rate 0.131316 FlowBytes/s 0.209784
service_private 0.118493
srv_diff_host_rate 0.099441
srv_count 0.062476
complex and non-linear, a common occurrence in network
dst_host_srv_rerror_rate 0.062244
service_domain_u 0.048430 data.
In brief, for this study, MI was specifically chosen be-
causeitisamodel-agnosticmetricthatquantifiesbothlinear
Compared to other AI-based feature selection methods, andnon-lineardependenciesbetweenfeaturesandthetarget
such as recursive feature elimination or embedded methods variable [51]. This is crucial in network traffic data, where
based on decision trees [49], MI has the upper hand by complex, non-linear feature interactions define malicious
being model-agnostic. Many AI-based techniques are tied behavior. By selecting the top 25% of features based on MI
to specific algorithms or models, which may introduce weights(Tables3&4),weensuredthatthereducedfeature
biases or limit generalizability across different datasets setmaintainedthecoreinformationnecessaryforaccurately
or classifiers. MI, however, evaluates feature importance representing the data, while reducing computational load.
basedonstatisticaldependenciesindependentofanyspecific This methodological rigor is essential for the Architectural
model, making it a versatile and unbiased approach [50]. Selection Framework, as it ensures that any observed dif-
This enables MI to offer a more robust selection process, ference in architectural competence between models (e.g.,
particularly in scenarios where feature relationships are GANs vs.VAEs) is due totheir inherent design, ratherthan
6 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
the initial selection of features. emerging paradigm, iterative denoising on structured
tabulardata.Theimplementationwasspecificallychal-
lenged against the high volume, unstructured flow data
of CIC-IDS2017 to rigorously quantify the architec-
tural limitations related to computational scale.
b: GenerativeAdversarialNetworks(GANs)
GAN-based models (CTGAN, CopulaGAN, GANBLR++,
CasTGAN) were implemented due to their established ca-
pability as state-of-the-art synthetic tabular data generators.
Their architectures were expected to be robust due to spe-
cificdesignchoices.Forexample,CTGANandCopulaGAN
wereimplementedutilizingtheirfeaturesdesignedtohandle
mixed data types, a necessity for network traffic, which
containsbothdiscrete(categorical)andcontinuousfeatures.
CTGAN specifically employs conditional generation and
mode-specificnormalization,whichwehypothesizedwould
be essential for preserving the non-linear feature dependen-
FIGURE1. Methodsforgeneratingsynthetictabulardata cies crucial for realistic network traffic samples.
D. HARDWAREANDSOFTWAREENVIRONMENT
C. GENERATIVEMODELIMPLEMENTATIONAND The experiments were performed on a high-performance
ARCHITECTURALRATIONALE workstation (13th Gen Intel® Core™ i9-13900, 32 GB
We systematically evaluated twelve methods, grouped into RAM) with a dedicated NVIDIA GeForce RTX 4090 GPU
twomainarchitecturalcategoriesthatsplitintothree(Figure toguaranteereproducibilityandprovideafaircomputational
1), to establish a robust comparative framework. Rather comparison baseline for all AI-based architectures. The
than providing general definitions, we focus on the imple- software environment utilized Python 3.12.4, leveraging
mentation choices that were critical for handling network PyTorch for deep learning tasks and the SDV library for
data complexity. All experiments were conducted on a tabular GAN implementations (CTGAN, TVAE, Copula-
high-performanceworkstationutilizingadedicatedNVIDIA GAN). To ensure the statistical validity of the performance
GeForce RTX 4090 GPU to ensure uniform computational claims, particularly concerning utility, all TSTR evaluations
conditions. were executed over twenty independent trials (N=20). This
methodology allowed for the calculation of the mean and
1) StandardStatisticalandResamplingArchitectures standard deviation for both Accuracy and F1 score, provid-
(Non-AIBaselines) ing the necessary statistical dispersion required for robust
Methods such as ROS, SMOTE, ADASYN, and Cluster analysis and comparison against the TRTR baseline (as
Centroids (CC) were included primarily as class balance quantified via t-tests in Table 5, 6,7, and 8).
baselines. Their utility was assessed in correcting class
imbalance prior to measuring their ability to capture com- IV. EVALUATIONMETRICS
plex data structures. GMM and Bayesian Networks (BN) The following section details how each evaluation metric
were also included to evaluate the performance of classical was measured to assess the experimental results.
probabilistic modeling against deep generative methods, es-
pecially concerning computational and memory constraints 1) Fidelity/RealismQuantification
when facing large-scale flow data like CIC-IDS2017. Fidelityreferstothenecessityforsyntheticdatatoresemble
the underlying statistical properties of real data closely
2) AIbasedmethods [52].Thismetric’s coremathematicaldefinitionisthateach
a: VariationalAutoencoders(VAEs)andDiffusionModels variable’s probability distribution in the synthetic dataset
• Tabular VAE (TVAE): This VAE architecture was should closely match that of the corresponding variable
implemented to evaluate its ability to learn high- in the real dataset [53]. However, beyond replicating the
dimensional latent representations of network traf- individual behavior of each variable, it is equally important
fic. We tested whether its inherent encoding-decoding toexaminetheinterdependenciesandrelationshipsbetween
structure, which is computationally expensive, could variables. To evaluate these relationships, we compare the
achieve a superior Fidelity-Utility balance compared correlationsamongvariablesinbothdatasets[54].Thus,we
to the adversarial process of GANs. quantified this using three composite metrics:
• Tabular Diffusion Model (TABDDPM): This archi- • Data Structure (DS): This binary metric checks for
tecture was included to test the viability of a recently the strict adherence of synthetic variables to the orig-
VOLUME11,2023 7

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
FIGURE2. CorrelationHeatmapforNSLKDD(Part1/2)
inal data’s logical minimum and maximum values, values. This evaluation method helps assess whether
such as ensuring binary columns (e.g., logged_in, each approach maintains the required data boundaries.
flag_SF) contain only 0 or 1 values. Failure to meet • Correlation (Corr): This assessment is performed by
this structural requirement is marked as NO and indi- examining the correlation heatmap, which represents
cates a fundamental flaw in the model’s architectural the absolute values of the correlation coefficients for
generation process. For example, in Table 5, the first all variables (see Figure 2 and Figure 3 for key NSL
syntheticdatasetwasgeneratedbyROS,andthevalue KDDheatmaps).Itevaluatesthestrengthanddirection
in the DS column is YES, indicating that all binary of relationships in both real and synthetic datasets. If
andbooleanvariablesadheredtotheirexpectedvalues. there is a significant difference between the absolute
However, the next row, corresponding to SMOTE, correlation heatmap of the synthetic data and the real
showsNOundertheDScolumnbecause,apartfromthe data, as well as in the heatmap of the absolute correla-
target variable in the NSL-KDD data, the binary and tiondifferences,theresultismarkedasNO.Otherwise,
boolean variables did not conform to their expected it is marked as YES in the Corr column of all of the
8 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
FIGURE3. CorrelationHeatmapforNSLKDD(Part2/2)
results tables. the PD column, for the ROS method, all variables
• Probability Distribution (PD): This compares the exhibitedidenticalPDsaccordingtodistributioncurves
underlying probability distribution of each variable in Figure 4, resulting in a PD of 0% difference. Con-
between the real and synthetic datasets, ensuring that versely, for the Adaptive Synthetic Sampling method,
their statistical properties are aligned. To calculate the one variable out of 26 exhibited a different PD (see
statistics for the PD comparison, the following steps supplementary material (S1)) for a complete graphical
were undertaken: PD comparison. Using Equation 4, the percentage
1) For every variable in the synthetic and real difference was calculated as:
datasets, the underlying PD was estimated using 1
PD (%)= ×100≈3.8% (5)
Kernel Density Estimation (KDE). 26
2) Each variable’s PD was visualized. For clarity,
2) Utility/ClassificationPerformance
individual figures showing the real and synthetic
Utility measures the effectiveness of synthetic data for its
PDs were generated. In some cases, side-by-
intended downstream application, training Intrusion IDS
side figures were created to provide a direct
models [55]. The standard comparison approach compares
comparison (Figure 2). Complete PD comparison
modelperformancewhentrainedonrealdata(TRTR:Train
graphsforbothNSL-KDDandCIC-IDS2017are
andTestonRealData)againstperformancewhentrainedon
provided in Supplementary material (S1).
synthetic data (TSTR: Train on Synthetic Data and Test on
3) ThealignmentofthePDwasquantifiedusingthe
RealData).IfperformancemetricsintheTSTRscenarioare
following formula:
comparable to or exceed the TRTR baseline, the synthetic
Number of Variables with Different PD data is considered a viable alternative to the real data [56].
PD (%)= ×100
Total Number of Variables For network traffic analysis, utility is determined by
(4) assessing the ML model’s ability to classify traffic (normal
Where "Number of Variables with Different PD vs.attack).WhilecomprehensivemetricslikeF1score,pre-
indicatesthecountofvariableswhosePDdiffered cision, and recall are necessary for imbalanced datasets, the
between the real and synthetic datasets. F1 score robustly measures the harmonic mean of precision
For the NSL-KDD dataset, which contains 26 total andrecall[57].ThisstudycalculatedTSTRAccuracyasthe
variables,theresultsaresummarizedinTable5.Under primary comparative metric for model utility, as reported in
VOLUME11,2023 9

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
FIGURE4. ProbabilityDistributionComparisonforNSLKDD.
Table5andTable7.Awell-performingTSTRindicatesthat classes are equal, i.e., follow a 50-50 ratio in the whole
the synthetic data has successfully captured the essential data. Thus, in Table 5, under the CB column for ROS and
patterns and relationships within the real data, making it SMOTE, it is mentioned 0% diff, and for the Adaptive
suitable for model development and deployment in privacy- Synthetic Sampling, it is 0.14% diff.
sensitive environments. Forscalability,weassessthecomputationalcost(training
To account for the inherent stochasticity of deep genera- timeandmemoryrequirements)andfailurerates,whichare
tivemodelsandtoensurethescientificrigorofperformance crucial for determining a model’s practical suitability for
differences, all TSTR Accuracy metrics were quantified as deployment in real-world security infrastructure.
themean(x¯)±standarddeviation(σ)overtwentyindepen-
dentTSTRruns(N =20).Furthermore,weutilizedapaired V. RESULTS
t-testtoassessthestatisticalsignificanceoftheperformance This section presents the empirical results to evaluate the
difference (utility) between key generative models and the generativemodelperformancebasedonfidelity,utility,class
TRTRbaseline,providingcritical,validatedevidenceforthe balance, and scalability across two distinct network traffic
Architectural Selection Framework. datastructures(NSL-KDDandCIC-IDS2017).Thedetailed
quantitative results are summarized in Table 5 (NSL-KDD)
3) ClassBalanceandScalability and Table 7 (CIC-IDS2017), but the primary findings are
Class balance (CB) difference addresses the third research integrated into a visual architectural trade-off analysis.
question by measuring the model’s ability to maintain a
balanced class distribution (Normal vs. Attack) in the gen- A. ARCHITECTURALPERFORMANCEONFIDELITYAND
erateddata.CBreferstothedistributionofinstancesacross UTILITY
different classes in the dataset [58]. Maintaining a balanced We analyze the trade-off between fidelity and utility to
class distribution in real-world datasets is essential for answerthefirstandsecondresearchquestions,whichquery
training robust ML models, as imbalanced classes can lead the best models and the influence of dataset characteristics.
to biased models that perform poorly on underrepresented The complete quantitative assessment, including the rigor-
classes [59]. ousF1score,stabilityanalysis(Mean±SD),andstatistical
significance against the TRTR baseline for NSL-KDD is
Class Balance Difference (%)=|P −P |
synthetic,Normal synthetic,Attack summarized in Table 6, and for the continuous flow-heavy
×100
CIC-IDS2017 dataset, the complete statistical summary is
(6)
provided in Table 8. A Composite Architectural Trade-Off
Thus, the CB results mentioned in Table 5 and Table 7 Plot (Figure 5) was generated to visually synthesize the
represent how much difference exists between the NOR- performance of the generative models across both datasets.
MAL and ATTACK cases. If the classes in the synthetic This figure immediately highlights two key architectural
data are the same, there is zero difference; otherwise, the findings:
difference percentage is calculated based on the equation. 1) Dominance of GAN Architectures: GAN-based
This equation 6 gives 0% diff if the normal% and attack% models (CTGAN, CopulaGAN) consistently occupy
10 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
FIGURE5. CompositeTrade-OffAnalysisofSyntheticDataModels
the upper left quadrant across both datasets, demon- tecturalconstraintwhenfacedwithlarge-volume,
stratingthemostrobustbalanceofhighutilityandsu- unstructured flow data.
periorfidelity(lowPDdifferenceandhighcorrelation While statistical methods like ROS and SMOTE achieved
preservation)(Table5andTable7).Thisarchitectural high Utility (accuracy 0.999), this is due to their primary
superiorityisquantifiedbytheirperformanceonCIC- functionasClassBalanceBaselines,generatinginterpolated
IDS2017,whereCopulaGANachievedanF1scoreof samplesthat,whileeasilyclassified,lackthehighstatistical
0.9756±0.0005, exhibiting extremely low variance fidelity required to be considered truly generative. Their
in performance and demonstrating its architectural inability to maintain data structure (DS: No for SMOTE
stability when faced with high-volume, continuous- and ADASYN on NSL-KDD) suggests that their simplicity
flow data. compromises realism.
2) Dataset Influence on Architectural Failure: Perfor-
mance severely degraded for non-GAN architectures
B. COMPUTATIONALANDSCALABILITYCONSTRAINTS
when moving from the categorical heavy NSL-KDD
Thethirdresearchquestionaddressesthepracticaltrade-offs
to the continuous flow-heavy CIC-IDS2017.
regarding computational cost and scalability for real-world
• Statistical Failure: Models like GMM, which deployment. Our results reveal significant architectural bar-
rely on parametric assumptions, exhibited the riers for non-GAN models when scaling to large datasets.
lowest fidelity across both datasets (PD diff 1) DiffusionModelFailureonCIC-IDS2017:Themost
of 99.1% on NSL-KDD and 61.9% on CIC- pronounced constraint was observed in the Diffu-
IDS2017), confirming their architectural inability sion Model (TABDDPM) and the Bayesian Network.
to model the complex, multimodal nature of net- As shown in Table 7, these models failed to exe-
work flows. cute on the large-scale CIC-IDS2017 dataset due to
• Diffusion Model Limitations: The iterative de- prohibitively high computational costs and memory
noising architecture of TABDDPM performed requirements for relationship construction. This out-
poorly on NSL-KDD (PD diff 98.3%) and ex- come confirms that architectures relying on extensive
hibited a catastrophic failure to scale to the CIC- iterative processes or graphical model construction
IDS2017 dataset, indicating a fundamental archi- are currently impractical for large, high-dimensional
VOLUME11,2023 11

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
tabular network data, regardless of their theoretical models achieve near-perfect F1 utility (≈0.9998±0.0001),
generative potential. confirming their efficacy as class balance baselines, their
2) ProbabilisticModelLimitations:TheBayesianNet- inability to maintain the fundamental Data Structure (DS:
work (BN) architecture similarly failed to generate No) constitutes an architectural failure. We define this phe-
results for the CIC-IDS2017 dataset. This highlights nomenon as compromised fidelity; high operational utility
thechallengeofapplyingprobabilisticgraphicalmod- is achieved via interpolation at the expense of generative
els, which require substantial memory and processing architectural competence. This failure is evident despite the
power for initial feature relationship construction, to minimal standard deviation, confirming their stability in
large network flow volumes. generating structurally flawed data. While statistical meth-
In contrast, CTGAN and CopulaGAN, despite being ods achieved high F1 utility (≈ 0.9990) on CIC-IDS2017
resource-intensive generative models, successfully pro- (Table 8), their high performance is still architecturally
cessed both datasets, establishing them as the most viable compromised. For instance, CC and CasTGAN exhibit
architectural choice when balancing generative power with high utility but show Compromised Fidelity by failing the
the need for scalability in a dynamic network security Data Structure check (DS: No in Table 7), indicating that
environment. their utility is achieved via class manipulation rather than
generative competence. Notably, for the continuous flow-
C. DETAILEDCOMPARATIVESUMMARY heavy CIC-IDS2017 dataset, certain high-fidelity architec-
Tables 5 and 7 provide comprehensive and granular results tures (ROS, SMOTE, CTGAN, and CopulaGAN) achieved
that support the architectural findings. a0%PDdifference(Table7).Thiszerodiscrepancy,quanti-
The discussion and scientific interpretation of these re- fied via Kernel Density Estimation (KDE), serves as empir-
sultsinthecontextofIDSdeploymentwillbefullyexplored ical proof of the perfect approximation of continuous flow
in the discussion section. distributions, validating the architectural suitability of these
models for modern flow-based security data. Furthermore,
VI. DISCUSSION the GMM architecture, despite showing a low standard
The systematic comparison across heterogeneous network deviation (0.0016), yielded poor utility (F1: 0.4745) on
datasetsandmodelarchitecturesvalidatesthenecessityofan the CIC-IDS2017 dataset. This confirms that the GMM
Architectural Selection Framework for generating synthetic architecture is stable but ineffective, consistently failing to
network traffic. Our findings extend beyond simple bench- model the complex, non-Gaussian distributions inherent to
markingtoestablishevidence-basedguidelinesforselecting continuous flow data.
generative models, guided by the critical trade-off between Amonggenerativearchitectures,TVAEachievedthehigh-
architectural robustness and data structure compatibility. est F1 score (0.9813±0.0009), demonstrating strong
utility. However, the Architectural Selection Framework
A. RESOLUTIONOFTHEFIDELITY-UTILITYTRADE-OFF requires an optimal balance, not just peak utility. TVAE’s
ResearchQuestion1aimedtodeterminewhicharchitectures superior F1 score is achieved at a significant Fidelity cost
best strike a balance between realism and practical utility. (PDdiff26.7%vs.CopulaGAN’s5.4%).Conversely,Copu-
Figure5definitivelyshowsthatGANs,specificallyCTGAN laGAN(0.9770±0.0008F1)exhibitstheloweststandard
and CopulaGAN, form the optimal performance frontier, deviation among all generative models, proving superior
possessingthenecessaryarchitecturalcomplexitytosucceed architectural robustness and achieving the ideal balance of
across different network data types (Table 5 and Table 7). high utility with rigorous fidelity preservation, cementing
The success of these GAN models is technically rooted its position on the optimal performance frontier. The poor
in their ability to handle mixed discrete and continuous performance of the iterative Diffusion Model (TABDDPM)
feature types, such as binary flags, categorical protocols, on NSL-KDD (PD diff 98.3%) and its subsequent failure
andcontinuousflowmetrics.CTGAN’suseofaConditional to scale further highlights the fragility of non-GAN archi-
Generatorcoupledwithmode-specificnormalizationenables tectures. Finally, the performance of GANBLR++ provides
it to preserve complex dependencies, where the adversarial critical evidence of architectural instability, as its low mean
process forces the generator to capture the multivariate utility (F1: 0.6327 on NSL-KDD, F1: 0.5843 on CIC-
dependenciesthatdefinerealisticattackpatterns,resultingin IDS2017) combined with extreme performance variance
low PD Differences (below the 10% threshold) and passing (up to ±0.1251 SD on NSL-KDD and ±0.0418 SD on
the stringent Correlation check. Furthermore, the resulting CIC-IDS2017) makes it statistically unreliable and entirely
highfidelitytranslatesdirectlytoeffectivemachinelearning unsuitable for production IDS deployment.
training, with CopulaGAN achieving a TSTR F1 score of The statistical summary for the CIC-IDS2017 dataset
0.9770±0.0008, confirming their viability as replacements (Table 8) further validates the Architectural Robustness of
for real data in training adaptive IDS. conditional GANs against continuous flow data. Copula-
The structural failure observed in high-utility resampling GAN(0.9756±0.0005F1)maintainsthehighestgenerative
models (SMOTE, ADASYN, CC) is quantified (Table 6), utility and stability, confirming its architectural suitabil-
represented by Hollow Markers in Figure 5. While these ity for high-dimensional, continuous features. Its minimal
12 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
TABLE5. ComparisonofSyntheticDataUtilityonNSL-KDDDataset
StatisticalSimilarity(SS) Accuracy F1-Score
Category Method CB (Mean±SD) (Mean±SD)
DS Corr PD
(TSTR) (TSTR)
ROS Yes Yes 0%diff 0%diff 0.9998±0.0001 0.9998±0.0001
SMOTE No Yes 0%diff 0%diff 0.9999±0.0001 0.9998±0.0001
ADASYN No Yes 3.8%diff 0.14%diff 0.9998±0.0001 0.9998±0.0001
Non-AI(Statistical)
ClusterCentroids(CC) No Yes 0%diff 0%diff 0.9995±0.0001 0.9998±0.0001
GMM No Yes 99.1%diff 99.9%diff 0.5314±0.0024 0.3718±0.0028
BayesianNetwork(BN) No No 0%diff 17.2%diff 0.9587±0.0009 0.9582±0.0009
TVAE Yes Yes 23.1%diff 26.7%diff 0.9807±0.0009 0.9813±0.0009
TABDDPM No No 98.3%diff 34.2%diff 0.51±N/A N/A
AI-Based(Classical+Generative) CTGAN Yes Yes 7.7%diff 6.7%diff 0.9667±0.0010 0.9685±0.0010
GANBLR++ No No 99%diff 8.8%diff 0.5916±0.0861 0.6327±0.1251
CopulaGAN Yes Yes 7.7%diff 5.4%diff 0.9761±0.0008 0.9770±0.0008
CasTGAN No Yes 27%diff 11.1%diff 0.9582±0.0027 0.9588±0.0027
"SS"=StatisticalSimilarity,"DS"=DataStructure,"Corr"=Correlation,"PD"=ProbabilityDistribution,"CB"=ClassBalance.AllAccuracyand
F1-ScoreresultsareMean±StandardDeviationacross20repetitions(TSTR),comparedagainsttheTRTRBaseline(0.9995±0.0001).
standard deviation (±0.0005) provides empirical proof that C. SCALABILITYANDPRACTICALCONSTRAINTSFOR
the architectural design is highly robust, resisting the high- IDSDEPLOYMENT
variance outputs observed in other unstable architectures, Thecomputationalcostfindingsdirectlytranslateintoprac-
such as GANBLR++ (F1: 0.5843±0.0418). The extreme ticaldeploymentconstraintsforasecurityanalystdesigning
variance of GANBLR++ on both datasets (Tables 6 and 8) an Adaptive IDS (Research Question 3).
confirms a consistent architectural failure mode of instabil-
• Impracticality of Emerging Architectures: The fail-
ity, rendering it unsuitable for reliable security deployment.
ure of TABDDPM and the Bayesian Network to ex-
ecute on the large-scale CIC-IDS2017 dataset is the
B. ARCHITECTURALCOMPATIBILITYANDDATA most significant practical finding. As documented in
STRUCTUREINFLUENCE Table 7 and Table 8, the utility results for these
Research Question 2 investigated how the underlying data architectures are labeled ’N/A,’ explicitly confirming
structure of network traffic influences architectural perfor- that the iterative denoising process (TABDDPM) and
mance. Our analysis demonstrates that data characteristics graphical model construction (BN) pose prohibitive
are a primary selection constraint. computational barriers for high-volume tabular data.
• Robustness to Categorical vs. Continuous Data: Consequently, these architectures, despite their theo-
The tight clustering of GAN model markers (Blue retical promise, cannot be realistically considered for
Circles for categorical NSL-KDD and Red Triangles training IDSs that rely on frequent synthetic data
for continuous CIC-IDS2017 in Figure 5) in the top generation using massive flow datasets.
left quadrant provides empirical proof of their archi- • Operational Feasibility: CTGAN and CopulaGAN
tectural resilience. This is quantitatively supported by offer the most practical deployment architecture. They
theirconsistentstability:CopulaGANmaintainsanF1- successfully navigated both small and large datasets
score standard deviation below ±0.0008 across both while maintaining high fidelity, establishing a clear
datasets (Table 6 and Table 8), demonstrating that its path for their implementation in real-world security
architecturesuccessfullyaccommodatesdiversefeature systems requiring balanced, realistic training data for
structures, from categorical NSL-KDD to continuous rapid, adaptive model updates. The trade-off is higher
CIC-IDS2017, without performance degradation. computationaldemandcomparedtostatisticalmethods,
• Vulnerability to Architectural Collapse: The results but this cost is justified by the proven preservation
expose specific architecture-to-data mismatches. Prob- of structural and feature dependencies that statistical
abilistic Graphical Models (BN) and Diffusion Models methods lack.
(TABDDPM) demonstrated failure when faced with
the high-volume, high-dimensional structure of CIC- VII. FUTUREWORK
IDS2017. This is not merely an optimization problem Building upon the empirical evidence of the Architec-
butanarchitecturalconstraint,astheresourcesrequired tural Selection Framework, which proved the dominance
for iterative denoising (TABDDPM) or initial relation- of GANs and the scalability failure of Diffusion models
ship mapping (BN) proved prohibitive for continuous for tabular network data, future research must transition to
flow data, effectively rendering these approaches non- architecturaloptimizationanddeploymentrigor.Weidentify
viable for modern network environments. three scientifically deep directions:
VOLUME11,2023 13

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
TABLE6. StatisticalSignificanceSummaryofSyntheticDataUtility(TSTRvs.TRTRBaseline,NSL-KDD,N=20)
Category Method Accuracy F1-Score
Interpretation
(Mean±SD) (Mean±SD)
ROS 0.9998±0.0001 0.9998±0.0001 Near perfect utility and stability. High
Utility achieved as a Class Balance
Non-AI(Statistical) Baseline.
SMOTE 0.9999±0.0001 0.9998±0.0001 Highest utility, architectural failure
(DS: No) confirms compromised fi-
delitydespitehighF1.
ADASYN 0.9998±0.0001 0.9998±0.0001 Near perfect utility and stability, ar-
chitectural failure (DS: No) indicates
compromisedfidelity.
CC 0.9995±0.0001 0.9998±0.0001 Near perfect utility, architectural fail-
ure (DS: No) indicates compromised
fidelity.
GMM 0.5314±0.0024 0.3718±0.0028 Poor utility, low stability, confirms ar-
chitectural incompatibility with multi-
modalnetworkdata.
BN 0.9587±0.0009 0.9582±0.0009 Significant utility loss, high stability
(lowSD)foraclassicalmodel.
TVAE 0.9807±0.0009 0.9813±0.0009 HighestgenerativeF1,excellentstabil-
AI-Based(Classical+Generative) ity, but achieved with higher fidelity
lossthanGANs.
TABDDPM 0.51±N/A N/A N/A
CTGAN 0.9667±0.0010 0.9685±0.0010 Highutilitywithlowvariance(robust-
ness),optimalbalancewithhigharchi-
tecturalfidelity.
GANBLR++ 0.5916±0.0861 0.6327±0.1251 Worst overall utility, extreme architec-
turalinstability.
CopulaGAN 0.9761±0.0008 0.9770±0.0008 Near TVAE utility with highest archi-
tectural stability (lowest ± SD among
GANs). Optimal performance frontier
model.
CasTGAN 0.9582±0.0027 0.9588±0.0027 Acceptable utility, slightly higher vari-
ance indicates lower architectural sta-
bilitythanCTGAN/CopulaGAN.
Note:AllTSTRmethodsshowedastatisticallysignificantdifferenceagainsttheTRTRBaseline
(Accuracy=0.9995±0.0001,F1=0.9994±0.0001),withp<0.0001.TheMean±SDvaluesquantifytheutilityandstabilityacross20
repetitions.
A. ARCHITECTURESFORENHANCEDFIDELITYAND within the GAN latent space to isolate features that
PRIVACY pose the highest risk of re-identification (e.g., specific
The current trade-off between realism and privacy requires IP addresses or source ports) and applying localized,
innovativearchitecturalsolutionsthatguaranteedataprotec- feature-specific perturbation strategies, rather than ap-
tion without compromising the high fidelity necessary for plying uniform noise to the entire dataset. This move
anomaly detection. fromglobaltolocalizedprivacymeasuresiscriticalfor
maintaining high utility in sensitive network data.
• Differential Privacy (DP) Integration in Adversar-
ial Training: Future work must focus on embedding
B. DYNAMICFEATUREDEPENDENCYMODELINGAND
strict Differential Privacy (DP) mechanisms directly
ADVANCEDEVALUATION
into the generator and discriminator components of
The findings on Correlation and Data Structure failure
CTGAN-like architectures. A key challenge is mitigat-
modes (Figure 5, hollow markers) reveal the inadequacy
ingtheknownperformancedegradation(dropinTSTR
of current metrics to capture true logical relationships in
accuracy) when using DP. Research should explore
network traffic.
novel objective functions that incorporate DP-specific
regularizers, aiming to minimize the loss landscape • Conditional Dependency Quantification: Future re-
divergencecausedbynoiseinjectionwhilemaximizing search must move beyond simple correlation to rig-
the preservation of complex, non-linear feature depen- orously quantify logical and conditional dependencies
dencies essential for network traffic realism. within network flows (e.g., ensuring a "logged_in"
• ArchitecturalDeconvolutionforFeatureSensitivity: flag is only ’1’ if the protocol is TCP). This requires
Weproposeinvestigatingarchitecturescapableofquan- developing a new suite of evaluation metrics based on
tifyingfeaturesensitivityduringthegenerationprocess. ConditionalMutualInformation(CMI)orProbabilistic
This involves developing a deconvolutional approach Graphical Models (PGM) that can provide quantitative
14 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
TABLE7. ComparisonofSyntheticDataUtilityonCIC-IDS2017Dataset
Statistical Similarity (SS) Accuracy F1-Score
Category Method CB (Mean ± SD) (Mean ± SD)
DS Corr PD
(TSTR) (TSTR)
ROS Yes Yes 0%diff 0%diff 0.9991±0.0001 0.9991±0.0001
SMOTE Yes Yes 0%diff 0%diff 0.9990±0.0004 0.9989±0.0001
Non-AI (Statistical) ADASYN Yes Yes 0%diff 0.2%diff 0.9986±0.0005 0.9986±0.0003
CC No Yes 0%diff 0%diff 0.9930±0.0001 0.9930±0.0005
GMM No No 61.9%diff 46.1%diff 0.4509±0.0023 0.4745±0.0016
BN N/A
TVAE Yes No 1.4%diff 69.4%diff 0.9718±0.0007 0.9719±0.0004
TABDDPM N/A
AI-Based (Classical + Generative) CTGAN Yes Yes 0%diff 5%diff 0.9538±0.0003 0.9607±0.0007
GANBLR++ No No 47.6%diff 64.4%diff 0.5378±0.0665 0.5843±0.0418
CopulaGAN Yes Yes 0%diff 5%diff 0.9755±0.0005 0.9756±0.0005
CasTGAN No No 4.8%diff 58.3%diff 0.9734±0.0005 0.9737±0.0004
"SS"=StatisticalSimilarity,"DS"=DataStructure,"Corr"=Correlation,"PD"=ProbabilityDistribution,"CB"=ClassBalance.AllAccuracyand
F1-ScoreresultsareMean±StandardDeviationacross20repetitions(TSTR),comparedagainsttheTRTRBaseline(0.9995).
TABLE8. StatisticalSignificanceSummaryofSyntheticDataUtility(TSTRvs.TRTRBaseline,CIC-IDS2017,N=20)
Category Method Accuracy F1-Score
Interpretation
(Mean±SD) (Mean±SD)
ROS 0.9991±0.0001 0.9991±0.0001 Nearperfectutilityandstability.Highly
effectiveClassBalanceBaseline.
Non-AI(Statistical) SMOTE 0.9990±0.0004 0.9989±0.0001 High utility with minimal variance.
Achievesutilityviainterpolation-based
balancing.
ADASYN 0.9986±0.0005 0.9986±0.0003 Highutilityandstability.Highlyeffec-
tiveClassBalanceBaseline.
CC 0.9930±0.0001 0.9930±0.0005 High utility and stability, but architec-
tural failure (DS: No) confirms Com-
promise.
GMM 0.4509±0.0023 0.4745±0.0016 Poorutility,stablebutineffective.Low
SDconfirmsstability,butlowF1con-
firmsunsuitability.
TVAE 0.9718±0.0007 0.9719±0.0004 High generative utility and stability
(low SD). Utility comes at a cost of
fidelity.
AI-Based(Classical+Generative) CTGAN 0.9538±0.0003 0.9607±0.0007 High utility and stability. Robust ar-
chitectural performance on continuous
flows.
GANBLR++ 0.5378±0.0665 0.5843±0.0418 Extremeutilitylosscoupledwithcatas-
trophic architectural instability (high
SD).
CopulaGAN 0.9755±0.0005 0.9756±0.0005 Optimal Performance Frontier Model.
Highest generative utility and superior
stability.
CASTGAN 0.9734±0.0005 0.9737±0.0004 Highutilityandstability.Architectural
failure(DS:No)indicatesCompromise.
Note:TheTRTRBaselineforthisdatasetisAccuracy=0.9995,F1=0.9995.AllTSTRmethodsshowedastatisticallysignificantdifferenceagainst
theTRTRBaseline(p<0.0001).TheMean±SDvaluesquantifytheutilityandstabilityacross20repetitions.
’pass/fail’criteriaforgenerativevalidity,goingbeyond the synthesized data not only represents static prop-
the descriptive PD Difference. erties but also realistic temporal patterns of evolving
• ArchitecturalAdaptationforDataDynamics:Given threats.
the rapid evolution of attack vectors, future gener-
ative architectures must adapt to data dynamic fea- C. LARGESCALESIMULATION
tures—featuresthatchangerapidlyovertime(e.g.,flow The scalability barriers identified for Diffusion Models
rate,packetpersecond).Thisrequiresexploringhybrid necessitate technical solutions for real-world security de-
sequential-tabular models that can incorporate time- ployment.
seriesmodeling(e.g.,TransformersorLSTMs)intothe
• Optimizing Iterative Architectures for Tabular
conditional generation process of GANs, ensuring that
Data: A deep scientific investigation is required to
VOLUME11,2023 15

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
optimize the iterative denoising kernel of Diffusion ACKNOWLEDGMENT
Models (TABDDPM). This research should focus on The work presented here was mainly financed by the Eu-
replacing or modifying the Gaussian diffusion process ropean Celtic+ and Swedish Vinnova project (C2022/1-3)"
withakernelspecificallyadaptedfordiscreteormixed- CISSAN – Collective Intelligence Supported by Security
typetabulardata,potentiallybyleveraginghierarchical Aware Nodes.
structures or quantization methods to reduce the enor-
mous computational cost associated with the current REFERENCES
application of continuous domain diffusion to tabular
[1] A.Shahraki,M.Abbasi,A.Taherkordi,andA.D.Jurcut,“Acomparative
spaces. studyononlinemachinelearningtechniquesfornetworktrafficstreams
• AdaptiveIDSArchitecturalIntegration:Futurework analysis,”ComputerNetworks,vol.207,p.108836,2022.
[2] J.L.Guerra,C.Catania,andE.Veas,“Datasetsarenotenough:Challenges
should focus on operationalizing the Architectural Se-
inlabelingnetworktraffic,”Computers&Security,vol.120,p.102810,
lection Framework by building an Adaptive Intrusion 2022.
IDS where the generative model (e.g., CTGAN) is an [3] S.Layeghy,M.Gallagher,andM.Portmann,“Benchmarkingthebench-
mark—comparingsyntheticandreal-worldnetworkidsdatasets,”Journal
integratedcomponentoftheMLpipeline.Thisinvolves
ofInformationSecurityandApplications,vol.80,p.103689,2024.
designing a system where the IDS dynamically moni- [4] A.Kotal,A.Piplai,S.S.L.Chukkapalli,andA.Joshi,“Privetab:Secure
torsitsperformancedriftandautomaticallytriggersthe and privacy-preserving sharing of tabular data,” in Proceedings of the
2022ACMonInternationalWorkshoponSecurityandPrivacyAnalytics,
generationofnew,balanced,andhigh-fidelitysynthetic
pp.35–45,2022.
data for retraining, effectively making the IDS self- [5] D. Ganji and C. Chakraborttii, “Towards data generation to alleviate
healing against concept drift and emerging threats. privacy concerns for cybersecurity applications,” in 2023 IEEE 47th
AnnualComputers,Software,andApplicationsConference(COMPSAC),
pp.1447–1452,IEEE,2023.
VIII. CONCLUSION [6] I.H.Sarker,A.Kayes,S.Badsha,H.Alqahtani,P.Watters,andA.Ng,
This study presented an architectural selection framework “Cybersecuritydatascience:anoverviewfrommachinelearningperspec-
forsyntheticnetworktrafficgeneration,systematicallyeval- tive,”JournalofBigdata,vol.7,pp.1–29,2020.
[7] M.Arjovsky,S.Chintala,andL.Bottou,“Wassersteingenerativeadversar-
uatingtwelvegenerativemodels,includingStatistical,VAE,
ialnetworks,”inInternationalconferenceonmachinelearning,pp.214–
GAN,andDiffusionarchitectures,acrossheterogeneousnet- 223,PMLR,2017.
workdatasets(categorical-heavyNSL-KDDandcontinuous [8] Y. N. Rao and K. Suresh Babu, “An imbalanced generative adversarial
network-basedapproachfornetworkintrusiondetectioninanimbalanced
flow-heavy CIC-IDS2017). The findings demonstrate that
dataset,”Sensors,vol.23,no.1,p.550,2023.
model-data structural compatibility is the key determinant [9] Z.Lin,Y.Shi,andZ.Xue,“Idsgan:Generativeadversarialnetworksfor
of generative performance. Among the evaluated methods, attackgenerationagainstintrusiondetection,”inPacific-asiaconference
onknowledgediscoveryanddatamining,pp.79–91,Springer,2022.
GAN-based models, particularly CTGAN and CopulaGAN,
[10] N.Sivaroopan,C.Madarasingha,S.Muramudalige,G.Jourjon,A.Jaya-
consistently achieved the best balance between fidelity and sumana,andK.Thilakarathna,“Synig:syntheticnetworktrafficgeneration
utility, showing strong architectural adaptability across both throughtimeseriesimaging,”in2023IEEE48thConferenceonLocal
ComputerNetworks(LCN),pp.1–9,IEEE,2023.
dataset types. In contrast, statistical models compromised
[11] A.FigueiraandB.Vaz,“Surveyonsyntheticdatageneration,evaluation
structural integrity for class balance (low fidelity), while methodsandgans,”Mathematics,vol.10,no.15,p.2733,2022.
diffusion-based models, despite high fidelity, suffered from [12] M.Tavallaee,E.Bagheri,W.Lu,andA.A.Ghorbani,“Adetailedanalysis
ofthekddcup99dataset,”in2009IEEEsymposiumoncomputational
prohibitivecomputationalcosts,limitingtheirscalabilityfor
intelligenceforsecurityanddefenseapplications,pp.1–6,Ieee,2009.
largenetworktraffic.Theproposedframeworkoffersaction- [13] I.Sharafaldin,A.H.Lashkari,A.A.Ghorbani,etal.,“Towardgenerating
able guidance for practitioners to select suitable generative anewintrusiondetectiondatasetandintrusiontrafficcharacterization.,”
architecturesbasedondatasetstructureanddeploymentcon-
ICISSp,vol.1,pp.108–116,2018.
[14] R. Shi, Y. Wang, M. Du, X. Shen, Y. Chang, and X. Wang, “A com-
straints, thereby contributing to more efficient and reliable
prehensive survey of synthetic tabular data generation,” arXiv preprint
synthetic traffic generation for cybersecurity applications. arXiv:2504.16506,2025.
Future research should extend this evaluation to temporal [15] M.C.Stoian,E.Giunchiglia,andT.Lukasiewicz,“Asurveyontabular
datageneration:Utility,alignment,fidelity,privacy,andbeyond,”arXiv
and multimodal datasets, incorporate adaptive model–data
preprintarXiv:2503.05954,2025.
matching mechanisms, and investigate optimization strate- [16] O.H.Abdulganiyu,T.A.Tchakoucht,Y.K.Saheed,andH.A.Ahmed,
gies to enhance the scalability of diffusion-based models. “Xidintfl-vae: Xgboost-based intrusion detection of imbalance network
trafficviaclass-wisefocallossvariationalautoencoder,”TheJournalof
Supercomputing,vol.81,no.1,pp.1–38,2025.
SUPPLEMENTARYMATERIAL [17] D.Wang,Y.Huang,W.Ying,H.Bai,N.Gong,X.Wang,S.Dong,T.Zhe,
Supplementary files are provided to support the findings K.Liu,M.Xiao,etal.,“Towardsdata-centricai:Acomprehensivesurvey
oftraditional,reinforcement,andgenerativeapproachesfortabulardata
of this study. The complete set of comparison graphs and
transformation,”arXivpreprintarXiv:2501.10555,2025.
supporting analysis is available as a separate single PDF [18] A.S.Dina,A.Siddique,andD.Manivannan,“Effectofbalancingdata
document. usingsyntheticdataontheperformanceofmachinelearningclassifiers
for intrusion detection in computer networks,” IEEE Access, vol. 10,
• S1: Complete Probability Distribution Comparison for pp.96731–96747,2022.
NSL-KDD Dataset [19] N.V.Chawla,K.W.Bowyer,L.O.Hall,andW.P.Kegelmeyer,“Smote:
• S2: Complete Probability Distribution Comparison for syntheticminorityover-samplingtechnique,”Journalofartificialintelli-
genceresearch,vol.16,pp.321–357,2002.
CIC-IDS2017 Dataset
[20] H.He,Y.Bai,E.A.Garcia,andS.Li,“Adasyn:Adaptivesyntheticsam-
• S3: Correlation Heatmaps for CIC-IDS2017 Dataset plingapproachforimbalancedlearning,”in2008IEEEinternationaljoint
16 VOLUME11,2023

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
conferenceonneuralnetworks(IEEEworldcongressoncomputational [43] C. E. Shannon, “A mathematical theory of communication,” The Bell
intelligence),pp.1322–1328,Ieee,2008. systemtechnicaljournal,vol.27,no.3,pp.379–423,1948.
[21] C.Chokwitthaya,Y.Zhu,S.Mukhopadhyay,andA.Jafari,“Applyingthe [44] I.GuyonandA.Elisseeff,“Anintroductiontovariableandfeatureselec-
gaussianmixturemodeltogeneratelargesyntheticdatafromasmalldata tion,”Journalofmachinelearningresearch,vol.3,no.Mar,pp.1157–
set,”inConstructionResearchCongress2020,pp.1251–1260,American 1182,2003.
SocietyofCivilEngineersReston,VA,2020. [45] L.Breiman,“Randomforests,”Machinelearning,vol.45,pp.5–32,2001.
[22] L.N.Martins,F.B.Gonçalves,andT.P.Galletti,“Generationandanalysis [46] D.Stiawan,M.Y.B.Idris,A.M.Bamhdi,R.Budiarto,etal.,“Cicids-2017
ofsyntheticdataviabayesiannetworks:arobustapproachforuncertainty dataset feature analysis with information gain for anomaly detection,”
quantificationviabayesianparadigm,”arXivpreprintarXiv:2402.17915, IEEEAccess,vol.8,pp.132911–132921,2020.
2024. [47] R.Mahto,S.U.Ahmed,R.u.Rahman,R.M.Aziz,P.Roy,S.Mallik,
[23] R.Challagundla,M.Dorodchi,P.Wang,andM.Lee,“Synthetictabular A. Li, and M. A. Shah, “A novel and innovative cancer classification
data generation: A comparative survey for modern techniques,” arXiv frameworkthroughaconsecutiveutilizationofhybridfeatureselection,”
preprintarXiv:2507.11590,2025. BMCbioinformatics,vol.24,no.1,p.479,2023.
[24] H. Koubeissy, A. Amine, M. Kamradt, and A. Makhoul, “Survey on [48] X. Zhang, X.-M. Zhao, K. He, L. Lu, Y. Cao, J. Liu, J.-K. Hao, Z.-
tabulardataprivacyandsyntheticdatagenerationinindustry4.0,”Applied P. Liu, and L. Chen, “Inferring gene regulatory networks from gene
Intelligence,vol.55,no.13,p.935,2025. expressiondatabypathconsistencyalgorithmbasedonconditionalmutual
[25] S.Bourou,A.ElSaer,T.-H.Velivassaki,A.Voulkidis,andT.Zahariadis, information,”Bioinformatics,vol.28,no.1,pp.98–104,2012.
“Areviewoftabulardatasynthesisusinggansonanidsdataset,”Informa- [49] J. Hua, W. D. Tembe, and E. R. Dougherty, “Performance of feature-
tion,vol.12,no.09,p.375,2021. selectionmethodsintheclassificationofhigh-dimensiondata,”Pattern
[26] A. Kiran and S. S. Kumar, “A comparative analysis of gan and vae Recognition,vol.42,no.3,pp.409–424,2009.
basedsyntheticdatageneratorsforhighdimensional,imbalancedtabular [50] H.Peng,F.Long,andC.Ding,“Featureselectionbasedonmutualinfor-
data,”in20232ndInternationalConferenceforInnovationinTechnology mationcriteriaofmax-dependency,max-relevance,andmin-redundancy,”
(INOCON),pp.1–6,IEEE,2023. IEEETransactionsonpatternanalysisandmachineintelligence,vol.27,
[27] D.AnshelevichandG.Katz,“Synthetictabulardatagenerationusinga no.8,pp.1226–1238,2005.
vae-ganarchitecture,”Knowledge-BasedSystems,p.113997,2025. [51] K.ChurchandP.Hanks,“Wordassociationnorms,mutualinformation,
[28] L.Xu,M.Skoularidou,A.Cuesta-Infante,andK.Veeramachaneni,“Mod- andlexicography,”Computationallinguistics,vol.16,no.1,pp.22–29,
elingtabulardatausingconditionalgan,”Advancesinneuralinformation 1990.
processingsystems,vol.32,2019. [52] M.Wolf,J.Tritscher,D.Landes,A.Hotho,andD.Schlör,“Benchmarking
[29] I.Gulrajani,F.Ahmed,M.Arjovsky,V.Dumoulin,andA.C.Courville, ofsyntheticnetworkdata:Reviewingchallengesandapproaches,”Com-
“Improvedtrainingofwassersteingans,”Advancesinneuralinformation puters&Security,p.103993,2024.
processingsystems,vol.30,2017. [53] S.C.-H.Yang,B.Eaves,M.T.Schmidt,K.B.Swanson,andP.Shafto,
[30] A. Alshantti, D. Varagnolo, A. Rasheed, A. Rahmati, and F. Westad, “Structuredevaluationofsynthetictabulardata,”2023.
“Castgan: Cascaded generative adversarial network for realistic tabular [54] A.KiranandS.S.Kumar,“Amethodologyandanempiricalanalysisto
datasynthesis,”IEEEAccess,2024. determinethemostsuitablesyntheticdatagenerator,”IEEEAccess,2024.
[31] T. J. Anande, S. Al-Saadi, and M. S. Leeson, “Generative adversarial [55] A.F.Karr,C.N.Kohnen,A.Oganian,J.P.Reiter,andA.P.Sanil,“A
networksfornetworktrafficfeaturegeneration,”InternationalJournalof frameworkforevaluatingtheutilityofdataalteredtoprotectconfidential-
ComputersandApplications,vol.45,no.4,pp.297–305,2023. ity,”TheAmericanStatistician,vol.60,no.3,pp.224–232,2006.
[32] L. D. Manocchio, S. Layeghy, and M. Portmann, “Flowgan-synthetic [56] M.Pereira,M.Kshirsagar,S.Mukherjee,R.Dodhia,J.LavistaFerres,and
networkflowgenerationusinggenerativeadversarialnetworks,”in2021 R.deSousa,“Assessmentofdifferentiallyprivatesyntheticdataforutility
IEEE24thInternationalConferenceonComputationalScienceandEngi- andfairnessinend-to-endmachinelearningpipelinesfortabulardata,”
neering(CSE),pp.168–176,IEEE,2021. Plosone,vol.19,no.2,p.e0297271,2024.
[33] Y. Yin, Z. Lin, M. Jin, G. Fanti, and V. Sekar, “Practical gan-based [57] Y.Zhang,N.Zaidi,J.Zhou,andG.Li,“Interpretabletabulardatagenera-
syntheticipheadertracegenerationusingnetshare,”inProceedingsofthe tion,”KnowledgeandInformationSystems,vol.65,no.7,pp.2935–2963,
ACMSIGCOMM2022Conference,pp.458–472,2022. 2023.
[34] C.Yang,D.Xu,andX.Ma,“Researchonthesimulationmethodofhttp [58] P.Thölke,Y.-J.Mantilla-Ramos,H.Abdelhedi,C.Maschke,A.Dehgan,
trafficbasedongan,”AppliedSciences,vol.14,no.5,p.2121,2024. Y. Harel, A. Kemtur, L. M. Berrada, M. Sahraoui, T. Young, et al.,
[35] G.Bovenzi,F.Cerasuolo,D.Ciuonzo,D.DiMonda,I.Guarino,A.Mon- “Classimbalanceshouldnotthrowyouoffbalance:Choosingtheright
tieri,V.Persico,andA.Pescapé,“Mappingthelandscapeofgenerativeai classifiersandperformancemetricsforbraindecodingwithimbalanced
innetworkmonitoringandmanagement,”IEEETransactionsonNetwork data,”NeuroImage,vol.277,p.120253,2023.
andServiceManagement,2025. [59] E.R.FernandesandA.C.deCarvalho,“Evolutionaryinversionofclass
[36] M. A. Rahman, G. A. Francia, and H. Shahriar, “Leveraging gans for distribution in overlapping areas for multi-class imbalanced learning,”
syntheticdatagenerationtoimproveintrusiondetectionsystems,”Journal InformationSciences,vol.494,pp.141–154,2019.
ofFutureArtificialIntelligenceandTechnologies,vol.1,no.4,pp.429–
439,2025.
[37] A.Kotelnikov,D.Baranchuk,I.Rubachev,andA.Babenko,“Tabddpm:
Modellingtabulardatawithdiffusionmodels,”inInternationalConfer-
enceonMachineLearning,pp.17564–17579,PMLR,2023.
DURE ADAN AMMARA is a Ph.D. student
[38] N. Sivaroopan, D. Bandara, C. Madarasingha, G. Jourjon, A. P. Jaya-
sumana, and K. Thilakarathna, “Netdiffus: Network traffic generation in the Department of Computer Science at the
bydiffusionmodelsthroughtime-seriesimaging,”ComputerNetworks, BlekingeInstituteofTechnology(BTH)inSwe-
vol.251,p.110616,2024. den.AdanholdsaBachelorofScience(B.S.)in
[39] M.Villaizán-Vallelado,M.Salvatori,C.Segura,andI.Arapakis,“Diffu- Mathematics and a Master of Science (M.S.) in
sionmodelsfortabulardataimputationandsyntheticdatageneration,” ComputationalScienceandEngineeringfromthe
ACMTransactionsonKnowledgeDiscoveryfromData,vol.19,no.6, National University of Sciences and Technology
pp.1–32,2025. (NUST) in Pakistan, where he was awarded the
[40] J.Shi,M.Xu,H.Hua,H.Zhang,S.Ermon,andJ.Leskovec,“Tabdiff: President’sGoldMedalforacademicexcellence.
amixed-typediffusionmodelfortabulardatageneration,”arXivpreprint HisresearchfocusesonapplyingGenerativeAI,
arXiv:2410.20626,2024. specificallyGenerativeAdversarialNetworks(GANs),togeneratesynthetic
[41] H.Zhang,J.Zhang,B.Srinivasan,Z.Shen,X.Qin,C.Faloutsos,H.Rang- networktrafficandsmartgrid-basedSupervisoryControlandDataAcqui-
wala,andG.Karypis,“Mixed-typetabulardatasynthesiswithscore-based
sition (SCADA) data. This research aims to enhance Intrusion Detection
diffusioninlatentspace,”arXivpreprintarXiv:2310.09656,2023.
Systems within the context of smart grid cybersecurity. It is part of the
[42] X.Lu,X.Ye,andY.Cheng,“Anoverlappingminimization-basedover-
EU-CISSAN (Celtic Next) project dedicated to advancing cybersecurity
sampling algorithm for binary imbalanced classification,” Engineering
solutionsforIoT-drivensmartgrids.
ApplicationsofArtificialIntelligence,vol.133,p.108107,2024.
VOLUME11,2023 17

Authoretal.:PreparationofPapersforIEEETRANSACTIONSandJOURNALS
JIANGUODINGreceived his Doctorate in En-
gineering (Dr.-Ing.) from the faculty of mathe-
maticsandcomputerscienceattheUniversityof
Hagen, Germany. He is currently an Associate
ProfessorattheDepartmentofComputerScience,
Blekinge Institute of Technology, Sweden. His
research interests include cybersecurity, critical
infrastructureprotection,intelligenttechnologies,
blockchain,distributedsystemsmanagementand
control,andseriousgames.HeisaSeniorMem-
beroftheIEEE(SM’11)andaSeniorMemberoftheACM(SM’20).
KURTTUTSCHKUisaprofessorforTelecom-
munication Systems at the Blekinge Institute of
Technology (BTH). Prior to BTH, Kurt had the
Chair of Future Communication at the Univ. of
Vienna(2008to2013)andworkedattheNational
Inst. for Inform. and Comm. Tech. (NIST) in
Tokyo.HehasaPh.D.inCS(’99)andaHabilita-
tion(’08)fromtheUniversityofWürzburg,DE.
Kurt’s research focuses on efficient and secure
architectures and operations of the future. soft-
warizedandsmartnetworksandinfrastructures(incl.NFV,SDN,Clouds,
SmartGrids, and networked services). He has specialised in their orches-
tration, performance, and security using technologies, like marketplaces,
Blockchains,anddistributedAI.Lately,KurtisaddressingthetopicsofXR,
dataprivacyanddigitalsovereignty,secureIoTcontrolloops,andtheuseof
generativeAIinnetworksecurity.Hewasoristheprimaryinvestigatorfor
multiple national and international projects (H2020 Bonseyes/BonsAPPs,
HorizonEurope dAIedge, Vinnova/Celtic+ CISSAN, KKS profile HINTS
&KKSHÖGSymphony).HeisalsothedirectorofstudiesoftheSwedish
IndustrialGraduateSchoolforCybersecurity.KurtservedasGeneralChair
oftheIEEENFV-SDNconferencefrom2017to2022.
18 VOLUME11,2023
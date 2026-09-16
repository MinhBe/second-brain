MULTI-AGENTHONEYPOT-BASEDREQUEST-RESPONSECONTEXTDATASETFOR
IMPROVEDSQLINJECTIONDETECTIONPERFORMANCE
HaoYu1,HuiLi1∗,FengYuanShi1,WenjieYu1,PinHanHo2,ZehuaWang3,BinWang1∗
1SchoolofElectronicandComputerEngineering,PekingUniversity
2DepartmentofElectricalandComputerEngineering,TheUniversityofWaterloo
3DepartmentofElectricalandComputerEngineering,TheUniversityofBritishColumbia
ABSTRACT Recentadvancesinmachinelearningandlargelanguage
models [6] have significantly improved SQLi detection by
SQL injection remains a major threat to web applica-
capturing payload semantics, outperforming rule-based sys-
tions, as existing defenses often fail against obfuscation and
temsandsignature-drivendefenses[7]. However,mostML-
evolving attacks because of neglecting the request-response
baseddetectorsstillsufferfromacriticalflaw: theyprioritize
context. This paper presents a context-enriched SQL injec-
the analysis of isolated payloads while neglecting the bidi-
tion detection framework, focusing on constructing a high-
rectional context of HTTP request-response pairs [8]. This quality request-response dataset via a multi-agent honeypot
oversightmeanstheycannotfullyexploitcriticalsignalslike
system: the Request Generator Agent produces diverse ma-
responselatency,statuscodes,orserver-generatederrortext,
licious/benignrequests, theDatabaseResponseAgentmedi-
all of which are essential for distinguishing successful SQLi
atesinteractionstoensureauthenticresponseswhileprotect-
frombenignqueriesorfailedattackattempts, andforgener-
ing production data, and the Traffic Monitor pairs requests
alizingtounseenobfuscatedattacktechniques.
with responses, assigns labels, and cleans data, yielding to-
To address this context gap, we build a high-quality
tally 140,973 labeled pairs with contextual cues absent in
request-response dataset via a multi-agent honeypot system:
payload-onlydata. Experimentsshowthatmodelstrainedon
the Request Generator Agent generates diverse malicious
this context dataset outperform payload-only counterparts:
and benign traffic to simulate real-world attack scenarios,
CNNandBiLSTMachieveover40%accuracyimprovement
theDatabaseResponseAgentmediatesinteractionstoensure
indifferenttasks,validatingthattherequest-responsecontext
authentic server responses while safeguarding production
enhancesthedetectionofevolvingandobfuscatedattacks.
datathroughshadowdatabaseisolation,andtheTrafficMon-
Index Terms— SQLi detection, request-response con-
itor Agent pairs requests with responses, assigns precise
text,agent,webapplicationsecurity
labels, andcleansdata—ultimatelyyielding140,973labeled
pairs that include contextual cues. We further validate that,
1. INTRODUCTION by providing comprehensive semantic cues absent in tradi-
tional payload-only corpora, this context-rich dataset acts
SQLinjection(SQLi)remainsoneofthemostcriticalthreats as the foundation for enhancing model performance and en-
towebapplications,enablingadversariestobypassauthenti- ablesmoreaccurateidentificationofbothknownandemerg-
cation, exfiltrate sensitive data, or gain persistent control of ing SQLi attacks. This work emphasizes that the request-
back-endsystems[1]. Despitelong-standingmitigationtech- response context is not merely an auxiliary feature but a
niquessuchasinputvalidation[2],parameterizedqueries[3], core enabler of effective SQLi detection, and that a well-
and Web Application Firewalls (WAFs) [4], SQLi continues constructed context dataset is critical for bridging the gap
to rank among the OWASP Top Ten vulnerabilities [5]. A between existing defenses and the demands of real-world
commonshortcomingofprevailingdefensesistheirfocuson attackscenarios.
isolated inputs or pre-defined signatures, neglecting the se-
manticalignmentbetweenuserrequestsandserverresponses
2. RELATEDWORK
thatoftenrevealsattacksuccess,suchasdatabaseerrormes-
sages or anomalous outputs. As a result, these defenses are
2.1. TraditionalMethods
increasinglyinsufficientagainstobfuscatedattacks, dynamic
queryconstruction,andrapidlyevolvingattackvectors. TraditionalSQLinjectiondefensesmainlyrelyoninputval-
idation, parameterized queries, the principle of least privi-
*Correspondingauthor. ThisworkissupportedbyGuangdongProvin-
lege,andinputfiltering. Inputvalidationandfilteringrestrict
cial Laboratory of Ultra High Defnition Immersive Media Technology
(GrantNo.2024B1212010006) maliciouscharactersandmalformedinputs,whileparameter-
6202
raM
3
]RC.sc[
1v36920.3062:viXra

ized queries bind user inputs to prevent query manipulation databasesignals, replicatingattackers’trial-and-errorbehav-
[9,10,11]. Theprincipleofleastprivilegefurtherlimitspo- ior. Tosupportthisadaptivegenerationprocess, theagentis
tential damage by restricting database access [12]. In addi- equippedwiththreededicatedtools:
tion,lexicalandsyntacticanalysismethodsdetectSQLinjec-
tionbyparsingquerystructuresandpatterns[13]. Although • Multi-techniqueInjectionGenerator: Preconfigured
theseapproachesarestraightforwardtodeploy,theytypically with templates covering all common SQL injection
dependonpredefinedrulesorsignaturesandrequirefrequent techniques. Theagentinvokesthistooltogeneratetar-
updatestohandleevolvingattacktechniques. geted requests, ensuring coverage of diverse injection
modeswithoutover-relianceonasingletype.
2.2. MachineLearningMethods • Cross-Database Adapter: Stores syntax rules for
major relational databases including MySQL, Post-
Recent studies have explored machine learning and deep
greSQL, Oracle, SQLite, SQL Server, and MariaDB.
learning techniques for SQL injection detection. Early ap-
The agent uses this tool to adjust payload syntax, en-
proachesformulateSQLidetectionasaclassificationproblem
abling compatibility with different database environ-
based on handcrafted features extracted from query strings
ments.
[14]. More recently, pre-trained language models such as
BERT have been adopted to capture deeper semantic rep- • Adversarial Evasion Simulator: Integrates common
resentations of SQL queries, achieving improved detection obfuscation, encoding, and semantic variation tech-
performance [15]. BERT-based semantic embedding and niques. The agent calls this tool to introduce mod-
scoringmethodsfurtherimprovethediscriminationbetween ifications to base payloads, mimicking the evasion
benignandmaliciousqueries[16,7].Despitetheseadvances, strategiesemployedbyrealattackers.
most existing methods focus on isolated query payloads and
largely overlook the broader contextual signals available in All generated requests X Req are passed to the Database
real-worldsystems. ResponseAgenttogetherwiththeirassociatedinjectionintent
To address similar limitations in other security domains, fordownstreamexecution.
recent work has explored multi-agent collaborative frame-
works that integrate complementary contextual signals. For 3.2. DatabaseResponseAgent
example, Argus demonstrates that multi-agent collaboration
TheDatabaseResponseAgentmediatesinteractionsbetween
caneffectivelyreducefalsepositivesincomplexsecurityde-
generated requests and backend databases. Under the injec-
tection tasks, motivating the use of multi-agent systems to
tion intent specified upstream, this agent makes execution-
movebeyondsingle-viewanalysis[17].
level decisions through its associated tools, shaping how re-
questsareprocessedandhowresponsebehaviorsemerge.
3. DATASETBUILDINGFRAMEWORK
• Multi-DBConnector:Integratesnativedriversforvar-
To construct a contextualized SQL-injection dataset suitable ious Relational Database Management Systems. The
for training and evaluation, we designed a multi-agent hon- agent uses this tool to establish connections with tar-
eypot framework, as shown in Fig.1. The framework de- getdatabases,ensuringthatthedatabaseresponsesare
composesthedatacollectionprocessintothreegoal-oriented authenticandconsistentwithreal-systembehavior.
agentsthatcollaboratethroughautonomousdecision-making
• ShadowDatabaseIsolator: Implementsroutingrules
andfeedback-driven interaction, rather thanstatic functional
thatforwardallrequeststocloned”shadowdatabases”
modules. The agents jointly form a closed-loop process in
(with identical structures to production databases) in-
whichrequestgeneration,databaseexecution,anddataqual-
steadofrealbusinessdatabases. Thistoolprotectspro-
itycontroliterativelyinfluenceeachother,enablingadaptive
ductiondatafromdestructivequerieswhilepreserving
optimizationoftrafficrealismandlabelingconsistency.
genuinedatabasefeedback.
3.1. RequestGeneratorAgent • High-AvailabilityLoadBalancer: Managesapoolof
shadow database replicas. The agent invokes this tool
TheRequestGeneratorAgentproducesdiversemaliciousand todistributeincomingrequestsacrossreplicas,prevent-
benign HTTP requests. Rather than relying on fixed tem- ing service disruption under high attack loads and en-
plates, it constructs attack payloads based on OWASP Top suringstabletrafficprocessing.
10SQLicategories,recentCVEvulnerabilities,andpatterns
observed in mainstream penetration testing tools. It adapts After processing each request, the agent provides the re-
payloadsyntaxviaDatabaseResponseAgentfeedback(Sec- quest X with its database response X to the Traffic
Req Resp
tion 3.2) and optimizes evasion strategies based on shadow MonitorAgentfordownstreaminterpretation.

Request Generator Agent Database Response Agent Traffic Monitor Agent
Builds diverse requests Interacts with database Organizes dataset
Multi-technique Injection Generator Multi-DB Connector Context Pairer Ground-Truth Labeler
Boolean-Based1 r ' e a g n e d x d p a ' t ^ a 1 b ' a - s - e + () Union-Based(s - e 1 le ' c u t n u io s n er s ( e )) l , e ( c s t e l 1 e , ct Request Request Request Packet 2️⃣ E 0️⃣ rro B r- e B n a i s g e n d 1️⃣ 3️⃣ B In o l o i l n e e a n 4️⃣ -Ba S se ta d cked
version())--+ HTTP request: 5️⃣ Time-Based 6️⃣ Union-Based
GET/MySQL/getUserkey=
MySQL C CO r N o ' C W s A s o - T r D l ( d 'H ') a e t ll a o' b ,S as Q e L A S d e a rv p e t r er 'Hello' + 'World' Shad I o s w o l D at a o t r abase High-A B va a i l l a a n b c i e li r ty Load Response 1 M R % I e D 2 s 7 % p % 2 o 2 8 n 0 % A s 2 e N 8 D S P E % a L 2 c E 0 k C O e T R t .. D . %28 Dataset C s u pl r it ator
training
HTTP response:
Adversarial Evasion Simulator (200 None) Cleaned Dataset
Shadow Database URI:http://localhost... clean validation
SelEcT u s i e d r s FROM F S R E O L M EC u T s e id rs S F E R L O EC M T / / * * * * / / u i s d e /* rs */ Backend Database Backend Databases k { ," " e u i y s d = e " r 1 : n 1 % a ," m 2 p 7 a e % s " s : 2 " w D 0 o A u rd m N " b D :" " . D } .. umb" Conte L x a t b P e a l ir Raw Dataset test
Fig.1. Thisgraphshowstheframeworkofdatacollectingprocedure.
3.3. TrafficMonitorAgent 3.4. Request-ResponseContextDataset
The Traffic Monitor Agent transforms raw traffic into struc- Afterdatacleaning,theframeworkproduced140,973request-
tured,readydatabyinterpretingobservedresponsesimposed response pairs in total, each annotated with an integer label
byupstreamagentsthroughsequentiallyinvokingthefollow- (0–6) denoting injection type (benign, boolean-based, error-
ingtools. based, inline, stacked, time-based blind, or union-based).
Eachrecordcontains:
• ContextPairerTMon: Usesmetadata,suchassession
1
IDs and timestamps, to pair HTTP requests from the
• Request-ResponsePair:Combinedrequestandmatch-
RequestGeneratorAgentwithcorrespondingserverre-
ing server responses, retaining semantic hints about
sponses from the Database Response Agent, eliminat-
attack success, since responses frequently contain in-
ing mismatches between requests and responses. For-
dicators such as error logs, response delays, or status
mally, the Context Pairer outputs a request-response
codesthatareabsentinpayload-onlydatasets.
pairas
X Pair =T 1 Mon(X Req ,X Resp ) (1) • Label: Basedontheinjectedtechnique.
• Ground-Truth Labeler TMon: Maps injection tech-
2 This dataset focuses on the importance of bidirectional
niquesfromthetoolconfigurationsoftheRequestGen-
context.Suchcontextualfeaturessignificantlyenhancemodel
eratorAgenttointegerlabels. Theagentusesthistool
generalization,asvalidatedinoursubsequentexperiments.
to assign accurate labels to paired records, ensuring
alignment with real attack categories. Formally, the
ContextPaireroutputsalabelas 4. EVALUATIONANDANALYSIS
Y =TMon(X ), y ∈{0,1,...,6} (2)
2 Pair 4.1. ModelSelection
• Dataset Curator T 3 Mon: A data processing module In real-world deployment scenarios, SQL injection detec-
dedicatedtorefininglabeledrequest-responsepairsinto tion systems must operate under strict latency constraints,
a high-quality dataset. This tool performs data clean- which imposes significant performance requirements on de-
ingbyremovingcorruptedrecords(e.g.,incompletere- tection models [18]. While large-scale neural networks de-
sponsescausedbynetworkinterruptions)andduplicate liverhighdetectionaccuracy,theirsubstantialcomputational
entries,bothofwhichhelpeliminatenoise. Italsocon- andmemoryoverheadrendersthemimpracticalforreal-time
ductsstratifiedpartitioning,splittingdataintotraining, traffic inspection on commodity hardware or edge devices.
validation,andtestsubsetswhilepreservingthedistri- Lightweight neural network architectures are therefore es-
butionofattackcategoriestoavoidsamplingbias. For- sential to balance throughput and responsiveness—for this
mally,theDatasetCuratoroutputsadatasetas reason,wefirstevaluatefourrepresentativelightweightmod-
D =TMon(X ,Y) (3) els: CNN(ConvolutionalNeuralNetwork),RNN(Recurrent
3 pair
Neural Network), LSTM (Long Short-Term Memory), and
In conclusion, the Traffic Monitor Agent produces a re- BiLSTM (Bidirectional Long Short-Term Memory). These
questelement: models are selected for their widespread application in se-
D =TMon(cid:0) TMon(cid:0) TMon(X ,X ) (cid:1)(cid:1) (4) quencedataprocessingandtheirinherentefficiency, making
3 2 1 Req Resp them well-suited for resource-constrained deployment envi-
This process yields a semantically consistent request- ronments while still retaining basic capabilities for pattern
responsedataset. recognitioninSQLi-relateddata.

4.2. Datasets or anomalous outputs—that are invisible in payload-only
data.
To validate the role of request-response context in improv-
However,theabsoluteaccuracyoflightweightmodelson
ing SQL injection detection performance, we use two types
the Context dataset remains unsatisfactory. Even with con-
ofdatasetswithdifferentcolornotations: theContextdataset
textualinformation,limited-capacitymodelsstruggletofully
ismarkedas ,andthePayloaddatasetas . Itiscrucial
capturethecomplexityofSQLipatterns. Tofurthervalidate
to emphasize that these two datasets are homologous: both
whether the Context dataset can continue to exert its advan-
are derived from the original traffic generated by the multi-
tages in more advanced experimental settings, we designed
agenthoneypotframeworkdetailedinSection3. Theyshare
additionalexperiments,focusedonverifyingtheeffectiveness
anidenticaldatadistribution,coveringthesamecategoriesof
oftheContextdatasetonknowledgedistillation.
benignrequestsandSQLiattacktypes. Theonlydistinction
lies in their data collection scope: the Context dataset cap-
4.4. Performance of Context Dataset on Knowledge Dis-
tures complete bidirectional request-response context traffic,
tillation
includingrequestpayloads,serverresponseswithandassoci-
ated metadata; in contrast, the Payload dataset only extracts
Knowledgedistillationisastandardtechniqueforimproving
therequestpayloadportionfromthesameoriginaltraffic,ex-
the accuracy of small-scale models, which transfers knowl-
cluding all response-related context information. These two
edge from a high-capacity teacher model to a lightweight
datasetsareappliedintwoclassificationtasksforSQLinjec-
student model. To address the unsatisfactory absolute accu-
tiondetection: the2-classtaskadoptsabinarydivisionlogic,
racy of lightweight models observed in previous evaluations
where label 0 (representing benign traffic) is treated as one
and further verify the effectiveness of the Context dataset in
category, and labels 1–6 (corresponding to all malicious at-
advanced model optimization scenarios, we conduct evalua-
tack types) are merged into a single category of ”malicious
tions on lightweight models enhanced by knowledge distil-
traffic”todistinguishonlybetweenbenignandmalicioustraf-
lation technique. Specifically, we assess the performance of
fic;incontrast,the7-classtasktreatseachofthelabels0–6as
distilledlightweightstudentmodelsacrossdifferentarchitec-
anindependentcategory,furtherclassifyingmalicioustraffic
tures(CNN,RNN,LSTM,BiLSTM)underboth7-classand
intothesixspecificattacktypesmentionedabove.
2-classSQLiclassificationtasks.
4.3. Performance of Context Dataset on Lightweight 2-Class 7-Class
Models 100 10099.9 85.683.3 94.8 83.3 98.8 83.3100 98.697.3 84.1 88.5
75 75 59.8
50 50 35.4 35.3 35.4
2-Class 7-Class
98.3 25 25
10 5 7 0 0 5 57.0 51.6 59.5 69.0 59.6 71.4 60.6 3 4 5 0 0 0 37.2 22.6 43.1 23.4 43.2 35.3 43.1 35.3 0 CNN RNN LSTMBiLSTM 0 CNN RNN LSTMBiLSTM
20
25 10 Fig. 3. Accuracy comparison of knowledge distilled models
0 0
onPayloadvs. Contextdatasets
CNN RNN LSTMBiLSTM CNN RNN LSTMBiLSTM
As shown in Fig.3, on the distilled scenario, models
Fig. 2. Accuracy comparison of traditional models on Pay-
trained on the Context dataset also significantly outperform
loadvs. Contextdatasets
those trained on the Payload dataset. This advantage is
AsshowninFig.2,modelstrainedontheContextdataset particularly notable in the 7-class classification task, where
generally tend to outperform those trained on the Payload BiLSTM achieved a 53.1% improvement, LSTM a 48.8%
datasetinmostcases,eitherbylargeorminormargins,only improvement,andRNNa24.4%improvement.
the RNN has a slight deviation in the 2-class classification
task. However,thissituationisarareedgecaseanddoesnot 5. CONCLUSION
changetheoveralltrendoftheContextdatasetimprovingthe
model’s SQL injection detection performance. Specifically, Thispaperproposedacontext-enrichedSQLinjectiondetec-
CNN showed a 41.3% improvement in 2-class classification tionframeworkbasedonamulti-agenthoneypotsystem. The
task and a 14.6% improvement in 7-class classification task, Request Generator Agent, Database Response Agent, and
and BiLSTM improved by 10.8% in 2-class and 7.8% in 7- Traffic Monitor Agent collaboratively construct a request-
class. response context dataset, capturing semantic cues absent in
This trend holds in both 2-class and 7-class settings, payload-only corpora. Experiments across multiple mod-
demonstratingthatcontextualfeaturesfromserverresponses els demonstrate significant accuracy gains, validating that
providecrucialsignals—suchaserrorcodes,responsedelays, contextualdataisessentialforgeneralizableSQLidetection.

6. REFERENCES [10] Vugar Abdullayev and Alok Singh Chauhan, “Sql in-
jection attack: Quick view,” Mesopotamian journal of
[1] Ignacio Samuel Crespo-Mart´ınez, Adria´n Campazas- Cybersecurity,vol.2023,pp.30–34,2023.
Vega, A´ngel Manuel Guerrero-Higueras, Virginia
Riego-DelCastillo, Claudia A´lvarez-Aparicio, and [11] Santiago Ibarra-Fiallos, Javier Bermejo Higuera,
CaminoFerna´ndez-Llamas, “Sqlinjectionattackdetec- Monserrate Intriago-Pazmin˜o, Juan Ramon Bermejo
tioninnetworkflowdata,” Computers&Security,vol. Higuera, Juan Antonio Sicilia Montalvo, and Javier
127,pp.103093,2023. Cubo, “Effective filter for common injection attacks
in online web applications,” IEEE Access, vol. 9, pp.
[2] Muhammad Saidu Aliero, Imran Ghani, Kashif Naseer 10378–10391,2021.
Qureshi,andMohdFo’adRohani,“Analgorithmforde-
tecting sql injection vulnerability using black-box test- [12] SamuelJero,JulianaFurgala,RunyuPan,PhaniKishore
ing,” Journal of Ambient Intelligence and Humanized Gadepalli, AlexandraClifford, BiteYe, RogerKhazan,
Computing,vol.11,no.1,pp.249–266,2020. Bryan C Ward, Gabriel Parmer, and Richard Skowyra,
“Practicalprincipleofleastprivilegeforsecureembed-
[3] PrinceRoy,RajneeshKumar,andPoojaRani, “Sqlin- dedsystems,”in2021IEEE27thReal-TimeandEmbed-
jectionattackdetectionbymachinelearningclassifier,” ded Technology and Applications Symposium (RTAS).
in 2022 International conference on applied artificial IEEE,2021,pp.1–13.
intelligence and computing (ICAAIC). IEEE, 2022, pp.
[13] Dhruv Mehta, Hartik Suhagiya, Harvy Gandhi, Man-
394–400.
ish Jha, Pratik Kanani, and Aniket Kore, “Sqliml:
[4] Nisrean Thalji, Ali Raza, Mohammad Shariful Islam, A comprehensive analysis for sql injection detection
NagwanAbdelSamee,andMonaMJamjoom, “Ae-net: using multiple supervised and unsupervised learning
Novelautoencoder-baseddeepfeaturesforsqlinjection schemes,” SNComputerScience,vol.4,no.3,pp.281,
attack detection,” IEEE access, vol. 11, pp. 135507– 2023.
135516,2023.
[14] BahmanArasteh,BabakAghaei,BehnoudFarzad,Key-
[5] Mohammed Nasereddin, Ashaar ALKhamaiseh, Malik van Arasteh, Farzad Kiani, and Mahsa Torkamanian-
Qasaimeh, and Raad Al-Qassas, “A systematic review Afshar, “Detectingsqlinjectionattacksbybinarygray
of detection and prevention techniques of sql injection wolfoptimizerandmachinelearningalgorithms,” Neu-
attacks,” Information Security Journal: A Global Per- ral Computing and Applications, vol. 36, no. 12, pp.
spective,vol.32,no.4,pp.252–265,2023. 6771–6792,2024.
[6] Bin Wang, Hui Li, AoFan Liu, BoTao Yang, Ao Yang, [15] Ziyao Liu, “Research on sql injection detection based
YiLuZhong,WeixiangHuang,RunhuaiHuang,Weimin on deep learning,” in 2023 IEEE 7th Information
Zeng, and Yanping Zhang, “Reflexgen: The unexam- Technology and Mechatronics Engineering Conference
ined code is not worth using,” in ICASSP 2025-2025 (ITOEC).IEEE,2023,vol.7,pp.746–749.
IEEE International Conference on Acoustics, Speech
[16] KornSooksatra,BikramKhanal,PabloRivas,andDon-
andSignalProcessing(ICASSP).IEEE,2025,pp.1–5.
ald R Schwartz, “Attribution scores of bert-based sql-
[7] Dongzhe Lu, Jinlong Fei, and Long Liu, “A seman- queryautomaticgradingforexplainability,” in2023In-
ticlearning-basedsqlinjectionattackdetectiontechnol- ternational Conference on Computational Science and
ogy,” Electronics,vol.12,no.6,pp.1344,2023. Computational Intelligence (CSCI). IEEE, 2023, pp.
213–220.
[8] Haifeng Gu, Jianning Zhang, Tian Liu, Ming Hu, Jun-
longZhou,TongquanWei,andMingsongChen,“Diava: [17] Bin Wang, Hui Li, Liyang Zhang, Qijia Zhuang,
a traffic-based framework for detection of sql injection AoYang,DongZhang,XijunLuo,andBingLin, “Ar-
attacksandvulnerabilityanalysisofleakeddata,” IEEE gus: Amulti-agentsensitiveinformationleakagedetec-
TransactionsonReliability,vol.69,no.1,pp.188–202, tionframeworkbasedonhierarchicalreferencerelation-
2019. ships,” arXivpreprintarXiv:2512.08326,2025.
[9] Majid Alshammari, “Deep learning approaches to [18] Sagar Neupane, “Detecting and mitigating sql injec-
sql injection detection: evaluating anns, cnns, and tionvulnerabilitiesinwebapplications,” arXivpreprint
rnns,”inInternationalConferenceonMathematicaland arXiv:2506.17245,2025.
Statistical Physics, Computational Science, Education
and Communication (ICMSCE2023). SPIE, 2023, vol.
12936,pp.131–138.
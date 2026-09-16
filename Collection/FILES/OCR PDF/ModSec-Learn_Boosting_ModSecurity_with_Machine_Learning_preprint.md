ModSec-Learn: Boosting ModSecurity with
Machine Learning
Christian Scano1,2 , Giuseppe Floris2 , Biagio Montaruli3,6 ,
Luca Demetrio4 , Andrea Valenza5 , Luca Compagna3 , Davide Ariu2 ,
Luca Piras2 , Davide Balzarotti6 , and Battista Biggio1,2
1 University of Cagliari, Cagliari, Italy
{battista.biggio,giuseppe.floris}@unica.it
2 Pluribus One, Cagliari, Italy
{davide.ariu,luca.piras}@pluribus-one.it
3 SAP Security Research, Mougins, France
{biagio.montaruli,luca.compagna}@sap.com
4 University of Genova, Genova, Italy
luca.demetrio@unige.it
5 Prima Assicurazioni, Milano, Italy
andrea.valenza@prima.it
6 EURECOM, Biot, France
davide.balzarotti@eurecom.fr
Abstract. ModSecurityiswidelyrecognizedasthestandardopen-source
Web Application Firewall (WAF), maintained by the OWASP Founda-
tion. It detects malicious requests by matching them against the Core
Rule Set (CRS), identifying well-known attack patterns. Each rule is
manually assigned a weight based on the severity of the corresponding
attack,andarequestisblockedifthesumoftheweightsofmatchedrules
exceedsagiventhreshold.However,wearguethatthisstrategyislargely
ineffective against web attacks, as detection is only based on heuristics
andnotcustomizedontheapplicationtoprotect.Inthiswork,weover-
comethisissuebyproposingamachine-learningmodelthatusestheCRS
rules as input features. Through training, ModSec-Learn is able to tune
thecontributionofeachCRSruletopredictions,thusadaptingthesever-
ity level to the web applications to protect. Our experiments show that
ModSec-Learnachievesasignificantlybettertrade-offbetweendetection
and false positive rates. Finally, we analyze how sparse regularization
can reduce the number of rules that are relevant at inference time, by
discardingmorethan30%oftheCRSrules.Wereleaseouropen-source
code and the dataset at https://github.com/pralab/modsec-learn and
https://github.com/pralab/http-traffic-dataset, respectively.
Keywords: WebApplicationFirewalls·MachineLearning·WebSecu-
rity · SQL injection · OWASP ModSecurity Core Rule Set
4202
nuJ
91
]GL.sc[
1v74531.6042:viXra

2 C. Scano et al.
1 Introduction
Web applications are constantly evolving and deployed at a broad scale to offer
a plethora or variegated services, imposing serious challenges in securing them
againstanincreasingnumberofattacks[12].Amongthese,SQLinjection(SQLi)
consists of injecting a malicious SQL code payload inside regular queries, caus-
ing the target web application to either behave in an unintended way or expose
sensitive data. Even if countermeasures to this attack are well known [1,13,14],
the Open Web Application Security Project (OWASP) Foundation still clas-
sifies SQLi as one of the top-10 most dangerous web threats [16]. Thus, Web
ApplicationFirewalls(WAFs)arecommonlyusedasadefensetoolinenterprise
systems [3,1] to counter such attacks and protect web applications. They work
by filtering the incoming requests directed towards the web applications and
blocking suspicious connections. In this work, we focus on ModSecurity [11], an
established open-source WAF solution that builds its defense on top of signa-
turesofwell-knownattacks,collectedbytheOWASPFoundationandknownas
theCoreRuleSet(CRS).TheCRSversionusedinthiswork(4.0.0)includes319
rules, out of which 170 target critical injection attacks [17]. Specifically, SQLi
is the most represented class of injection attack counting 60 rules. All rules are
assigned with an heuristic severity level used to evaluate whether an HTTP re-
quest is malicious or not. Thus, detection is achieved through the summation
of the scores of matched rules, blocking the incoming request if a threshold is
exceeded. However, this setup has three shortcomings: (i) the severity of each
rule is purely heuristic, and it might not reflect the real behavior of the network
to protect; (ii) rules only target attack patterns, but they are not taking into
accountlegitimatenetworktraffic,potentiallyyieldingahighfalsepositiverate;
and (iii) different rules might either interfere with each other, or be redundant.
InthisworkwefirstshowthatthedetectionalgorithmofModSecuritybased
on CRS rules is largely ineffective due to the highlighted limitations. We then
propose ModSec-Learn, a novel machine-learning WAF that uses the CRS rules
asinputfeatures.Inthisway,theseverityscoreofeachruleissubstitutedbythe
weightattributedtothatrulebythemachine-learningmodel,allowingModSec-
Learntotunetheirrelevanceandadaptitselftothewebservicestoprotect.We
test different machine-learning models used to implement ModSec-Learn, and
we compare their predictive performance against ModSecurity, showing that
the detection rate improves more than 45% at 1% false positive rate. Lastly, we
investigatewhetherCRScontainsredundantrules,computingembeddedfeature
selection through ℓ regularization, highlighting that 18 out of 60 rules can be
1
discarded as ModSec-Learn attributes no relevance on them.
2 Background
In this section we provide an overview of SQLi attacks and the OWASP CRS.
SQL Injection (SQLi). It is a family of web threats that aims to retrieve sen-
sitiveinformationfromatargetdatabase,modifydatawithoutauthorization,or

ModSec-Learn: Boosting ModSecurity with Machine Learning 3
even execute privileged operations on the database [2]. This can be achieved via
specificSQLcodefragmentsthatarepassedintheoriginalrequest.Iftheappli-
cationdoesnotsanitizetheuser-providedinputandsimplyconcatenatesitwith
therestofthequery,theSQLfragmentisinterpretedaspartoftheoriginalSQL
command. For example, considering the vulnerable SQL query of Listing 1.1, a
malicious user could inject some SQL fragments in the $user parameter, e.g.,
"admin’–- ",toexfiltrateallthesensitiveinformationoftheprovidedusername.
SELECT * FROM users WHERE username = ’$user’ AND
password = ’$passwd’
Listing 1.1: Example of SQL query vulnerable to SQL injection (SQLi).
ModSecurity. It isan open-source WAFsolution for real-timewebapplication
security monitoring and hardening, which relies on a customizable set of rules
to stop a large variety of web-based threats.
The OWASP Core-Rule-Set (CRS) Project. It is one of the most widely-
used open-source sets of detection rules targeting OWASP Top 10 web security
risks [16]. It is widely adopted both in open-source WAFs like ModSecurity [11]
and Coraza1, as well as in more than ten commercial solutions [17].
Detection Rules.Theyaredesignedtodetectspecifictypesofwebattacks.Each
rule is denoted by a unique identifier representing the specific class of attack it
is intended to identify. Rules are also associated with two notable configuration
parameters, i.e., the Paranoia Level (PL) and severity level.
Paranoia Level.ItisusedtoselectwhichrulesareenabledtoanalyzetheHTTP
requests [17]. The CRS includes four PLs (PL1 - PL4) and each rule is assigned
to a specific PL. Moreover, rules are grouped together by PL in a nested way:
setting a certain PL enables all the rules assigned to that PL, as well as those
assigned to lower PLs. For instance, PL3 enables all the rules related to such
PL, as well as those assigned to PL1 and PL2.
Anomaly Scoring. Each detection rule is heuristically assigned with a severity
level,apositiveintegervaluethatquantifieshowmenacingacapturedrequestis
[17].Tocomputeadecision,ModSecurityappliestherulesonincomingrequests,
anditsumsalltheseveritylevelsofallthematches.Ifsuchasummationexceeds
a threshold, the incoming request is flagged as malicious. In CRS there are four
severity levels: CRITICAL (5), ERROR (4), WARNING (3) and NOTICE (2).
3 Improving Modsecurity with Machine Learning
We now present ModSec-Learn, the main contribution of our work, whose ar-
chitecture is depicted in Fig. 1. ModSec-Learn is built on top of two main com-
ponents: (i) a feature extraction phase that encodes the CRS rules into a vector
representation, and (ii) a machine-learning model that learns how to optimally
combinetheCRSrules.Thisaimstosurpasstheshortcomingofmanuallytuning
the severity levels while keeping the predictive power of the CRS rules.
1 https://coraza.io

4 C. Scano et al.
temp
Benign SQLi Mo O d W C Se R A c S S u P r ity … 1 0 1 𝑥 𝑥 𝑥 … # ! " ML-ba 𝑓 se (𝒙 d ) tuning 𝑓(𝒙) ≥ 𝜃 SQLi Attack
Benign
Fig.1: ModSec-Learn architecture. A machine-learning model is trained using
the CRS rules as input features (52 features) to improve the trade-off between
detectionrateandfalsealarms.Thisamountstolearningamodeloftheincoming
trafficdirectedtowardstheprotectedwebservices.Sparseregularizationcanalso
be used to select a subset of the available rules, instead of using PLs.
Detection Rules as Features.TheinputspaceisrepresentedbySQLqueries
that are classified as malicious or benign by a machine-learning model. Each
SQL query is a string of readable characters, represented as z ∈Z, being Z the
space of all possible queries. Let D be the set of selected SQLi rules from CRS,
and d = |D| its cardinality. We denote with ϕ : Z (cid:55)→ X a function that maps a
SQL query z to a d-dimensional feature vector x = (x ,...,x ) ∈ X = {0,1}d,
1 d
where each feature is set to 1 if the corresponding SQLi rule has been triggered
by the SQL query z, and 0 otherwise. We want to remark that, although in this
paper we focus on rules targeting SQLi attacks, this feature representation can
be applied to any rule within the CRS.
Optimal Combination of CRS Rules with ML. We train three different
machine-learning models on the aforementioned feature set. In particular, we
use two linear models, i.e., Support Vector Machine (SVM) [7] and a Logistic
Regression (LR) [4], using both ℓ and ℓ penalties; and a non-linear Random
2 1
Forest (RF) [5] model. Linear models are especially relevant in this context as
they can be used to automatically tune the severity score to be assigned to each
rule, instead of using the default ModSecurity values. Moreover, when using
sparse (ℓ ) regularization, these models enable us to automatically select the
1
optimal subset of CRS rules to be used, rather than resorting to a predefined
PL.Letusfinallyremarkthatourapproachcanbeappliedtoanylinearandnon-
linear machine-learning model, even if in the non-linear case it would be more
complextointegratethemodelwithintheexistingModSecurityimplementation.
Novel Dataset. We aim to create a novel dataset consisting of legitimate sam-
ples based on real-world traffic as well as a comprehensive set of SQLi pay-
loads. Regarding the legitimate samples, since they are not readily available in
the wild, we collected 508,529 samples provided in the open-appsec dataset2,
which contains legitimate samples from various real-world scenarios. However,
the open-appsec dataset has only 458 SQLi payloads, which means that it is
heavily biased towards legitimate samples. To counter this issue, we augmented
theoriginalSQLipayloaddatasetofopen-appsecusingthefollowingsources:(i)
the HTTP Params dataset3, (ii) a SQLi dataset available on Kaggle4 and (iii)
2 https://github.com/openappsec/waf-comparison-project/tree/main/Data
3 https://github.com/Morzeux/HttpParamsDataset
4 https://www.kaggle.com/datasets/sajid576/sql-injection-dataset/data

ModSec-Learn: Boosting ModSecurity with Machine Learning 5
a new set of SQLi payloads generated through the SQLi testing tool SQLmap5
by executing SQLmap with different tampering scripts designed for payload ob-
fuscation. The final SQLi payload dataset includes 30,543 samples. Finally, we
createdabalanceddatasetbyrandomlyselecting25,000benignand25,000SQLi
samples from the novel dataset to ensure a fair evaluation of ModSecurity and
machine-learning models.
4 Experimental Analysis
We now evaluate both ModSecurity (Sect. 4.2), showing that relying on heuris-
tically assigned weights is suboptimal, and we continue by highlighting how
ModSec-Learn enhances the performances thanks to the adaptation of weights
(Sect. 4.3), while also reducing the number of rules needed (Sect. 4.4).
4.1 Experimental Setup
We now describe the setup underlying our experimental analysis.
Training set (train).Itcontains40,000samplesrandomlychosenfromtheorig-
inal dataset, divided in 20,000 benign and 20,000 SQLi queries to keep the two
classes balanced.
Test set (test).Itcontains10,000samples(5,000benign,and5,000SQLiqueries)
randomlychosenfromtheoriginaldataset.Thisdatasethasnointersectionwith
the training set described above, and we use it to evaluate the performances of
vanilla ModSecurity, and ModSec-Learn at different PLs.
Setup of ModSecurity. We evaluate ModSecurity v3.0.10 with CRS v4.0.0,
using pymodsecurity v0.1.06, which implements Python bindings to interface
with ModSecurity. Since we focus on the detection of SQLi attacks, we only
enabletheSQLirules7.WhiletheCRSconsistsof60rules,only52areactivated
bythesamplesinourtrainingset;thus,wediscardtheremaining8rules.These
52 are also the total number of features used to train models.
ModSec-Learn with SVM, RF, and LR.Weleveragethescikit-learnv1.4.0
[18] implementation of SVM (LinearSVC), RF, and LR to train each ModSec-
Learn model. As for ModSec-Learn SVM and LR, we applied both ℓ and ℓ as
1 2
penalization norms. The saga [8] solver was used to apply both norms to the
LR. We manually tested 5 values for the regularization parameter C of SVM:
{10−3,10−2,10−1,5·10−1,1.0}. After training the SVMs and LRs for each PLs
and penalization norms, we found that 5·10−1 was the optimal value for the
hyper-parameterC.Theotherhyper-parameterswerelefttotheirdefaultvalue.
5 https://sqlmap.org
6 https://github.com/AvalZ/pymodsecurity
7 https://github.com/coreruleset/coreruleset/blob/v4.0.0/rules/
REQUEST-942-APPLICATION-ATTACK-SQLI.conf

6 C. Scano et al.
Table 1: TPR at 1% FPR of ModSec and ModSec-Learn (SVM, RF, and LR)
evaluated on the test sets. For each WAF, we higlight the best results in bold.
PL1 PL2 PL3 PL4
ModSec vanilla 92.50% 75.45% 68.55% 68.55%
ModSec-Learn SVM (ℓ ) 92.50% 99.22% 99.04% 99.02%
1
ModSec-Learn SVM (ℓ ) 92.50% 99.22% 99.04% 99.02%
2
ModSec-Learn LR (ℓ ) 92.50% 99.34% 99.35% 99.35%
1
ModSec-Learn LR (ℓ ) 92.50% 99.34% 99.34% 99.34%
2
ModSec-Learn RF 92.50% 99.41% 99.45% 99.45%
4.2 Evaluation of ModSecurity
The first goal of our experimental analysis is understanding the detection capa-
bilityofthevanillaModSecurity.Ratherthanfocusingonlyonitsdefaultvalues,
weexperimentwithitoveritsentireconfigurationspace,consideringallthepos-
sible values for the PLs and the classification threshold. Hence, for each PL, we
computetheReceiver-Operating-Characteristic(ROC)curve,whichreportsthe
True Positive Rate (TPR, i.e., the fraction of correctly-detected malicious SQLi
requests) against the False Positive Rate (FPR, i.e., the fraction of wrongly-
classified legitimate requests) obtained by considering all possible classification
thresholdvalues.WereportourfindingswithredlinesinFig.2,whileinTable1,
we extrapolate the TPR values at 1% FPR. We would like to point out that,
although the ROC curves in Fig. 2 already show the detection rates for each
possibleoperatingpoint(i.e.,thevalueofFPR),wereporttheresultsinTable1
at 1% FPR because it is a reasonable value commonly adopted in the litera-
ture[6,9].WedetailhereafterthekeyfindingsofourevaluationsofModSecurity
againstthetestset(test).Theresultsofthisfirstevaluationareindicatedwith
red lines in Fig. 2. The ROC curve of PL1 (default PL for ModSecurity) has
proven to be the best among the PLs since, in this configuration, the number of
activerulesisminimal,only20rulesenabled,causingareducednumberoffalse
positives. The results for PL2 show a detection rate of 75.45% at a 1% FPR.
Thisconfirmsthat,aspreviouslystated,havingmoreactiverules(31morethan
PL1) leads to more false positives and decreased performance. Additionally, the
ROC curves for both PL3 (which has 7 more rules enabled than PL2) and PL4
(which has 2 more rules enabled than PL3) are almost identical. This indicates
that the additional SQLi rules of PL4 do not improve the detection capabilities.
Thus, as highlighted by the curves, at the best of its capabilities, ModSecurity
with CRS is still missing plenty of potential threats.
4.3 Evaluation of ModSec-Learn
We now analyze the performance of SVM, LR, and RF ModSec-Learn against
thetestset(test).WeplottheROCcurvesinFig.2usingbluesolidanddashed

ModSec-Learn: Boosting ModSecurity with Machine Learning 7
1.0
0.9
0.8
0.7
0.6
0.5
106 105 104 103 102 101 100
False Positive Rate (FPR)
)RPT(
etaR
evitisoP
eurT
PL 1
1.0
0.9
0.8
0.7
0.6
0.5
103 102 101 100
False Positive Rate (FPR)
)RPT(
etaR
evitisoP
eurT
PL 2
1.0
0.9
0.8
0.7
0.6
0.5
103 102 101 100
False Positive Rate (FPR)
)RPT(
etaR
evitisoP
eurT
PL 3
1.0
0.9
0.8
0.7
0.6
0.5
103 102 101 100
False Positive Rate (FPR)
)RPT(
etaR
evitisoP
eurT
PL 4
RF ModSec SVM - 1 SVM - 2 LR - 1 LR - 2
Fig.2: ROCcurvesofModSecurityvanilla(ModSec)andModSec-Learn(SVM,
RF, and LR), evaluated on test. Each curve reports the average detection rate
ofSQLiattacks(i.e.,theTruePositiveRate)againstthefractionofmisclassified
benign SQL queries (i.e., the False Positive Rate). The zoomed section helps to
understand the performance of each model when lines overlap.
linesforSVM-ℓ andSVM-ℓ ,greensolidlinesforRF,yellowsolidanddashed
1 2
lines for LR - ℓ and LR - ℓ , respectively. They clearly show the superiority of
1 2
ModSec-Learn w.r.t. the respective ModSecurity vanilla counterpart regardless
of the operating point, i.e., for any FPR value, the detection rate of ModSec-
Learn approaches is higher or equal for all PLs. Specifically, considering the
results of PL 4 reported in Table 1, the TPR at 1% FPR of linear SVM with ℓ
1
and ℓ is 44.71% higher than ModSecurity. Considering the LR with ℓ and ℓ ,
2 1 2
the TPRs at 1% FPR is 44.93% higher compared with ModSecurity. While, as
fortheRF,theTPRat1%FPRis45.07%higherthantheModSecurityvanilla.
This confirms that, even by learning optimal weights, the rules enabled by PL1
are inappropriate for effectively discriminating benign samples from malicious
ones. Finally, unlike the ModSecurity vanilla, the majority of ModSec-Learn
models achieve the best detection rate for PL4 (even though the results for PL4
are slightly higher than those obtained for PL2). This result underlines that,
even when adding rules that may lead to more false positives, machine learning
can tune the importance of each rule to achieve a better TPR/FPR trade-off.

8 C. Scano et al.
8
6
4
2
0
2
4
100 120 130 131 140 150 151 160 170 180 190 200 210 230 240 250 251 260 270 280 290 300 310 320 330 340 350 360 362 370 380 390 400 410 430 431 432 440 450 470 480 490 500 510 511 520 521 530 540
CRS SQLi Rules
thgieW
ModSec
LR - 1
LR - 2
Fig.3: Weight values learned at PL 4 by ModSec-Learn LR - ℓ (blue) and
1
ModSec-Learn LR - ℓ (light red), and the weight used by ModSecurity vanilla
2
(green). The additional color, i.e., red, is given by the overlapping of the green
and blue bars with the light red ones. We only report the last three digits of the
rule IDs on the x-axis as the first three digits are equal to 942 for all rules.
4.4 Imposing Sparsity through Regularization
We now analyze the effect of regularization by investigating whether it is pos-
sible to select fewer rules from CRS as features. We leverage a regularization
termwiththeℓ normtoimposesparsityonthetrainedmodel,andweevaluate
1
its impact on the relevance of each CRS rule on the classification process. We
also compare results with the weights computed through the inclusion of an ℓ
2
regularization term. Fig. 3 displays the distribution of rule weights of ModSec-
Learn implemented with LR at PL 4. We chose this PL to enable all rules and
provide a complete overview of their impact. The blue and light red bins rep-
resent the weights computed with ℓ and ℓ regularization, respectively, while
1 2
the green ones are the ModSecurity severity scores (overlaps are colored in dark
red). Since severity scores ranges from 2 to 5, we normalize them using the min-
imum and maximum of LR ones. The results presented in Table 1 demonstrate
that the ℓ regularization norm can achieve the same performances of LR with
1
ℓ norm while using even fewer rules, 18 rules weighted as 0, while ℓ norm and
2 2
ModSecurity use all available rules. It’s important to note that the rules set to
a weight of 0 by the machine learning model are deemed unnecessary for the
classificationtask.Moreover,somerulesmightreceivenegativeweights,indicat-
ing that their presence is more indicative of legitimate behavior. Applying this
approach to the configuration of security tools such as ModSecurity introduces
a more grounded and less arbitrary method for security rule selection. Rather
than relying on manual selection or a predefined set of rules that may not be
optimal with respect to the data that will then be found to classify, the use of
ModSec-Learn makes it possible to automate both the selection of rules and the
assignment of their weights, optimizing ModSecurity performance on the data.

ModSec-Learn: Boosting ModSecurity with Machine Learning 9
5 Related Work
Althoughpreviousworkhasproposedseveralmachine-learningsolutionstocounter
SQLi attacks [13,14], this study focuses specifically on ModSecurity. Earlier re-
search [19,20] evaluated ModSecurity’s performance, considering the impact of
the PL under various web attacks, but used limited attack samples and did not
analyzetheTPR-FPRtrade-off.Folinietal.[10]exploredunsupervisedanomaly
detection for unknown attacks, while Tran et al. [21] propose a first attempt to
combine machine learning with the CRS rules. However, they did not evaluate
ModSecurity.Nguyenetal.,[15]proposedahybridapproach,combiningModSe-
curity with a machine-learning model for request categorization. However, none
of these studies assessed the TPR-FPR trade-off for each PL as in this work.
Furthermore,wearethefirsttoinvestigatetheeffectivenessofregularizationfor
selectingusefulrules.Finally,wealsoshareourdatasettofosterfutureresearch.
6 Conclusion and Future Work
InthisworkweproposeModSec-Learn,anovelmethodologyfortrainingmachine-
learningclassifiersusingtheCRSrulesasinputfeatures.Thispermitstheadap-
tation of the severity levels of CRS rules to the application to defend, achiev-
ing the best trade-off between detection and false positive rates. We show that
ModSec-Learn improves the detection rate of the vanilla ModSecurity by more
than 45%, while removing more than 30% of the CRS rules through embedded
feature selection with ℓ regularization. While we only target SQLi attacks in
1
this work, we argue that our methodology is general enough to tackle also other
web threats, and it can be applied "as is" on different rulesets. Furthermore,
even if we only focused on ModSecurity, our evaluation can be repeated also on
otheropen-sourceandcommercialWAFs.Toconclude,wefirmlybelievethatour
workwillpavethewaytowardsstrengtheningclassicalrule-basedsolutionswith
machine learning-based approaches, filling the gap between these two worlds.
Acknowledgments. ThisresearchwassupportedbytheTESTABLEproject,funded
by the European Union’s Horizon 2020 research and innovation program (grant no.
101019206); and the ELSA project, funded by the European Union’s Horizon Europe
research and innovation program (grant agreement no. 101070617); and the SERICS
project (PE00000014) under the MUR National Recovery and Resilience Plan funded
by the European Union – NextGenerationEU.
References
1. Appelt,D.,Nguyen,C.D.,Panichella,A.,Briand,L.C.:Amachine-learning-driven
evolutionaryapproachfortestingwebapplicationfirewalls.IEEETransactionson
Reliability 67(3), 733–757 (2018)
2. Appelt, D., Panichella, A., Briand, L.: Automatically repairing web application
firewallsbasedonsuccessfulsqlinjectionattacks.In:2017IEEE28thInternational
Symposium on Software Reliability Engineering (ISSRE). pp. 339–350 (2017)

10 C. Scano et al.
3. Applebaum, S., Gaber, T., Ahmed, A.: Signature-based and machine-learning-
based web application firewalls: A short survey. Procedia Computer Science 189,
359–367 (2021), aI in Computational Linguistics
4. Bishop, C.M. (ed.): Linear Models for Classification, pp. 179–224. Springer New
York,NewYork,NY(2006).https://doi.org/10.1007/978-0-387-45528-0_4,https:
//doi.org/10.1007/978-0-387-45528-0_4
5. Breiman, L.: Random forests. Machine learning 45, 5–32 (2001)
6. Corona,I.,Biggio,B.,Contini,M.,Piras,L.,Corda,R.,Mereu,M.,Mureddu,G.,
Ariu, D., Roli, F.: Deltaphish: Detecting phishing webpages in compromised web-
sites.In:ComputerSecurity–ESORICS2017.pp.370–388.SpringerInternational
Publishing, Cham (2017)
7. Cortes, C., Vapnik, V.: Support-vector networks. Machine Learning 20, 273–297
(1995), http://dx.doi.org/10.1007/BF00994018, 10.1007/BF00994018
8. Defazio,A.,Bach,F.,Lacoste-Julien,S.:Saga:Afastincrementalgradientmethod
with support for non-strongly convex composite objectives (2014)
9. Demontis, A., Melis, M., Biggio, B., Maiorca, D., Arp, D., Rieck, K., Corona, I.,
Giacinto, G., Roli, F.: Yes, machine learning can be more secure! a case study on
android malware detection. IEEE Transactions on Dependable and Secure Com-
puting 16, 711–724 (2017)
10. Folini, C., Gilliéron, F.: A New Attempt To Combine The
CRS with machine Learning. https://coreruleset.org/2021/05/19/
a-new-attempt-to-combine-the-crs-with-machine-learning/ (2021)
11. Folini,C.,Ristic,I.:ModSecurityHandbook,SecondEdition.FeistyDuck,London,
GBR, 2nd edn. (2017)
12. Fredj,O.B.,Cheikhrouhou,O.,Krichen,M.,Hamam,H.,Derhab,A.:Anowasptop
tendrivensurveyonwebapplicationprotectionmethods.In:RisksandSecurityof
InternetandSystems:15thInternationalConference,CRiSIS2020,Paris,France,
November4–6,2020,RevisedSelectedPapers.p.235–252.Springer-Verlag,Berlin,
Heidelberg (2020)
13. Joshi, A., Geetha, V.: Sql injection detection using machine learning. In: 2014
International Conference on Control, Instrumentation, Communication and Com-
putational Technologies (ICCICCT). pp. 1111–1115 (2014)
14. Kar, D., Panigrahi, S., Sundararajan, S.: Sqligot: Detecting sql injection attacks
using graph of tokens and svm. Computers & Security 60, 206–225 (2016). https:
//doi.org/https://doi.org/10.1016/j.cose.2016.04.005, https://www.sciencedirect.
com/science/article/pii/S0167404816300451
15. Nguyen, T.C.H., Le-Nguyen, M.K., Le, D.T., Nguyen, V.H., Tôn, L.P., Nguyen-
An, K.: Improving web application firewalls with automatic language detection.
SN Computer Science 3(6), 446 (2022)
16. OWASP Foundation Inc.: Owasp top 10 (2021), https://owasp.org/Top10/, ac-
cessed on 22.02.2023
17. OWASP Foundation Inc.: Owasp core rule set. https://coreruleset.org (2023)
18. Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O.,
Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A.,
Cournapeau, D., Brucher, M., Perrot, M., Duchesnay, E.: Scikit-learn: Machine
learning in Python. Journal of Machine Learning Research 12, 2825–2830 (2011)
19. Singh,J.J.,Samuel,H.,Zavarsky,P.:Impactofparanoialevelsontheeffectiveness
of the modsecurity web application firewall. In: 2018 1st International Conference
on Data Intelligence and Security (ICDIS). pp. 141–144 (2018)

ModSec-Learn: Boosting ModSecurity with Machine Learning 11
20. Sobola, T.D., Zavarsky, P., Butakov, S.: Experimental study of modsecurity web
application firewalls. In: 2020 IEEE 6th Intl Conference on Big Data Security on
Cloud (BigDataSecurity), IEEE Intl Conference on High Performance and Smart
Computing, (HPSC) and IEEE Intl Conference on Intelligent Data and Security
(IDS). pp. 209–213 (2020)
21. Tran,N.T.,Nguyen,V.H.,Nguyen-Le,T.,Nguyen-An,K.:Improvingmodsecurity
waf with machine learning methods. In: Future Data and Security Engineering.
Big Data, Security and Privacy, Smart City and Industry 4.0 Applications. pp.
93–107. Springer, Singapore (2020)
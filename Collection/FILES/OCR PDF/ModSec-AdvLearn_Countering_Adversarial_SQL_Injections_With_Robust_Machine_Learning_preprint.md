ModSec-AdvLearn: Countering Adversarial SQL
Injections with Robust Machine Learning
Giuseppe Floris§, Christian Scano§, Biagio Montaruli§, Luca Demetrio*, Andrea Valenza,
Luca Compagna, Davide Ariu, Luca Piras, Davide Balzarotti, and Battista Biggio*, Fellow, IEEE
Abstract—Many Web Application Firewalls (WAFs) leverage expose sensitive data. Even if many countermeasures to this
the OWASP Core Rule Set (CRS) to block incoming malicious attack have been proposed [2–5], the Open Web Application
requests. The CRS consists of different sets of rules designed
Security Project (OWASP) Foundation still classifies it as one
by domain experts to detect well-known web attack patterns.
of the top-10 most dangerous web threats [6].
Both the set of rules and the weights used to combine them are
manuallydefined,yieldingfourdifferentdefaultconfigurationsof WebApplicationFirewalls(WAFs)arecommonlyusedasa
theCRS.Inthiswork,wefocusonthedetectionofSQLinjection defense tool in enterprise systems to counter such attacks and
(SQLi) attacks, and show that the manual configurations of the protect web applications [5, 7]. They work by filtering the
CRStypicallyyieldasuboptimaltrade-offbetweendetectionand
incoming requests directed towards the web applications and
falsealarmrates.Furthermore,weshowthattheseconfigurations
blocking suspicious connections. To this end, many available
arenotrobusttoadversarialSQLiattacks,i.e.,carefully-crafted
attacks that iteratively refine the malicious SQLi payload by WAF solutions leverage the OWASP Core Rule Set, i.e., a
queryingthetargetWAFtobypassdetection.Toovercomethese collection of signatures designed to detect well-known web
limitations, we propose (i) using machine learning to automate attack patterns. The CRS rules have all been developed by
the selection of the set of rules to be combined along with
experts in the domain of web security in the last decade,
their weights, i.e., customizing the CRS configuration based
helpingtowithstandavastplethoraofweb-basedattacks.The
on the monitored web services; and (ii) leveraging adversarial
training to significantly improve its robustness to adversarial CRSv4.0.0(oneofthelateststableversions)usedinthiswork
SQLi manipulations. Our experiments, conducted using the includes 319 rules, out of which 170 target critical injection
well-known open-source ModSecurity WAF equipped with the attacks[8].Withinthisset,SQLiisthemostrepresentedclass
CRS rules, show that our approach, named ModSec-AdvLearn,
of injection attack counting 62 rules.
can (i) increase the detection rate up to 30%, while retaining
TheCRSrulesaresub-dividedintofoursets,eachidentified
negligible false alarm rates and discarding up to 50% of the
CRSrules;and(ii)improverobustnessagainstadversarialSQLi by a specific Paranoia Level (PL). These sets are constructed
attacksupto85%,markingasignificantstridetowarddesigning such that PL1 ⊂ ... ⊂ PL4, i.e., increasing the PL amounts
moreeffectiveandrobustWAFs.Wereleaseouropen-sourcecode toincludemoreCRSrules,withPL4includingallofthem.In
at https://github.com/pralab/modsec-advlearn.
practice,higherPLstendtoexhibitahigherdetectionratebut
Index Terms—web application firewalls, machine learning, sql
also cause a higher number of false alarms. Within each PL,
injection, adversarial training
rulesareassignedaspecificweight,referredtoastheirseverity
level. The severity level of each rule is assigned by domain
I. INTRODUCTION
experts, based on their subjective evaluation of the potential
Web applications are constantly evolving and deployed at a
impact of the attack that such a rule aims to prevent. Then,
broad scale, thus enabling organizations to offer rich services
the score associated with each incoming request is computed
over the Internet. However, this imposes serious challenges
as the sum of the severity levels associated with the firing
in securing web applications against an increasing number
rules. If such a score exceeds a given threshold, the incoming
of attacks [1]. Among these, SQLi consists of injecting a
request is blocked. More details on how the PL1-PL4 CRS
malicious SQL code payload inside regular queries, causing
configurations work are provided in Sect. II.
the target web application to behave in an unintended way or
WhilethedomainknowledgepouredindevelopingtheCRS
rules is extremely valuable, in this work we use the well-
G. Floris, C. Scano and B. Biggio are with the Dept. of Electrical and
known ModSecurity WAF [9] equipped with the CRS rules to
Electronic Engineering, University of Cagliari, 09124 Cagliari, Italy e-mail:
(name.surname@unica.it),C.ScanoisalsowiththeDepartmentofComputer, show that the heuristic choices made to select and combine
ControlandManagementEngineering,SapienzaUniversity,Rome,Italy. such rules can lead to: (i) a suboptimal trade-off between
B. Montaruli and D. Balzarotti are with the Dept. of Digital Security,
detection rate and false alarms; and (ii) a substantial lack
EURECOM,06410Biot,France,e-mail:(name.surname@eurecom.fr).
Luca Demetrio is with the Department of Informatics, Bioengineering, of robustness to adversarial SQLi attacks, i.e., functionality-
Robotics and Systems Engineering (DIBRIS), University of Genova, 16146 preserving manipulations of the SQLi attack payload aimed
Genova,Italye-mail:(luca.demetrio@unige.it).
to evade detection [10, 11]. To overcome these limitations,
Andrea Valenza is with Prima Assicurazioni, 20131 Milano, Italy e-mail:
(andrea.valenza@prima.it). we then propose a novel robust machine learning approach
LucaCompagnaiswithEndorLabs,e-mail:(lcompagna@endor.ai). to selecting and combining the CRS rules, named ModSec-
Davide Ariu and Luca Piras are with Pluribus One, 09128 Cagliari, Italy
AdvLearn, which is conceptually represented in Fig. 1 and
e-mail:(name.surname@pluribus-one.it).
§ meansequalcontribution,while* referstocorrespondingauthors. detailed in Sect. III. This approach is built upon two main
5202
yaM
12
]GL.sc[
4v46940.8032:viXra

Fig. 1: Conceptual representation of ModSec-AdvLearn. A machine-learning model is trained using the CRS rules as input
features, and leveraging our novel adversarial training approach to improve robustness against adversarial SQLi attacks.
contributions. First, we propose using machine learning (ML) issue.Forthisreason,wefirmlybelievethatourworkprovides
to automate both rule selection and weighting, adjusting the interestingandnovelinsightsonhowtodesignrobustmachine
CRS configuration based on the traffic data collected from learning models for cybersecurity. We discuss these aspects
the monitored web services, and building on our preliminary along with related work in Sect. V, and the limitations of
findings in [11]. The underlying idea is to train a linear our approach as well as the corresponding future research
ML model using all the CRS rules as input features, aiming directionsinSect.VI.Wehavealsopubliclyreleasedourcode
to improve the trade-off between detection and false alarm to foster reproducibility of our work.1
rates, by specializing the model to the specifics of the traffic
data collected from the monitored applications. Furthermore,
II. BACKGROUND
enforcing a sparse regularization during training enables the We introduce here SQLi attacks and the OWASP CRS
selection of an effective subset of rules as a by-product, project. We then describe how to generate adversarial SQLi
avoiding the need for manual selection of the CRS rules in attacks using state-of-the-art fuzzing techniques.
each PL. The second main contribution of this work is the
A. SQL Injection (SQLi)
definition of a novel adversarial training scheme to improve
model robustness against adversarial SQLi attacks. To craft These attempts to retrieve or alter sensitive information
these attacks, we leverage WAF-A-MoLE [10], i.e., a black- from a target database, modifying data without authorization,
boxmutationalfuzzer[12]thatiterativelyselectsthebestcom- or even execute privileged operations on the database [4].
binationofrandommanipulationsofSQLipayloadstoreduce This can be achieved via specific SQL code fragments that
their probability of being detected by the targeted WAF. We are passed in the original request. If the application does
also show in Sect. III-B that using ℓ -norm regularization on not sanitize the user input and simply concatenates it with
∞
a linear model yields equivalent robust solutions, avoiding the the query, the SQL fragment is interpreted as part of the
computational burden of optimizing attacks during training. original SQL query. The login form of a web application
is a paradigmatic example (Listing 1). The credentials of
Through our experiments, reported in Sect. IV and con-
a user are provided in two input fields (e.g., $user and
ducted on two publicly-available datasets [10, 11], we show
$passwd) and sent via an HTTP request. The credentials
that ModSec-AdvLearn overcomes the limitations of the cur-
are then checked server-side via a database query. However, a
rent CRS, by detecting 30% attacks more with much fewer
malicioususerinjectsSQLfragmentsinthe$userparameter,
rules.ModSec-AdvLearnalsoprovidesanunprecedentedlevel
e.g., ”admin’-- ”. As shown in Listing2, this bypasses the
ofrobustness againstadversarial SQLiattacks,i.e., 85%more
originalSQLquery’spasswordcheck,resultinginasuccessful
thanthedefaultCRSconfigurations.Bydeepeningtheinvesti-
SQLi attack, allowing login with just a valid username.
gationofthisresult,wediscoverthatModSec-AdvLearngives
moreemphasistorulesthatare(i)lessaffectedbyadversarial SELECT * FROM users WHERE username = ’
SQLi attacks and (ii) accidentally triggered by side-effect $user’ AND password = ’$passwd’
artifacts introduced by the adversarial SQLi manipulations.
Listing 1: Example of SQL query vulnerable to injection.
To conclude, we remark that our work is the first to
demonstrate the effectiveness of adversarial training in the
WAFs domain (specifically, for detecting SQLi attacks) when SELECT * FROM users WHERE username = ’
admin’-- ’ AND password = ’x’
leveraging state-of-the-art input-space SQLi manipulations.
This is completely different from other domains like im-
Listing 2: Example of SQL Injection on Listing 1.
age classifiers, where adversarial training is not sufficient to
achieveahighlevelofrobustness,andtheeffectivemitigation
of the risks presented by adversarial examples is still an open 1https://github.com/pralab/modsec-advlearn

TABLE I: Manipulation functions applied by WAF-A-MoLE.
B. The OWASP Core-Rule-Set (CRS) Project
This open-source initiative is one of the most widely-used Manipulation Effectonpayload
sets of detection rules targeting OWASP Top 10 web security CaseSwapping CS(admin’ OR 1=1)→ADmIn’ oR 1=1
risks [6]. It is not only the reference rule set of several open- WhitespaceSubstitution WS(admin’ OR 1=1)→admin’\n OR 1(cid:127)=1
CommentInjection CI(admin’ OR 1=1)→admin’/**/OR 1=1
sourceWAFsolutionslikeModSecurity[9]andCoraza,2butis CommentRewriting CR(admin’/**/OR 1=1)→admin’/*abc*/OR 1=1
IntegerEncoding IE(admin’ OR 1=1)→admin’ OR 0x1=1
also adopted in many commercial solutions including Google OperatorSwapping OS(admin’ OR 1=1)→admin’ OR 1 LIKE 1
Cloud Armor, Microsoft Azure, and Cloudflare WAFs [8]. LogicalInvariant LI(admin’ OR 1=1)→admin’ OR 1=1 AND 2<>3
Detection Rules. These are regular expressions (regex) that
match specific byte patterns in requests. For instance, line 3
followingSQLipayload:admin’OR 1=1; --’.However,
of Listing 3 captures several patterns of comments commonly
by inserting a white space character (’ ’) in the original
used in SQLi attacks such as ”;--” and ”-- ”. Each rule is
attack payload, we generate a semantically-equivalent SQLi
denoted by a unique identifier (id in line 4), whose suffix
attack: admin’ OR 1=1; --’, that can evade the rule.
also indicates the type of attack it is designed to identify
WAF-a-MoLE. Our methodology builds upon WAF-A-
(those starting with 942 target SQLi attacks [8]). Notable
MoLE [10], a state-of-the-art, open-source SQLi guided mu-
among configuration settings are the Paranoia Level (line 8)
tational fuzzer [12], aimed at finding semantically-equivalent
and Severity Level (line 9), which are explained below.
SQLi attacks that evade detection through the application of
Paranoia Level. It defines the set of rules that are enabled to
functionality-preserving manipulations. These manipulations,
analyze the incoming HTTP requests [8]. The CRS includes
detailed in Table I, can be encoded as a function h(z,δ),
four PLs (PL1 - PL4) and each rule is assigned to a specific
where z is the SQLi query to be modified, and δ are the
PL; e.g., the rule in Listing 3 belongs to PL1 (line 8).
parameters defining the perturbation. For instance, WAF-A-
Moreover, rules are grouped together by PL in a nested way:
MoLE can include new comments into the SQLi, adding
settingacertainPLenablesalltherulesassignedtothatPL,as
always-true or always-false statements, converting numbers
wellasthoseassignedtolowerPLs.Forinstance,PL3enables
to a different base, or replacing them with SQL commands
all the rules related to such PL, as well as those assigned to
that,onceevaluated,producethesamenumber.Suchchoiceis
PL1 and PL2. Consequently, PL4 will enable all the rules.
controlled by δ, which specifies the type of manipulation and
SeverityLevel.EachCRSruleisheuristicallygivenaseverity
thecontentthatshouldbeinjectedorreplaced.WAF-A-MoLE
level, i.e., a positive integer that quantifies how severe the
then iteratively refines the choice of δ to decrease the confi-
corresponding attack could be [8]. The WAF applies the rules
denceofthetargetedWAFintoclassifyingthemodifiedSQLi
on each incoming request, and sums the severity levels of
payload as an attack. This is achieved by generating several
the firing rules. If the aggregated score exceeds a predefined
candidates through random choices of δ in each iteration, and
threshold,therequestisflaggedasmalicious.TheCRSdefines
retaining only those that successfully reduce the confidence
four severity levels: CRITICAL (5), ERROR (4), WARNING
score attributed by the WAF. In this work, we will use WAF-
(3) and NOTICE (2); e.g., the severity level of the rule
A-MoLE (i) to show that the standard configurations of the
in Listing 3 is CRITICAL (line 9), so it contributes to the
CRS can be bypassed by optimizing adversarial SQLi attacks
aggregated score with a value of 5.
againstthem,and(ii)togenerateadversarialSQLiqueriesfor
1 SecRule REQUEST_COOKIES|!REQUEST_COOKIES:/__utm/ our novel problem-space adversarial training approach.3
2 |REQUEST_COOKIES_NAMES|ARGS_NAMES|ARGS|XML:/*
3 "@rx (?i)/\*[\s\v]*?[!\+](?:[\s\v\(-\)\-0-9=A-Z_a-z]+)
?\*/" \ III. ROBUSTMACHINELEARNINGAGAINST
4 "id:942500, ADVERSARIALSQLIATTACKS
5 block,
6 msg:’MySQL in-line comment detected’, We detail here how we design our robust ML approach to
7 tag:’attack-sqli’,
8 tag:’paranoia-level/1’, (i) improving the tradeoff between detection and false alarm
9 severity:’CRITICAL’, rates by optimizing the selection and combination of the CRS
10 setvar:’tx.sql_injection_score=+
11 %{tx.critical_anomaly_score}’, rules(Sect.III-A),and(ii)improvingrobustnesstoadversarial
12 setvar:’tx.inbound_anomaly_score_pl1=+ SQLi attacks (Sect. III-B).
13 %{tx.critical_anomaly_score}’"
Listing 3: CRS rule detecting typical comments in SQLi. A. ModSec-Learn: Machine Learning for CRS
We start by discussing the building block developed from
C. Adversarial SQLi Attacks against WAFs our initial findings, i.e., ModSec-Learn (step 1 of Fig. 1). It
consistsoftwocomponents:(i)afeatureextractionphasethat
InthecontextofWAFs,theproblemoffindingSQLiattacks
encodes the CRS rules into a vector representation; and (ii)
thatcanbypassthetargetWAFisadversarialinnature.Tothis
a ML model that learns how to optimally combine the CRS
end,theattackermaymanipulateSQLiattackpayloadtoevade
rules, avoiding the manual tuning of their severity scores.
detectionwhilepreservingitsmaliciousfunctionality[10,13].
Forinstance,theSQLirulereportedinListing3candetectthe 3Werefertoourapproachasproblem-spaceadversarialtrainingtodiffer-
entiate it from approaches that simulate the effect of attacks by modifying
2https://coraza.io onlytheirfeaturevectors,withoutevenproducingtheactualsamples[14].

Detection Rules as Features. The input space is represented arenotadditive.Wethusconsiderheretwodistinctapproaches
bySQLqueriesthatareclassifiedasmaliciousorbenignbya to performing AT: feature-space and problem-space AT.
MLmodel.EachSQLqueryisastringofreadablecharacters, Feature-spaceAT.Inthissetting,wemakethena¨ıveassump-
represented as z ∈ Z, being Z the space of all possible tion that each adversarial SQLi attack can enable or disable
queries.LetDbethesetofselectedSQLirulesfromCRS,and up to a number λ of CRS rules to evade the target WAF. This
d=|D| its cardinality. We denote with ϕ:Z (cid:55)→X ={0,1}d amounts to optimizing the following min-max objective:
a function that maps a SQL query z to a d-dimensional (cid:88)
min max L(y ,f (x +δ )), (1)
Boolean feature vector x = (ϕ (z),...,ϕ (z)), where each i w i i
ϕ (z)correspondstoevaluating
1
thej-thSQL
d
iruleontheinput
w ∥δi∥1≤λ
i
j
query z. Each ϕ (z) returns 1 if the corresponding rule has where (i) x = ϕ(z ) is the d-dimensional Boolean vector
j i i
been triggered by the SQL query z, and 0 otherwise. representing the activations of the CRS rules for the given
OptimalCombinationofCRSRuleswithML.Tooptimally SQL sample z ; (ii) y ∈ Y = {−1,+1} is its label;
i i
tune the contribution of the CRS rules towards effectively (iii) f : X → R is the ML model, parameterized by w,
w
classifying the input requests we leverage three different ML which classifies a sample as positive if f (x) ≥ 0, and
w
algorithms on the feature representation defined above: two as negative otherwise; (iv) L : Y × R → R is the loss
linearmodels,i.e.,SupportVectorMachines(SVMs)[15]and function to be minimized; and (v) δ is the manipulation
i
Logistic Regression (LR) [16], both with ℓ and ℓ regular- that switches on or off at maximum λ rules from the CRS
1 2
ization; and a non-linear Random Forest (RF) model [17]. (expressed as an ℓ norm constraint). Furthermore, it must
1
Linear models are particularly valuable as they can auto- also hold that x + δ ∈ X = {0,1}d, as the activations
i i
maticallyadjusttheseverityscoreassignedtoeachrule,rather have to remain Boolean also after perturbation. In practice,
thanrelyingondefaultCRSvalues,whereasnon-linearmodels the min-max problem is solved iteratively. In each iteration,
may give us an indication of the best performance achievable. the inner problem amounts to finding adversarial examples
Furthermore,whensparse(ℓ )regularizationisapplied,linear against the given model, while the outer problem adjusts the
1
models can effectively select an optimal subset of CRS rules, model parameters w to re-classify them correctly.4
potentially eliminating the need for predefined PLs. Although In this work, we do not solve the problem given in Eq. 1
our approach is applicable to both linear and non-linear directly, as it is too computationally demanding. Instead,
models,integratinganon-linearmodelwithintheexistingCRS we derive an equivalent formulation for linear SVMs based
rules may pose additional complexity and scalability issues, on solving the inner problem in closed form, which simply
whilealsoworseningtheinterpretabilityoftheWAFdecisions. amounts to using a different regularization term.
Conversely, the weights learned by any linear model can be Robustness through Regularization with SecSVM. As orig-
directly plugged-in into the CRS rules without any significant inally shown by by Xu et al. [22], and subsequently adapted
disadvantage. Let us finally remark that, compared to our in [20] to the case of Android malware detection, the inner
previous work in [11], we extend the evaluation of ModSec- problem in Eq. 1 can be solved in closed form when the loss
Learnmodelsbyassessingtheirrobustnessagainstadversarial function L is linear. This is the case, e.g., when using the
attacks, and also considering an additional dataset [10]. hinge loss and a linear model f (x)=wtx+b, as in linear
w
SVM training. In this case, the inner problem in Eq. 1 for
B. ModSec-AdvLearn: Robustness against Adversarial SQLi
each sample can be rewritten as:
While ModSec-Learn can learn to automatically select and
max L(y,f (x))+δ⊤∇L(y,f (x)), (2)
combine the CRS rules from the training data, yielding a w w
∥δ∥1≤λ
better tradeoff between detection and false alarm rates, it
may not guarantee a sufficient degree of robustness against where the gradient ∇L(y,f w (x)) corresponds to the weight
adversarialSQLiattacks.Hence,wedetailherehowweextend vector w. The above problem then amounts to maxi-
ModSec-LearntoimproverobustnessagainstadversarialSQLi mizing a scalar product over an ℓ 1 -norm constraint, i.e.,
attacks. We refer to this approach as ModSec-AdvLearn (step max ∥δ∥1≤λ δ⊤w, whose solution is proportional to the dual
2 of Fig. 1). The underlying idea is to leverage adversarial norm of the weight vector, given as λ∥w∥ ∞ [22]. This means
training (AT) [18, 19] to include adversarial SQLi examples thatwecanrewritetherobust(min-max)optimizationproblem
during training, thereby giving the model the ability to with- given in Eq. 1 as a much simpler regularized problem:
stand the corresponding evasive attack patterns at test time. (cid:88)
min L(y ,f (x ))+λ∥w∥ . (3)
Inthecommonsettingofimageclassification,ATleverages w i w i ∞
i
gradient-basedattackstocraftadversarialexamples,asthecor-
This finding sheds light on the role of the regularization term,
responding optimization problem is end-to-end differentiable,
showing that its choice should be based on the type of noise
and the considered perturbations are simply additive. This is
that affects the input data. In particular, it tells us that ℓ is
not directly applicable in the case of SQLi attacks, as well ∞
as in other domains [20, 21], in which models are not end-
4Notethat,forsimplicity,inthegivenformulationweconsideradversarial
to-end differentiable (given the presence of non-differentiable
modificationsofbothbenignandmalicioustrainingsamples,butthiscanbe
pre-processing and feature extraction steps) and perturbations easilyadjustedtoconsideronlymanipulationsofmaliciousSQLiqueries.

the optimal regularizer for training a robust model against ℓ 1 - Algorithm 1: Adversarial training of ModSec-
norm (sparse) perturbations. It is also not difficult to see that, AdvLearn with WAF-A-MoLE
analogously,thestandardℓ 2 -normSVMisoptimalagainstℓ 2 - Input : D =(z i ,y i )M i=1 , the training set of SQL
norm (dense) perturbations [20, 22]. samples with labels; f, the ML model; L, the
Theaboveproblemcanbeequivalentlyre-parameterizedby loss function; N, the number of adversarial
(i) replacing the regularization parameter λ with the hyperpa- SQLi attacks to be added to the initial
rameter t, i.e., bounding the weight values w in [−t,t]; and training set.
(ii) introducing the slack variables ξ to measure how far each Output: f , the model with re-trained parameters w⋆
w⋆
sample z i is from being correctly classified: 1 Z′ ←{z i }N i=1 with z i ∼D s.t. y i =+1
min (cid:88) ξ (4) 2 for z in Z′
w,ξ i 3 z⋆ ← WAF-A-MoLE(z,f)
i
s.t. ξ ≥1−y f (x ), ∀i∈1,...,n (5) 4 Z ←Z ∪{z⋆}; Y ←Y ∪{+1};
ξ i ≥0, ∀ i i w ∈1, i ...,n (6) 5 w⋆ ←arg min w |Z 1 | (cid:80)| i Z = | 0 L(y i ,f w (z i ))
i
−t≤w ≤t, ∀j ∈1,...,d. (7)
6 return f w⋆
j
The given formulation corresponds to a linear programming
probleminitscanonicalform,whichcanbesolvedusingstan-
always-true or always-false conditions that do not change the
dard, off-the-shelf solvers, such as the simplex algorithm or
original evaluation of the payload, or encoding integers in a
interior-pointmethods.Inthiswork,theoptimizationproblem
specific base different from the original one.
issolvedusingthelinearprogrammingsolverprovidedbythe
TosolvetheproblemgiveninEq.8,weconsideragradient-
SciPylibrary5.WerefertothisrobustlearningapproachasSe-
free black-box optimization achieved through WAF-A-MoLE
cure Support Vector Machine (SecSVM) in our experiments.6
as shown in Alg. 1, modifying only the set of malicious
Problem-space AT with WAF-A-MoLE. Let us now define
SQLi payloads, and leaving benign SQL queries unchanged.
adifferentapproachtolearningrobustmodelsdirectlyagainst
Given a dataset Z of benign queries and SQLi attacks labeled
problem-space perturbations. The reason is that hardening as 0 and 1 respectively, we first create a new set (Z′) by
models via feature-space AT or with ad-hoc regularization
randomly sampling a given amount of SQLi from the training
methodsmayprovideanoverlypessimisticapproachtofeature
dataset (line 1). Then, for each SQLi sample of this newly
manipulation that does not consider the specific constraint
created set, we use WAF-A-MoLE (Sect. II-C) to generate
of realizable, semantic- and functionality-preserving SQLi
the corresponding adversarial SQLi (line 3) and add it to
attacks. In particular, practical SQLi manipulations may not
the training data with its malicious (+1) label (line 4). The
enableswitchingonoroffindividualCRSrulesindependently,
parameters of the model are finally optimized on the training
and may inadvertently trigger certain rules even if the attack
set including the adversarial SQLi samples (line 5).
aimstobypassthedetection.Furthermore,suchmanipulations
In our experiments, we will also retrain SecSVM with
cannot be modeled as additive perturbations, and comput-
the proposed problem-space AT method, to consider less
ing them typically requires inverting a complicated, non-
pessimistic,butpractical,adversarialattacks.Inprinciple,this
differentiable feature extraction step; in our case, this would
should allow us to further improve the robustness-detection
amount to reversingthe inner workings of each CRSrule. For
tradeoff of SecSVM against real-world SQLi attacks. We
this reason, feasible SQLi attacks, as many other adversarial
would like to finally remark that, even if we leverage an
perturbations aimed to bypass ML models for cybersecurity-
existingtoollikeWAF-A-MoLEtothisend,toourknowledge,
related tasks [21], cannot be typically optimized via gradient
this is the first attempt to define a novel problem-space
descent directly. To overcome these issues, we consider here
adversarial training approach to hardening ML-based WAFs
a more general problem-space AT procedure, defined as:
against practical adversarial SQLi attacks.
(cid:88)
minmax L(y ,f (ϕ(h(z ,δ ))), (8)
w δi∈∆
i
i w i i IV. EXPERIMENTALANALYSIS
We report here three different experiments to validate our
where h(z,δ) is a manipulation function that modifies the
methodology. First, we evaluate the detection capabilities of
input SQL query z and returns a semantic-preserving SQL
query z′, based on the choice of its input parameters δ ∈∆. the CRS. This is achieved by using the vanilla ModSecurity
WAF as the underlying engine (Sect. IV-B), showing that
The set ∆ constrains the input manipulations described in
its na¨ıve approach of combining the CRS rules based on
Table I to produce valid samples, e.g., picking only visible
manually-assigned weights is largely suboptimal and signifi-
characters when adding or re-writing comments, produce
cantlyvulnerabletoadversarialSQLiattacks.Second,weem-
5https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize. pirically show that the ML-based tuning adopted by ModSec-
linprog.html Learn allows one to fill the gaps of the vanilla ModSecurity,
6Notethat,evenifwekeepthesamenameoftheapproachproposedin[20],
by significantly enhancing its detection rate up to 30%, and
our SecSVM implementation is different, as we are neither using custom
boundsoneachfeaturevaluenoranyℓ2 regularization. we continue highlighting how ModSec-Learn enhances the

TABLEII:Numberoflegitimate,SQLi,andadversarialSQLi
performances thanks to the adaptation of weights, while also
samplesintrain,test,train-adv,andtest-adv,for
reducing the number of rules needed (Sect. IV-C). Third, we
the WAF-a-MoLE and ModSec-Learn datasets.
present the results of our novel adversarial training approach
showing that ModSec-AdvLearn is 85% more robust than
train train-adv
ModSecurity (Sect. IV-D).
Legitimate SQLi Legitimate SQLi AdversarialSQLi
A. Experimental Setup WAF-a-MoLE 10,000 10,000 10,000 5,000 5,000
ModSec-Learn 20,000 20,000 20,000 15,000 5,000
In this section, we describe the two datasets used in our test test-adv
analysis, along with the setup of the ModSecurity WAF, the Legitimate SQLi Legitimate SQLi AdversarialSQLi
WAF-A-MoLE fuzzer, and the ML models used. WAF-a-MoLE 2,000 2,000 2,000 - 2,000
Datasets. We conduct our experiments using two datasets. ModSec-Learn 5,000 2,000 5,000 - 2,000
The first one, WAF-A-MoLE Dataset [10], which consists of
393,629 malicious and 345,199 benign SQL queries. Benign
Implementation Details. We use pymodsecurity v0.1.0,9 as
samplesweregeneratedfromarestrictedSQLgrammar,while
our Python interface to ModSecurity. To efficiently query
attacks were generated using well-known web security testing
and test ModSecurity, we have extended WAF-A-MoLE by
tools such as SQLmap and OWASP ZAP [10]. The second
developing a dedicated pymodsecurity interface, which avoids
one, ModSec-Learn Dataset [11], instead consists of 25,000
instantiating the whole web server. This interface is available
malicious SQLi payloads and 25,000 benign HTTP requests,
in our open-source repository.
basedonreal-worldtraffic.Legitimatesampleswerecollected
Machine Learning. We leverage scikit-learn v1.4.0 imple-
from the open-appsec dataset,7, which contains samples from
mentations of SVM (LinearSVC), LR, and RF to implement
variousreal-worldscenarios.Malicioussampleswerecollected
bothModSec-LearnandModSec-AdvLearn.FortheSVMand
from multiple sources, and generated through security testing
LR models, we experiment with both ℓ and ℓ regularizers.
tools such as SQLmap, by executing it with different tamper- 1 2
We implement SecSVM as described in Sect. III-B, using
ing scripts designed for payload obfuscation.
the linear programming solver provided by SciPy. We refer
Wedivideeachdatasetintofoursubsets:training(train),
to it as ModSec-Learn SecSVM in the reported tables. The
test (test), adversarial training (train-adv), and adver-
hyperparametersofeachmodelaretunedviagridsearch,per-
sarial test (test-adv). Table II shows the distribution of
forming a 5-fold cross validation on the training set (train)
samples across the four subsets for each dataset: train
tomaximizethemeanF1score.InthecaseofModSec-Learn,
contains an equal number of benign and SQLi queries, and it
for the SVM and LR, we tune the regularization parameter
isusedtotrainourtargetWAFs;test,disjointfromtrain,
C ∈ {10−3,10−2,10−1,0.5,1.0}. The best value found is
is used to evaluate the baseline performances of target WAFs,
typically C = 0.5 for both models. For SecSVM, we tune
including vanilla ModSecurity, ModSec-Learn, and ModSec-
the hyperparameter t ∈ {0.1,0.2,...,1.0}. The best t value
AdvLearn, across different PLs; train-adv contains the
is typically found to be 0.5. The RF model is used with its
same samples of train, but 50% of the SQLi queries in
default hyperparameters. In the case of ModSec-AdvLearn,
theWAF-A-MoLEdatasetandthe25%oftheSQLiqueriesin
adversarial training is applied only for PL4, given that the
theModSec-LearndatasetareoptimizedusingWAF-A-MoLE
modelstrainedonthisPLdemonstratedbetterperformanceon
against the target WAF for problem-space AT; test-adv
the test set (see Sect. IV-C). The hyperparameters are tuned
contains the same samples of test, but optimizes all the
using the same procedure described in this paragraph, finding
SQLi queries using WAF-A-MoLE to bypass the target WAF,
approximately the same best values, except for SecSVM, for
i.e., to evaluate its robustness. We would like to clarify that,
which t=1.0 yields better results.
although using the same SQLi fuzzer (i.e., WAF-A-MoLE),
theadversarialexamplesgeneratedforbuildingtheadversarial B. Evaluation of ModSecurity
trainingandtestsetsaredifferent.Theyareindependentlyop-
The first goal of our experimental analysis is to understand
timized against each target model at test time, resulting in the
the detection capability of the vanilla ModSecurity. Rather
applicationofdifferent,optimalmanipulationstrategies.Thus,
than focusing only on CRS default values, we experiment
the sets are independent, ensuring an unbiased evaluation.
with it over its entire configuration space, considering all the
ModSecurity and WAF-A-MoLE Setup. We evaluate Mod-
possible values for the PLs and the classification threshold.
Security v3.0.10 with the CRS v4.0.0. Since we focus on the
Hence, for each PL, we compute the Receiver-Operating-
detectionofSQLiattacks,weonlyenableitsSQLirules.8 We
Characteristic (ROC) curve, which reports the detection rate,
configureWAF-A-MoLEtouseamaximumof2,000queries,
a.k.a. True Positive Rate (TPR, i.e., the fraction of correctly-
to ensure convergence of the attack optimization. Attacks are
detected malicious SQLi requests) against the False Positive
optimized by minimizing the confidence score assigned to the
Rate (FPR, i.e., the fraction of wrongly-classified legitimate
malicious class by the targeted WAF.
requests) obtained by considering all possible classification
7https://github.com/openappsec/waf-comparison-project/tree/main/Data threshold values. We report our findings with red lines
8https://github.com/coreruleset/coreruleset/blob/v4.0.0/rules/
REQUEST-942-APPLICATION-ATTACK-SQLI.conf 9https://github.com/pymodsecurity/pymodsecurity

WAF-A-MoLE dataset (PL 1) WAF-A-MoLE dataset (PL 2) WAF-A-MoLE dataset (PL 3) WAF-A-MoLE dataset (PL 4)
1.0
0.8
0.6
0.4
1.0
0.8
0.6
0.4
10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100
False Positive Rate (FPR)
ModSec-Learn dataset (PL 1) ModSec-Learn dataset (PL 2) ModSec-Learn dataset (PL 3) ModSec-Learn dataset (PL 4)
1.0
0.8
0.6
0.4
1.0
0.8
0.6
0.4
10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100
False Positive Rate (FPR)
)RPT(
etaR
evitisoP
eurT
)RPT(
etaR
evitisoP
eurT
ModSec RF SecSVM SVM 1 SVM 2 LR 1 LR 2
Fig.2:ROCcurvesofvanillaModSecurity(ModSec)andModSec-Learnapproaches(SVM,RF,LR,andSecSVM),evaluated
on test (solid lines) and test-adv (dashed lines), for WAF-A-MoLE (first two rows) and ModSec-Learn (last two rows)
datasets. Each curve reports the fraction of detected SQLi attacks against the fraction of misclassified legitimate requests.
in Fig. 2, while in Table III we extrapolate the TPR values at Robustness against Adversarial SQLi. The results on the
1% FPR. We want to point out that, although the ROC curves adversarialtestsetareindicatedwithreddashedlinesinFig.2.
in Fig. 2 already show the TPR for each possible operating The outcomes highlight a more alarming trend, thus clearly
point(i.e.,thevalueofFPR),wereporttheresultsinTableIII showing that ModSecurity is not able to withstand adversar-
at1%FPRbecauseitisareasonablevaluecommonlyadopted ial attacks. Both datasets exhibited a pattern similar to the
in the literature [20, 23]. We detail hereafter the key findings evaluationonthetestset(test).Specifically,withtheWAF-
of our evaluations of ModSecurity against both the test set A-MoLE dataset, the True Positive Rate (TPR) drops below
(test) and the adversarial test set (test-adv). 50% at a 1% FPR, which is worse than random guessing.
For the ModSec-Learn dataset, the situation is slightly better,
Evaluation on Clean Samples. We first test ModSecurity but still concerning. Particularly with PL3 and PL4, the TPR
on the data we have gathered, and the results of this first at 1% FPR is around 58%, only slightly better than random
evaluation are indicated with red solid lines in Fig. 2. The guessing.Thisemphasizesthatincreasingthenumberofrules
ROC curve of PL1 (default PL for ModSecurity) shows its does not improve detection capabilities; instead, it worsens
inability to discriminate between benign and malicious SQL them by increasing false positives.
queries, with a TPR of 63.85% at a 1% False Positive Rate
C. Evaluation of ModSec-Learn
(FPR). The results for PL2 are the best among all PLs, with
a TPR of 66.82% at 1% FPR. The ROC curves for both PL3 We analyze the performance of SVM and LR, using ℓ and
1
andPL4arealmostidentical,asPL4hasonlytwoactiverules ℓ regularizations, SecSVM and RF ModSec-Learn against
2
more than PL3, which do not even improve its detection rate. both the baseline clean and the adversarial samples.

TABLE III: TPR at 1% FPR evaluated on the baseline/adversarial (test/test-adv) test sets for ModSecurity (ModSec);
ModSec-Learn(SVM,LR,SecSVM,andRF);andModSec-AdvLearn(SVM,LR,SecSVM,andRF)usingPL4.Wealsoreport
the number of active rules (AR) for each model. Results are shown for both datasets: WAF-A-MoLE and ModSec-Learn.
PL1 PL2 PL3 PL4
Base AR ModSec-AdvLearn AR
WAF-A-MoLEdataset
test 63.85% 66.82% 61.00% 61.00% 62/62 —
ModSecvanilla
test-adv 34.25% 45.86% 39.12% 39.12% 62/62 —
test 69.40% 83.00% 86.84% 86.80% 37/62 85.30% 42/62
ModSec-LearnSVM(ℓ1)
test-adv 37.10% 59.90% 62.72% 63.97% 37/62 82.55% 42/62
test 69.50% 83.10% 86.80% 86.80% 50/62 85.25% 51/62
ModSec-LearnSVM(ℓ2)
test-adv 39.20% 59.90% 62.71% 62.95% 50/62 81.40% 51/62
test 69.40% 83.00% 86.64% 86.60% 29/62 84.10% 32/62
ModSec-LearnLR(ℓ1)
test-adv 36.50% 54.20% 60.91% 60.62% 29/62 79.85% 32/62
test 69.50% 82.54% 85.95% 85.95% 50/62 84.05% 52/62
ModSec-LearnLR(ℓ2)
test-adv 38.60% 53.75% 57.95% 58.37% 50/62 80.15% 52/62
test 69.50% 83.89% 87.00% 87.00% 46/62 87.22% 47/62
ModSec-LearnRF
test-adv 41.35% 66.75% 64.5% 64.30% 46/62 84.90% 47/62
test 63.70% 80.78% 82.75% 82.58% 61/62 84.15% 61/62
ModSec-LearnSecSVM
test-adv 57.65% 76.71% 61.96% 58.68% 61/62 81.84% 61/62
ModSec-Learndataset
test 92.80% 85.22% 75.71% 75.71% 62/62 —
ModSecvanilla
test-adv 59.50% 42.12% 31.07% 30.85% 62/62 —
test 92.80% 99.46% 99.31% 99.41% 35/62 99.26% 41/62
ModSec-LearnSVM(ℓ1)
test-adv 69.90% 70.87% 67.02% 69.86% 35/62 93.46% 41/62
test 92.80% 99.46% 99.31% 99.41% 49/62 99.26% 50/62
ModSec-LearnSVM(ℓ2)
test-adv 69.80% 73.87% 71.47% 70.66% 49/62 92.86% 50/62
test 92.80% 99.46% 99.46% 99.46% 31/62 99.61% 30/62
ModSec-LearnLR(ℓ1)
test-adv 73.05% 89.68% 89.95% 88.89% 31/62 94.03% 30/62
test 92.80% 99.46% 99.46% 99.46% 49/62 99.61% 50/62
ModSec-LearnLR(ℓ2)
test-adv 73.25% 87.75% 86.92% 87.61% 49/62 94.29% 50/62
test 92.80% 99.56% 99.56% 99.56% 49/62 99.65% 50/62
ModSec-LearnRF
test-adv 70.02% 86.20% 87.70% 87.45% 49/62 95.07% 50/62
test 92.80% 99.50% 99.50% 99.50% 56/62 99.65% 59/62
ModSec-LearnSecSVM
test-adv 86.50% 97.76% 98.26% 98.26% 56/62 98.41% 59/62
Evaluation on Clean Samples. We plot the ROC curves RF and SecSVM models. This may be since, in this case,
in Fig. 2 using and green (RF), violet (SecSVM), blue (SVM the adversarial SQLi attacks are able to exploit the rules
withℓ ),lightblue(SVMwithℓ ),orange(LRwithℓ ),brown enabled by PL3 and PL4 to evade the model, by removing
1 2 1
(LR with ℓ ), solid lines. They clearly show the superiority of patterns that were considered important at training time. On
2
ModSec-Learn w.r.t. the respective ModSecurity counterpart the other hand, with the ModSec-Learn dataset, it is observed
regardless of the operating point, i.e., for any FPR value, that starting from PL2, the detection capabilities exhibit a
the TPR of ModSec-Learn approaches is higher for all PLs fairly consistent trend. While there is a slight deterioration,
greater than 1. It is worth noting that, for PL1, the trained performanceremainsrelativelystableacrossthedifferentPLs.
MLmodelsachievesimilarresultstothevanillaModSecurity. Among all evaluated models, SecSVM is the most robust,
This confirms that, even by learning optimal weights, rules offeringstronggeneralizationandadversarialrobustness.Even
enabled by PL1 are inappropriate to effectively discriminate if RF was included to explore non linear alternatives, its
benignsamplesfrommaliciousones.Finally,unlikethevanilla performance is comparable to linear models like SecSVM,
ModSecurity, all ModSec-Learn models achieve the best TPR while worsening robustness. This confirms that linear models
for PL4 (even though the results for PL4 are slightly higher are sufficient to achieve excellent accuracy and are preferable
than those obtained for PL2). This result shows that, despite given their robustness and transparency. In addition, linear
adding rules that may increase the FPR, machine learning can models can be readily applied to the existing CRS system
adjust their importance to improve the TPR/FPR trade-off. by updating the rule weights after model training.10 This
easespracticaldeploymentwhilepreservinginterpretabilityof
Robustness against Adversarial SQLi. As shown in Fig. 2,
decisions — an important desideratum for web security.
the ModSec-Learn models suffer the presence of adversar-
Imposing Sparsity through Regularization. We now ana-
ial attacks, particularly with the WAF-A-MoLE dataset, but
lyze the effects of regularization by examining whether it is
they still outperform the vanilla ModSecurity. Analyzing the
possible to select a reduced set of CRS rules as features for
results from the WAF-A-MoLE dataset, it is evident that,
the best performance is achieved with PL4, except for the 10https://owasp.org/www-project-waf-advanced-ruleset-management/

classification. We employ an ℓ regularization term to impose Fig. 4, third row). The reason is that SecSVM is retrained on
1
sparsity on the trained models and assess its impact on the less pessimistic attacks when considering problem-space AT,
importance of each CRS rule in the classification process. thereby yielding an improved robustness-accuracy tradeoff.
Additionally, we compare these results with those obtained Robustness against Adversarial SQLi. Over the adversar-
usingℓ regularization,thedefaultnormusedbySVMandLR. ial test set, ModSec-AdvLearn outperforms its non-hardened
2
Fig. 3 displays the distribution of rule weights for ModSec- counterparts, especially when evaluated with the WAF-A-
Learn implemented with LR at PL4. We selected this PL to MoLEdataset,reachingthushigherrobustness(seethedashed
activateallCRSrules,providingacomprehensiveoverviewof lines of Fig. 4). Looking at the results in detail, with the
theirimpact.Theblueandlightredbarsrepresenttheweights WAF-A-MoLE dataset, the re-trained models improve the
calculatedwithℓ andℓ regularization,respectively,whilethe average detection performance by 33% compared to their
1 2
green bars represent the ModSecurity severity scores. Since non-hardened versions. For the ModSec-Learn dataset, the
the severity score ranges from 2 to 5, we normalized it using improvementislessmarkedinsomemodels,suchasModSec-
the minimum and maximum values of the LR weights. The AdvLearn LR, but it is still present. Moreover, considering
results presented in Table III demonstrate that SVM and LR the WAF-A-MoLE dataset for example, the best ModSec-
with ℓ regularization can achieve the same performance as AdvLearn (i.e., RF at PL4) is 85% more robust than the best
1
the counterpart with ℓ regularization while utilizing fewer vanilla ModSecurity (PL2). Of course ModSec-AdvLearn is
2
rules. Specifically, in the WAF-A-MoLE dataset, the SVM stillvulnerabletonewadversarialexamplesoptimizedagainst
modelemployed13rulesfewerthanwiththeℓ norm,andthe it, but the decrement in performance is lower compared to the
2
LR model 21 fewer than LR with ℓ . For the ModSec-Learn decrement caused by the non-hardened models.
2
dataset, SVM used 14 fewer rules than SVM with ℓ norm, Explaining Robustness of ModSec-AdvLearn. Here we
2
while LR used 21 fewer. Additionally, it is important to note explain why ModSec-AdvLearn achieves better robustness,
that,comparedtothe62totalrulesinCRS,linearmodelswith focusingonthelinearSVMmodel.First,wecomputetherule
ℓ regularization,aswellasRF,alreadyreducethenumberof activation delta as ∆a = a −a′. It captures the difference
2 i i i
rulesusedintheclassificationprocesscomparedtothevanilla between the probability that rule i is activated by standard
ModSecurity. On average, these models use a maximum of SQLi attacks (a ) and by their adversarial counterparts (a′).
i i
50 rules, effectively eliminating 12 rules deemed unnecessary If ∆a is positive (negative), it means that WAF-A-MoLE
i
for classification. The rules assigned a weight of 0 by the is bypassing (activating) rule i, and if it is zero it means
ML models are considered unnecessary for the classification that WAF-A-MoLE does not affect rule i. Second, as we
task. Moreover, some rules may receive negative weights, are considering a linear model, we also inspect its feature
suggesting that their presence might be more indicative of weights and observe how they change when the same model
legitimate behavior rather than malicious activity. Applying is retrained on adversarial SQLi queries. Within this scenario,
this approach to the CRS introduces a more data-driven and we analyze how each rule is affected by the adversarial
lessarbitrarymethodforselectingdetectionrules.Ratherthan SQLi attacks generated through WAF-A-MoLE (Fig. 5), as
rely on manual selection or a predefined set of rules that may well as how differently the baseline ModSec-Learn SVM and
not be optimal for the specific data being classified, ModSec- the ModSec-AdvLearn SVM compute weights for each rule
Learn enables automation of both rule selection and weight (Fig. 5). In Fig. 5 we plot the probability that a rule is active,
assignment, optimizing CRS’s performance on the data. and we display how different the distributions induced by the
malicious (cyan) and adversarial (yellow) SQLi queries are.
D. Evaluation of ModSec-AdvLearn
The rules are sorted by their value of ∆a , and grouped into
i
Given the best results on PL4 among all the PLs in three classes (separated by vertical black lines): rules evaded
termsofTPR/FPR,weselectthisconfigurationforre-training byWAF-A-MoLE(left),rulesthatWAF-A-MoLEisunableto
all ModSec-Learn models. We then evaluate the ModSec- bypass(center),andrulesthataretriggeredonlybyadversarial
AdvLearn against the test and test-adv sets of both attacks as a side effect (right). The same order is also used
datasets, and plot the results in Fig. 4. Also, we report the for the weights of the ModSec-Learn SVM and the ModSec-
TPR of ModSec-AdvLearn at 1% FPR in the second-to-last AdvLearn SVM shown in Fig. 5. We can observe that more
column of Table III. Hereafter, we discuss the performance than one-third of the rules are exploited by WAF-A-MoLE to
of ModSec-AdvLearn in comparison with ModSec-Learn. avoiddetection,asthefirstgrouphasadropintheprobability
Overall, we observe that the robustness achieved by ModSec- of being active. This is also confirmed by Fig. 5, where we
AdvLearn clearly outperforms its non-hardened counterparts, can see that most of the positive weights (i.e., the ones that
i.e., ModSec-Learn. Finally, we analyze the weights and increase the scores towards the malicious class) assigned by
predictions of ModSec-AdvLearn, and we thoroughly explain ModSec-Learn (cyan) are all concentrated in the first group,
its remarkable level of adversarial robustness. which is exactly the one leveraged by adversarial attacks.
Evaluation on Clean Samples. In the absence of attack, Conversely, ModSec-AdvLearn (yellow) is more robust since
ModSec-AdvLearn has comparable performance to ModSec- it spreads the importance on more rules, prioritizing the ones
Learn, except for SecSVM which shows an improvement in belonging to the second and third groups, making attacks
TPRontheModSec-Learndataset(cf.thevioletsolidlinesin harder to land and easier to detect. Of course, in this analysis,

8
6
4
2
0
2
4
01001001200000000001000000010000120000001012012000000010120000
00233455567890123455678901223456667890122333444567890112223456
11111111111112222222222233333333333334444444444444445555555555
CRS SQLi Rules
thgieW
ModSec
ModSec-Learn (LR - 1)
ModSec-Learn (LR - 2)
Fig. 3: Weight values learned at PL4 by ModSec-Learn LR-ℓ (blue) and ModSec-Learn LR-ℓ (light red), and the weights
1 2
used by ModSecurity (green). Rules are expressed as the last three digits of their IDs (all starting with 942).
WAF-A-MoLE dataset (PL4) WAF-A-MoLE dataset (PL4)
1.0
0.8
0.6
0.4
1.0
0.8
0.6
0.4
10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100
False Positive Rate (FPR)
ModSec-Learn dataset (PL4) ModSec-Learn dataset (PL4)
1.0
0.8
0.6
0.4
1.0
0.8
0.6
0.4
10 4 10 3 10 2 10 1 100 10 4 10 3 10 2 10 1 100
False Positive Rate (FPR)
)RPT(
etaR
evitisoP
eurT
)RPT(
etaR
evitisoP
eurT
the other hand, as shown in Fig. 4, for the most of the cases
ModSec-AdvLearn RF is more robust than the linear models
counterpart as its non-linearity exploits relationships among
different rules, forcing the attacker to manipulate more rules
in a consistent manner to bypass detection.
V. RELATEDWORK
In this section, we briefly review related work analyzing
the performance and robustness of ModSecurity and the CRS,
andconcludebydiscussingthemaindifferencesofourcurrent
work with our preliminary results in [11].
ModSecurityandCRS.Previousworkhasconsideredtheim-
pactofdifferenttypesofwebsecuritythreatsonModSecurity
when using the CRS configurations [24, 25]. However, unlike
ours, a very limited number of attack samples is normally
used (e.g., [24] uses only 27 samples), without providing
any detailed investigation of the trade-off between TPR and
FPR. Other approaches [26, 27] have applied ML to detect
web threats and only used ModSecurity as a baseline for
comparison, without even evaluating adversarial robustness.
Adversarial SQLi. Other work has considered adversarial
SQLi attacks against ModSecurity by proposing different
approaches based on ML [5], Reinforcement Learning (RL)
[13, 28, 29], fuzzing techniques [10, 30], and heuristic search
algorithm like Monte-Carlo tree search [31]. However, the
reported results are partial (e.g., [13, 31] just limit the anal-
ysis to the default PL1) and do not explain precisely why
ModSecurity is failing and how it could be improved. To
the best of our knowledge, no prior research has conducted
a comprehensive analysis of the CRS for ModSecurity as we
RF SecSVM SVM 1 SVM 2 LR 1 LR 2
havedoneinthiswork.Additionally,nopreviousstudieshave
Fig. 4: ROC curves of ModSec-Learn/AdvLearn (first/second
explored the potential of adversarial training in this domain,
column) on test/test-adv (solid/dashed lines), for WAF-
making us the first to propose a robust ML methodology for
A-MoLE/ModSec-Learn (top/bottom) datasets.
effectively enhancing the robustness of WAFs.
ModSec-Learn. With respect to our work introducing
ModSec-Learnin[11],wehaveextendedhereourapproachas
we focus on a linear model, which, as shown in Sect. IV-D follows:(i)wehaveexaminedtheimpactofadversarialattacks
is still vulnerable to adversarial attacks. Indeed, by looking ontheCRSwithintheSQLdomain;(ii)wehaveincreasedthe
at Fig. 5, ModSec-AdvLearn attributes negative weights (i.e., robustness of our approach by developing a novel adversarial
thosethatdecreasethescoretowardsthebenignclass)tosome training procedure (ModSec-AdvLearn); (iii) we have inves-
featuresofthefirstblock,henceleavingtheabilitytoWAF-A- tigated whether strongly-regularized models could withstand
MoLE to find some successful adversarial SQLi queries. On adversarialSQLiattacks,devisinganovelversionofSecSVM;

1.0
0.8
0.6
0.4
0.2
0.0
0000000000000120000000100120010010112120000012000000000011000
3013466309889266404581572052557922233446715662583230174513924
3421521231243533112334113112222234444444455535115542334451413
CRS SQLi Rules
ytilibaborp
noitavitcA
SVM - 1
adversarial
malicious
0.4
0.3
0.2
0.1
0.0
0.1
0.2
0000000000000120000000100120010010112120000012000000000011000
3013466309889266404581572052557922233446715662583230174513924
3421521231243533112334113112222234444444455535115542334451413
CRS SQLi Rules
thgieW
ModSec-AdvLearn
ModSec-Learn
Fig.5:Top:ActivationprobabilityofCRSrules(expressedusingthelastthreedigitsoftheirIDs,whichalwaysstartswith942)
onmalicious/adversarial(cyan/orange)SQLisamplesoptimizedagainstModSec-LearnSVM-ℓ ontheWAF-A-MoLEdataset.
1
Bottom: Rule weights learned by ModSec-Learn/ModSec-AdvLearn SVM-ℓ (cyan/orange) on the WAF-A-MoLE dataset.
1
(iv)wehaveanalyzedhowthebaselineandModSec-AdvLearn future work could also explore the integration of automated
compute weights for each rule, highlighting which rules are pentesting tools that leverage large language models [32], to
more robust to perturbations; and (v) we have included an extendthecapabilitiesofWAF-A-MoLE.Second,wealsosee
additional dataset [10] in our experiments. future developments in evaluating other state-of-the-art ML-
based WAFs. Indeed, we think that the same results can also
VI. CONCLUSIONSANDFUTUREWORK be obtained on more advanced models such as Convolutional
In this work, we proposed ModSec-AdvLearn, a novel Neural Networks (CNN) [33], as well as on different feature
methodologyfortrainingMLclassifiersusingtheCRSrulesas representation approaches [27, 34]. This is also true for
input features. This allows learning how to optimally tune the commercialWAFs.Tothisend,aninterestingfutureextension
severitylevels(i.e.,theweights)oftheCRSrules,yieldingan ofthisworkistoevaluatethemintermsoftransferability[35]
improved trade-off between detection and false positive rates. of adversarial SQLi attacks optimized on ModSecurity.
Furthermore, our approach relies upon a novel problem-space ACKNOWLEDGMENTS
adversarial training procedure that incorporates knowledge of
This research has been partly supported by the TESTABLE
state-of-the-art SQLi manipulations to counter the presence
project, funded by the EU H2020 research and innovation
of adversarial SQLi attacks. Among the main findings, we
program (grant no. 101019206); the ELSA project, funded by
show that ModSec-AdvLearn improves the detection rate of
the Horizon Europe research and innovation program (grant
the vanilla ModSecurity by 30%, while removing 50% of
no. 101070617); projects FAIR (PE00000013) and SERICS
the CRS rules through embedded feature selection with ℓ
1 (PE00000014) under the NRRP MUR program funded by the
regularization. It also improves adversarial robustness up to
EU – NGEU. This work was carried out while C. Scano
85%viarobustlinear models,withouthinderinginterpretabil-
was enrolled in the Italian National Doctorate on AI run by
ity of decisions and providing ease of integration with the
the Sapienza University of Rome in collaboration with the
current CRS implementations. We can thus state that our
University of Cagliari.
methodology provides a first, concrete example of how adver-
sarial machine learning can beused to effectively enhance the REFERENCES
robustness of WAFs against adversarial attacks, highlighting [1] O. B. Fredj, O. Cheikhrouhou, M. Krichen, H. Hamam,
novel, promising directions towards designing robust machine and A. Derhab, “An OWASP top ten driven survey on
learning models for cybersecurity-related applications. web application protection methods,” in 15th Int’l Conf.
We foresee several other promising avenues for advancing Risks&Sec.ofInternetSys.(CRiSIS),p.235–252,2020.
our work. First, although in this work we only target SQLi [2] W. G. J. Halfond and A. Orso, “Preventing sql injection
attacks, our methodology is general enough to tackle other attacksusingamnesia,”inProc.ofthe28thInt.Conf.on
web threats like cross-site scripting (XSS). In this direction, Software Engineering (ICSE), p. 795–798, 2006.

[3] A. Joshi and V. Geetha, “SQL injection detection using and Secure Computing, vol. 16, pp. 711–724, 2019.
machinelearning,”in2014Int.Conf.Control,Instrumen- [21] L. Demetrio, B. Biggio, G. Lagorio, F. Roli, and A. Ar-
tation, Comm. Comput. Tech., pp. 1111–1115, 2014. mando, “Functionality-preserving black-box optimiza-
[4] D. Appelt, A. Panichella, and L. Briand, “Automatically tion of adversarial windows malware,” IEEE Trans. on
repairing web application firewalls based on successful Inform.ForensicsandSec.,vol.16,pp.3469–3478,2021.
sql injection attacks,” in 2017 IEEE 28th Int. Symp. on [22] H. Xu, C. Caramanis, and S. Mannor, “Robustness and
Software Reliability Eng. (ISSRE), pp. 339–350, 2017. regularization of support vector machines.,” Journal of
[5] D. Appelt, C. D. Nguyen, A. Panichella, and L. C. machine learning research, vol. 10, no. 7, 2009.
Briand, “A machine-learning-driven evolutionary ap- [23] I. Corona, B. Biggio, M. Contini, L. Piras, R. Corda,
proachfortestingwebapplicationfirewalls,”IEEETrans. M. Mereu, G. Mureddu, D. Ariu, and F. Roli,
on Reliability, vol. 67, no. 3, pp. 733–757, 2018. “Deltaphish: Detecting phishing webpages in compro-
[6] OWASPFoundationInc.,“OWASPtop10,”2021. Avail- mised websites,” in ESORICS 2017, pp. 370–388, 2017.
able online. Accessed on 22 February 2023. [24] J. J. Singh, H. Samuel, and P. Zavarsky, “Impact of
[7] S. Applebaum, T. Gaber, and A. Ahmed, “Signature- paranoia levels on the effectiveness of the modsecurity
based and machine-learning-based web application fire- web application firewall,” in 1st Int. Conf. on Data
walls: A short survey,” Procedia Computer Science, Intelligence and Security (ICDIS), pp. 141–144, 2018.
vol. 189, pp. 359–367, 2021. [25] T.D.Sobola,P.Zavarsky,andS.Butakov,“Experimental
[8] OWASP Foundation Inc., “OWASP core rule set.” https: studyofmodsecuritywebapplicationfirewalls,”inIEEE-
//coreruleset.org, 2024. Accessed on 20th January 2024. BigDataSecurity, HPSC and IDS, pp. 209–213, 2020.
[9] C. Folini and I. Ristic, ModSecurity Handbook, Second [26] G. Betarte, A´. Pardo, and R. Mart´ınez, “Web application
Edition. London, GBR: Feisty Duck, 2nd ed., 2017. attacks detection using machine learning techniques,” in
[10] L. Demetrio, A. Valenza, G. Costa, and G. Lagorio, 17th IEEE Int’l Conference on Machine Learning and
“Waf-a-mole: Evading web application firewalls through Applications (ICMLA), pp. 1065–1072, IEEE, 2018.
adversarial machine learning,” in 35th Annual ACM [27] N.Montes,G.Betarte,R.Mart´ınez,andA.Pardo,“Web
Symp.onAppliedComputing(SAC),p.1745–1752,2020. applicationattacksdetectionusingdeeplearning,”in25th
[11] C. Scano, G. Floris, B. Montaruli, L. Demetrio, ProgressinPatt.Rec.,ImageAnalysis,ComputerVision,
A. Valenza, L. Compagna, D. Ariu, L. Piras, and Applications, pp. 227–236, Springer, 2021.
D. Balzarotti, and B. Biggio, “Modsec-learn: Boosting [28] X.WangandH.HU,“Evadingwebapplicationfirewalls
modsecurity with machine learning,” in Int’l Symp. with reinforcement learning,” 2020.
Distributed Comput. and AI, pp. 23–33, Springer, 2024. [29] Y. Guan, J. He, T. Li, H. Zhao, and B. Ma, “Ssqli:
[12] A. Zeller, R. Gopinath, M. Bo¨hme, G. Fraser, and A black-box adversarial attack method for sql injec-
C. Holler, “Mutation-based fuzzing,” in The Fuzzing tion based on reinforcement learning,” Future Internet,
Book, CISPA Helmholtz Center for Inform. Sec., 2023. vol. 15, no. 4, p. 133, 2023.
[13] M.HemmatiandM.A.Hadavi,“Bypassingwebapplica- [30] K. Li, H. Yang, and W. Visser, “DaNuoYi: Evolutionary
tionfirewallsusingdeepreinforcementlearning,”in18th multi-taskinjectiontestingonwebapplicationfirewalls,”
Int. ISC Conf. Inform. Sec. Crypt., pp. 35–41, 2021. IEEE Trans. on Software Engineering, 2023.
[14] F. Pierazzi, F. Pendlebury, J. Cortellazzi, and L. Cav- [31] Z. Qu, X. Ling, and C. Wu, AutoSpear: Towards Au-
allaro, “Intriguing properties of adversarial ml attacks tomatically Bypassing and Inspecting Web Application
in the problem space,” in IEEE Symp. on Security and Firewalls. Black Hat Asia, 2022.
Privacy (SP), pp. 1332–1349, IEEE, 2020. [32] G.Deng,Y.Liu,V.Mayoral-Vilches,P.Liu,Y.Li,Y.Xu,
[15] C. Cortes and V. Vapnik, “Support-vector networks,” T. Zhang, Y. Liu, M. Pinzger,and S. Rass, “PentestGPT:
Machine Learning, vol. 20, no. 3, 1995. Evaluating and harnessing large language models for
[16] C. M. Bishop and N. M. Nasrabadi, Linear Models for automatedpenetrationtesting,”in33rdUSENIXSecurity
Classification, vol. 4. Springer, 2006. Symp., pp. 847–864, 2024.
[17] L. Breiman, “Random forests,” Machine learning, [33] A. Luo, W. Huang, and W. Fan, “A cnn-based approach
vol. 45, pp. 5–32, 2001. to the detection of sql injection attacks,” in IEEE/ACIS
[18] A. Madry, A. Makelov, L. Schmidt, D. Tsipras, and 18th Int. Conf. on Computer and Information Science
A. Vladu, “Towards deep learning models resistant to (ICIS), pp. 320–324, IEEE, 2019.
adversarial attacks,” in ICLR, 2018. [34] D. Kar, S. Panigrahi, and S. Sundararajan, “Sqligot:
[19] B. Biggio and F. Roli, “Wild patterns: Ten years after Detectingsqlinjectionattacksusinggraphoftokensand
the rise of adversarial machine learning,” Pattern Recog- svm,”Computers&Security,vol.60,pp.206–225,2016.
nition, vol. 84, pp. 317–331, 2018. [35] A. Demontis, M. Melis, M. Pintor, M. Jagielski, B. Big-
[20] A. Demontis, M. Melis, B. Biggio, D. Maiorca, D. Arp, gio, A. Oprea, C. Nita-Rotaru, and F. Roli, “Why do
K. Rieck, I. Corona, G. Giacinto, and F. Roli, “Yes, adversarial attacks transfer? explaining transferability of
machine learning can be more secure! a case study on evasionandpoisoningattacks,”in28thUSENIXSecurity
androidmalwaredetection,”IEEETrans.onDependable Symp., pp. 321–338, 2019.

GiuseppeFlorisreceivedhisBScdegreeinElectri- LucaCompagnaworksatEndorLabs,contributing
cal,EletronicalandComputerEngineeringin2021, to the software security analysis research area. He
and his MSc degreein ComputerEngineering, Cy- receivedhisPh.D.inComputerSciencejointlyfrom
bersecurity,andArtificialIntelligencewithhonorsin the U. of Genova and U. of Edinburgh, working
September2023fromtheUniversityofCagliari.He on security protocols analysis. His areas of inter-
iscurrentlyaPh.D.studentinelectronicsandcom- ests include security testing, security engineering,
puterengineeringattheUniversityofCagliari.His automated reasoning, and their application to the
research focuses on Adversarial Machine Learning modelingandanalysisofindustrialrelevantscenar-
anditsapplicationsinthecybersecuritydomain. ios.AftersomeworkonDASTtechniquesforcross
domainweb-basedscenariosandCSRFexperiments,
he recently focused his attention to static analysis
andtothesecuritytestingofAI-basedcomponents.
Christian Scano received his BSc degree in Com-
puter Science in 2021 and his MSc degree in
ComputerEngineering,Cybersecurity,andArtificial DavideAriureceivedaPhDinelectronicsandcom-
Intelligence with honors in September 2024 from puter engineering from the University of Cagliari.
the University of Cagliari. He is currently enrolled He is co-founder and CEO of Pluribus One
in the national PhD in Artificial Intelligence and (http://www.pluribus-one.it) and co-chair of the
Computer Security at University of Cagliari and OWASP(http://owasp.org)ItalyChapter.
SapienzaUniversityofRome.Hisresearchfocuses
onWebApplicationSecurityandMachineLearning.
BiagioMontarulireceivedhisB.Sc.andM.Sc.de-
greesincomputerengineeringfromthePolytechnic
UniversityofBari(Bari),in2018and2021,respec- Luca Piras is the Operation Manager and Co-
tively.HeiscurrentlyaPh.D.candidateinartificial founder of Pluribus One. He received his MSc
intelligence and computer security at EURECOM Degree in Electronic Engineering in 2007 and his
(France). His research focuses on adversarial ma- Doctor Europaeus and PhD Degree in Computer
chine learning, with strong focus on its application Engineering in 2011, both from the University of
inthecyber-securitydomain. Cagliari. His expertise lies in Computer Vision,
Pattern Recognition, and Machine Learning. His
researchhasbeenpublishedinseveralinternational,
peer-reviewedjournalsandconferences.AtPluribus
One,heisresponsibleforseveralEU-fundedR&D
projectsandisamemberoftheOWASPFoundation.
Luca Demetrio (MSc 2017, PhD 2021) is an As-
sistant Professor at the University of Genoa, inves-
tigatingthesecurityofWindowsmalwaredetectors
DavideBalzarottiisafullProfessorandheadofthe
implementedwithMachineLearningtechniques.He
DigitalSecurityDepartmentatEURECOM.Hisre-
ispartofthedevelopmentteamofSecML,andthe
searchinterestsincludemostaspectsofsoftwareand
maintainerofSecMLMalware,aPythonlibraryfor
systemsecurityandinparticulartheareasofbinary
creatingadversarialWindowsmalware.
andmalwareanalysis,reverseengineering,computer
forensics, and web security. Davide authored more
than 100 publications in leading conferences and
journals. He has been the Program co-Chair of
Usenix Security 2024, ACSAC 2017, RAID 2012,
andEurosec2014.HereceivedanERCConsolidator
Andrea Valenza is an Application Security Engi- and an ERC PoC Grant for his research in the
neer at Prima Assicurazioni. He received his PhD analysis of compromised systems. Davide is also a member of the “Order
fromtheUniversityofGenova,withathesisfocused of the Overflow” team, which organized the DEF CON CTF competition
onnovelvulnerabilities,includingcounter-attacking between2018and2021.
automatic security scanners. His current research
interestisautomatedsecuritytesting,withafocuson
improving (and bypassing) regex-based validation,
Battista Biggio (MSc 2006, PhD 2010) is Full
anddetectionofvulnerabilitiesviastaticanalysis.
Professor of Computer Engineering at the Univer-
sity of Cagliari, Italy. He has provided pioneer-
ing contributions to machine learning security. His
paper “Poisoning Attacks against Support Vector
Machines”wontheprestigious2022ICMLTestof
Time Award. He chaired IAPR TC1 (2016-2020),
and served as Associate Editor for IEEE TNNLS
andIEEECIM.HeisnowAssociateEditor-in-Chief
forPatternRecognitionandservesasAreaChairfor
NeurIPSandIEEESymp.SP.HeisFellowofIEEE
andAAIA,ACMSeniorMember,andMemberofIAPR,AAAI,andELLIS.
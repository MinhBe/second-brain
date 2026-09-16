IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 1
AdvSQLi: Generating Adversarial SQL Injections
against Real-world WAF-as-a-service
Zhenqing Qu*, Xiang Ling*†, Ting Wang, Xiang Chen, Member, IEEE, Shouling Ji, Member, IEEE,
Chunming Wu†
Abstract—As the first defensive layer that attacks would hit, locations, with different scales and through different methods.
the web application firewall (WAF) plays an indispensable role Commonwebthreats[1]includeSQLinjection(SQLi),cross-
in defending against malicious web attacks like SQL injection
sitescripting,cross-siterequestforgery,anddistributeddenial-
(SQLi). With the development of cloud computing, WAF-as-a-
of-service,tonamejustafew.Accordingto[2],[3],[4],SQLi
service, as one kind of Security-as-a-service, has been proposed
to facilitate the deployment, configuration, and update of WAFs isoneofthemostcommonandthreateningattackmethods,by
in the cloud. Despite its tremendous popularity, the security whichtheattackerexploitssecurityvulnerabilitiesbyperform-
vulnerabilities of WAF-as-a-service are still largely unknown, ing SQL queries on the database, thereby directly accessing
whichishighlyconcerninggivenitsmassiveusage.Inthispaper,
unauthorized information, creating new user permissions, or
we propose a general and extendable attack framework, namely
even taking control of the underlying system.
AdvSQLi, in which a minimal series of transformations are
performedonthehierarchicaltreerepresentationoftheoriginal In particular, as illustrated in Figure 1(a), suppose there
SQLi payload, such that the generated SQLi payloads can not is a web server with a back-end script and a correspond-
only bypass WAF-as-a-service under black-box settings but also ing database. A normal client Alice can send a request of
keep the same functionality and maliciousness as the original
“getinfo?uid=1”, and receive her information. However, if an
payload. With AdvSQLi, we make it feasible to inspect and
attacker maliciously crafts an SQLi payload (i.e., “1’ or 1
understand the security vulnerabilities of WAFs automatically,
helping vendors make products more secure. = 1 --+”) within the request as shown in Figure 1(b), the
ToevaluatetheattackeffectivenessandefficiencyofAdvSQLi, attacker can receive all users’ information because the “or 1
we first employ two public datasets to generate adversarial = 1” makes the querying condition to be satisfied.
SQLi payloads, leading to a maximum attack success rate of TomitigatemaliciousrequestsliketheSQLiinthewild,the
100%againststate-of-the-artML-basedSQLidetectors.Further-
webapplicationfirewall(WAF)isoneofthemostwidelyused
more, to demonstrate the immediate security threats caused by
AdvSQLi,weevaluatetheattackeffectivenessagainst7WAF-as- and effective defensive systems [5], [6], [7]. WAF is normally
a-servicesolutionsfrommainstreamvendorsandfindallofthem deployed in the front of the back-end script, indicating that
are vulnerable to AdvSQLi. For instance, AdvSQLi achieves an any request from clients must be detected and filtered by the
attack success rate of over 79% against the F5 WAF. Through
WAF. Only requests detected as benign will be forwarded to
in-depth analysis of the evaluation results, we further condense
the back-end script for further processing. Therefore, WAFs
out several general yet severe flaws of these vendors that cannot
be easily patched. play a pivotal role in the immediate response to emerging
security vulnerabilities. For example, during the outbreak of
Index Terms—web security, WAF-as-a-service, SQL Injection,
the log4shell vulnerability, Cloudflare, among other vendors,
adversarial payloads
acted promptly by implementing detection rules within their
WAFinfrastructure[8].Todate,extensiveresearcheffortshave
I. INTRODUCTION
proposed tremendous WAF strategies to defend against SQLi.
Withthecontinuousevolutionandglobaldeploymentofthe These strategies can be broadly categorized into signature-
internet,webservicesareplayingincreasinglyimportantroles based (a.k.a rule-based) SQLi detection and machine learning
of social infrastructure in daily lives. On the other hand, they (ML)-based SQLi detection [9]. Signature-based SQLi detec-
are also being exposed to world-wide threats from different tion[10],[11],[12]isatraditionalbuteffectivestrategywhich
takesadvantageofvariousrulespre-definedbydomainexperts
This work is supported by the National Key R&D Program of China todetectmaliciousrequests.Moreover,motivatedbythegreat
(No.2022YFB2901305), the “Pioneer” and “Leading Goose” R&D Program
success of ML obtained from various tasks, a variety of ML-
ofZhejiang(No.2022C01085),andtheFundamentalResearchFundsforthe
Central Universities (Zhejiang University NGICS Platform). Xiang Ling is based SQLi detectors [13], [14], [15] have been proposed and
also supported by the National Natural Science Foundation of China under implemented, which learn to discriminate malicious requests
No.62202457.
based on the supervision of previously labelled datasets.
Zhenqing Qu, Xiang Chen, Shouling Ji, Chunming Wu are with the
CollegeofComputerScienceandTechnology,ZhejiangUniversity,Hangzhou Nevertheless, regardless of which kind of strategies are
310027, China (e-mail: quzhenqing@zju.edu.cn, wasdnsxchen@gmail.com, adoptedinWAFs,itisquitetroublesometodeploy,configure,
sji@zju.edu.cn, wuchunming@zju.edu.cn). Xiang Ling is with the Institute
and updatethe signaturesor modelsfor effectively andtimely
of Software, Chinese Academy of Science, Beijing 100190, China (e-mail:
lingxiang@iscas.ac.cn). Ting Wang is with the Department of Computer protection of the web server [16]. With the development of
Science at Stony Brook University, Stony Brook, NY 11794-2424, United cloud computing, WAF-as-a-service, as one kind of Security-
States(e-mail:twang@cs.stonybrook.edu).
*ZhenqingQuandXiangLingcontributeequallytothisresearch. as-a-service, has been proposed to facilitate the deployment,
†XiangLingandChunmingWuaretheco-correspondingauthors. configuration, and update of WAFs. The administrator who
4202
naJ
9
]RC.sc[
3v51620.1042:viXra

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 2
manages the web server only needs to redirect all requests to WAF-as-a-service solutions based on adversarial SQLi pay-
the interfaces of WAF-as-a-service provided by vendors, such loads under strict black-box settings.
that malicious requests like SQLi can be detected and filtered • ExtensiveevaluationresultsdemonstratethatAdvSQLinot
before being forwarded to the web server. only achieves a maximum success rate of 100% against
Despite the tremendous popularity and impressive perfor- state-of-the-art SQLi detection models but also bypasses
mance of WAF-as-a-service in detecting malicious requests, 7 mainstream commercial WAF-as-a-service products with
thesecurityvulnerabilitiesofWAFsarestilllargelyunknown, high attack success rates.
which is highly concerning given the massive usage of WAF-
as-a-service in the cloud. For instance, Peter M managed to
II. PROBLEMFORMULATION
bypassAkamai’sWAF,triggeringaserver-sidetemplateinjec-
tion (SSTI) vulnerability in a Spring Boot application, which In this section, we present the threat model of this paper.
thenledtoremotecommandexecution[17].Inasimilarvein,
the AON team used encoded payloads to successfully bypass
A. Adversary’s Goal
Cloudflare’sWAF,enablingthemtoexploittheObjectGraphic
Navigation Language (OGNL) injection vulnerability [18]. To Given an SQLi detector f :X →Y, which maps a pay-
inspect and understand the security vulnerabilities of WAFs load x∈X to a corresponding label y ∈Y ={0,1} (i.e.,
automatically,weproposeAdvSQLi,ageneralandextendable 0 indicates benign and 1 indicates malicious), an adversary
attack framework that can effectively and efficiently generate aims to generate an adversarial payload x adv which can be
adversarial SQLi payloads to bypass real-world WAF-as-a- misclassified by f, i.e., f(x adv )̸=f(x).
service under the black-box settings, as the feedback output We consider a realistic scenario that an SQLi payload x
ofWAF-as-a-servicetotheattackertypicallyisbinary.Witha which is originally correctly classified as malicious by f
large and diverse set of payloads, we are capable of systemat- (i.e., f(x)=1), while the adversary attempts to generate an
ically assessing and understanding the security vulnerabilities adversarial SQLi payload x adv from x with minimal efforts,
within WAFs. such that x adv can not only bypass the SQLi detector (i.e.,
In particular, AdvSQLi first represents the original SQLi f(x adv )=0) but also preserves the same semantics (i.e.,
payload with a hierarchical tree and then employs a weighted functionality and maliciousness) as x as follows.
mutation strategy based on the context-free grammar to gen-
erate a set of equivalent SQLi payloads, which keep the argminf(x )
adv
same functionality and maliciousness as the original SQLi T
payload. Finally, AdvSQLi exploits the Monte-Carlo tree s.t f(x)=1
(1)
search as a novel approach to efficiently guide the exploration x =T(x)
adv
of adversarial SQLi payloads in the vast space.
Sem(x )=Sem(x)
Extensive evaluation results demonstrate that AdvSQLi adv
outperforms all baseline attack methods with regard to the in which T denotes the adversarial function that generates
attack effectiveness and efficiency, achieving a maximum adversarial payload x from the input payload x, while
adv
success rate of 100% against ML-based SQLi detection mod- Sem(x) is the semantic analyzer to check if x and x are
adv
els within fewer queries. Furthermore, we also evaluate the semantic-equivalent.
attack effectiveness of AdvSQLi against 7 WAF-as-a-service
solutions in the wild from mainstream vendors (i.e., AWS,
B. Adversary’s Capability
Cloudflare, F5, Fortinet, Wallarm, CSC, and ModSecurity)
under 4 practical request methods, and draw a conclusion that In this paper, we consider a classic but strict black-box
the generated payloads can bypass most of them, indicating attack in the problem space [19], [20], in which the adversary
the immediate threats caused by AdvSQLi. For instance, limits the attack surface to the testing phase while does
AdvSQLi achieves the attack success rate of over 79% not have any information on the target SQLi detector (e.g.,
against the F5 WAF. To summarize, we make the following architectures, parameters, feature representations, etc.) except
contributions. for the input and output. According to the output information
• We present and implement AdvSQLi, in which a weighted of different SQLi detectors in the wild, the black-box attacks
mutation strategy based on context-free grammar is first can be further divided into two cases. The first is the black-
proposed to generate a vast space of equivalent SQLi boxattackswithprobability(BBw/prob.),inwhichthetarget
payloads. Then, the Monte-Carlo tree search is exploited to SQLi detector (e.g., ML-based SQLi detectors) can output the
efficientlyselecttheadversarialpayloadfromthevastspace. predicted label (i.e., y =0 or 1) as well as the corresponding
Manual changes are unnecessary when attacking different probability (i.e., p ∈ [0,1]). The second is the black-box
y
WAF-as-a-service concerning unique payloads under kinds attacks without probability (BB w/o prob.), in which the
of request methods, namely, AdvSQLi is a broad-spectrum target SQLi detector can only output the predicted label (i.e.,
attack framework that works out of the box with strong y =0 or 1). In fact, for the adversary that targets most WAF-
generalizability and extensibility. as-a-service in the wild, it is a strict black-box attack, i.e.,
• To the best of our knowledge, this is the first work system- BB w/o prob., by which the adversary can only judge by the
atically assesses the security vulnerabilities of real-world HTTP status code.

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 3
https://examples.com/getInfo?uid=1 select info from user where id = ‘1’;
User Alice Alice’s Info Back-end Alice’s Info Database
Script
(a) TheinnocentuserAlicecangetherowninformation.
https://examples.com/getInfo?uid=1’ or 1 = 1 --+ select info from user where id =
SQLi Payload ‘1’ or 1 = 1 --’;
Ordinary All Users’ Info Back-end All Users’ Info Database
Attacker Script
(b) TheordinaryattackerperformsSQLiattackandstealsallusers’information.
getInfo?uid=1 getInfo?uid=1 select info from user where id = ‘1’;
User Alice Alice’s Info Alice’s Info Back-end Alice’s Info Database
WAF-as-a-service Script
(c) Alicecanstillgetherowninformation.
getInfo?uid=
1’ or 1 = 1 --+ Cannot Reach
Ordinary 403 Forbidden Back-end Database
Attacker WAF-as-a-service Script
(d) Theordinaryattacker’srequestisblockedbytheWAF-as-a-service.
getInfo?uid= getInfo?uid= select info from user where id =
1’ || 0x1 /*!=*/0x1/*foo*/ --+ 1’ || 0x1 /*!=*/0x1/*foo*/ --+ ‘1’ || 0x1 /*!=*/0x1/*foo*/ -- ’;
All Users’ Info All Users’ Info All Users’ Info
AdvSQLi Back-end Database
WAF-as-a-service Script
(e) AdvSQLisuccessfullybypassestheWAF-as-a-serviceandstealsallusers’information.
Fig. 1. Illustration of how our proposed attack AdvSQLi can bypass the WAF-as-a-service to acquire all users’ information, compared with the ordinary
attackerandtheinnocentuser.Notethatthearchitectureoftheinfrastructuresinproductionenvironmentsmaybemorecomplicatedthaninthisdiagram,yet
itdoesnotimpacttheeffectivenessofAdvSQLi.
III. RELATEDWORKANDCHALLENGES cantriggerthevulnerability.Onthecontrary,withtheprocess
of finding semantic-preserving payloads for a failed payload,
Thissectionprovidesabriefstudydescriptionofuntargeted
the targeted attacks, can systematically assess the security
black-box testing and adversarial attacks in the traditional
vulnerabilities based on a diverse set of malicious payloads.
domains, and their difference with our task.
Demetrio et al. [25] proposed WAF-A-MoLE, a tool that can
Automated Black-box Testing (Untargeted Attacks). In
evade ML-based WAFs for failed payloads. They first defined
the last decade, there has been abundant research on em-
7string-basedSQLipayloadmutationoperatorsandemployed
ploying algorithms to facilitate vulnerability discovery [21],
a priority queue to guide the mutation process. Specifically,
including finding vulnerabilities in applications and firewalls
WAF-A-MoLE repeatedly mutates the initial payload to gen-
toreducethemanualworkload.Trippetal.[22]proposedXSS
erateseveralpayloadsandselectsthemutatedpayloadwiththe
Analyzer, a learning-based black-box testing method for web
lowestmaliciousscoreastheinitialpayloadforthenextround,
applications.Itlearnsfromfailedattemptstoprunethesearch
until it bypasses the target WAF or reaches the termination
space. Further, Appelt et al. [7], [23] proposed ML-Driven,
condition.Inspiredbytheworkofevadingmalwaredetectors,
a search-based approach that combines ML and evolutionary
Wangetal.[26]proposedaWAFevasionframeworkbasedon
algorithms (EAs) to test the detection capabilities of WAFs.
RL. They followed the mutation operators in [25] and defined
ML-Driven selects payloads with high bypassing probabilities
a feature vector of three levels of histograms to represent
and mutates them with the help of EAs to generate payloads.
the State of the SQLi payload. After training with Deep
Zhang et al. [3] proposed ART4SQLi, an adaptive random
Q-learning (DQN) and Proximal Policy Optimization (PPO)
testing method for SQLi vulnerability detection, which is
algorithms, the RL Agent can select an optimal mutation
basedonthecontext-freegrammartoparseandextractpayload
operator according to the current State. Hemmati et al. [27]
features. ART4SQLi chooses payloads far from the initial
improved [26] in several aspects, including expanding the
payload from existing collections until it bypasses the target
mutation methods, defining State based on the FastText, etc.
WAF.Amoueietal.[24]proposedRAT,whichclusterssimilar
payloads based on n-gram features. However, the above approaches are not satisfactory in
Automated WAF Bypassing (Targeted Attacks). The some aspects. Firstly, the mutation methods depend on string
above work proposes valuable concepts, e.g., learning-based replacement based on regular expression (RE), which is
methodsthatcanspeedupthevulnerabilitydiscoveryprocess. not semantic-preserving. According to the Chomsky hier-
However, they do not need to preserve the functionality of archy [28], the RE-based rule descriptions (i.e., rule-based
the payload, but only need to find an arbitrary payload that grammar) cannot fully cover the program-language-based at-

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 4
tack payloads (e.g., SQLi payloads). That is, the string-based on the basis of the hierarchical tree, AdvSQLi employs a
mutation method may miss mutable parts of the payload. weightedmutationstrategybasedonthecontext-freegrammar
Besides, it is possible to damage the original function of to generate a set of equivalent SQLi payloads, which keep
the SQLi payload, which we will prove through subsequent the same functionality and maliciousness as the original one.
evaluations. In addition, the binary output and the practical With the two steps, we implement a semantic-preserving
limitation of probing attempts by WAF-as-a-service further mutation method according to the semantics, characteristics,
challengetheadaptabilityofpriorityqueueandRLmethodsin and constraints of the original payload. Finally, AdvSQLi
real-worldscenarios,necessitatingamorestrategicandsparing exploits the Monte-Carlo tree search as a novel approach to
useofmutationattempts[29],[30].Literatureinothersecurity efficiently guide the exploration of adversarial SQLi payloads
fields [31], [32], [33] also pointed out that approaches based inthevastspace.IntheMonte-Carlotreesearch,themalicious
on RL cannot achieve surprising results in such problems due scoresfeedbackbyWAFsareunnecessary.Thatis,AdvSQLi
to limitations such as the representation of feature state. is capable of attacking real-world WAFs.
AdversarialAttacks.Intraditionaladversarialattacktasks,
suchasimages[34],theadversaryperformssmalldisturbances
inthecontinuousspacewithoutaffectingthepresentationform
to evaluate the vulnerabilities of image classification models. A. Hierarchical Tree Representation
However, as to generating adversarial SQLi payloads, the
Normally, a HTTP URL (e.g., https://examples.com/
adversary can only perform problem space transformations in
getInfo?uid=1) consists of four elements: schema (i.e.,
the discrete space. Moreover, the gradient-based optimization
“https”), domain name (i.e., “examples.com”), path to the
methods (e.g., FGSM [35]) in continuous space cannot be
resource (i.e., “getInfo”) and the parameter(s) (i.e., “?uid=1”)
applied to guide our attack procedure, as an SQLi payload
with multiple pairs of key (i.e., “uid”) and value (i.e., “1”,
is a discrete object and the adversary does not have any
also termed as payload). In fact, the process of SQL injection
information of f [36]. Previous work in adversarial NLP
attack is limited to the core part of URL, i.e., the parameter
presents valuable mutation methods in the discrete space. For
value(s), and keeps other parts unchanged. For example, the
example, Li et al. [37] proposed several mutation methods to
SQLi attack can inject a malicious payload of “'or 1 = 1 --
deceiveML-basedtextunderstandingmodels.Asthemeaning
+” at the end of the original payload of “1”, resulting in a
of the text is likely to be preserved by human readers after
maliciousURL,i.e.,https://examples.com/getInfo?uid=1' or1
these slight character changes [38], these mutation methods
= 1 --+.
are acceptable. However, these works cannot be applied to
generate SQLi payloads, as the generated payload has to Recall that the goal of AdvSQLi is to generate adversarial
keep the same functionality and maliciousness as the original SQLipayloadsbasedontheoriginalSQLipayload.Therefore,
one [19]. AdvSQLi should not only be limited to the payload of the
KeyChallenges.Inconclusion,theprincipalchallengeswe original SQLi (i.e., 1' or 1 = 1 --+), but also ensure that
encounter in effectively and efficiently generating payloads the generated adversarial SQLi has the same functionality
that bypass detection are twofold: and maliciousness as the original injection. To address this
1) Semantic Preservation: There is a critical absence problem, according to the different roles played by different
of a truly semantic-preserving mutation method for SQLi partsintheoriginalSQLi,wedividetheoriginalSQLipayload
payload generation. 2) Optimization in Discrete Space: The into three modules, i.e., left boundary (i.e., “1'”), query (i.e.,
default strategy in the vast and discrete problem space has “ or 1 = 1”) and right boundary (i.e., “--+”), and further
been to employ random transformations. This approach lacks limit the attack surface of AdvSQLi to the module of query
efficiency due to the immense search space and is further in the original SQLi payload. In particular, both the left
complicated by semantic constraints. boundary and the right boundary are restricted to unchanged,
However,extantmethodsthatleveragereinforcementlearn- so that the functionality of the original SQLi is preserved.
ing (RL) and priority queues fall short in the context of real- The query is the core module of the original SQLi payload
world WAF-as-a-service applications. Therefore, it becomes and is needed to be further processed and manipulated for
crucialtodevelopamutationapproachthatnotonlypreserves generating adversarial SQLi payloads. What is more, instead
the semantics of SQLi payloads but also an optimization of simply treating the query in the original SQLi payload as
strategy that is tailored for black-box attacks within this a sequence of strings [25], [26], [27], we further represent
problem space. it with a hierarchical tree. Formally, for the hierarchical
tree representation, each parent (non-leaf) node is an SQL
IV. ADVSQLI:ADVERSARIALSQLIGENERATION statement that assembles all tokens from its ordered child
In order to address the aforementioned challenges in by- nodes from left to right, and each leaf node is the atomic
passingWAF-as-a-serviceforprofits,weproposeageneraland token (e.g., integer, the keyword of ‘or’, etc) in SQL.
extendableattackframeworkAdvSQLitogenerateadversarial On the basis of the hierarchical tree representation, we can
SQLi payloads. Figure 2 illustrates the framework overview performmorefine-grainedandcustomizedprocessingforeach
of AdvSQLi. In particular, AdvSQLi first represents the node according to its unique characteristics and constraints,
originalSQLipayloadwithahierarchicaltreetoperformfine- which could facilitate the generation of adversarial SQLi
grained and customized processing for each node. Further, payloads based on mutation as in the following subsection.

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 5
2 Mutation with
1 Hierarchical Tree Representation Context-free Grammar 3B: 5A:
A B C White Comment DML Comment
Qu o e r r 1 y = T r 1 ee 1 D o M r L CFG D O M R L DM || L C / o * m !o m r* e / nt… Space /*foo*/ = /*!=*/
1 2 3 2 T 1 a = u t 1 . CFG 2 T a < u > t . 3 B Tr o u o e l No B t o F o al l se …
1’ or 1 = 1 --+ D o M r L Tau 1 t = o lo 1 gy S W p h a i c te e 3 S W p h a i c te e CFG \n C / o * m fo m o e * n / t \t … After a few rounds 3B #0 3A 3C
SQLi payload blocked by WAF Int 4 e 1 ger D 5 M = L Inte 1 6 ger 5 4 In D te M = 1 g L er C C F F G G C In o /* m 0 t ! e x = m g 1 * e e / n r t se D D l l e i M M k c e L L t 1 S D ‘ l f t i o r K M i o n E L ’ g … … M N R C o o d o T e t S 5C5 # B 1 5A #2 C B h e i s l 1 d t C
SQL Hierarchical Tree 6 Inte 1 ger CFG St ‘ r 1 in ’ g I ‘ n n t a e m ge e r ’ In 0 te x g 1 er… ( I T . r S e e e l e P c o t l i i o c n y)
Search Space
|| 0x1 Q /* u != e * r / y 0 T x r 1 e / e *foo*/ 3B Finish the search 3B #0 3A 3C 3B #0 3A 3C 3B #0 3A 3C
5A #1 #1 #1
1 2 3 4A 5C5B 5A 1C 5C5B 5A 1C 5C5B 5A 1C
1’ || 0x1 /*!=*/ 0x1/*foo*/--+ DM || L 0x T 1 a u /* t ! o = l * o / g 0 y x1 Co /* m fo m o* e / nt 6C #2 #2 #2
4A 4A 4A:
SQLi payload which can bypass WAF Int 0 4 e x g 1 er Co / m 5 *!= m * e / nt In 0 te x 6 g 1 er 1B #3 4A #3 #3 Inte 1 ger In 0 te x g 1 er
IV. Backpropagation III. Simulation II. Expansion
(Default Policy) (Tree Policy)
All Selections Chain △
Final Hierarchical Tree Reach Max Step
Payload Reconstruction 3 Monte-Carlo Tree Search Guided Search
Fig.2. ThepipelineofAdvSQLi:ItfirstrepresentstheoriginalSQLipayloadwithahierarchicaltree,andthenemploysaweightedmutationstrategybased
onthecontext-freegrammartogenerateasetofequivalentSQLipayloads,whichkeepthesamefunctionalityandmaliciousnessastheoriginalone.Then,
itexploitsMCTStoefficientlyguidetheexplorationofadversarialSQLipayloadsinthevastspace.ItisnotedthatonlypartsoftheHierarchicalTreeare
shownforsimplicity.
B. Mutation with Context-free Grammar TABLEI
Examplesofmutationmethods.*meansthattheoperatorisflexiblefor
In order to generate both functionality-preserving and
differentrequestmethods.
maliciousness-preserving adversarial SQL injection, our pro-
posed AdvSQLi resorts to the problem space attack methods,
Mutation Example
i.e., manipulating the original SQL injection payload x with
Case Swapping or 1 = 1 → oR 1 = 1
a minimal cost of transformations, so that the generated
Whitespace Substitution* or 1 = 1 → \tor1\n=1
adversarial SQL injection payload x adv can bypass the target Comment Injection* or 1 = 1 → /*foo*/or 1 =/*bar*/1
SQLi detector (e.g., WAF-as-a-service). We first limit the Comment Rewriting /*foo*/or 1 = 1 → /*1.png*/or 1 = 1
transformation to addition and replacement on the original Integer Encoding or 1 = 1 → or 0x1 = 1
Operator Swapping or 1 = 1 → or 1 like 1
SQLipayloadsandthenproposeaweightedmutationstrategy
Logical Invariant or 1 = 1 → or 1 = 1 and ‘a’ = ‘a’
based on the context-free grammar (CFG) to generate a set of
Inline Comment union select → /*!union*/ /*!50000select*/
candidate adversarial SQLi payloads, which keeps the same where xxx → where xxx and True
Where Rewriting
functionality and maliciousness as the original SQLi payload. where xxx → where (select 0) or xxx
That is, for each node and subtree in the tree representation or 1 = 1 → || 1 = 1
DML Substitution*
and name = ‘foo’ → && name = ‘foo’
of the original SQLi payload, our weighted mutation strategy
‘1’ = ‘1’ → 2 <> 3
can generate a set of candidate actions that can be applied to
Tautology Substitution 1 = 1 → rand() ¿= 0
the original SQLi payload for generating a corresponding set 1 = 1 → (select ord(’r’) regexp 114) = 0x1
of candidate adversarial SQLi payloads.
In the weighted mutation strategy, we first present the
context-free grammar G which is formally defined as a 4-
tuple G = (S,V,Σ,R). In particular, S is the set of starting the tautology can be transformed into a boolean expression
symbols, which is associated with the nodes and subtrees of that turns out to be true S True (i.e., one of the non-terminal
thehierarchicaltree;V isafinitesetofnon-terminalsymbols, symbols) or terminal symbols, e.g., string τ, complex τ
which is used to expand the scope of generation, representing and numeric τ. For the non-terminal S True , we can either
intermediate states i.e., potential generation targets; Σ is a directly transform it into one of terminal symbols Σ true
finite set of terminal symbols disjoint from V, indicating the (e.g., “2<>3”,“True”, “Not False”), or another non-terminal
actual contents of generation. R is a set of predefined rules symbol in a recursive way, which could finally generate one
thatareusedtoiterativelytransformtheoriginalSQLipayload of candidate SQLi payload “true\n&&/**foo*/select 1\tand
into another equivalent form of SQLi payload that preserves 2<>3”.
the original functionality and maliciousness. WiththeabovetreerepresentationandtheCFG,inaddition
Taking the subtree of tautology (i.e., “1 = 1”) in the to covering the mutation operators in the baseline methods,
hierarchical tree representation as an example, we can use G we propose several novel and practical mutation operators
to generate a set of candidate equivalent forms. Alternatively, (e.g., Inline Comment, Where Rewriting, DML Substitution,

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 6
and Tautology Substitution in Table I). With the following N represents the visit times, and c is a parameter that can
two examples, we stress that our semantic-based method is trade off between exploitation and exploration [40].
more general (i.e., covering more surface of payloads) and The overall process of AdvSQLi is shown in Algorithm 1.
safe (i.e., semantic-preserving). 1) The existing methods can First, we represent the SQLi payload as a hierarchical tree t
only identify “1=1” in payloads for mutation, while with the (line 1), i.e., the first part of Figure 2. After that, we find all
benefitofsemantic-basedmatching,AdvSQLicanmutatefor operable nodes in t (line 2), in other words, nodes such as
“1=1”,“1=1”,“-3.7=-3.7”,“1=1.0”,“‘foo’=‘foo”’.2)The databasetablenamesaresettoalockedstate.WeuseCFGto
existing methods mutate “rlike” to “r=” and mutate “order” to generate equivalent nodes (or subtrees) for all operable nodes
“||der”,tonameafew,whichwillinvalidatetheentirepayload. (line 3), i.e., the second part of Figure 2. Then, we create the
root node of MCTS, which contains the computational budget
Algorithm 1: Main Procedure of AdvSQLi and our hierarchical tree (lines 5-6). Further, we call MCTS
Input : payload x, max steps s, computational budget, within the max steps s (lines 8-13), which is reflected in the
black-box situation p, WAF clsf. third part of Figure 2. According to the state after each round
Output: attack result, final score, final payload x′. ofthegame,wecanjudgewhetherwewin,i.e.,reconstructing
1 t←BuildTree(x) ; // Section IV-A the SQLi payload based on the chain of all MCTS selections
2 t∗ ←ExploreOperationalNodes(t);
3 M ←CFG(t∗) ; // Section IV-B (line 14). At last, we can obtain the bypassing payload.
4 s←Min(s,len(t∗)) ; // Max Steps.
5
6
s
n
t
o
a
d
t
e
e
←
←
M
M
C
C
T
T
S
S
N
S
o
t
d
a
e
t
(
e
s
(
t
t
a
,
t
M
e)
,
;
p) ; //
//
In
R
i
o
t
ot
St
N
a
o
t
d
e
e
.
.
V. EVALUATION
7 for i←1 to s do Next, we conduct an empirical evaluation of AdvSQLi.
8 for j ←1 to budget do We consider black-box settings with or without probability
9 expand node←TreePolicy(node) ;
situations, which respectively correspond to state-of-the-art
10 reward←DefaultPolicy(expand node) ;
11 Backup(expand node,reward); ML-based SQLi detectors and commercial WAF-as-a-service
12 node′ ←BestChild(node); products. Under both settings, we compare AdvSQLi with a
13
x′ ←ConstructPayload(node′);
set of state-of-the-art attacks. Note that due to their different
14
score←clsf(x′);
optimization strategies (e.g., MCTS, RL, priority queue), it
15 if score<threshold of clsf then
16 Return True,score,x′; is challenging to find a unified configuration. Instead, we
17
node←node′; adopt a two-stage approach that first assesses the validity of
18 Return False; payloadsandthenconductsotherevaluations.Specifically,the
evaluation is designed to answer the following key questions:
•RQ1:Semanticpreservation.IsAdvSQLiabletopreserve
the original semantics of payloads?
C. MCTS Guided Search
•RQ2:AttackeffectivenessagainstML-basedSQLidetec-
As our CFG-based mutation method can theoretically gen-
tion. Is AdvSQLi effective against state-of-the-art ML-based
erate infinite candidates, we employ the Monte-Carlo tree
SQLi detectors?
search (MCTS) to solve it, which has proven effective in
• RQ3: Attack effectiveness against WAF-as-a-service. Is
AlphaGo [39]. In AdvSQLi, MCTS is to continuously build
AdvSQLi effective against real-world WAF-as-a-service?
a search tree, where each node represents a state of the
• RQ4: Ablation study. What is the effectiveness of each
SQLihierarchicaltree,andtheedgescorrespondtomutations,
individual mutation method?
i.e., replacements of the node in the SQLi hierarchical tree.
Datasets. We evaluate the attack performance of AdvSQLi
Commonly, MCTS contains four steps: Selection is to find
on two commonly used datasets HPD and SIK, and our
the best node worth exploring in the search tree employing
own dataset MDD. More precisely, HPD [41] is shorted for
the Upper Confidence Bounds (UCB) algorithm (Equation 2),
the HttpParamsDataset which not only includes all malicious
i.e., the most worth exploring state of the SQL hierarchy
SQLi payloads from CSIC [42], but also plenty of SQLi
tree. Expansion is to perform an operation randomly and
payloads generated by sqlmap [43]. The two types of SQLi
create a new child node, which means choosing a node in the
payloads in HPD are widely used in SQLi detection [44],
hierarchical tree and replacing it with one of the equivalent
[45], [46]. SIK [47] is shorted for the SQL injection dataset
replacements generated by CFG. Simulation is to continue
in Kaggle, which is employed as the evaluation dataset in
the “game” until reaching the maximum number of mutation
one of our baseline attack methods. For each dataset, as the
steps. Then, we can get its score. Back-propagation is to
number of benign samples in each dataset is about twice
provide feedback on the score of the newly expanded node to
that of malicious samples, we randomly select 3,000 samples
all the previous parent nodes, and update the score and visit
(2,000 benign samples and 1,000 malicious samples) as the
times of these nodes to facilitate the calculation of the UCB
validation set and the testing set, respectively, and make
score later.
the remaining samples as the training set. However, due to
(cid:115)
score ucb = v′ ∈ a ch rg ild m r a en x of v ( N Q( ( v v ′ ′ ) ) + c 2l N n ( N v′ ( ) v) ) (2) t b h u e ild div c e o r r s r i e t s y po o n f di s n a g mp ru le n s tim in e t e h n e vi a r b o o n v m e en d t a s ta i s n ets a , s w ho e rt ca t n im no e t .
Besides, v′ and v represent the current node and its parent In response, to verify the functionality and maliciousness of
node respectively, Q represents the cumulative quality value, the generated payloads dynamically, we manually constructed

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 7
TABLEIII
Performanceoftargetmodels.δ meansthethresholdcalculatedbyFPR.
MDD AdvSQLi/ Back-end with multiple FPR=1% FPR=1‰
Baseline runtime environments Target AUC
Dataset
Model (%) Acc(%) δ Acc(%) δ
(a) ForRQ1:Employtheback-endsofvariousruntimeenvironmentstoverify
thefunctionalityandmaliciousnessofgeneratedpayloads. WAF-Brain HPD 99.14 85.80 0.333 62.18 0.500
WAF-Brain SIK 96.97 68.45 0.286 54.25 0.572
CNN HPD 99.96 99.45 0.044 99.90 0.159
CNN SIK 99.99 99.45 0.007 99.85 0.145
LSTM HPD 99.96 99.45 0.002 99.90 0.006
AdvSQLi/ LSTM SIK 99.99 99.50 0.025 99.90 0.105
HPD/SIK ML-based SQLi detectors
Baseline
(b) For RQ2: Use ML-based SQLi detectors to evaluate the effectiveness and
efficiency.Thedatasetsareusedinthetraining,validationandtestingphases. deploy them: AWS, F5, CSC, Fortinet: We create four
Access Control Lists (ACLs) on AWS. Further, we subscribe
to the rules of these vendors and integrate them into the
corresponding ACL. Cloudflare: We subscribe to its pro plan
toenablethefull-blownWAF.Wallarm:WedeployaWallarm
MDD/ AdvSQLi/ WAF-as-a-services Back-end with
HPD/SIK Baseline from 7 vendors SQLi Vulnerability. node on the Google Cloud Platform. ModSecurity: We build
ModSecurity based on Nginx and embed the latest version of
(c) For RQ3 and RQ4: Evaluate the effectiveness when attacking commercial
WAFs.Thedatasetsareonlyusedinthetestingphase. the OWASP CoreRuleSet (CRS) in it.
Attack Methods. Previous research has made some progress
Fig.3. Workflowofevaluation.
in generating adversarial SQLi payloads. 1) WAF-A-MoLE:
Demetrio et al. [25] defined 7 mutation methods based on
MDD, including prevalent SQLi payloads with union-based regular expression, and used a priority queue to guide their
injection, blind injection, error-based injection, and so on. mutation process (i.e., payloads with low scores are used as
theinitialpayloadsforthenextround).2)Wangetal.[26]and
TABLEII Hemmati et al. [27] followed the mutation operators in [25],
Summarystatisticsofdatasets.Thenumberbeforeorafter“/”denotesthe and they proposed a search strategy based on RL [54]. We
numberofbenign/maliciouspayloads.
use WAF-A-MoLE as one of the baseline methods. Since
neither [26] nor [27] has open-sourced attack modules, we
Datasets Training Validation Testing Total
implementtheirmethodbasedonDQNandcallitDRL.Inad-
HPD 15,304/8,852 2,000/1,000 2,000/1,000 30,156
dition, to evaluate the effectiveness of the MCTS method and
SIK 12,840/9,168 2,000/1,000 2,000/1,000 28,008
toexploretheupperlimitofattack,weimplementtwovariants
MDD - - -/100 100
of AdvSQLi: 1) AdvSQLi(R), which randomly combines
thecandidatenodesofthehierarchicaltree.2)AdvSQLi(A),
Target Models. The target WAFs are divided into two cate-
which performs permutations on the candidates of all nodes.
gories to cover black-box with and without probability situa-
tions:
1) SQLi Detection Models. We use the character-based TABLEIV
Attackmethods.“Both”meansitissuitableforbothblack-boxwithand
anomalydetectionmodelWAF-Brain[48]asoneofourtarget withoutprobabilitysituations,i.e.,ML-basedSQLidetectionandreal-world
models, which is a state-of-the-art AI-based WAF and is WAF-as-a-service.
widely used by previous work [25], [26]. However, given the
Method Capability MutateMethod SearchStrategy
unsatisfactory generalization of WAF-Brain on our datasets, WAF-A-MoLE BBw/prob. String-based PriorityQueue
we train two classification models (i.e., CNN [49], [50], [51] DRL BBw/prob. String-based RL(DQN)
AdvSQLi Both Semantic-based MCTS
andLSTM[52],[53])basedonstate-of-the-artSQLidetection
AdvSQLi(R) Both Semantic-based Random
and text classification literature. We use “=”, “|”, “,” and “ ” AdvSQLi(A) Both Semantic-based Violent
as keywords for vocabulary segmentation and train both CNN
andLSTMmodelsatthewordlevelonHPDandSIKdatasets Metrics and Parameters. The metrics of our attack evalu-
usingPyTorch.Theperformanceofthethreemodelsisshown ations are: (i) Attack Success Rate (ASR) represents the
in Table III. As subsequent evaluations show that the WAF- percentageofmalicioussamplesthatcanbypasstheWAFafter
BrainistooeasytobypassatFPRof1%and1‰,wemanually theattack.(ii)ValidityofGeneratedPayloads(VGP)reflects
designate a threshold of 0.1 following the settings of [26]. the feature of semantic-preserving of an attack method. (iii)
2) Real-world WAF-as-a-service Solutions. To verify the Query refers to the query number we perform on a payload
real-worldattackeffectivenessofAdvSQLi,wepurchaseand to bypass WAF. Here are some parameters that may affect
deploy7WAF-as-a-servicesolutionsfrommainstreamvendors the running results: In AdvSQLi and WAF-A-MoLE, the key
including Amazon Web Services (AWS), F5, Cyber Security parameters are Step and Budget. Recall from Algorithm 1
Cloud (CSC), Fortinet, Cloudflare, Wallarm, and the state- that the outer loop (lines 6-16) is constrained by Step, which
of-the-art open-sourced WAF ModSecurity. Specifically, we repetitively builds a search tree and updates the optimal node.
employ the following real-world settings to configure and Moreover,theinnerloop(lines7-10)isconstrainedbyBudget,

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 8
which iteratively builds and extends the search tree under
the current root node. As for WAF-A-MoLE, we treat the
size of each priority queue as the budget and the number of
priority queue rounds as a step. Therefore multiple queries
are performed in a step in WAF-A-MoLE and AdvSQLi.
Besides, the number of steps and queries are equal in DRL
and AdvSQLi(R).
A. RQ1: Semantic Preservation
Evaluation setup. We propose a dynamic method to perform
the semantic-preserving assessment, i.e., comparing the run-
ning results of the generated payloads and the original one.
Figure3(a)sketchestheworkflow.Specifically,wefirstcreate
two databases (MySQL 5.7 and MySQL 8.0) and build the
correspondingtables,columns,anddatabasedonMDD.Then, Fig. 4. VGP of AdvSQLi and relationship between VGP and ASR of
we integrate these databases in back-end scripts (PHP 5.6, WAF-A-MoLE. The horizontal blue line means that the VGP of AdvSQLi
isalways100%.Thedescendingorangelinereferstothechangingtrendof
PHP 7.4, and Python 3.7) with SQLi vulnerabilities. This
the VGP of WAF-A-MoLE with the number of attack steps, which is the
leaves us with 6 web services where we can steal information average value under various runtime environments. The rising lines refer to
through SQLi attacks. Furthermore, we mutate the samples in thechangingtrendoftheASRwiththenumberofattacksteps.
MDD utilizing AdvSQLi and WAF-A-MoLE, and then send
the mutated payloads to these web services to observe the
AdvSQLiandWAF-A-MoLEto10.Besides,wesetthequery
runningresults.SincethemutationmodulesofWAF-A-MoLE
numberofattemptsofAdvSQLi(R)to10,000forefficiency.
andDRLareidentical,weonlyevaluateWAF-A-MoLE.Inthis
context, we evaluate the relationship between VGP and attack
steps. Roughly, we generate about 10,000 mutated payloads
with WAF-A-MoLE and AdvSQLi, respectively. Moreover,
to determine the subsequent parameters for a fair comparison,
we evaluate the relationship between ASR and attack steps of
WAF-A-MoLE based on multiple models.
Results.FromFigure4,wecanseethatthepayloadsmutated
by AdvSQLi are always valid (VGP is 1.0), i.e., preserving
the original functionality and maliciousness. This is insep-
arable from our semantic-based mutation method. However,
the string-based mutation method in WAF-A-MoLE and DRL
(a) HPD-LSTM(FPR=1%) (b) SIK-CNN(FPR=1%)
mutates “rlike” to “r=” and mutate “order” to “||der”, to
name a few, which do damage the original semantics of the Fig.5. RelationshipsbetweenASRandQuery(within100)whenattacking
payloadsandinvalidatethem.Forexample,halfofthemutated againstSQLidetection.ThegreydottedlineresultsfromtheAdvSQLi(R)
underthedefaultsettings.
payloads generated by the string-based mutation method are
invalidwhenthenumberofattackstepsis4.Besides,Figure4
Results. 1) Effective. The middle part of Table V shows
shows that both the VGP and ASR curves of WAF-A-MoLE
the ASR results of attacking against SQLi detection under
tend to be flat when the attack step is larger than 10. For
default settings. Intuitively, SQLi detection based on anomaly
a fair comparison, we take the number of attack steps at 10
detection, CNN, and LSTM are all vulnerable to adversarial
as the default parameter of WAF-A-MoLE for the subsequent
attacks.Forexample,severalattackmethodscanachieveASRs
evaluations.
of100%onWAF-Brain.WefindthatAdvSQLiisbetterthan
Answer to RQ1: AdvSQLi is semantic-preserving, while other attack methods in terms of higher ASRs. For instance,
the baseline methods (i.e., WAF-A-MoLE and DRL) fail the ASR of AdvSQLi is twice that of WAF-A-MoLE, three
to preserve semantics. Namely, the adversarial payloads times that of AdvSQLi(R), and seven times that of DRL
generated by AdvSQLi maintain the original functionality whenattackingagainsttheLSTMmodel(FPR=1‰)underthe
and maliciousness. SIK dataset. 2) Efficient. Figure 5 sketches the relationships
betweenASRandQuery.ItisclearthatAdvSQLialwaysout-
performs other methods, regardless of the number of queries.
B. RQ2: Attack Effectiveness against ML-based SQLi Detec- In most cases, the ASRs of AdvSQLi surpass AdvSQLi(R)
tion
withindozensofqueries.Comparedwithotherbaselinemeth-
Evaluation setup. We evaluate the attack effectiveness and ods, the effectiveness of WAF-A-MoLE gradually surpasses
efficiencybyutilizingtheattackmethodsinTableIVtoattack others with the increase of queries. However, it still tends to
themodelsinTableIII.Wesetthemaximumnumberofsteps be stable in the end and cannot exceed AdvSQLi.
of each attack method to 10 and set the default budget of Parameters adjustment. We conduct detailed evaluations

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 9
TABLEV
TheASRresultsofattackingagainstSQLidetectionwhenunderdefaultsettingsandwhenincreasingthenumberofattackstepsto20.WAMmeans
WAF-A-MoLE.δ meansthethresholdcalculatedbyFPR.
Attack Success Rate (%)
Dataset Target SQLi δ FNR Parameter: Step = 10 (Default) Parameter: Step = 20
Detection (%)
WAM DRL AdvSQLi(R)AdvSQLiAdvSQLi(A) WAM DRL AdvSQLi(R)AdvSQLiAdvSQLi(A)
WAF-Brainδ=0.10.100 0.1 75.56 4.15 97.34 99.97 98.01 99.86 8.62 97.47 99.93 98.04
WAF-Brain1% 0.33331.3 100 69.62 100 100 99.59 100 86.15 100 100 100
WAF-Brain1‰ 0.50076.7 100 81.95 100 100 100 100 90.40 100 100 100
HPD CNN1% 0.044 0.1 9.34 6.97 7.94 26.46 25 11.48 7.54 9.58 27.03 26.12
CNN1‰ 0.159 0.1 13.68 9.44 13.28 34.90 32.9 16.8810.54 14.78 36.27 34.93
LSTM1% 0.002 0.1 10.18 3.90 9.34 23.62 16.8 14.41 4.40 11.34 23.99 20.32
LSTM1‰ 0.006 0.1 11.41 5.04 11.08 26.03 18.2 15.85 5.47 13.08 26.43 22.72
WAF-Brainδ=0.10.100 0.5 77.1213.89 98.06 100 99.16 99.9324.40 99.48 100 100
WAF-Brain1% 0.28662.599.9365.31 99.93 100 99.64 100 82.15 100 100 100
WAF-Brain1‰ 0.57291.5 100 98.85 100 100 100 100 100 100 100 100
SIK CNN1% 0.007 0.1 25.1611.01 12.48 35.97 27 29 12.98 15.55 39.74 32.23
CNN1‰ 0.145 0.2 44.1225.05 27.42 56.78 45 49.3027.25 35.64 58.48 52.40
LSTM1% 0.025 0.0 36.50 9.87 20.57 78.80 61.40 49.5310.77 31.03 83.10 74.20
LSTM1‰ 0.105 0.1 42.6112.45 27.53 91.36 74.90 56.5213.58 39.87 95.03 84.68
to further explore the impact of the parameters mentioned TABLEVI
above on the effectiveness and efficiency of different attack TheASRresultsunderbudgetis10and20.WAMmeansWAF-A-MoLE
methods. We first increase the maximum number of steps of
AdvSQLiandWAF-A-MoLEto20andrepeatallevaluations. Attack Success Rate (%)
Target SQLi
In order to explore the impact of the computational budget on Dataset Budget=10 Budget=20
Detection
the attack results, we increase the budget of AdvSQLi and WAM AdvSQLi WAM AdvSQLi
WAF-A-MoLE to 20.
WBδ=0.1 75.56 99.97 99.56 100
Results. 1) Step. The results of ASR are shown in the
WB1% 100 100 100 100
right part of Table V. Evidently, the ASRs of various attack
WB1‰ 100 100 100 100
methods increase more or less. However, AdvSQLi still has HPD CNN1% 9.34 26.46 10.54 27.83
an absolute advantage over the baseline methods. 2) Budget. CNN1‰ 13.68 34.90 14.71 36.87
From Table VI, we can observe that the ASRs improve as the LSTM1% 10.18 23.62 11.58 24.59
budget increases for almost all models. Moreover, when the LSTM1‰ 11.41 26.03 12.21 27.09
budget is 20, WAF-A-MoLE is still not better than AdvSQLi
WBδ=0.1 77.12 100 99.59 100
with budget 10, which proves the advantage of AdvSQLi.
WB1% 99.93 100 100 100
Answer to RQ2: AdvSQLiismoreeffectiveandefficient WB1‰ 100 100 100 100
than all baseline methods, achieving higher ASRs with SIK CNN1% 25.16 35.97 26.49 38.64
CNN1‰ 44.12 56.78 46.62 58.22
fewer queries.
LSTM1% 36.50 78.8 41.23 82
LSTM1‰ 42.61 91.36 48.21 94.49
C. RQ3: Attack Effectiveness against WAF-as-a-service
Evaluation setup. We deploy a modified version of SQLi-
labs [55] with the underlying database on the Google Cloud when sending the payload via GET. As for the baseline
Platform. Further, we protect it by utilizing seven real-world methods, the mutation methods of WAF-A-MoLE and DRL
WAFs in turn by modifying DNS resolutions and forwarding are identical, and do not support attacking black-box WAFs
traffic. In this case, AdvSQLi acts as a client to continuously given their score-based attack guidance. Therefore, we im-
send attack requests to the protected web service. plement a random search-based variant for WAF-A-MoLE
Real-worldadaptation.Notethat,ourmodifiedback-endweb and perform the same adaptations in mutation methods. We
servicesupports4commonHTTPrequestmethods(i.e.,GET, employ WAF-A-MoLE to attack the web service protected by
GET(JSON),POST,andPOST(JSON))correspondingtocom- ModSecurity and elide the results of other WAF-as-a-service
prehensive real-world situations. We fine-tune the mutation for experimental efficiency.
process in AdvSQLi adaptively to preserve the semantics Results. Table VII illustrates the FNR and ASR results of
of the generated payloads across different request methods, attacking against 7 WAF-as-a-service, and Table VIII shows
e.g., \n needs to be encoded as %0A for non-JSON requests the ASR and Query results of AdvSQLi and WAF-A-MoLE
and the “#” sign cannot be present in comments (/*#*/) against ModSecurity.

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 10
TABLEVII than 60% of malicious requests will be directly forwarded to
Resultsofattackingagainstreal-worldWAFs.A(R)meansAdvSQLi(R). the back-end service. On the contrary, Fortinet and Wallarm
performwellastheirFNRsarelowandrelativelyevenamong
HPD SIK
different request methods.
Request
WAFaaS FNR ASR(%) FNR ASR(%) 2) ASR illustrates the robustness of a WAF against adver-
Method
(%) (%)
A(R)AdvSQLi A(R)AdvSQLi sarialattacks.IfaWAFexhibitshighFNRsandASRssimulta-
neously,itisevidentthatitsprotectiveeffectisunsatisfactory.
GET 5.3 15.21 18.69 8.2 10.80 14.39
GET(JSON) 60.2 86.43 89.45 63.4 96.45 99.73 Overall, our attacks against WAF-as-a-service are successful.
AWS
POST 3.4 29.19 30.02 14.5 26.46 31.97 The ASRs against AWS on the SIK dataset even reached
POST(JSON)60.2 84.17 89.45 63.4 96.17 99.73 99.73%. Besides, the ASRs of each WAF have a similar
GET 40.7 70.66 82.46 45.1 69.95 79.60 distribution to FNRs, which further confirms our conclusion
GET(JSON) 40.5 67.73 83.87 43.7 61.99 82.06 that we have drawn above on the effectiveness of WAFs. By
F5
POST 35.6 70.50 83.7 41.9 66.09 80.72 analyzing the ASRs, we can find that when requesting web
POST(JSON)35.4 71.05 85.76 40.5 60.50 82.69
services in JSON-type parameters, ASRs are much higher
GET 19.7 63.14 77.33 37.1 50.08 70.27 than non-JSON. It is a great security risk given the current
Cyber
Security GET(JSON) 20 65.75 77.38 37.1 53.26 70.91 development trend of web services, i.e., more and more web
POST 19.7 63.26 75.22 37.1 46.97 70.38
Cloud services are designed based on the decoupled architecture,
POST(JSON) 20 64.50 74.50 37.1 52.46 71.38
most of which use JSON to transfer data.
GET 8.8 48.25 53.40 14.2 45.16 55.19
GET(JSON) 9.7 78.07 83.17 15.7 73.40 81.24
Fortinet POST 8.8 48.9 53.40 14.0 45.75 55.06 TABLEVIII
TheASRandQueryresultsofAdvSQLiandWAF-A-MoLEagainst
POST(JSON) 9.7 77.52 83.17 15.5 73.58 81.28
ModSecurity.Theaveragequeryiscalculatedbasedonsuccessfulsamples
GET 8.1 20.13 21.33 18.8 26.39 32.43 crossedinbothattackmethods.WAMmeansWAF-A-MoLE.
Cloud- GET(JSON) 17.7 35.60 37.79 29.2 55.73 58.13
flare POST 47.1 35.35 35.92 63.2 47.96 48.77 ASR(%) Average Query
Dataset Request Method
POST(JSON)47.1 35.16 35.92 63.2 47.96 49.05
AdvSQLi WAM AdvSQLi WAM
GET 1.4 16.94 18.76 6.5 24.20 33.94
GET 11.61 6.61 9.80 30.11
GET(JSON) 1.4 16.94 18.76 6.4 24.17 34.01
Wallarm GET(JSON) 49.06 47.02 10.15 18.91
POST 1.4 15.14 17.28 6.7 20.52 31.26 HPD
POST 10.61 5.61 10.66 29.66
POST(JSON) 2.4 16.79 17.40 7.6 23.86 32.24
POST(JSON) 10.61 5.31 9.93 30.31
GET 0.1 5.74 11.61 3.3 5.63 10.88
GET 10.88 7.34 10.67 31.5
Mod- GET(JSON) 20.1 42.59 49.06 30.9 49.73 58.32
GET(JSON) 58.32 48.05 10.26 32.65
Security POST 0.1 5.44 10.61 3.5 4.53 9.55 SIK
POST 9.55 7.36 10.37 30.44
POST(JSON) 0.1 4.90 10.61 3.5 4.50 9.55
POST(JSON) 9.55 5.80 10.65 30.32
The four WAFs hosted on AWS (AWS, F5, CSC, and
1) FNR directly reflects the protection effectiveness of
Fortinet)arelesscapableofpreventingSQLithanotherWAFs.
WAFs. In general, the protective effects of each WAF are
Wallarm is effective because it has low FNRs and ASRs.
uneven. Classified according to different request methods, in
Besides, Fortinet has ASRs many times higher than FNRs,
themajorityofcases,theFNRsofthetwoGET-basedrequest
which means that it cannot defend against adversarial attacks
methods are greater than or equal to those for POST-based
very well. Interestingly, ModSecurity shows the strongest
methods, which means that the protection of the latter is
robustness if we ignore the shortcomings in the defense of
stricter. If this is not a design flaw, it is likely that the vendor
GET(JSON) requests, which means that open-sourced tools
deliberately did it. When making requests to web services
may have natural advantages. Comparing the two attack
via POST, there is typically a larger attack payload, leading
methods we proposed, overall, AdvSQLi has much higher
vendorstoimplementstricterprotectivemeasures.Incontrast,
ASRs than AdvSQLi(R) against all WAF-as-a-service. We
GET requests, which generally do not carry such complex
can see from Table VII that in hard-to-attack situations (such
content, may be subject to more lenient scrutiny to prevent
as ModSecurity), the ASRs of AdvSQLi are twice that of
the accidental interception of legitimate traffic. Further, we
AdvSQLi(R). From Table VIII, we can see that AdvSQLi
can divide WAFs into four categories by inferring WAF’s
is more effective and efficient than WAF-A-MoLE, as it
responses to different requests based on FNRs: 1) F5, CSC,
achieves nearly twice the ASRs with only one-third queries
Fortinet, and Wallarm treat the four request methods equally.
of WAF-A-MoLE in several cases.
2)Cloudflareimplementsdifferentstrategiesbasedonwhether
the request method is GET or POST. 3) AWS treats the
payload separately based on whether the request parameter Answer to RQ3: All WAF-as-a-service under tests are vul-
is in JSON type. 4) ModSecurity processes requests via nerable to AdvSQLi. More importantly, some vendors have
GET(JSON) separately, yet treats the remaining three request severe deficiencies, e.g., the insufficiency in parsing JSON-
methods equally. Alarmingly, both AWS and Cloudflare have typeparameters.AdvSQLiismoreeffectivethanthebaseline
FNRs of over 60% on the SIK dataset. In other words, more methodswhenattackingagainstreal-worldWAF-as-a-service.

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 11
D. RQ4: Ablation Study
Overall conclusion. In addition to analyzing the ASR results,
it is meaningful to know the root causes of bypassing, i.e.,
the concrete vulnerabilities of WAFs. We automatically an-
alyze all bypass samples in RQ3 based on the hierarchical
trees to conclude more comprehensively. Supplemented by
manual methods, we get the conclusions in Figure 6 within
the format of Table I. Intuitively, individual attack methods
are not always effective in attacking all WAF-as-a-service.
Fig.7. ExamplesthatcanbypassWAF-as-a-service.
The mutation methods we propose (i.e., Inline Comment and
DML Substitution) and Whitespace Substitution are the most
effective methods. Interesting, just adding some comments VI. DISCUSSION
into the SQLi payloads can bypass F5, Fortinet, Wallarm, and
A. Responsible Disclosure
ModSecurity in some cases. We speculate that the detection
signatures in these WAFs are not robust, causing these by- We reported the above results to the affected vendors by
passes. submitting vulnerability reports and contacting their technical
supportstaffandsecurityresearchersviaemails.Upuntilnow,
three vendors have mitigated the flaws, and four vendors are
working:
F5: The F5 Security Incident Response Team responded to
our email quickly and said that they would “reach out to the
respective team”. Three weeks after our report, we were told
that they had updated the rules for AWS WAF and the issue
was addressed.
Cloudflare: We submitted our findings to Cloudflare
through its supporting system and the HackerOne platform.
After productive communications, we were informed that the
WAF team had “deployed some changes”, yet they would not
tell us the details.
Wallarm:Theyattachedgreatimportancetoourreportand
Fig.6. EffectivemutationmethodsinbypassingWAF-as-a-service.Fullcircle
meansthatthisactioniseffectiveinmostcases;Halfcircleindicatesthatit declared that they “are doing everything to resolve it as soon
mayworkunderspecificpayloadsorcombinedwithothermutations. as possible”. A month after our report, we learned from the
updatefromtheWallarmdetectionteamthattheissuehasbeen
Case studies.Hereafter,wefurtheranalyzethevulnerabilities resolvedandtherulesetforSQLidetectionisnow“widerand
throughspecificexamples.Weselectthreerepresentativepay- more accurate”.
loadsfromMDD,whichcanstealtablenames,columnnames, AWS: The AWS Security Team replied to our email and
and sensitive information. There is no doubt that the WAFs proceeded to investigate it immediately. After a thorough
(AWS, F5, and Cloudflare) will block them if we directly investigation, they said they “will make a change to mitigate
send them to the web service. At this time, we input the the behavior” and will inform us “once they’ve released the
above payloads into AdvSQLi and none of the three WAFs related improvements”.
intercepted our carefully constructed payloads. By analyzing FortinetandCyberSecurityCloud:Aftergettingintouch
thebypassingpayloads,wecanfindthatreplacingwhitespaces with these vendors through their support email, we learned
with control characters (i.e., Whitespace Substitution) can thattheyhadconfirmedtheflawsandproceededtosolvethem.
bypass AWS. Furthermore, if we replace Data Manipulation Theirwordsare“plantoaddresssomeofthese”and“improve
Language(DML)tokenswithinlinecomments,wecanbypass the rules in later update”, yet we have not received any new
F5 and Cloudflare. updates.
ModSecurity: We reached the rules team (OWASP CRS)
Insummary,thesecasestudiesfurtherverifyourconjecture:
and engine team (Trustwave ModSecurity Security Team)
vendors’ detection signatures are non-robust, causing severe
respectively.OneCRSco-leaderconfirmedthatCRSdidhave
vulnerabilities.
flaws and ModSecurity is insufficient in parsing query strings
inJSONformat,yettheycandolittlebeyonddiggingthrough
Answer to RQ4: Effective mutation methods for specific JSON with their rules. Their developers are still working
WAFsanddifferentpayloadsareunique.Combiningmultiple with us based on our detailed conclusions. While the security
mutation methods, AdvSQLi is much more effective in researcher from ModSecurity said that the lack of JSON
bypassingmainstreamWAF-as-a-servicesolutionsduetotheir parsing is not due to some bug or malfunction. ModSecurity
vulnerable detection signatures for semantic matching and would not parse JSON objects in query arguments or request
regular expression matching. headers by design. Yet he admitted that “the absence could

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 12
sometimes make writing effective rules more cumbersome”, D. Limitations and Future Work
andtheyplantoimplementthefeatureinModSecurityv3.1.1. Therearesomenaturallyinherentlimitationstothiskindof
work. Even though these do not affect the overall conclusion,
we discuss them in the following for completeness.
B. Potential Defenses
1) Dataset: We try our best to find open-sourced datasets,
We conduct a preliminary exploration of two potential asthereisnobenchmarkdatasetforSQLi.Onemayarguethat
defense methods, i.e., adversarial training (AT) and pre- the baseline method [25] presented a dataset [58] containing
processing (PP). bothbenignandmaliciousSQLsamples.However,inourtask,
Adversarial training. We can improve the robustness of benign samples should be ordinary HTTP request parameters,
ML-based WAF through AT [56]. Firstly, we attack the and malicious samples should be constructed HTTP request
CNN1% modelwith8852SQLipayloadsinthetrainingsetof parameters containing SQL statements. Therefore, we have to
HPD to obtain adversarial examples, using the AdvSQLi(R) exclude the dataset in [25] and only find two commonly used
attack method here for time considerations. Next, we add datasetsofSIKandHPDprobablyduetothepotentialsecurity
the 1341 x to the training set and retrain the CNN1% risks or intellectual property.
adv
model according to the previous settings. Then, we re-attack 2) Verification of semantic-preserving: To the best of our
the new model with SQLi payloads from the test set. From knowledge, there is no practical way to check whether two
Table IX, we can see that the performance of the CNN model SQLi payloads are semantic-equivalent other than comparing
droppedslightlyafterAT,e.g.,theASRofAdvSQLi(R)has the running results [59]. Therefore preliminary evaluations
dropped by 32.9%, and the ASR of AdvSQLi has dropped (RQ1) without the protection of WAF-as-a-service are per-
by 30.59%. AT might be effective in defending AdvSQLi. formed. Although the results show that our atomic-level mu-
However, the limitation is that it needs to have sufficient tation methods are semantic-preserving, we cannot guarantee
adversarial samples for training or know the details of the strict semantic equivalence in all possible cases due to the
attack strategy [37]. Therefore, AT is limited in defending assorted types of SQLi payloads.
against unknown adversarial attacks because attackers usually 3) Manual definition of CFG: The manual definitions of
do not disclose their methods. CFGaretoensurethatAdvSQLiwillnotinvalidatetheSQLi
Pre-processing. Just like dead code removal in programs, payloadsorcauseunexpecteddamage.Itmayhavelimitations,
we use some pre-processing methods to remove the “noise” suchasmakingthegeneratedpayloadslimitedbypriorknowl-
in SQLi payloads: unify the capitalization of letters, remove edge.Yetwehavemitigatedthisby,e.g.,recursivelydefinition
comments,removecontrolsymbols,andsoon.FromTableIX, of CFG to enrich the diversity of the generated payloads.
we can see that the ASRs dropped by less than 10% on both Besides, as we have provided the corresponding interfaces,
attack modes. Therefore, AdvSQLi is robust to common pre- subsequent researchers who want to extend AdvSQLi only
processing methods. need to add simple entries in CFG.
Next, we will continue tracking vendors’ feedback until
they fix the flaws completely. We shall implement the method
TABLEIX
of automatically analyzing and summarising the payloads
THEASRRESULTSAFTERDEFENSES.ATMEANSADVERSARIAL
TRAININGANDPPMEANSPRE-PROCESSING. based on the hierarchical tree to discover more generalized
bypass patterns, which we could embed into other tools (e.g.,
Defense AUC Accuracy ASR(%) sqlmap) or provide to vendors. In addition, we plan to extend
Mode (%) (%) AdvSQLi(R) AdvSQLi
our framework to other domains, such as cross-site scripting
- 99.959 99.90 7.94 26.46
attacks,webshell,etc.Besides,wewillexploretheintegration
AT 99.854 96.10 5.32 18.36
PP 99.959 99.90 6.32 25.18 ofmulti-factorauthenticationschemesintoWAFsystems,such
as three-factor authentication based on extended chaotic maps
and quantum-resistant two-factor authentication [60], [61],
[62],toaugmentthedefensivestrengthandrobustnessofweb
systems reliant on WAFs.
C. Rethinking WAF-as-a-service
Most real-world mainstream vendors employ the signature- VII. CONCLUSION
based detection strategy combining semantic analysis and We conduct the first systematic and comprehensive study
regular expression matching, which we have proven seriously on the security vulnerabilities of WAFs in the cloud, by
vulnerable. For ML-based WAF, the direct detection ability in proposing and implementing AdvSQLi. With this general
the laboratory environment is passable, however, the effect and extendable attack framework that works out of the box,
of defending against adversarial attacks is not gratifying. attackers can bypass WAF-as-a-service solutions of different
Intriguingly, there are vendors, such as Wallarm [57], already vendors for unique payloads effortlessly. Extensive evaluation
using ML technology to supplement the detection signatures results demonstrate that AdvSQLi can effectively and effi-
adaptively and achieve feasible defense effects with low FNR ciently bypass both state-of-the-art ML-based SQLi detectors
and ASR. This inspires us: can vendors build more promising and commercial WAF-as-a-service solutions from mainstream
WAFs by better utilizing AI methods or even implementing a vendors. Moreover, we condense out several fundamental de-
WAF with multi-modal detection mechanisms? ficiencies of real-world WAF-as-a-service, e.g., the vulnerable

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 13
detectionmechanisms,thenon-robustsignatures,andtheflaws [23] D.Appelt,C.D.Nguyen,A.Panichella,andL.C.Briand,“Amachine-
in parsing JSON-type parameters, which have successfully learning-driven evolutionary approach for testing web application fire-
walls,” IEEE Transactions on Reliability, vol. 67, no. 3, pp. 733–757,
helped mainstream vendors improve their products.
2018.
[24] M.Amouei,M.Rezvani,andM.Fateh,“Rat:Reinforcement-learning-
REFERENCES drivenandadaptivetestingforvulnerabilitydiscoveryinwebapplication
firewalls,” IEEE Transactions on Dependable and Secure Computing,
[1] Cloudflare, Inc., “What is web application security?” https://www. 2021.
cloudflare.com/learning/security/what-is-web-application-security, [25] L.Demetrio,A.Valenza,G.Costa,andG.Lagorio,“Waf-a-mole:evad-
2022. ingwebapplicationfirewallsthroughadversarialmachinelearning,”in
[2] A. Pramod, A. Ghosh, A. Mohan, M. Shrivastava, and R. Shettar, Proceedingsofthe35thAnnualACMSymposiumonAppliedComputing,
“Sqli detection system for a safer web application,” in 2015 IEEE 2020,pp.1745–1752.
International Advance Computing Conference (IACC). IEEE, 2015, [26] X. Wang and H. Han, “Evading web application firewalls with
pp.237–240. reinforcement learning,” CUHK 2021 Course IERG5350, 2020.
[3] L. Zhang, D. Zhang, C. Wang, J. Zhao, and Z. Zhang, “Art4sqli: [Online].Available:https://openreview.net/forum?id=m5AntlhJ7Z5
Theartofsqlinjectionvulnerabilitydiscovery,”IEEETransactionson [27] M. Hemmati and M. A. Hadavi, “Using deep reinforcement learning
Reliability,vol.68,no.4,pp.1470–1489,2019. to evade web application firewalls,” in 2021 18th International ISC
[4] W. Tian, J. Xu, K.-M. Lian, Y. Zhang, and J.-f. Yang, “Research on ConferenceonInformationSecurityandCryptology(ISCISC). IEEE,
mockattacktestingforsqlinjectionvulnerabilityinmulti-defenselevel 2021,pp.35–41.
webapplications,”inThe2ndInternationalConferenceonInformation [28] N. Chomsky, “Three models for the description of language,” IRE
ScienceandEngineering. IEEE,2010,pp.1–5. Transactionsoninformationtheory,vol.2,no.3,pp.113–124,1956.
[5] S.Prandl,M.Lazarescu,andD.-S.Pham,“Astudyofwebapplication [29] S.Das,T.Yurek,Z.Xiang,A.Miller,L.Kokoris-Kogias,andL.Ren,
firewallsolutions,”inInternationalConferenceonInformationSystems “Practical asynchronous distributed key generation,” in 2022 IEEE
Security. Springer,2015,pp.501–510. SymposiumonSecurityandPrivacy(SP). IEEE,2022,pp.2518–2534.
[6] A. M. Vartouni, M. Teshnehlab, and S. S. Kashi, “Leveraging deep [30] D. Wang, Z. Zhang, P. Wang, J. Yan, and X. Huang, “Targeted on-
neural networks for anomaly-based web application firewall,” IET In- line password guessing: An underestimated threat,” in Proceedings of
formationSecurity,vol.13,no.4,pp.352–361,2019. the 2016 ACM SIGSAC conference on computer and communications
[7] D. Appelt, C. D. Nguyen, and L. Briand, “Behind an application security,2016,pp.1242–1254.
firewall, are we safe from sql injection attacks?” in 2015 IEEE 8th
[31] H.S.Anderson,A.Kharkar,B.Filar,D.Evans,andP.Roth,“Learning
internationalconferenceonsoftwaretesting,verificationandvalidation
toevadestaticpemachinelearningmalwaremodelsviareinforcement
(ICST). IEEE,2015,pp.1–10. learning,”arXivpreprintarXiv:1801.08917,2018.
[8] S. Rushil and C. Thomas, “How cloudflare security
[32] C.Wu,J.Shi,Y.Yang,andW.Li,“Enhancingmachinelearningbased
responded to log4j 2 vulnerability,” https://blog.cloudflare.com/
malware detection model by reinforcement learning,” in Proceedings
how-cloudflare-security-responded-to-log4j2-vulnerability/,2021.
of the 8th International Conference on Communication and Network
[9] S.Applebaum,T.Gaber,andA.Ahmed,“Signature-basedandmachine-
Security,2018,pp.74–78.
learning-based web application firewalls: A short survey,” Procedia
[33] Z. Fang, J. Wang, B. Li, S. Wu, Y. Zhou, and H. Huang, “Evading
ComputerScience,vol.189,pp.359–367,2021.
anti-malwareengineswithdeepreinforcementlearning,”IEEEAccess,
[10] I.Ristic,Modsecurityhandbook. FeistyDuck,2010.
vol.7,pp.48867–48879,2019.
[11] G.Buehrer,B.W.Weide,andP.A.Sivilotti,“Usingparsetreevalidation
[34] X.Ling,S.Ji,J.Zou,J.Wang,C.Wu,B.Li,andT.Wang,“DEEPSEC:
topreventsqlinjectionattacks,”inProceedingsofthe5thinternational
A uniform platform for security analysis of deep learning model,” in
workshoponSoftwareengineeringandmiddleware,2005,pp.106–113.
IEEESymposiumonSecurityandPrivacy(S&P). SanFrancisco,USA:
[12] R. Ezumalai and G. Aghila, “Combinatorial approach for preventing
IEEE,2019,pp.673–690.
sql injection attacks,” in 2009 IEEE International Advance Computing
[35] I.J.Goodfellow,J.Shlens,andC.Szegedy,“Explainingandharnessing
Conference. IEEE,2009,pp.1212–1217.
adversarialexamples,”arXivpreprintarXiv:1412.6572,2014.
[13] T. Liu, Y. Qi, L. Shi, and J. Yan, “Locate-then-detect: Real-time web
[36] M. Schwarzl, P. Borrello, G. Saileshwar, H. Mu¨ller, M. Schwarz, and
attack detection via attention-based deep neural networks.” in IJCAI,
D. Gruss, “Practical timing side-channel attacks on memory compres-
2019,pp.4725–4731.
sion,”in2023IEEESymposiumonSecurityandPrivacy(SP). IEEE,
[14] I.Corona,D.Ariu,andG.Giacinto,“Hmm-web:Aframeworkforthe
2023,pp.1186–1203.
detection of attacks against web applications,” in 2009 IEEE Interna-
[37] J. Li, S. Ji, T. Du, B. Li, and T. Wang, “Textbugger: Generat-
tionalConferenceonCommunications. IEEE,2009,pp.1–6.
ing adversarial text against real-world applications,” arXiv preprint
[15] D. Kar, S. Panigrahi, and S. Sundararajan, “Sqligot: Detecting sql
arXiv:1812.05271,2018.
injectionattacksusinggraphoftokensandsvm,”Computers&Security,
[38] G.Rawlinson,“Thesignificanceofletterpositioninwordrecognition,”
vol.60,pp.206–225,2016.
IEEE Aerospace and Electronic Systems Magazine, vol. 22, no. 1, pp.
[16] M.D.JuniorandN.F.Ebecken,“Anewwafarchitecturewithmachine
learningforresource-efficientuse,”Computers&Security,vol.106,p. 26–27,2007.
102290,2021. [39] D. Silver, A. Huang, C. J. Maddison, A. Guez, L. Sifre, G. Van
[17] O. Charlie, “Akamai waf bypassed via spring Den Driessche, J. Schrittwieser, I. Antonoglou, V. Panneershelvam,
boot to trigger rce,” https://blog.cloudflare.com/ M.Lanctotetal.,“Masteringthegameofgowithdeepneuralnetworks
how-cloudflare-security-responded-to-log4j2-vulnerability/,2022. andtreesearch,”nature,vol.529,no.7587,pp.484–489,2016.
[18] F. Tameesh, “Red team case study: Bypass- [40] L. Kocsis and C. Szepesva´ri, “Bandit based monte-carlo planning,” in
ing cloudflare waf for successful ognl injection,” European conference on machine learning. Springer, 2006, pp. 282–
https://www.aon.com/cyber-solutions/aon cyber labs/ 293.
red-team-case-study-bypassing-cloudflare-waf-for-successful-ognl-injection[4/,1] Morzeux, “Http params dataset,” https://github.com/Morzeux/
2020. HttpParamsDataset,2020.
[19] F. Pierazzi, F. Pendlebury, J. Cortellazzi, and L. Cavallaro, “Intriguing [42] C. T. Gime´nez, A. P. Villegas, and G. A´. Maran˜o´n, “Http data set
propertiesofadversarialmlattacksintheproblemspace,”in2020IEEE csic 2010,” Information Security Institute of CSIC (Spanish Research
SymposiumonSecurityandPrivacy(SP). IEEE,2020,pp.1332–1349. NationalCouncil),2010.
[20] B. Biggio and F. Roli, “Wild patterns: Ten years after the rise of [43] sqlmapproject, “sqlmap,” https://github.com/sqlmapproject/sqlmap,
adversarial machine learning,” Pattern Recognition, vol. 84, pp. 317– 2022.
331,2018. [44] M. Ring, S. Wunderlich, D. Scheuring, D. Landes, and A. Hotho, “A
[21] M. Felderer, M. Bu¨chler, M. Johns, A. D. Brucker, R. Breu, and survey of network-based intrusion detection data sets,” Computers &
A.Pretschner,“Securitytesting:Asurvey,”inAdvancesinComputers. Security,vol.86,pp.147–167,2019.
Elsevier,2016,vol.101,pp.1–51. [45] G. D. L. T. Parra, P. Rad, K.-K. R. Choo, and N. Beebe, “Detecting
[22] O. Tripp, O. Weisman, and L. Guy, “Finding your way in the testing internet of things attacks using distributed deep learning,” Journal of
jungle:alearningapproachtowebsecuritytesting,”inProceedingsof NetworkandComputerApplications,vol.163,p.102662,2020.
the 2013 International Symposium on Software Testing and Analysis, [46] C.Luo,Z.Tan,G.Min,J.Gan,W.Shi,andZ.Tian,“Anovelwebattack
2013,pp.347–357. detectionsystemforinternetofthingsviaensembleclassification,”IEEE

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 14
Transactions on Industrial Informatics, vol. 17, no. 8, pp. 5810–5818, Here we describe the workflow of context-free grammar
2020. in AdvSQLi with an detailed example: Suppose we have a
[47] S. S. H. Shah, “sql injection dataset,” https://www.kaggle.com/
node of “1 = 1” in the hierarchical SQLi representation tree.
syedsaqlainhussain/sql-injection-dataset,2021.
[48] B.-L.S.team,“Waf-brain-thecleverandefficientfirewallfortheweb,” According to its semantic of tautology, we can mutate it to
https://github.com/BBVA/waf-brain,2019. terminal symbols of string-type tautology(τ , like “‘foo’
string
[49] Y.ZhangandB.Wallace,“Asensitivityanalysisof(andpractitioners’ like ‘foo”’ in Table X), complex tautology (τ , such as
guide to) convolutional neural networks for sentence classification,” complex
arXivpreprintarXiv:1510.03820,2015. “(select ord(’r’) regexp 114) = 0x1”), number-type tautology
[50] T. Mikolov, E. Grave, P. Bojanowski, C. Puhrsch, and A. Joulin, “Ad- (τ , such as “0x2 = 2”) or feed it into an entry of “true”
number
vancesinpre-trainingdistributedwordrepresentations,”arXivpreprint boolean expression (S ) for further processing, as shown
arXiv:1712.09405,2017. True
in the first line of Figure 8. Here the algorithm chooses the
[51] A.Rakhlin,“Convolutionalneuralnetworksforsentenceclassification,”
GitHub,2016. latter one, i.e., line 1→line 2 in Figure 9. Deep into rule 9 of
[52] K.Zhang,“Amachinelearningbasedapproachtoidentifysqlinjection Figure 8, S can be mutated to terminal symbols of “true”
True
vulnerabilities,” in 2019 34th IEEE/ACM International Conference on
boolean expression (e.g., 1, select 1, 2<>3 in Table X) or be
AutomatedSoftwareEngineering(ASE). IEEE,2019,pp.1286–1288.
[53] Y. Yu, G. Liu, H. Yan, H. Li, and H. Guan, “Attention-based bi-lstm mutated into a recursive nested form combined with whites-
modelforanomaloushttptrafficdetection,”in201815thInternational paces and “or” expression (S ·S ·Σ ·S · Σ ).
True and true
Conference on Service Systems and Service Management (ICSSSM).
Afterwards, we can see that it uses rule 9, rule 6, rule 7
IEEE,2018,pp.1–6.
[54] R.S.SuttonandA.G.Barto,Reinforcementlearning:Anintroduction. and rule 10 in Figure 8 respectively, and finally generates
MITpress,2018. a candidate SQLi payload “true\n&&/**foo*/select 1\tand
[55] Audi-1,“Sqli-labs,”https://www.github.com/Audi-1/sqli-labs,2014.
2<>3”, which is semantically equivalent to “1 = 1”.
[56] I.J.Goodfellow,J.Shlens,andC.Szegedy,“Explainingandharnessing
adversarialexamples,”arXivpreprintarXiv:1412.6572,2014. It is paramount that the context-free grammar (including
[57] Wallarm,“Wallarmnode(ai-basedng-wafinstance)bywallarm,”https: startingsymbols,non-terminalsymbols,terminalsymbols,and
//aws.amazon.com/marketplace/pp/prodview-5rl4dgi4wvbfe.
predefinedrules)aremanuallydefined,whichistoensurethat
[58] zangobot,“Waf-a-moledataset,”https://github.com/zangobot/wafamole
dataset,2020. AdvSQLi will not invalidate the generated SQLi payloads or
[59] R. Zhong, Y. Chen, H. Hu, H. Zhang, W. Lee, and D. Wu, “Squirrel: cause unexpected damage. Subsequent researchers only need
Testingdatabasemanagementsystemswithlanguagevalidityandcov-
to add simple items in the interfaces of our grammar if they
eragefeedback,”inProceedingsofthe2020ACMSIGSACConference
onComputerandCommunicationsSecurity,2020,pp.955–970. want to extend it.
[60] Q. Wang, D. Wang, C. Cheng, and D. He, “Quantum2fa: efficient
quantum-resistanttwo-factorauthenticationschemeformobiledevices,”
IEEETransactionsonDependableandSecureComputing,2021. TABLEX
[61] S. Roy, A. K. Das, S. Chatterjee, N. Kumar, S. Chattopadhyay, and EXAMPLESOFTERMINALSYMBOLSINCFG.Σ,τ,f ANDγAREALL
J.J.Rodrigues,“Provablysecurefine-graineddataaccesscontrolover TERMINALSYMBOLS;SPECIFICALLY,f INDICATESTHATITNEEDSTO
multiple cloud servers in mobile cloud computing based healthcare PASSINVALUES,SUCHASCHANGINGTHECASEOFANYWORD(LINE3
applications,” IEEE Transactions on Industrial Informatics, vol. 15, OFFIGURE1);τ MEANSTAUTOLOGYANDγREFERSTOCOMMENTS.
no.1,pp.457–468,2018.
[62] S.Qiu,D.Wang,G.Xu,andS.Kumari,“Practicalandprovablysecure Σ Examples
three-factorauthenticationprotocolbasedonextendedchaotic-mapsfor
mobile lightweight devices,” IEEE Transactions on Dependable and Σ slash /
SecureComputing,vol.19,no.2,pp.1338–1351,2020. Σ asterisk *
Σ ,\t,\n
Σor or,||
Σ and and,&&
APPENDIX Σ false 0,select0,2=3,false
Σtrue 1,select1,2<>3,true
Context-Free Grammar γ
chars
a21r*!,skx9{1-,2sd.$5s,sd2j3znm,39nsq1
γsentence helloworld,todayisdog,overthealphabet
γ benign provincia=burgos,login=karina9,pic=1.gif
1 S τ →S True | τ string | τ complex | τ number f inlinecomment union→/*!union*/,where→/*!where*/
2 S
∀
→f
inlinecomment
(∀) fswapcase select→sElECt,OR→or,from→FrOM
3 S →f (∀ )
f
changebase
1→0x1,256→0x100,176→select176
∀word swapcase word τ number 78=78,1=1,2021like2021,0x2=2
4 S ∀number →f changebase (∀ number ) τstring ‘6’like‘6’,‘foo’like‘foo’,‘bar’=‘bar’
5 S Where →Σ where · S False · Σ or | Σ where · S True · Σ and τ (selectord(‘r’)regexp114)=0x1,
6 S →Σ | S complex (select1)=(selectord(‘r’)between114and115)
γ
7 S →S · S · S
γ γleft γbody γright
8 S →Σ | S · S · Σ · S · Σ
False false False or false In addition to line 9 in Figure 8, some of the other rules
9 S →Σ | S · S · Σ · S · Σ
True true True and true (e.g., line 8 and line 12) are also defined recursively, which
10 S →Σ · S
γleft slash γasterisk might cause an endless loop, i.e., terminal symbols can never
11 S →S · Σ
γright γasterisk slash
be reached in generating the candidate SQLi payload. To
12 S →S · Σ | Σ
γasterisk γasterisk asterisk asterisk
address this issue, instead of simply defining the max depth
13 S →γ · γ · γ
γbody chars sentence benign
of recursion, we present a weighted mutation strategy (Algo-
rithm 2) by employing a decay rate D (e.g., 0.5). The weight
Fig.8. Asimplifiedversionofcontext-freegrammarforgeneratingsemantic of a non-terminal character V being selected will decrease
replacements.Sisthestartingsymbol;Σ,τ,fandγareallterminalsymbols;
Specifically,f indicatesthatitneedstopassinvalues,suchaschangingthe exponentially according to D, e.g., the weight of selecting V
caseofanyword(line3);τ meanstautologyandγ referstocomments. for the third time is 0.53.

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 15
Fig.9. Anexampleofusingcontext-freegrammartogenerateanequivalentreplacementfor“1=1”.Thecontentsofthesamecolorconnectedbyarrows
indicatethestatesbeforeandafteronestepgeneration
Algorithm 2: Weighted CFG Generation in the interfaces of our grammar if they want to extend it.
Data: CFG Rules R, Entry Symbol sym, Decay Rate Experimental performance consumption
D, Chosen Counts C AsthefindingsinRQ2,AdvSQLidemonstratesacapability
Result: Generated sentence sentence to achieve a higher attack success rate with fewer interaction
1 sentence←EmptyString ; steps. To provide a deeper understanding of the associated
2 weights←EmptyList ; time and performance overheads, we conduct the following
3 for e in R[sym] do experiments.
4 if e in C then WereimplementtheexperimentsinRQ2,whicharecarried
5
weights.append(DC[e])
out on an Ubuntu 20.04 server, equipped with 64GB RAM
6 else and powered by an Intel(R) Xeon(R) Silver 4210R CPU.
7 weights.append(1.0) The primary objective was to assess both the runtime and
// Weighted selection function.
memory consumption. It’s important to emphasize that the
8 rand sym← R[sym][WeightedChoice reported memory consumption values represent the average
(weights)] ;
taken from continuous sampling throughout the entire experi-
9 C[rand sym] ←C[rand sym]+1 ; mentduration.Webenchmarkedagainsttwobaselinemethods,
10 for s in rand sym do WAF-A-MoLE and DRL, and also assessed both AdvSQLi(A)
11 if s in R then – a simplified version of our primary approach and AdvSQLi,
// Call itself recursively.
our core method.
12 sentence←sentence+Self (R,s,D,C) ;
AsshowninTableXI,thememoryconsumptionacrossdif-
13 else
ferentmethodsisfairlyconsistent,withonlyminordifferences
14 sentence←sentence+s ;
observed. In most scenarios, AdvSQLi consumes about 10%
15 C[rand sym] ←C[rand sym]−1 ;
additionalmemorycomparedtotheothertechniques,marking
16 return sentence ;
its competitive efficiency. DRL emerges as the fastest method.
This speed can be attributed to its pre-completed training
phase. During the attack, DRL only needs to select the most
Besides, it is worth mentioning that the above-mentioned suitable mutation method based on the current payload state.
context-free grammar (including starting symbols, non- As anticipated, AdvSQLi does demand the most time, which
terminal symbols, terminal symbols, and predefined rules) are is closely tied to the construction and search processes of its
manually defined, which is to ensure that AdvSQLi will not Monte Carlo tree. Although AdvSQLi exhibits a higher time
invalidate the generated SQLi payloads or cause unexpected overhead, its vastly superior attack success rate compared to
damage.Subsequentresearchersonlyneedtoaddsimpleitems thebaselinemethodsjustifiesthiscost.Whenwedistributethis

IEEETRANSACTIONSONINFORMATIONFORENSICSANDSECURITY 16
TABLEXI
TheconsumptionresultsofattackingagainstSQLidetectionunderthesettingssamewith#TableV.WAMmeansWAF-A-MoLE.Thetimeandmemory
consumptionofDRLonlyinvolvestheinferencephaseanddoesnotincludethepre-trainingphase.ThetimeconsumptionofattackingWAF-Brainmodels
islimitedbytheinferencespeed.
Consumption
Dataset TargetSQLi Time(s) Memory(MB)
Detection
AdvSQLi(R) AdvSQLi WAM DRL AdvSQLi(R) AdvSQLi WAM DRL
WAF-Brainδ=0.1 554.53 2240.03 4713.73 1751.27 344.55 369.34 355.98 397.46
WAF-Brain1% 135.02 315.48 577.12 564.39 344.08 365.68 361.01 388.27
WAF-Brain1‰ 18.42 51.97 198.96 53.76 342.88 362.49 343.59 382.28
HPD CNN1% 293.44 1161.01 1029.56 198.52 350.72 370.13 340.38 376.7
CNN1‰ 290.83 982.02 950.73 179.91 351.07 370.53 343.74 373.76
LSTM1% 654.28 2218.46 1036.59 223.82 350.55 371.04 355.3 375.66
LSTM1‰ 639.42 2154.88 983.12 221.69 350.41 370.82 350.55 383.88
WAF-Brainδ=0.1 483.96 1817.85 5434.94 1342 346.52 372.88 356.02 373.04
WAF-Brain1% 91.95 183.19 362.42 383.37 339.86 367.58 343.88 379.64
WAF-Brain1‰ 6.82 21.51 52.23 26.8 341.22 364.02 356.68 366.52
SIK CNN1% 266.19 1015.42 1009.42 183.85 350.77 376.21 355.51 378.28
CNN1‰ 252.28 976.15 955.46 179.08 351.45 378.1 354.65 370.32
LSTM1% 525.8 1925.24 954.07 232.8 352.42 377.26 357.17 373.65
LSTM1‰ 509.53 1865.95 920.89 223.93 349.9 376.39 356.19 375.16
time consumption across 1000 samples, the results provide a Xiang Chen received the B.Eng. and M.Eng. de-
worthy trade-off for its efficacy. grees from Fuzhou University, in 2019 and 2022,
respectively. He is currently pursuing the Ph.D.
degree with the College of Computer Science and
Technology,ZhejiangUniversity,China.Hehaspub-
lishedpapersinIEEEINFOCOMandIEEEICNP.
HereceivedtheBestPaperAwardfromIEEE/ACM
IWQoS 2021 and the Best Paper Candidate from
IEEE INFOCOM 2021. His research interests in-
cludeprogrammablenetworksandnetworksecurity.
Zhenqing Qu is a graduate student at Zhejiang
University.Hisresearchfocusesonwebsecurityand
data-driven security. He has spoken at Black Hat
Asia 2022. He is a member of the Azure Assassin
Alliance CTF Team. Additionally, he has reported
several severe defects to mainstream security ven-
dors,whichwereconfirmedandfixedquickly. Shouling Ji is a ZJU 100-Young Professor in the
College of Computer Science and Technology at
Zhejiang University and a Research Faculty in the
School of Electrical and Computer Engineering at
GeorgiaInstituteofTechnology(GeorgiaTech).He
receivedaPh.D.degreeinElectricalandComputer
Engineering from Georgia Institute of Technology
, a Ph.D. degree in Computer Science from Geor-
gia State University, and B.S. (with Honors) and
Xiang Ling is currently an assistant professor at
M.S. degrees both in Computer Science from Hei-
InstituteofSoftware,ChineseAcademyofSciences.
longjiang University. His current research interests
HereceivedhisPhDdegreefromZhejiangUniver-
includeData-drivenSecurityandPrivacy,AISecurityandBigDataAnalytics.
sity.Hisresearchfocusesondata-drivensecurity,AI
HeisamemberofACM,IEEE,andCCFandwastheMembershipChairof
security and program analysis. His work has been
theIEEEStudentBranchatGeorgiaStateUniversity(2012-2013).
publishedtop-rankedconferencesandjournals,like
IEEES&P,INFOCOM,ICSE,TNNLSandTKDD.
ChunmingWuiscurrentlyaProfessorwiththeCol-
legeofComputerScienceandTechnology,Zhejiang
University.HeisalsotheAssociateDirectorofthe
ResearchInstituteofComputerSystemArchitecture
Ting Wang is an Associate Professor and Empire andNetworkSecurity,ZhejiangUniversity,andthe
Innovation Scholar in the Department of Computer DirectoroftheFluctlightSecurityLab.Hisresearch
Science at Stony Brook University. He received interests include network security, reconfigurable
his Ph.D. degree from Georgia Tech. He conducts networkandnext-generationnetworkinfrastructures.
research at the interface of machine learning, pri- Hehaspublishedmorethan90papersinaseriesof
vacy, and security. His recent work focuses on international journals, magazines, and conferences,
improving AI technologies in terms of security as- e.g.,CCS,S&P,USENIX,INFOCOM,ToN,etc.
surance, privacy preservation, and decision-making
transparency.
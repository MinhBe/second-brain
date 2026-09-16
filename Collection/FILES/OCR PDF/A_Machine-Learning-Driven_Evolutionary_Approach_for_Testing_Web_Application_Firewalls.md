1
A Machine Learning-Driven Evolutionary
Approach for Testing Web Application Firewalls
Dennis Appelt, Cu D. Nguyen, Annibale Panichella, Lionel C. Briand Fellow, IEEE
(cid:70)
Abstract—Webapplicationfirewalls(WAF)areanessentialprotection the Open Web Application Security Project (OWASP) finds
mechanismforonlinesoftwaresystems.Becauseoftherelentlessflow that the prevalence of SQLi vulnerabilities is common and
ofnewkindsofattacksaswellastheirincreasedsophistication,WAFs the impact of a successful exploitation is severe [50]. While
have to be updated and tested regularly to prevent attackers from
we assess our approach based on the example of SQLi, we
easily circumventing them. In this paper, we focus on testing WAFs
believethatmanyoftheprinciplesofourmethodologycan
for SQL injection attacks, but the general principles and strategy we
beadaptedtootherformsofattacks.
proposecanbeadaptedtoothercontexts.WepresentML-Driven,an
Varioustechniqueshavebeenproposedintheliterature
approachbasedonmachinelearningandanevolutionaryalgorithmto
automaticallydetectholesinWAFsthatletSQLinjectionattacksbypass to detect SQLi attacks based on a variety of approaches,
them. includingwhite-boxtesting[21],staticanalysis[20],model-
Initially,ML-Drivenautomaticallygeneratesadiversesetofattacks based testing [30], and black-box testing [18]. However,
and submit them to the system being protected by the target WAF. such techniques present some limitations which may ad-
Then, ML-Driven selects attacks that exhibit patterns (substrings) versely impact their practical applicability as well as their
associatedwithbypassingtheWAFandevolvethemtogeneratenew
vulnerability detection capability. For example, white-box
successfulbypassingattacks.Machinelearningisusedtoincrementally
testingtechniquesandstaticanalysistoolsrequireaccessto
learn attack patterns from previously generated attacks according to
sourcecode[33],whichmightnotbepossiblewhendealing
their testing results, i.e., if they are blocked or bypass the WAF. We
with third-party components or industrial appliances, and
implemented ML-Driven in a tool and evaluated it on ModSecurity,
a widely used open-source WAF, and a proprietary WAF protecting a are linked to specific programming languages [19]. Model-
financial institution. Our empirical results indicate that ML-Driven is based testing techniques require models expressing the se-
effective and efficient at generating SQL injection attacks bypassing curitypoliciesortheimplementationofWAFsandtheweb
WAFsandidentifyingattackpatterns. application under test [30], which are often not available
or very difficult to manually construct. Black-box testing
IndexTerms—SoftwareSecurityTesting,SQLInjection,WebApplica- strategiesdonotrequiremodelsorthesourcecodebutthey
tionFirewall.
are less effective in detecting SQLi vulnerabilities. Indeed,
comprehensive reviews on black-box techniques [13], [18]
have revealed that many types of security vulnerabilities
1 INTRODUCTION
(including SQLi attacks) remain largely undetected and,
WEB application firewalls (WAF) protect enterprise thus,warrantfurtherresearch.
web systems from malicious attacks. As a facade to In our preliminary work [9], we introduced a novel
the web application they protect, WAFs inspect incoming black-box technique, namely ML-Driven, that combines
HTTPmessagesanddecidewhetherblockingorforwarding the classical (µ+λ) evolutionary algorithm (EAs) with ma-
them to the target web application. The decision is often chine learning algorithms for generating tests (i.e., attacks)
performed based on a set of rules, which are designed to bypassing a WAF’s validation routines. ML-Driven uses
detect attack patterns. Since cyber-attacks are increasingly machinelearningtoincrementallylearnattackpatternsand
sophisticated, WAF rules tend to become complex and dif- build a classifier, i.e., that predicts combinations of attack
ficult to manually maintain and test. Therefore, automated substrings (“slices”) associated with bypassing the WAF.
testingtechniquesforWAFsarecrucialtopreventmalicious The resulting classifier is used within the main loop of
requestsfromreachingwebapplicationsandservices. (µ+λ)-EAs to rank tests depending on which substrings
In this work, we focus our testing efforts on a common compose them and the corresponding bypassing probabili-
categoryofattacks,namelySQLinjections(SQLi).SQLihas ties.Ineachiteration,testswiththehighestrankareselected
received a lot of attention from academia as well as practi-
andmutatedtogenerateλnewtests(offsprings),whichare
tioners[7],[10],[14],[24],[25],[26],[27],[32],[34],[45].Yet then executed against the WAF. The corresponding execu-
tionresultsareusedtore-traintheclassifiertoincrementally
improveitsaccuracy.Throughsubsequentgenerations,tests
• DennisAppelt,CuD.Nguyen,AnnibalePanichella,andLionelC.Briand
arewiththeSnTCentre,UniversityofLuxembourg,L-2721Luxembourg, areevolvedtoincreasethenumberofattacksabletobypass
Luxembourg. thetargetWAF.
ManuscriptreceivedMarchxx,2016;revisedyyyyyyxx,2016. We defined two variants of ML-Driven, namely

2
ML-Driven DandML-Driven B,thatdifferinthenumber to large numbers of features and datasets, but with
oftestsbeingselectedforgeneratingnewtests(offsprings). complementaryadvantagesanddrawbacks.
The former variant selects fewer tests to evolve but gener- • Extendingthepreviousevaluationandconductinga
ates more offsprings per selected test, thus increasing ex- large-scaleexperimentonaproprietaryWAFprotect-
ploitation(deepsearch).Thelattervariantselectsmoretests ingafinancialinstitution.
to mutate, which results in a lower number of offsprings • Comparing ML-Driven with SqlMap and WAF
perselectedtest,henceincreasingexploration(broadsearch). Testing Framework, which are state-of-the-art
Our preliminary study with ModSecurity1, a popular open vulnerabilitydetectiontools.
source WAF, has shown that both ML-Driven D and • A qualitative analysis showing that the additional
ML-Driven B are effective in generating a large number distinct attacks found by ML-Driven E help secu-
ofdistinctSQLiattackspassingthoughttheWAF.However, rity analysts design better patches compared to the
ML-Driven D performs better in the earlier stages of the other ML-Driven variants, RAN, and state-of-the-
search while ML-Driven B outperforms it in the last part artvulnerabilitydetectiontools.
ofthesearch,forreasonswewillexplain.
The remainder of the paper is structured as follows.
In the race against cyber-attacks, time is vital. Being
Section2providesbackgroundinformationonWAFsaswell
abletolearnandanticipateattacksthatsuccessfullybypass
asSQLiattacksanddiscussesrelatedwork.Section3details
WAFs in a timely manner is critical. With more successful,
our approach followed by Section 4 where we describe the
distinct attacks being detected, the WAF administrator is
designandprocedureofourempiricalevaluation.Section5
in a better position to identify missed attack patterns and
describes the evaluation results and their implications re-
to devise patches that block all further attacks sharing the
gardingourresearchquestionswhileSection6explainsand
same patterns. Therefore, our goal is to devise a technique
illustrates how to use the generated attacks for repairing
that can efficiently generate as many successful distinct
vulnerable WAFs. Further reflections on the results are
attacks as possible. To this aim, in this paper we ex-
providedinSection7whileSection8concludesthispaper.
tended our prior work and propose an adaptive variant
of ML-Driven, namely ML-Driven E (Enhanced), that
combinesthestrengthsofML-Driven D(deepsearch)and
2 BACKROUND AND RELATED WORK
ML-Driven B (broad search) in an adaptive manner. In
ML-Driven E, the number of offsprings is computed dy- Inthissection,weprovidebackgroundnotionsaboutSQLi
namicallydependingonthebypassingprobabilityassigned vulnerabilities and describe existing white-box and black-
toeachselectedtestbytheconstructedclassifier.Conversely, boxapproachesaimedatuncoveringthem.
ML-DrivenBandDgenerateafixednumberofoffsprings
perattack/test.Therefore,ML-Driven Eisamoreflexible
2.1 SQLInjectionVulnerabilities
approachthatbetterbalancesexplorationoverruntime.
In systems that use databases, such as web-based systems,
Moreover, we conducted a much larger empirical study
the SQL statements accessing back-end databases are usu-
with two popular WAFs that protect three open-source
ally treated as strings. These strings are formed by con-
and 44 proprietary web services. The results show that the
catenating different string fragments based on user choices
enhancedversionofourtechnique(ML-Driven E)signifi-
or the application’s control flow. Once a SQL statement is
cantly outperforms: (i) its predecessors ML-Driven B and
formed,itissubmittedtothedatabaseservertobeexecuted.
ML-Driven D; (ii) a random test strategy, which serves as
For example, a SQL statement can be formed as follows (a
a baseline; (iii) two state-of-the-art vulnerability detection
simplifiedexamplefromoneofourwebservicesinthecase
tools,namelySqlMapandWAF Testing Framework. We
study):
also performed a qualitative analysis of the attacks gener-
atedbyourapproachandwefoundoutthattheyenablethe $sql = "select * from hotelList where
identificationofattackpatternsthatarestronglyassociated country =’";
$sql = $sql.$country;
withbypassingtheWAFs,thusprovidingbettersupportfor
$sql = $sql."’";
improvingtheWAFs’ruleset.
$result = mysql_query($sql) or
To summarize, the key contributions of this paper in- die(mysql_error());
clude:
Thevariable$countryisaninputprovidedbytheuser,
• Enhancing ML-Driven with an adaptive test selec- which is concatenated with the rest of the SQL statement
tionandgenerationheuristic,whichmoreeffectively and then stored in the string variable $sql. The string is
exploresattackpatternswithhigherlikelihoodofby- then passed to the function mysql_query that sends the
passingtheWAF.ThisenhancedML-Drivenvariant SQLstatementtothedatabaseservertobeexecuted.
is intended to replace its predecessors, leaving the SQLi is an attack technique in which attackers inject
practitionerswithasingle,yetthebest,option. malicious SQL code fragments into input parameters that
• Assessing the influence of the selected machine lack proper validation or sanitization. An attacker might
learning algorithm on the test results by comparing constructinputvaluesinawaythatchangesthebehaviorof
two alternative classification models, namely Ran- theresultingSQLstatementandperformsarbitraryactions
domTreeandRandomForest,whicharebothadapted on the database (e.g. exposure of sensitive data, insertion
or alteration of data without authorization, loss of data, or
1.https://www.modsecurity.org eventakingcontrolofthedatabaseserver).

3
Inthepreviousexample,iftheinput$countryreceived recognized by the firewall as SQLi attacks and generate
the attack payload ’ or 1=1 --, the resulting SQL state- bypassingtestcasesthatavoidthosepatterns.
mentis: Tripp et al. [48] proposed XSS Analyzer, a learning
approach to web security testing. The authors tackle the
select * from hotelList
where country=’’ or 1=1 --’ problemofefficientlyselectingfromacomprehensiveinput
spaceofattacksbylearningfrompreviousattackexecutions.
Theclauseor 1=1isatautology,i.e.,theconditionwill Based on the performed learning, the selection of new
always be true, and is thus able to bypassing the original attacks is adjusted to select attacks with a high probability
conditioninthewhereclause,makingtheSQLqueryreturn ofrevealingavulnerability.Morespecifically,XSSAnalyzer
allrowsinthetable. generates attacks from a grammar and learns constraints
WebApplicationFirewalls.Webapplicationswithhigh thatexpresswhichliteralsanattackcannotcontaininorder
securityrequirementsarecommonlyprotectedbyWAFs.In to evade detection. The authors find that XSS Analyzer
the overall system architecture, a WAF is placed in front of outperforms a comparable state-of-the-art algorithm, thus,
the web application that has to be protected. Every request suggestingthatlearninginputconstraints(aconceptsimilar
that is sent to the web application is examined by the to the path conditions in ML-Driven) is effective to guide
WAFbeforeitreachesthewebapplication.TheWAFhands thetestcasegeneration.
over the request to the web application only if the request In contrast to our work, XSS Analyzer applies learning
complieswiththefirewall’sruleset. to individual literals only while our approach also learns
A common approach to define the firewall’s rule set ifacombinationofliteralsislikelytobypassorbeblocked.
is using a black-list. A black-list contains string patterns, Therefore,XSSAnalyzercannotcapturemorecomplexinput
typically defined as regular expressions. Requests recog- constraints involving multiple literals simultaneously, e.g.,
nized by these patterns are likely to be malicious attacks anattackshouldcontainliterala,butnotbandcinorderto
(e.g., SQLi) and, therefore, are blocked. For example, the evade detection. Furthermore, to analyze which literals in
following regular expression describes the syntax for SQL an attack are blocked, XSS Analyzer first splits each attack
comments, e.g., /**/ or #, which are frequently used in intoitscomposingtokens;then,itresendseachtokentothe
SQLiattacks: targetwebapplication.Sincemultipleattackscansharethe
same tokens, XSS Analyzer sends each token only once to
/\*!?|\*/|[’;]--|--[\s\r\n\v\f]
|(?:--[^-]*?-) avoid performing the same analysis multiple times. This
|([^\-&])#.*?[\s\r\n\v\f]|;?\\x00 procedure consumes a large quantity of HTTP requests. In
contrast, ML-Driven does not require to resubmit individ-
There are several reasons why a WAF may provide
ualslices,butlearnspathconditionssolelyfrompreviously
insufficient protection, including implementation bugs or
executed test case and, thus, spends its test budget more
misconfiguration.OnewaytoensuretheresilienceofaWAF efficiently. In addition, there are differences between XSS
againstattacksistorelyonanautomatedtestingprocedure AnalyserandML-Drivenintermsofobjectives:Theformer
that thoroughly and efficiently detects vulnerabilities. This
addresses cross-site scripting sanitization in web applica-
paperaddressesthischallengeforSQLinjections,oneofthe
tions,whilethelatteraddressesthedetectionofSQLiattacks
maintypesofattacksinpractice.
inWAFs.
Ingrammar-basedtesting,astrategytypicallysamplesa
large input space defined by a grammar. Several grammar-
2.2 RelatedWork
based approaches exist in the literature for testing security
Previous research on ensuring the resilience of IT systems properties of an application under test [37], [47]. Gode-
against malicious requests has focused on the testing of froid et al. [23] proposed white-box fuzzing, which starts
firewallsaswellasinputvalidationmechanisms. by executing an application under test with a given well-
Offuttetal.introducedtheconceptofBypassTestingin formed input and uses symbolic execution to create input
whichanapplication’sinputvalidationistestedforrobust- constraintswhenconditionalstatementsareencounteredon
ness and security [38]. Tests are generated to intentionally the execution path. Then, new inputs are created that ex-
violate client-side input checks and are then sent to the ercise different execution paths by negating the previously
server application to test whether the input constraints are collected constraints. The implementation of the approach
adequatelyevaluated.Liuetal.[35]proposedanautomated found a critical memory corruption vulnerability in a file-
approach to recover an input validation model from pro- processing application. In a follow-up work, the authors
gramsourcecodeandformulatedtwocoveragecriteriafor propose grammar-based white-box fuzzing [21], which ad-
testing input validation based on the model. Desmet et dressesthegenerationofhighlystructuredprograminputs.
al. [17] verify a given combination of a WAF and a web Inthiswork,well-formedinputsaregeneratedfromagram-
application for broken access control vulnerabilities, e.g. mar and the constraints created during execution are ex-
forceful browsing, by explicitly specifying the interactions pressedasconstraintsongrammartokens.Togeneratenew
of application components on the source code level and by inputs, aconstraint solversearches thegrammar forinputs
applying static and dynamic verification to enforce only that satisfy the constraints. The authors implemented their
legal state transitions. In contrast, we propose a black- work in a tool named SAGE and found several security-
box technique that does not require access to source code related bugs [22]. In contrast to the mentioned work of
or client-side input checks to generate test cases. In our Godefroid et al., our work does not require access to the
approach,weusemachinelearningtoidentifythepatterns sourcecodeoftheapplicationundertest,whichisinmany

4
practical scenarios not available, but proposes a black-box WeconsiderthreemaincategoriesofSQLiattacksinour
approach based on machine learning to efficiently sample grammar:(i)Boolean,(ii)Union,and(iii)Piggy-Backed.These
theinputspacedefinedbyanattackgrammar. type of attacks aim at manipulating the intended logic by
The topic of testing network firewalls has also been injectingadditionalSQLcodefragmentsintheoriginalSQL
addressed by an abundant literature. Although network queries.Webrieflydiscusseachattackcategoryandprovide
firewallsoperateonalowerlayerthanapplicationfirewalls, exampleattacksthatcanbederivedusingourgrammar.For
which are our focus, they share some commonalities. Both adetaileddiscussionrefertotheliterature[10],[27].
use policies to decide which traffic is allowed to pass or BooleanAttacks.TheintentofabooleanSQLiattackisto
should be rejected. Therefore, testing approaches to find influencethewhereclausewithinaSQLstatementtoalways
flaws in network firewall policies might also be applicable evaluate either to true or false. As a result, a statement,
to web application firewall policies. Bruckner et al. [1] into which a boolean SQLi attack is injected, returns on its
proposedamodel-basedtestingapproachwhichtransforms execution either all data records of the queried database
a firewall policy into a normal form. Based on case studies tables(incasethewhereclauseevaluatesalwaystotrue)or
they found that this policy transformation increases the none (in case the where clause evaluates always to false).
efficiency of test case generation by at least two orders of This attack method is typically used to bypass authenti-
magnitude. Hwang et al. [29] defined structural coverage cation mechanisms, extract data without authorization, or
criteria of policies under test and developed a test gener- toidentifyinjectableparameters.Theexampledescribedin
ation technique based on constraint solving that tries to Section2.1isaninstanceofbooleanattacks.
maximize structural coverage. Other research has focused Union Attacks. The union keyword joins the result
on testing the firewalls implementation instead of policies. set of multiple select statements and, hence, union SQLi
Al-Shaer et al. [3] developed a framework to automatically attacks are typically used to extract data located in other
testifapolicyiscorrectlyenforcedbyafirewall.Therefore, database tables than the original statement is querying.
the framework generates a set of policies as well as test For example, consider an application that retrieves a list of
traffic and checks whether the firewall handles the gen- product names based on a search term. The SQL statement
erated traffic correctly according to the generated policy. toretrievetheproductnamesmightbe:
Some authors have proposed specification-based firewall
SELECT name FROM products WHERE name LIKE
testing. Jürjens et al. [30] proposed to formally model the
"%search term%"
tested firewall and to automatically derive test cases from
the formal specification. Senn et al. [43] proposed a formal where search term is a string provided by the user.
language for specifying security policies and automatically If the SQL statement is formed in an insecure way, an
generate test cases from formal policies to test the firewall. attacker could provide the search term phone%" UNION
Incontrast,inadditiontotargetingapplicationfirewalls,our SELECT passwd FROM users #%", which would result
approach does not rely in any models of security policies inthestatement:
or the firewall under test, such formal models are rarely
SELECT name FROM products WHERE name LIKE
availableinpractice.
"%phone%" UNION SELECT passwd FROM users
Hence,inadditiontoalistofproductscontainingthesearch
3 APPROACH
term phone, the attacker could obtain the passwords of all
This section introduces an approach for testing WAFs. Sec- userswiththemodifiedqueryabove.
tion 3.1 defines the input space for this testing problem Piggy-BackedAttacks. InSQL,thesemicolon(;)canbe
as a context-free grammar. Section 3.2 presents a simple used to separate two SQL statements. Piggy-Backed attacks
attackgenerationstrategythatrandomlysamplestheinput usethesemicolontoappendanadditionalstatementtothe
space and serves as baseline. Section 3.3 presents two test originalstatementandcanbeusedforawiderangeofattack
generation strategies that make use of machine learning purposes(e.g.dataextractingormodification,anddenialof
to guide test generation towards areas in the input space service). An example of a piggy-backed attack is ; DROP
that are more likely to contain successful attacks. Finally, TABLE users #.Ifthisattackisinjectedintoavulnerable
Section 3.4 details an approach to combine such attack SQLstatement,itdropsthetableuserand,thus,potentially
generationstrategiestoachievebetterresults. breakstheapplication.
The grammar. We defined a grammar for SQLi attacks
in the Extended Backus Normal Form, which is publicly
3.1 AContext-FreeGrammarforSQLiAttacks available4 on GitHub. An excerpt of the grammar is de-
SQLi attacks (or test cases in this context) are small “pro- picted in Figure 1. The start symbol of the grammar
grams” that aim at changing the intent of the target SQL is (cid:104)start(cid:105), while “::=” denotes the production symbol, “,”
queries they are injected in. We systematically surveyed is concatenation, and “|” represents alternatives (grammar
knownSQLiattackspublishedintheliterature,e.g.,[5],[6], rule 1 of Figure 1). The grammar covers three different
[24] and from other sources e.g., OWASP2, and SqlMap3. contexts in which SQLi attacks can be inserted into: numer-
Then,wedefinedacontext-freegrammarforgeneratingand icCtx, sQuoteCtx, and dQuoteCtx. SQLi attacks belonging to
analyzingSQLiattacks. thefirstcontextyieldsyntacticallycorrectstatementsifthey
are injected in a numerical context (rule 2 of Figure 1). For
2.https://www.owasp.org
3.http://sqlmap.org 4.https://github.com/dappelt/xavier-grammar

5
example, the attack 1 OR true belongs to numericCtx and
1. (cid:104)start(cid:105)::= (cid:104)numericCtx(cid:105)|(cid:104)sQuoteCtx(cid:105)|(cid:104)dQuoteCtx(cid:105);
yields a syntactically correct statement if injected into the
statementSELECT * FROM person WHERE age=<user_- InjectionContext
input> where the placeholder <user_input> is intended to 2. (cid:104)numericCtx(cid:105)::= (cid:104)digitZero(cid:105),(cid:104)wsp(cid:105),(cid:104)booleanAtk(cid:105),(cid:104)wsp(cid:105)
be replaced with a numerical value. Similarly, the second | (cid:104)digitZero(cid:105), (cid:104)parC(cid:105), (cid:104)wsp(cid:105), (cid:104)booleanAtk(cid:105), (cid:104)wsp(cid:105), (cid:104)operOr(cid:105),
(cid:104)parO(cid:105),(cid:104)digitZero(cid:105)
and third context, sQuoteCtx and dQuoteCtx, target SQL
| (cid:104)digitZero(cid:105),[(cid:104)parC(cid:105)],(cid:104)wsp(cid:105),(cid:104)sqliAtk(cid:105),(cid:104)comment(cid:105);
statements in which the user input is used as string literal 3. (cid:104)sQuoteCtx(cid:105)::= (cid:104)squote(cid:105), (cid:104)wsp(cid:105), (cid:104)booleanAtk(cid:105), (cid:104)wsp(cid:105), (cid:104)operOr(cid:105),
and surrounded by single quotes (rule 3 of Figure 1) and (cid:104)squote(cid:105)
| (cid:104)squote(cid:105), (cid:104)parC(cid:105), (cid:104)wsp(cid:105), (cid:104)booleanAtk(cid:105), (cid:104)wsp(cid:105), (cid:104)operOr(cid:105),
double quotes (rule 4), respectively. For example, the SQLi
(cid:104)parO(cid:105),(cid:104)squote(cid:105)
attack " OR "a"="a belongs to dQuoteCtx and yields a | (cid:104)squote(cid:105),[(cid:104)parC(cid:105)],(cid:104)wsp(cid:105),(cid:104)sqliAtk(cid:105),(cid:104)comment(cid:105);
syntactically correct statement if injected into SELECT * 4. (cid:104)dQuoteCtx(cid:105)::= (cid:104)dquote(cid:105), (cid:104)wsp(cid:105), (cid:104)booleanAtk(cid:105), (cid:104)wsp(cid:105), (cid:104)operOr(cid:105),
FROM person where name="<user_input>". (cid:104)dquote(cid:105)
| (cid:104)dquote(cid:105), (cid:104)parC(cid:105), (cid:104)wsp(cid:105), (cid:104)booleanAtk(cid:105), (cid:104)wsp(cid:105), (cid:104)operOr(cid:105),
Ourgrammarcanbeextendedtoincorporateothervari- (cid:104)parO(cid:105),(cid:104)dquote(cid:105)
ants of SQLi attacks. For example, the non-terminal (cid:104)blank(cid:105) | (cid:104)dquote(cid:105),[(cid:104)parC(cid:105)],(cid:104)wsp(cid:105),(cid:104)sqliAtk(cid:105),(cid:104)comment(cid:105);
(rule30ofFigure1)canhavemoresemanticallyequivalent 5. (cid:104)sqliAtk(cid:105)::= (cid:104)unionAtk(cid:105)|(cid:104)piggyAtk(cid:105)|(cid:104)booleanAtk(cid:105);
terminal characters: +, /**/, or unicode encodings: %20, UnionAttacks
%09, %0a, %0b, %0c, %0d and %a0; the quotes (single or 6. (cid:104)unionAtk(cid:105)::= (cid:104)union(cid:105), (cid:104)wsp(cid:105), [(cid:104)unionPostfix(cid:105)], (cid:104)operSel(cid:105), (cid:104)wsp(cid:105),
double) can be represented using HTML encoding, and so (cid:104)cols(cid:105)
| (cid:104)union(cid:105), (cid:104)wsp(cid:105), [(cid:104)unionPostfix(cid:105)] , (cid:104)parO(cid:105), (cid:104)operSel(cid:105), (cid:104)wsp(cid:105),
on. Since the grammar is an input to our approach it can
(cid:104)cols(cid:105),(cid:104)parC(cid:105);
alsobereplacedwithalternativegrammars,whichdefinean 7. (cid:104)union(cid:105)::= (cid:104)operUni(cid:105)|"/*!",["50000"],(cid:104)operUni(cid:105),"*/"|...;
inputspacefordifferentattacktypes(e.g.cross-sitescripting 8. (cid:104)unionPostfix(cid:105)::= "all",(cid:104)wsp(cid:105)|"distinct",(cid:104)wsp(cid:105);
orXMLinjection).
Piggy-backedAttacks
9. (cid:104)piggyAtk(cid:105)::= (cid:104)operSem(cid:105),(cid:104)operSel(cid:105),(cid:104)wsp(cid:105),(cid:104)funcSleep(cid:105)|...;
3.2 Grammar-basedRandomAttackGeneration
Boolean-basedAttacks
Based on the proposed grammar, the random attack gener- 10. (cid:104)booleanAtk(cid:105)::= (cid:104)orAtk(cid:105)|(cid:104)andAtk(cid:105);
ation (RAN) procedure is straightforward: Beginning from 11. (cid:104)orAtk(cid:105)::= (cid:104)operOr(cid:105),(cid:104)booleanTrueExpression(cid:105);
12. (cid:104)andAtk(cid:105)::= (cid:104)operAnd(cid:105),(cid:104)booleanFalseExpression(cid:105);
thestartsymbol(cid:104)start(cid:105),arandomlyselectedproductionrule
13. (cid:104)booleanTrueExpression(cid:105)::= (cid:104)unaryTrue(cid:105)|(cid:104)binaryTrue(cid:105);
is applied recursively until only terminals are left. Since
SQLOperatorsandKeyword
there is no loop in the grammar, this attack generation
15. (cid:104)operNot(cid:105)::= "!"|"not";
procedurewillalwaysterminate.TheoutputSQLiattackis
16. (cid:104)operBinInvert(cid:105)::= "";
produced by concatenating all terminal symbols appearing 17. (cid:104)operEqual(cid:105)::= "=";
inthegeneratedinstanceofthegrammar. 18. (cid:104)operLt(cid:105)::= "<";
19. (cid:104)operGt(cid:105)::= ">";
To produce a set of diverse random SQLi attacks that
20. (cid:104)operLike(cid:105)::= "like";
yieldsagoodcoverageofthegrammar,eachproductionrule 21. (cid:104)operIs(cid:105)::= "is";
isselectedwithaprobabilityproportionaltothenumberof 22. (cid:104)operMinus(cid:105)::= "-";
23. (cid:104)operOr(cid:105)::= "or"|"||";
distinctproductionrulesdescendingfromthecurrentone.
24. (cid:104)operAnd(cid:105)::= "and"|"&&";
Among the techniques presented in this work, RAN 25. (cid:104)operSel(cid:105)::= "select"
implements the simplest strategy for sampling the input 26. (cid:104)operUni(cid:105)::= "union";
27. (cid:104)operSem(cid:105)::= ";";
spacedefinedbytheattackgrammar.Indeed,multipleSQLi
28. (cid:104)comment(cid:105)::= "#"|(cid:104)ddash(cid:105),(cid:104)blank(cid:105);
attacks can be generated by simply re-applying RAN mul- 29. (cid:104)ddash(cid:105)::= "––"
tiple times until the maximum number of tests/attacks (or
Obfuscation
the maximum running time) is reached. Bypassing attacks
30. (cid:104)inlineComment(cid:105)::= "/**/";
are then detected by executing all generated SQLi attacks 31. (cid:104)blank(cid:105)::= " ";
againstthetargetWAF. 32. (cid:104)wsp(cid:105)::= (cid:104)blank(cid:105)|(cid:104)inlineComment(cid:105)
3.3 MachineLearning-GuidedAttackGeneration
Fig.1.ExcerptofthegrammarusedinthepaperexpressedinExtended
As the difficulty to find bypassing attacks increases, i.e. a BackusNormalForm.
WAFdetectsalargeproportionofattacks,arandomattack
generationstrategy(e.g.,RAN)willincreasinglybecomein-
efficient.Insuchsituations,amoreadvancedtestgeneration given test case [36], [39], [46]. For example, in white-box
strategy that spends more computational effort to identify unit testing, approach level [36] and branch distance [36] are
test cases with a higher bypassing probability is expected used to determine how far is the execution path of test t
tobemoreefficient.Inthissection,weintroduceamachine from covering a given branch in the control flow graph.
learning-basedapproach,calledML-Driven,tosamplethe However, in the context of security testing, the target SQLi
inputspaceinamoreefficientmannerthanRANdoes. vulnerabilities are not known a-priori and, thus, such a
Theoretically, SQLi attacks could be generated using distancefunctionf cannotbedefined.Therefore,wefacethe
search-basedtestingtechniques[4],[12],[36],[40].However, problemtoefficientlychoosefromalargesetofSQLiattacks
the application of these techniques requires the definition the ones that are more likely to reveal holes in the WAF
of a distance function f that measures the distance between undertest.Theproblemischallengingbecausethereislittle
a coverage target to reach and the execution results of a information available to estimate how close a test comes to

6
bypassingtheWAF.Whenatestisexecuted,onlyoneofthe
<start>
followingtwoeventscanbeobserved:bypassing,orblocked.
Thisleavesthesearchwithnoguidancetoeffectivelyassess <sQuoteCtx>
how close a blocked attack is from bypassing the WAF.
<squote> <wsp> <sqliAtk> <comment>
Lack of guidance is a well-known issue to address when
applying search-based techniques since previous studies ‘ ⎵ <booleanAtk> #
(e.g.,[44])showedthatsophisticatedsearchalgorithms(e.g.,
evolutionaryalgorithm)donotprovideanyadvantageover <orAtk>
random search (i.e., the approach in Section 3.2) when the
<operOr> <booleanTrueExpression>
gradientofthefunctionf hasmanyplateaus(flagproblem).
To tackle this problem, we introduce ML-Driven, a OR <binaryTrue>
search-basedtechniquethatusesmachinelearningtomodel
how the elements (attributes of attacks) of the tests are <dquote> <char> <dquote> <operEqual> <dquote> <char> <dquote>
associated with the likelihood of bypassing the WAF, the
“ a ” = “ a ”
latterbeingusedtoguidethesearch.Inthesearchprocess,
Fig.2.Thederivationtreeofthe“boolean”SQLiattack:’ OR“a”=“a”#.
tests that are predicted to have such high likelihood are
considered to have a high fitness and are more likely to
S1 S2 S3 S4
be generated. ML-Driven first employs random test gen-
eration, as described in the previous section, to generate <squote> <wsp> <sqliAtk> <comment>
an initial training set. Then, these tests are sent to a web
application protected by the WAF, and are labelled as “P” ‘ ⎵ <booleanAtk> #
or“B”dependingonwhethertheybypassorareblockedby <orAtk>
the WAF, respectively. Tests and execution results are then
<operOr> <booleanTrueExpression>
encoded and used as initial training data to learn a model
estimatingthelikelihood(f)withwhichtestscanbypassthe
OR <binaryTrue>
WAF. Using this measure we can rank, select, and modify
tests associated with high f values to produce new tests. <dquote> <char> <dquote> <operEqual> <dquote> <char> <dquote>
Thesenewtestsarethenexecuted,andtheirresults(“P”or “ a ” = “ a ”
“B”) are used to improve the prediction model, which will
in turn help generating more distinct tests that bypass the
Fig.3.ExamplesubsetofslicesdecomposedfromthetreeinFig.2.
WAF.
Inwhatfollows,wewilldiscussindetailtheprocedure substrings by decomposing its derivation tree into slices.
used to decompose and encode test cases into a training Thedefinitionofasliceisasfollows:
set, and the machine learning algorithms that are used to
Definition1(Slice). AslicesisasubtreeT(cid:48)ofaderivationtree
estimate the likelihood of each test to bypass the WAF.
Finally,wedescribeML-Driven,oursearch-basedapproach
T suchthatT(cid:48) containsastrictsubsetofleavesofT.
guidedbymachinelearning.
Asliceissupposedtorepresentasubstringofanattack,
hence only subtrees of a derivation tree that contain a
3.3.1 AttackDecomposition
subset of leaves are considered to be slices. Otherwise, if
We can derive a test from the grammar by applying recur-
the subtree contains the same leaves as the derivation tree,
sively its production rules. This procedure can be repre-
therepresentedstringisnotasubstring,butthesamestring
sented as a derivation tree. A derivation tree (also called
as the derivation tree. For example, for the derivation tree
parse tree) of a test is a graphical representation of the
in Fig. 2 the subtree with the root (cid:104)sQuoteCtx(cid:105) contains all
derivation steps that are involved in producing the test.
the leaves of the whole derivation tree and, therefore, is
In a derivation tree, an intermediate node represents a
not a slice. A sample of four slices decomposed from the
non-terminal symbol, a leaf node represents a terminal
derivationtreeofthisexampleisdepictedinFig.3.Among
symbol, and an edge represents the applied production.
all possible slices of a derivation tree, we are interested in
Fig. 2 depicts the derivation tree of the boolean attack:
extractingtheminimalones,i.e.,slicesthatcannotbefurther
’ OR“a”=“a”#. In the course of generating this test, we
dividedintosub-slices:
firstapplythe(cid:104)start(cid:105)rule:
(cid:104)start(cid:105) ::= (cid:104)numericCtx(cid:105)|(cid:104)sQuoteCtx(cid:105) Definition2(MinimalSlice). Aslicesisminimalifithasonly
| (cid:104)dQuoteCtx(cid:105);
twonodes:arootandonlyonechildthatisaleaf.
andderive(cid:104)sQuoteCtx(cid:105).Wethenapplythethirdruleofthe
grammartoderive(cid:104)squote(cid:105),(cid:104)wsp(cid:105),(cid:104)sqliAtk(cid:105),and(cid:104)comment(cid:105). Theproceduretodecomposeaderivationtreeintoslices
This procedure is repeated until all non-terminal symbols is detailed in Algorithm 1. Starting from the root node
are transformed into terminal symbols. The attack string the algorithm recursively computes slices from descendant
represented by a derivation tree is obtained by concatenat- nodes by calling VISIT(child, root, S) in line 5. In line 11,
ingtheleavesfromlefttoright. the condition (root.leafs \ node.leafs) (cid:54)= ∅ ensures that
We use derivation trees to identify which substrings of onlysubtreescomplyingwithDef.1areconsidered.Inline
a SQLi attack are likely to be responsible for the attack 14, the recursion ends if the node forms a minimal slice,
being blocked or not. Specifically, an attack is divided into as defined in Def. 2, otherwise the recursion continues.

7
Algorithm1Treedecompositionintoslices. TABLE1
1: procedureDECOMPOSETREE(root) Anexampleoftestdecompositionsandtheirencoding.
2: S ←∅
3: children←root.childNodes t.id vector label t.id s1 s2 s3 s4 s5 clz
4: forallchild∈childrendo 1 (cid:104)s1,s2,s3(cid:105) B 1 1 1 1 0 0 B
5: VISIT(child,root,S) 2 (cid:104)s1,s2,s4(cid:105) B 2 1 1 0 1 0 B
6: endfor 3 (cid:104)s4,s5(cid:105) P 3 0 0 0 1 1 P
7: returnS
learning technique to predict which slices or combinations
8: endprocedure
9: procedureVISIT(node,root,S) ofslicesareassociatedwithtestsbypassingorbeingblocked
10: s←getSlice(node) (cid:46)getthesliceforwhichnodeisthe by the WAF. To be able to identify such slices, we rely on
root machine learning techniques that provide an interpretable
11: if(root.leafs\node.leafs)(cid:54)=∅then output model. That is, the reason for the classification of
12: S ←S∪s attacks into bypassing or blocked should be easily com-
13: endif
prehensible.Therefore,thoughotheralgorithmsgenerating
14: ifsisminimalthen
classificationrulescouldhavebeenusedaswell,weselected
15: return
16: else decisiontrees(DTs)forthistask.
17: children←node.childNodes ADTisatreestructurewithdecisionnodesandleaves;
18: forallchild∈childrendo adecisionnoderepresentsanattributefromadataset;each
19: VISIT(child,root,S) branchfromsuchanoderepresentsapossiblevalueforthe
20: endfor
correspondingattribute;andaleafnoderepresentsaclassi-
21: endif
ficationforallinstancesthatreachthisnode.Inourcontext,
22: endprocedure
eachdecisionnoderepresentsasliceandthebranchesfrom
For example, applying the decomposition procedure to the the node can be “0” or “1”, corresponding to whether the
derivationtreeinFig.2yieldsasetof12distinctslices. slice is absent or present. A leaf node classifies instances
We conjecture that the appearance of one or more slices into blocked or bypassing and is labelled accordingly with
in a test could result in the test getting blocked or not. In “B” or “P”. Fig. 4 shows an example decision tree learned
thenextsections,wedevelopthisideafurtherbyanalyzing fromthedatainTable1.
slices of a collection of tests and predicting, using machine The paths from the root node of the decision tree to
learning, how their appearance in the tests affect their its leaf nodes embody the combinations of slices which are
likelihoodofbypassingaWAForbeingblocked. likely to be the reason for tests to bypass or to be blocked,
dependingontheclassification.Moregenerally,wedefinea
3.3.2 TrainingSetPreparation
conceptofpathconditionas:
Given a set of tests that have been labelled with their
Definition 3 (Path Condition). A path condition represents
execution result against a WAF, that is a “P” or “B” label,
a set of slices that the machine learning technique deems to be
wetransformeachtestintoanobservationinstancetofeed
relevant for the attack’s classification into blocked or bypassing.
ourmachinelearningalgorithm.
1) Each test is decomposed into a vector of slices t i = i T n he w p h a ic t h hc v o a n l d = itio 1 n | i 0 s , r a ep n r d es k en is te t d he as n a um co b n e j r u o n f ct r i e o le n v (cid:86) an k i t ( s s l i ic = es. val),
(cid:104)s 1 ,s 2 ,...,s Ni (cid:105) by applying the attack decomposition
procedure. The procedure for computing path conditions depends
2) Eachsliceisassignedagloballyuniqueidentifier.Ifthe on the machine learning algorithm that is used to build
same slice is part of multiple tests, it is referenced by decision trees. We have selected two alternative algorithms
the same identifier. We map each unique slice to an andassessedtheiroverallimpactontestresults.
attribute(afeature)ofthetrainingdatasetformachine RandomTree.Themostprominentdifferencetoclassical
learning. decisiontreealgorithms(e.g.C4.5[42])isthatRandomTree
3) Every test is transformed into an observation of the relies on randomization for building the decision tree [15].
training data set by checking whether the slices used When selecting an attribute for a tree node, the algorithm
as attributes are present or not in the corresponding choosesthebestattributeamongstarandomlyselectedsub-
vectorofslicesofthetest. set of attributes. By choosing only subset of attributes, the
As a concrete example, let us consider three tests algorithm scales well with the size of the training data set.
t 1 ,t 2 ,t 3;thefirsttwoareblockedwhilethelastcanbypassa Inourcontext,ascalablelearnerisimportantsincethedata
WAF.Theirdecompositionsintoslicesandlabelsareshown sets contain a larger number of attributes and the decision
ontheleftsideofTable1,andtheirencodedrepresentation treeisfrequentlyrebuilt,asdescribedinSection3.3.4.
on the right side of the table. In total, we have five unique Given a decision tree and a slice vector V of a test
slices from all the tests and they become attributes of the t, we can obtain the path condition for t by visiting the
training data for machine learning. If a slice appears in a decisiontreefromtherootandcheckthepresence(value=
test,itscorrespondingattributevalueinthetrainingdatais 1)orabsence(value=0)oftheattributesencounteredwith
“1”,andotherwise“0”. respect to V. The procedure stops once a leaf is reached.
Forinstance,Fig.4presentsadecisiontreelearnedfromthe
3.3.3 DecisionTreeandPathCondition example data discussed in Table 1. For test t 1, the attribute
Bydecomposingtestsintoslicesandtransformingtheminto s 3 is present in the test’s slice vector (cid:104)s 1 ,s 2 ,s 3 (cid:105), and thus
alabelleddataset,wecannowapplyasupervisedmachine t 1 follows the left branch. Hence, the path condition is

8
Algorithm2ML-DrivenSQLiattackgeneration.
S3
1 0 1: procedureMLDRIVENGEN(initTests,outputTests)
Fig. 4. An example of a deci- 2: execute(initTests)
B 1 S5 0 siontreeobtainedfromthetraining 3: P ←initTests
datainTable1. 4: archive←UPDATEARCHIVE(P)
P B 5: //learntheinitialclassifier
6: trainData←transform(archive)
(s 3 = 1). Similarly, for test t 3 with the slice vector (cid:104)s 4 ,s 5 (cid:105), 7: DT ←learnClassifier(trainData)
the attribute s 3 is not present, thus the right branch is 8: rankTests(P,DT)
followed leading to attribute s 5, which is present in the 9: whilenot-donedo
slice vector. Therefore, the resulting path condition for t 3 1 1 1 0 : : e O xe ← cu O te F ( F O S ) PRINGSGEN(P,λ,MAXM)
is(s
3
=0∧s
5
=1).
12: archive←UPDATEARCHIVE(O)
RandomForest.Machineclassificationmethodsarewell- 13: //re-trainingtheclassifier
known to be unstable, i.e., a small change in the training 14: trainData←transform(archive)
data can result in a different classification model [51]. En- 15: DT ←learnClassifier(trainData)
semblemethodshavebeenproposedtoaddresstheissue.In 16: //newpopulation
17: P ←SELECT(P ∪O)
essence,multiplemodelsarelearnedsothattheircollective
18: endwhile
predictions can mitigate bias in individual models. In this 19: outputTests←filterBypassingTests(archive)
work,weimplementanensembleofclassifierstoguidethe 20: returnoutputTests
testgeneration,i.e.,insteadofusingonlyoneRandomTree, 21: endprocedure
weextendourtechniquetomakeuseofensemblesoftrees
produced by RandomForest [15]. However, the benefits of
RandomForest come at the cost of an increased computa- bypassingtheWAFdeterminedtheclassifierbuiltinlines5-
tionaloverhead,e.g.learninganensembleofRandomTrees 6ofAlgorithm2.Theclassifierisbuiltasfollows:(i)thetests
takes longer than learning only a single RandomTree. We are transformed into the training set (routine trainData in
evaluate in Section 5 whether the benefits justify the in- line6);(ii)aclassifierDT isthentrainedfromthedata(line
creasedoverhead. 7ofAlgorithm2).Then,individualsintheinitialpopulation
A RandomForest consists of multiple RandomTrees. To are ranked using the DT classifier (routine rankTests in
classifyanattackwithRandomForest,eachindividualRan- line8),whichassignseachindividual(test)aprobabilityof
domTreefirstclassifiestheattackandcomputesthepredic- bypassingtheWAF.
tion confidence (an estimated probability for the classifica- Inthemainloopinlines9-18,thepopulationisevolved
tion is to be correct). Then, all individual classifications are throughsubsequentiterations,calledgenerations.λnewso-
consolidated by computing the average of the prediction lutionsaregeneratedusingtheroutine OFFSPRINGSGEN in
confidence values for each class. Finally, the class with the line10.Sucharoutineselectsthebestindividuals(parents)
highestpredictionconfidenceischosenbyRandomForestas and mutates them to generate λ new individuals, called
finalclassification. offsprings. The offsprings are executed against the target
To compute the path condition for a given attack with WAF (line 11) and labelled as “bypassing” or “blocked”
RandomForest, for all trees that classify the attack as by- depending on their execution results. In line 12, the newly
passing a path condition is computed separately. Thereby, generated tests are added to an archive (line 12), which is a
thepathconditionforeachtreeiscomputedaccordingtothe secondpopulationusedtokeeptrackofalltestsbeinggen-
previouslydescribedprocedure.Theoverallpathcondition eratedacrossthegenerations[39].Then,theDT classifieris
fortheentireRandomForestis,then,theconjunctionofthe retrainedbyconvertingthearchiveintothetrainingset(line
pathconditionscomputedfromthetrees. 14)andre-applyingtheMLtraining(line15).Attheendof
each generation, a new population is formed in line 17 by
3.3.4 ML-DrivenEvolutionaryTestingStrategy selecting the fittest µ tests among parents and offsprings
according the DT classifier. The loop terminates when the
To increase the likelihood of generating bypassing attacks,
maximumnumberofgenerations(orthemaximumrunning
we propose a ML-driven evolutionary testing strategy
time)isreached(conditionnot-doneinline9).
whose pseudo-code is detailed in Algorithm 2. It combines
machine learning algorithms (either RandomTree or Ran- Therefore, the three key components of Algorithm 2
domForest) with the classical (µ+λ) Evolutionary Algorithm are: (i) the ML-driven fitness assignment; (ii) the selection
(EA), which is a population-based evolutionary algorithm operator; and (iii) the mutation operator applied for gener-
with a population size µ and a restricted number of λ ating offsprings. These key components are detailed in the
offsprings. followingparagraphs.
As any EA, Algorithm 2 starts with an initial set of ML-driven fitness assignment. In this paper, each can-
solutions (initTests) usually called population. The initial didate test t is assigned a fitness score by using machine
population can be either generated by the random attack learningalgorithms.InAlgorithm2,aclassifierDT isbuilt
generatorfromSection3.2orbyselectingtestsfromexisting at the beginning of the search (lines 6-7) at the end of each
test suites. The initial tests are executed against a target generation (lines 14-15 of Algorithm 2) using the archive as
WAF (line 2) if their execution results are not yet known training set. Such an archive is updated whenever new test
(i.e., in case of randomly generated tests). Each solution cases(either“bypassing”or“blocked”)aregenerated(lines
is assigned a fitness score according to its probability of 4, 12). To build the classifier, the archive is transformed

9
Algorithm3Offspringsgeneration slice are determined based on the root symbol of the slice
1: procedureOFFSPRINGSGEN(parents,λ,MAXM) andallproductionrulesofthegrammarthatstartwiththis
2: offsprings←∅ symbol.Forexample,takingslices 2inFig.3thatstartswith
3: while|offsprings|<λdo (cid:104)wsp(cid:105) and derives (cid:104)blank(cid:105), we obtain only one production
4: t←selectTest(parents)
rulefromthegrammar:
5: V ←getSliceVector(t)
(cid:104)wsp(cid:105)::= (cid:104)blank(cid:105)|(cid:104)inlineComment(cid:105);
6: pathCondition←getPath(V,DT)
7: s←pickASliceFrom(V) As a result, we determine only one alternative slice that
8: whiles(cid:54)=nulldo startswith(cid:104)wsp(cid:105)andderives(cid:104)inlineComment(cid:105).
9: ifsatisfy(s,pathCondition)then At the mutation step in line 10 of Algorithm 3, the pa-
10: newTests←mutate(t,s,MAXM) rameterMAXM isanintegervaluethatlimitsthenumberof
11: offsprings←offsprings∪newTests mutantsthataregeneratedfortesttandslices.Ifthenum-
12: endif
13: s←pickASliceFrom(V)
ber of alternative slices for t and s is greater than MAXM,
14: endwhile
only MAXM alternative slices are selected and used, in
15: endwhile turn, to form mutants. If the number of alternative slices
16: returnoffsprings is lower than MAX M, all available slices are used to form
17: endprocedure mutants.Therefore,atmostMAXN offsprings(mutants)are
generated from each parent t, where each offspring differs
fromitsparentinonesingle(alternative)slice.
into a training set (lines 6, 7) using the steps discussed in Motivations. Let us now explain why we decided to
Section3.3.2.Then,theclassifierDT istrainedusingeither opt for the classical (µ,λ)-EA, which is a mutation-based
RandomTree or RandomForest. Once built, DT can be used evolutionary algorithm with no crossover operator. With
to estimate the probability of a given test t to bypass the
this algorithm, MAXN offsprings are generated from one
target WAF depending on which slices appear in the three single test t via mutation only. Crossover, which is another
decompositionoft(seeSection3.3.1).
well-knowoperatorwidelyappliedinvariousevolutionary
Elitist selection. In (µ+λ)-EAs, µ parents and λ off- algorithms (e.g., genetic algorithms), is not applied here.
springs compete to form the new population of µ individ- Usually,itgeneratestwooffspringsfromapairofsolutions
ualsforthenextgeneration.InAlgorithm2,thisprocedure (parents) by randomly exchanging their genes. However,
is implemented by the routine SELECT (line 17). Once the for our problem, a crossover operator cannot be defined
fitness assignment has been performed using DT, the tests since different solutions (tests) within the same population
in the current population are ranked in descending order have different derivation trees that represent instances of
of their bypassing probability. The top µ test cases in the incompatiblederivationrulesofourgrammar.Forexample,
rankingareselectedtoformthenextpopulation. let us assume we select for reproduction two test cases t 1
Generating offsprings. The routine used to generate and t 2. The former instantiates the derivation rule (cid:104)start(cid:105)
offsprings is detailed in Algorithm 3. Given a set of µ ::= (cid:104)numericCtx(cid:105) while the latter is an instance of the rule
parents,sucharoutinegeneratesmutantsfromeachparent (cid:104)start(cid:105) ::= (cid:104)sQuoteCtx(cid:105). If we apply any crossover operator
untilreachingatotalnumberofλoffsprings(loopcondition (e.g., the single-point crossover), then the resulting two
inline3ofAlgorithm3).Ineachiterationoftheloopinlines offspringswouldviolateourgrammarsinceeachofthenew
3-15, Algorithm 3 selects the test with the highest rank as test case would contain slices from different (incompatible)
candidatetestformutation.Ifmorethanonecandidatehave derivationrules.
tiedranks,theselectionisrandomamongthem.Ifatesthas Exploration vs. Exploitation. Assuming that the total
been selected before, it will not be selected again. For each number of offsprings (λ) to generate is constant, MAXM
selected parent t (line 4), offsprings are generated starting controls how the evolutionary algorithm explores the test
from its corresponding path condition (pathCondition), space either broadly (exploration) or deeply (exploitation).
whichisdeterminedusingtheroutinegetPath(line6)from When MAXM is small, the approach generates fewer off-
theslicevectorV oftheattackt(obtainedinline5). springs per selected test, but selects more tests to mutate,
Then,offspringsaregeneratedfromaparenttbyreplac- thus exploring the test space in a broader fashion (higher
ingitsslicessinV withotheralternativeslicesaccordingto exploration). When MAXM is large, on the contrary, the
our grammar. In particular, one slice s is randomly picked approach generates more offsprings per selected test, but
from the slice vector V of the attack t (line 7) and it is selects fewer tests to mutate, thus exploring the test space
replaced with an alternative slice s(cid:48) to generate new tests in a deeper fashion (higher exploitation). In the evalua-
(routine mutate in line 10). Both s and s(cid:48) have to satisfy tion section two variants of ML-Driven are distinguished:
the given path condition. That is, they either appear in ML-Driven B(broad,withMAX
M
=10)andML-Driven
the predicate and comply with it, or do not appear in D (deep, with MAX M = 100). Section 3.4 presents a thor-
the predicate of the path condition. If s does not satisfy oughanalysisonhowtheparameterMAX M influencesthe
the path condition, it is not considered for generating mu- overalltestresults.
tants/offsprings(conditioninline9).
3.4 Enhancing ML-Driven: An Adaptive Approach to
To better explain this mutation procedure, let us con-
sider the test t 2 from Table 1 with slice vector (cid:104)s 1 ,s 2 ,s 4 (cid:105). BalanceExplorationandExploitation
According to the slices in Figure 3, the path condition for Maintaining a good balance between exploration and ex-
t 2 is (s 1 = 1); thus, we can select s 2 or s 4 and replace ploitation is extremely important for a successful applica-
them with their alternatives. Equivalent alternatives of a tion of EAs [49]. In our case, the balance is determined

10
by the parameter MAXM, which affects the number mu- Algorithm4Adaptiveoffspringsgeneration
tants (offsprings) generated from each selected test. For 1: procedureADAPTIVEOFFSPRINGSGEN(population,λ,DT)
ML-Driven D,MAXM issettoahighervalue,whichleads 2: offsprings←∅
selectingfewertestsformutation(≈λ/100),butgenerating 3: while|offsprings|<λdo
4: T ←selectAttacksForMutation(parents)
more mutants per selected test (higher exploitation). For
5: forallt∈T do
ML-Driven B,MAXM issettoalowervalue,whichleads
6: m t ←getMutationBudget(t,T,DT)
selecting more tests for mutation (≈ λ/10), but generating 7: V ←getSliceVector(t)
fewermutantsperselectedtest(higherexploration).Notice 8: pathCondition←getPath(V,DT)
that for both variants the total test budget is the same, but 9: whilem t >0do
theallocationofthetestbudgetdiffers. 10: s←pickASliceFrom(V)
A detailed analysis presented in Section 5.1, shows that 11: ifsatisfy(s,pathCondition)then
novariantissuperiorovertheother[8]:ML-Driven Dper- 12: newTest←mutate(t,s)
13: offsprings←offsprings∪newTest
formsbetteratthebeginningofthesearchbutML-Driven
14: m t ←m t −1
B outperforms it in later stages. The reason for this phe- 15: endif
nomenon is because of the number of bypassing tests se- 16: endwhile
lected and their influence on the overall performance. At 17: endfor
the beginning, there are only a few available tests with 18: endwhile
19: returnoffsprings
a high bypassing probability. Due to the higher value of
20: endprocedure
MAXM, ML-Driven D is likely to select only these tests
formutationand,thus,exploitsbettertheneighborhoodof
highly probable bypassing tests. This leads to generating of test t with λ (total number of offsprings), t is assigned
more bypassing attacks in the earlier stages of the search.
a share of the total budget proportional to its relative
Reversely, since MAXM is lower in ML-Driven B, more
bypassing probability. In other words, the number of off-
testsareselectedformutation,resultinginselectingnotonly springs/mutants to generate for each test t is proportional
thefewtestswithahighbypassingprobability,butalsotests
toitsbypassingprobabilityinrelationtotheprobabilitiesof
with a low bypassing probability. As a result, ML-Driven
allselectedparents.
Bgeneratesfewernewbypassingtests.
ML-Driven E shares the same pseudo-code with
On the other hand, after some iterations there are more
ML-Driven D and ML-Driven B with the exception of
tests with a high bypassing probability being available
the routine OFFSPRINGSGEN used to generate offsprings
for mutation. In such a scenario, selecting more tests and
in Algorithm 2. Instead of using Algorithm 3, ML-Driven
mutating each one less often helps preserving diversity:
E uses the new adaptive routine detailed in Algorithm 4,
ML-Driven B will explore the neighborhoods of multiple
which includes the proposed modification to the budget
highlyprobablebypassingtests.ML-Driven Dexploresthe
calculation.
neighborhoods of fewer tests while many other tests with
similarbypassingprobabilityremainunexplored. Similarly to Algorithm 3, Algorithm 4 generates λ off-
In this section, we propose an improved variant of springswithintheloopinlines3-18.Thedifferencesconcern
our attack generation strategy called ML-Driven E (En- (i) the number test cases selected as parents; and (ii) the
hanced).ItsgoalistocombinethestrengthsofML-Driven numberofmutants/offspringsgeneratedfromeachindivid-
BandML-Driven Dbyadaptivelyadjustingtheparameter ualparent.Inline4,theroutineselectAttacksForMutation
MAXM to better balance exploration and exploitation. We selects a set of attacks T that have the highest bypass-
propose ML-Driven E, which is a more flexible approach ing probability from all available attacks in the current
for assigning the test budget to individual tests. Instead population. All attacks above a configurable threshold σ,
of generating a fixed number of mutants per test, as done e.g., in our experiment σ=80%, are selected. The loop from
withML-DrivenB/D,thenumberofmutantsiscalculated line 5 to 17 is executed for each selected attack in T.
dynamically. The rationale of ML-Driven E is twofold: Within the loop, in line 6 the routine getMutationBudget
First, the available test budget should be allocated only calculates the number of offsprings/mutants m t to gen-
to tests with a high bypassing probability. Second, the test erate from attack t with respect to T and DT, the latter
budget should be divided amongst all tests in proportion beingtheclassifier.Inotherwords,thismethodimplements
of that probability, thus favoring those more likely to yield Equation 1. Lines 9 to 16 describe the mutation procedure
newattacks. for t, that is mostly unchanged from the original version
Giventhetotalnumberofoffspringsλtogenerate,aset of the algorithm, except that the number of generated off-
T of tests selected as parents, the probability P(t) of test springs/mutantsfortissettom t.
t to bypass the WAF, then the number of offsprings m t to Since the number of tests with a bypassing probability
generatefortesttisdefinedas: larger than 80% may vary across generations, both the
number of selected parents and the budget allocation vary
P(t)
m t = (cid:80) P(x) ∗λ (1) over time. When there are only few tests with a large
x∈T bypassingprobability(≥ σ),Algorithm4selectsonlythose
On the right-hand side, the fraction represents the relative testsasparents.Asresult,thenumberofoffspringsm t gen-
bypassing probability of t by dividing its bypassing prob- eratedfromeachparenttwillbelarge(higherexploitation).
ability with the sum of all bypassing probabilities of tests Instead, when the current population contains many tests
x ∈ T. By multiplying the relative bypassing probability with a large bypassing probability (≥ σ), the total budget

11
of µ offsprings is shared among a larger set of parents. requests,theWAFvalidatesincomingrequestsintwosteps:
As a consequence, fewer mutants will be generated from First, the values in a request are validated with respect
each parent (higher exploration). Therefore, Algorithm 4 to data types (e.g., string or numeric) and boundary con-
adaptivelybalancesexplorationandexploitationdepending straints, e.g., a credit card number is expected to be a
on the number tests in the current population that have a sequence of 16 to 19 digits. In a second step, each value is
bypassingprobabilitygreaterthanσ. checked to make sure that it does not contain known mali-
ciousstringpatterns(i.e.,usingaSQLiblacklist)commonly
used in attacks. Only if the request passes both validation
4 EMPIRICAL STUDY
stepstherequestisforwardedtotheback-endservices.
Thissectionevaluatestheproposedtestingstrategiesintwo
The computation time required to evaluate all testing
separate case studies: a popular open-source WAF and a
strategies with the proprietary WAF is highly expensive
proprietary WAF that protects a financial institution. Sec-
because of (i) the slow responsive time of the web ser-
tion 4.1 introduces the case studies. Section 4.2 formulates
vices, (ii) the number of testing strategies to compare, and
the research questions. Section 4.3 explains the procedure
(iii) the number of repetitions to perform for each testing
we followed to execute the experiments while Section 4.5
strategy. Therefore, for the experiment we used of a high-
describestheexperimentvariables.
performance cluster [2] when testing the proprietary WAF.
Furthermore, we had to optimize a replica of the test en-
4.1 SubjectApplications vironment to significantly decrease response times when
4.1.1 Open-SourceWAF invokingservices.
In our optimized test environment, all configurations
In this case study, the firewall under test is ModSecurity,
related to request filtering, that is whether a request is
which implements the OWASP core rule set. ModSecurity
blocked or let through, are copied. Other configurations,
is an open-source web application firewall that can be
e.g. logging or encryption, are disabled. The web appli-
deployed with the Apache HTTP Server to protect web
cation under protection is replaced by a simple mock-up
applications hosted under the server. Depending on the
application, which implements the same interface as the
applications under protection, different firewall rule sets
originalapplicationunderprotection.Themock-upreplays
definedfordifferentpurposescanbeused.TheOWASPcore
a set of recorded responses from the original application
rules target various kinds of attacks, e.g. Trojan, Denial of
and, thus, the WAF remains unaffected. Table 2 shows the
Service,andSQLInjection,andaremaintainedbyanactive
message round trip time (RTT) per operation computed
communityofsecurityexperts.
over a time span of 30 days with the actual environment
ThewebapplicationsunderprotectionareHotelRS,Cy-
clos, and SugarCRM. HotelRS is a service-oriented based
(RTT ACT) compared to the optimized environment on the
system,providingwebservicesforroomreservation.Itwas
HPC(RTT HPC).Aswecansee,thetimehasbeenreduced
significantly. Note that, even with these optimizations, the
developedandusedin[16].Cyclosisapopularopen-source
total computation time of our experiments is equivalent to
Java/Servlet Web Application for e-commerce and online
8years,337days,and12hoursonasingleCPUcore.
payment5. SugarCRM is a popular customer relationship
Even though an optimized test environment is required
management system6. SugarCRM and Cyclos have been
from an experimental standpoint, in practice, testing the
widelyusedinpractice.Inourexperimentsetting,thethree
firewall is just a single test activity in an array of test
applicationsaredeployedonanApacheHTTPServerunder
activities (e.g., testing the WAF, services, front-end). Given
Linux. ModSecurity is embedded within the web server; it
timeandresourceconstraints,creatingandmaintainingtest
protects the application’s web services from SQLi attacks.
environmentsthatarespecificforeachsingletestactivityis
Specifically, since these web services receive SOAP mes-
verycostly.Basedonourexperience,wefoundthattesten-
sages7 from web clients, a malicious client can seed a SQLi
gineersprefertotestcopiesoftheactualWAFconfiguration
attackstringintoaSOAPmessageandsubmitittotheweb
andservices.
servicesinordertogainillegalaccesstodataorfunctionality
Since we, by design, optimized our test environment
ofthesystem.
to enable large scale experiments, the test execution times
Inthispaper,notethatourtestingtargetistheWAFthat
in our experimental setting is not representative of test
protectstheapplications,nottheapplicationsthemselves,as
executiontimesintheactualenvironment(seeTable2).This
our focus is on testing firewalls. HotelRS, SugarCRM, and
isaproblemasitbiasestheresultsofourexperimentstothe
Cyclos play solely the role of a destination for SQLi tests
advantageofapproachesthatarelessexpensiveintermsof
thatbypasstheWAF.
test case generation but lead to the execution of more test
cases, such as random testing. Therefore, in our analyses,
4.1.2 ProprietaryWAF
we transform the time scale of the optimized environment
In the industrial setting, we evaluate our approach on a
into a realistic one, accounting for the actual test execution
proprietaryWAFthatisusedinacorporateITenvironment
timesinpractice.
to protect back-end web services. These services are the
Assume T = {t 1 ,...,t n } is a set of timestamps mea-
backbone of a financial corporation and process thousands
sured on the experimental environment, such that one
of transactions daily. To provide protection from malicious
timestamp is noted after the execution of every test. Then,
5.http://project.cyclos.org for the i-th test case execution, f(t i ) = t i + (RTT ACT −
6.http://sourceforge.net RTT HPC ) ∗ i transforms a timestamp t i ∈ T into the
7.http://www.w3.org/TR/soap12-part1 correspondingtimestampintheactualenvironment(f(t i )).

12
TABLE2 comparison of the techniques by comparing the number of
Averageresponsetimeinmillisecondsofsomewebserviceoperations bypassingattacksfoundbyeachtechnique.
inourexperimentalenvironmentcomparedtothecasestudy’s
environment.
RQ4: Are we learning new, useful attack patterns as the
Op.1 Op.2 Op.3 Op.4 numberofdistinct,bypassingattacksincreases?
RTTHPC 11,36 11,39 11,46 16,61
RTTACT 456,56 180,02 302,09 854,63
RQ4 assesses whether, as we find more bypassing tests,
we also identify more attack patterns that can be use-
ful to improve the rule set of the WAF. In our con-
Wewillusethelattertimescaletocompareteststrategiesin
text, an attack pattern is the underlying root cause that
arealisticfashion.
enables an attack to bypass the WAF. For example, the
attacks union *!50000*select pwd from user and
4.2 ResearchQuestions
union *!50000*select 99 share the pattern union
*!50000*select (root cause) while the remainder of the
This work investigates several variants of a machine
attacks differ. We want to investigate whether identifying
learning-driventestingstrategyandarandomtestingstrat-
successful attack patterns help understanding why attacks
egy. We compare and evaluate all these strategies for their
arebypassingandeventuallyfixtheWAFtocorrectlydetect
capability of finding bypassing attacks on both subject ap- furtherattacks.FortheML-Driventechniques,suchapat-
plications,i.e.ModSecurityandtheproprietaryWAF.
ternischaracterizedbyapathcondition(seeDef.3).Apath
Since all testing strategies generate attacks from the condition characterizes the slices, or combination of slices,
same input space, i.e. the grammar introduced in section that are likely causing an attack to bypass. Thus, a path
3.1, we evaluate how efficient the different strategies are in condition represents a pattern that is not correctly detected
sampling the input space for bypassing attacks. Therefore, bytheWAF.
wemeasureforeachstrategyhowmanydistinctbypassing To answer RQ4, we measure how many path condi-
attacksarefoundovertime. tions can be extracted from a model that is learned by the
ML-Driven techniques. More specifically, we analyze the
RQ1: How efficient are ML-Driven E, ML-Driven
growth in the number of path conditions as the number of
B,ML-Driven D,andRANinfindingbypassingtests?
successful,distinctattacksgrowsovertime.
Toassesstheimpactofthemachinelearningalgorithms
4.3 Procedure
on the test result, we implemented two alternative classi-
fiersforeachoftheML-Drivenstrategies:RandomTreeand Weimplementedthetechniquesproposedinthisworkinto
RandomForest. As detailed in Section 3.3.3, both algorithms our SQLi testing tool called Xavier. Xavier supports the au-
have complementary advantages and drawbacks. In brief, tomatedtestingofwebservicesforSQLivulnerabilitiesand
RandomForest is an ensemble classifier and, hence, is ex-
hasbeendescribedin[10].ML-Drivengeneratestestcases
pected to be more robust against changes in the training
intheformofSQLiattackstrings,suchas’ OR“1”=“1”#.
set than RandomTree. However, RandomForest comes at a To generate malicious requests, Xavier takes such attack
higher computational cost than RandomTree, since multiple stringsandinjectsthemintosampleSOAPmessages,which
models have to be learned. To assess the influence of both are subsequently sent to an application under test. Xavier
algorithmsonourapproach,werunML-Drivenwithboth therefore relies on sample SOAP messages as inputs. They
algorithmsandcomparethenumberofidentifiedbypassing can be taken from existing web service test suites, or can
attacksandpathconditionsinagiventimebudget. easily be generated from the WSDL8 that describes the
serviceinterfaceundertest.
RQ2: Does the choice of machine learning algorithm In our experiments, when available, we use SOAP mes-
matter? sagesfromthefunctionaltestsuiteoftheserviceundertest
(Cyclos and our industrial case study) or, otherwise, we
manuallycreateSOAPmessagesfromtheWSDLs(HotelRS,
We evaluate whether, in our context, the benefits of
SugarCRM).Eachofthesemessagesconsistsofanumberof
the RandomForest compared to the RandomTree justify
parameters and their legitimate values, which the services
the increased computation overhead to learn the classifier.
expect and that the WAF has to let through. In our testing
Therefore,wecomparehowmanybypassingtestsarefound
process,eachSOAPmessageisconsideredseparately.Atest
overtimewiththesetwoalgorithms.Inaddition,weassess
generation technique, ML-Driven or RAN, continuously
whether the algorithms have an impact on the stability
generates attacks, injecting one attack each time into a
of the test result, i.e., we compare the variation among
parameter of the selected SOAP message to create a new
repetitionsofthesametestrun.
SOAPmessage,andthensendsittothewebserver.
Incoming SOAP requests to the web server are first
RQ3: How does ML-Driven compare to similar tech-
treatedbytheWAFandonlythosethatcomplywithfirewall
niques?
rulesareforwardedtowebapplications,andotherwiseare
blocked. In case a request is blocked, the WAF replies to
RQ3 compares our proposed technique with existing
techniques for testing WAFs. We perform a quantitative 8.http://www.w3.org/TR/wsdl

13
the client that issued the request with a special response, Forest,weusedtheirimplementationsavailableinWeka[28]
stating that the request has been denied. When our testing withthedefaultparametervalues.
tool, Xavier, receives such a response, it marks the test, Numberofrepetition.Toaccountfortherandomization
embedded in the original request, with a blocked label “B” involved in the testing techniques (e.g., RAN), each algo-
(forblocked),andotherwiseapassedlabel“P”(bypassing). rithmwasrun10timesforeachsubjectapplication.
4.4 ParameterSetting
4.5 Variables
For the ML-Driven approaches, there are various param-
The following dependent variables are controlled or mea-
eters to set for both the machine learning algorithms and
(µ+λ)-EA. For most of the parameters (e.g., machine learn- suredinourexperiments:
ing training setting), we follow the recommendations from • D t: The number of distinct tests that can bypass
theliterature[15],[28],[41].Moreover,weusedatrial-and- a target WAF at time t is a way to measure the
error procedure to calibrate the parameters µ and λ. The efficiency of a test strategy. Note that, given two
finalparametervaluesareasfollows: distinct tests in the same attack category, one might
Population size (µ). Typically, the population size for be caught by the WAF while the other bypasses it.
EAs can vary from tens to several thousands of individ- Thismaybecausedbytestsinacategorythatshould
uals [41]. The best setting for this parameter depends on behandledbydifferentrules,someofthemmissing
the nature of the problem and on the size of the search or incorrect in the current WAF rule set, or by an
space [31]. In our case, the population size determines identical rule that is not general enough to block all
the number of tests that will be preserved for the next testsinacategory.Therefore,identifyingsimilarbut
generation. A small population size may lead to loss of distinct bypassing tests is useful to identify attack
test cases with large bypassing probability, thus reducing patterns.
the chances of generating new attacks able to pass through • D pc:Thenumberofdistinctpathconditionsthatcan
the WAF. From our preliminary experiments, we observed beextractedfromdecisiontrees.Eachpathcondition
that a population size of 500 individuals works best for characterizesastringpatternthatagroupofbypass-
ML-Driven since it helps preserving as many as possible ingattackshasincommon.Suchstringpatternscan
probablebypassingattacks. beaddedtotheWAFrulestopreventfurtherattack
Number of offsprings (λ). In ML-Driven, newly gen- attemptscontainingthesamepattern.Hence,D pc is
eratedoffsprings(testcases)areusedtoupdatethearchive, a measure for how many attack patterns have been
which is later used to retrain the classifier DT by applying uncovered.
eitherRandomTreeorRandomForest.Therefore,offspringsare
theadditional“datapoints”thatareusedforupdatingDT. Foreachsubjectapplication,weraneachtestingstrategy
A large λ value means that in each generation a significant 10timesandcollectedthenumberofdistinctbypassingtests
portion of the training set consists of new test cases; a
(D t)anddistinctpathconditions(D pc)ineachrun.Tothis
small λ value leads to retraining DT with almost the same
aim,everytimeanewtesttwasgenerated,wecollectedthe
training set (i.e., updating DT would be less effective). In passing wall-clock time since the beginning of the search
thispaper,wesetλ=4000toguaranteethatDT isalways and then executed t to see whether or not it could bypass
retrained with a large portion new test cases. While the the WAF. Therefore, we can compare the values of D t and
total number offsprings is fixed, the number of offsprings D pc collectedovertime.
generated from each test t differs for the three variants of To verify whether D t scores significantly differ when
ML-Driven. For ML-Driven B and ML-Driven D, it is using two different testing strategies (e.g., RAN and
fixed and it is equal to MAXM = 10 and MAXM = 100, ML-Driven E), we used the Wilcoxon test with a signifi-
respectively. In ML-Driven E, the number of offsprings
cancelevelofα=0.05.TheWilcoxontestisanon-parametric
test and, thus, does not require the data to be normally
for each test is determined dynamically using the adaptive
distributed. For the statistically analysis, we collected the
strategydescribedinSection3.4.
Archive size. The archive keeps track of all attacks D t scores achieved by each alternative testing approach
after intervals of 35 minutes for each repetition, resulting
generated across the generations and it is used at the end
infivetimewindowsforeachrun.
of each generation as training set for machine learning. To
avoid exceeding the resources of a typical laptop and to
finish in a reasonable time we limit the training set to 6000 5 RESULTS
blocked attacks and 6000 bypassing attacks. If the number
In this section, we describe the results obtained in our
of tests in the archive is larger, we consider only the most
casestudiesregardingtheresearchquestionsformulatedin
recenttests,i.e.,thoseproducedinlatestgenerations.
Section4.2.
Stopping condition. The search terminates when the
maximum search budget of 175 minutes is reached for
5.1 RQ1: How efficient are ML-Driven E, ML-Driven
ModSecure. For the proprietary WAF, we used a larger
B,ML-Driven D,andRANinfindingbypassingtests?
search budget of 500 minutes. To allow a fair comparison,
RANwasconfiguredwiththesamestoppingcondition. To answer RQ1, we applied the testing techniques to both
Machine learning setting. For the machine learning subject applications and measured how many bypassing
algorithmsusedinthispaper,i.e.,RandomTreeandRandom- testswerefoundovertime(D t).Inparticular,wecompared

14
1000
800
600
400
200
0 0 35 70 105 140 175
Time (minutes)
D t
1400
ML-Driven E
ML-Driven B
1200
ML-Driven D
RAN
1000
800
600
400
200
0
0 35 70 105 140 175
Time (minutes)
Fig. 5. Average number of bypassing tests (Dt) found for nine tested
operations(10repetitionseach)forModSecurity.
theperformanceofthetechniquesbasedonthecumulative
number of distinct bypassing tests generated over time. In
the following, we discuss the results for ModSecurity and
theproprietaryWAFseparately.
5.1.1 ResultsforModSecurity
For the open-source WAF, we randomly selected nine pa-
rameters in total for testing, three parameters from each
webapplication(HotelRS,SugarCRM,andCyclos).Foreach
technique, Fig. 5 depicts the average number of distinct,
bypassing tests generated over time for ModSecurity mea-
suredwithinintervalsoffiveminutes.Thetestingresultsfor
eachindividualparameterareinatechnicalreport[8].Fig.6
depictsthesamedataasboxplotstohelpvisualizestatistical
variationacrossthe10repetitions.Table3reportstheresults
oftheWilcoxontestbylisting,ineachcell,theteststrategies
thataresignificantlyoutperformedbythestrategymatching
thecorrespondingcolumn.
The first observation is that all techniques can generate
tests that bypass the WAF, suggesting that the WAF does
notprovidecompleteprotectionfromSQLiattacks,putting
online systems under its protection at risk. Further, by ob-
servingexecutedSQLstatementsonthedatabase,wefound
that these bypassing tests can exploit SQLi vulnerabilities
in HotelRS and SugarCRM. Second, the sharply increasing
plots corresponding to ML-Driven E, ML-Driven B and
ML-Driven D indicate that they are much more efficient
thanRAN,thebaselineforcomparison.Overall,theresults
show that the ML-Driven techniques outperform RAN by
an order of magnitude with respect to the number of dis-
tinct bypassing tests generated. The Wilcoxon test revealed
thatthesedifferenceswerealwaysstatisticallysignificantas
depictedinTable3(p-values<0.01).
Among the machine learning-driven techniques,
ML-Driven E constantly finds the most bypassing tests
compared to ML-Driven B and ML-Driven D, which
suggests that the adaptive budget allocation works
well. The differences between ML-Driven E and its
predecessors are always statistically significant in all the
five time windows. One issue with ML-Driven D/B is
that at the beginning of the test run, ML-Driven D finds
D t
ML-Driven E
ML-Driven B
ML-Driven D
RAN
Fig.6.Statisticalvariationforthenumberofbypassingtestsfound(Dt)
acrossalltestedparametersforModSecurity.
TABLE3
ResultsoftheWilcoxontestforModSecure.Foreachtestingstrategy
(e.g.,ML-E)wereportwhetheritstatisticallyoutperformstheits
counterparts(e.g.,RAN)whenp-values<0.01.
TimeWindow RAN(p<0.01) ML-B(p<0.01) ML-D(p<0.01) ML-E(p<0.01)
35min RAND RAND RAND
ML-B ML-B
ML-D
70min RAND RAND RAND
ML-B
ML-D
105min RAND RAND RAND
ML-B
ML-D
140min RAND RAND RAND
ML-D ML-B
ML-D
175min RAND RAND RAND
ML-D ML-B
ML-D
more bypassing tests, while this is the opposite later
in the test run. More specifically, after a time window
of 35 minutes ML-Driven D is statistically superior to
ML-Driven B while between 70 and 105 minutes the two
ML-Driven approaches are statistically equivalent; finally,
in the last two time windows (i.e., 140 and 175 minutes),
ML-Driven B statistically outperforms ML-Driven D.
Since both techniques implement the same algorithm,
this phenomenon can be attributed to a difference in the
choiceofparameters,or,moreprecisely,theparameterthat
determines the number of mutants generated per test (a
detailedanalysisisprovidedinatechnicalreport[8]).While
ML-Driven D and B generate a fixed number of mutants
per test, ML-Driven E adjusts the number of mutants in
proportion to the test’s bypassing probability. As a result,
ML-Driven E spends the test budget more efficiently and
findsbypassingattacksfaster.
TheplotsfortheML-Driventechniquesarealsoslightly
oscillating, thus depicting the effect of iterative re-training
of the classifier. The flat segments match the time intervals
where the classifier is recomputed and no new tests are
generated.Theslopesoftheplotstendtodecreaseovertime
as it becomes increasingly harder to find new bypassing
teststhathavenotyetbeenexecuted.

15
14000
12000
10000
8000
6000
4000
2000
0 0 125 250 375 500
Time (minutes)
D t
40000
ML-Driven E
ML-Driven B 35000
ML-Driven D
RAN
30000
25000
20000
15000
10000
5000
0 0 125 250 375 500
Time (minutes)
Fig.7.Averagenumberofbypassingattacks,proprietaryWAF,alltested
parameters.
5.1.2 ResultsfortheproprietaryWAF
We now address RQ1 for the second subject application,
theproprietaryWAF.AsforModSecurity,alltechniquesare
evaluatedmeasuringthenumberofbypassingteststhatare
foundovertime.
Due to the considerably higher complexity of the WAF
in the industrial case study, we selected a higher number
of parameters for testing. Given that all testing strategies
have to be applied to each parameter and each test run
was repeated 10 times, testing all parameters would have
been infeasible. Therefore, we selected one parameter for
each distinct data type in the WSDL of the services under
test,whichresultedinatotalof75parameters.TheWAFin
thiscasestudydeterminestheinputvalidationroutinetobe
executed for a parameter based mainly on the correspond-
ing data type; hence selecting one parameter per data type
maximizesthecoverageofinputvalidationroutines.
Out of the 75 tested parameters, bypassing tests could
be generated for 29 parameters. Each testing technique
was able to generate bypassing tests for all of these 29
parameters. Fig. 7 depicts the average number of distinct
bypassing tests per test strategy. The average is computed
fromalltestedparametersand10repetitionsperparameter.
Outofalltechniques,ML-Driven Egeneratesthemost
bypassingtestsonaverage,followedbyML-Driven Band
ML-Driven D. RAN finds the least bypassing tests. Since
the statistical variation in the plots is high (see boxplot in
Fig.8),weseparatetheparametersintogroupstobetteran-
alyzetheresults.Parametersinthesamegroupsharesimilar
input constraints in terms of number of allowed characters
and tend to produce a similar number of bypassing test
cases.ItisworthnoticingthatthisparticularWAFconsiders
not only such input constraints but also other criteria (e.g.,
SQLi blacklist). Therefore, parameters in a same group do
not necessarily produce the same results. Table 4 shows
the groups: Group 1 has two parameters that share an
input constraint that restricts the number of characters to a
maximumofeight.Similarly,Groups2,3,and4havesimilar
constraints with 16, 25, and 35 characters, respectively. For
each group, Table 5 reports the results of the Wilcoxon test
whencomparingthenumberofbypassingattacksgenerated
D t
ML-Driven E
ML-Driven B
ML-Driven D
RAN
Fig.8.Boxplotsofthenumberofbypassingtests,alltestedparameters,
proprietaryWAF.
2500
2000
1500
1000
500
0
0 125 250 375 500
Time (minutes)
D t
ML-Driven E
ML-Driven B
ML-Driven D
RAN
Fig.9.Group2:Averagenumberofbypassingattacks,proprietaryWAF,
7parameters.
bythedifferenttestingstrategies.
According to Table 5, we observe that for Groups 2, 3,
and 4 ML-Driven E is always significantly superior to its
predecessoraswellastoRAN.However,lookingatFig.9-
11 we notice the following trend: the more bypassing tests,
the smaller the difference in test results across ML-Driven
techniques.Forexample,ML-Driven Egeneratesonaver-
age +25% bypassing attacks compared to the second best
approachinthecomparison(i.e.,ML-Driven B)forGroup
2. For Group 3, the gap between ML-Driven E and the
closestalternativeapproach(i.e.,RAN)is+30%onaverage.
ForGroup4,theaveragedifferencebetweenML-Driven E
anditspredecessorislowerthan10%.
The average number of bypassing tests for the two
TABLE4
Groupsofparameterswithasimilarinputconstraint.
#Parameter InputConstraint
Group1 2 Upto8Char.
Group2 7 Upto16Char.
Group3 8 Upto25Char.
Group4 12 Upto35Char.

16
10000
8000
6000
4000
2000
0
0 125 250 375 500
Time (minutes)
D t
ML-Driven E
ML-Driven B
ML-Driven D
RAN
Fig. 10. Group 3: Average number of bypassing attacks, proprietary
WAF,8parameters.
25000
20000
15000
10000
5000
0
0 125 250 375 500
Time (minutes)
D t
45
40
35
30
25
20
15
10
5
0
0 125 250 375 500
Time (minutes)
ML-Driven E
ML-Driven B
ML-Driven D
RAN
Fig. 11. Group 4: Average number of bypassing attacks, proprietary
WAF,12parameters.
parametersinGroup1isdepictedinFig.12.Alltechniques
tend to saturate after about 125 minutes and, after that,
the number of bypassing tests increases very slightly. RAN
is the most effective approach, significantly outperforming
all ML-Driven variants after 105 minutes of running time
(see Table 5). At the end of the search, RAN reaches up to
approximately 40 bypassing tests while all the ML-Driven
techniquesfindaround30bypassingtests.Themostpromi-
nent difference of this group, as compared to the others, is
that very few bypassing tests are found. This is due to the
factthatthenumberofallowedcharactersisonlyeight,thus
resultinginasmallnumberofattackstobypass.Examining
thetrainingsetsusedtolearntheclassifiersmoreclosely,we
findthatthetrainingsetsareheavilyimbalanced.Thereare
only between 15 and 30 bypassing attacks compared to up
to6000blockedattacks,i.e.,theyrepresentonly0.25%-0.5%
of the data points in the training set. For the other tested
parameters, where the machine-learning driven techniques
outperform RAN, there are typically several hundreds of
bypassingattacksinatrainingset.Asaresultoftheimbal-
ancedtrainingdata,thelearnedclassifierhasalowrecall(≈
80%)andislessaccurateinpredictinganattack’sbypassing
D t
ML-Driven E
ML-Driven B
ML-Driven D
RAN
Fig. 12. Group 1: Average number of bypassing attacks, proprietary
WAF,2parameters.
probability. RandomTree and RandomForest tend to generate
a constant classifier in such a scenario, i.e., the resulting
classifierlikelylabelsalldatatestsas“blocked”becausethis
leadstoaverylowclassificationerror(<1%).
Moreover, if we analyze the training sets used in con-
secutive retraining iterations (generations), we find that
there are not substantially more bypassing attacks added
to the training set. The quality of the classifier does not
improve over the subsequent generations and is hardly
worth the computation time necessary for retraining. To
address this shortcoming, we conclude that the classifier
shouldonlyberetrainedifthetrainingdatahassufficiently
improved.Otherwise,theexistingclassifiermaybeusedto
generate more offsprings until more bypassing attacks are
found or the test budget is exceeded. In addition, in the
presence of high imbalanced training sets, we may apply
variouswell-knownstrategiesinmachinelearning,suchas
datare-samplingstrategies,weightedtraining,andpenalty-
based training. Investigating the best strategy to address
theimbalanceproblemforML-Drivenispartofourfuture
agenda.
5.2 RQ2: Does the choice of machine learning algo-
rithmmatter?
To answer RQ2, we run ML-Driven E with the chosen
machinelearningalgorithms,namelyRandomTreeandRan-
domForest, and we compare the results. For this analysis,
wefocusonML-Driven Eonlysinceitisthemostefficient
variantofML-Drivenaccordingtotheresultsdiscussedin
Section5.1.Theevaluationisperformedontheopen-source
casestudy(ModSecurity)inthesamefashionasforRQ1.
Fig. 13 shows the average number of bypassing tests
for nine selected parameters and 10 repetitions. The re-
sultindicatesthatML-Driven EwithRandomForestfinds
slightlymorebypassingteststhanML-Driven EwithRan-
domTree. However, the difference is not practically signif-
icant. The advantage of using a more stable classifier is
partially lost due to the increased computation time for
constructing this classifier. Therefore, although Random-
Forest may generate a more accurate/stable classifier than

17
TABLE5 1200
ResultsoftheWilcoxontestfortheproprietaryWAF.Foreachtesting
strategy(e.g.,ML-E)wereportwhetheritstatisticallyoutperformsits
counterparts(e.g.,RAN)aswellthecorrespondingp-values. 1000
Group TimeWindow RAN ML-B ML-D ML-E 800
35min ML-D(p=0.01)
70min ML-D(p=0.01) ML-D(p=0.03) RAND(p<0.01)
105min ML-B(p=0.03) ML-D(p=0.04)
ML-D(p=0.01) 600
ML-E(p<0.01)
140min ML-B(p<0.01)
ML-D(p<0.01)
1 ML-E(p<0.01) 400
175min ML-B(p<0.01)
ML-D(p<0.01)
ML-E(p<0.01)
35min ML-D(p<0.01) RAND(p<0.01) R M A L N -B D ( ( p p < < 0 0 .0 .0 1 1 ) ) 200
ML-D(p<0.01)
70min ML-D(p<0.01) RAND(p<0.01) RAND(p<0.01)
ML-B(p<0.01)
ML-D(p<0.01) 0 0 35 70 105 140 175
105min ML-D(p<0.01) RAND(p<0.01) RAND(p<0.01) Time (minutes)
2 ML-B(p<0.01)
ML-D(p<0.01)
140min ML-D(p<0.01) RAND(p<0.01) RAND(p<0.01)
ML-B(p<0.01)
ML-D(p<0.01)
175min ML-D(p<0.01) RAND(p<0.01) RAND(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
35min ML-B(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
70min ML-B(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
105min ML-B(p<0.01) RAND(p<0.01)
3 ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
140min ML-B(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
175min ML-B(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
35min RAND(p<0.01) RAND(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
70min RAND(p<0.01) RAND(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
105min RAND(p<0.01) RAND(p<0.01) RAND(p<0.01)
4 ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
140min RAND(p<0.01) RAND(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
175min RAND(p<0.01) RAND(p<0.01) RAND(p<0.01)
ML-D(p<0.01) ML-B(p<0.01)
ML-D(p<0.01)
RandomTree, its overhead negatively affects the number
of generations (i.e., the number of tests to run against the
WAF) that can be performed within the same amount of
time (search budget). In other words, the gain in accuracy
when using RandomForest does not compensate its over-
head when used inside the test case generation loop. Even
if less precise, RandomTree enables more iterations and an
increasednumberofnewtestexecutions.
Fig.14showsasampleboxplotcorrespondingtotheob-
servedstatisticalvariationforonerepresentativeparameter
over 10 repetitions. We can see that the variation is small
and similar for RandomForest and RandomTree. Similar
results are observed for the other parameters. Therefore, to
conclude, the choice between the two considered machine
learning algorithms has no significant impact with respect
to the number of bypassing tests or the degree of variation
amongrepetitions.
5.3 RQ3: How does ML-Driven compare to similar
techniques?
To answer RQ3, we compare our proposed technique
ML-Drivenwithsimilartools.Thetoolsconsideredinthis
comparisonarechosenaccordingtothefollowingselection
criteria: Similar objective as ML-Driven, i.e., finding SQLi
stset
gnissapyB#
ML-Driven E (Forest)
ML-Driven E (Tree)
Fig.13.ComparisonoftheRandomTreeandRandomForestclassifier.
Averagenumberofbypassingtestsfoundforninetestedoperations(10
repetitionseach)inModSecurity.
1400
1200
1000
800
600
400
200
0 0 35 70 105 140 175
Time (minutes)
stset
gnissapyB#
ML-Driven E (Forest)
ML-Driven E (Tree)
Fig. 14. Boxplots for the number of bypassing tests found with one
representativeparameter(get-relationships)inModSecurity.
attacks that bypass a WAF under test; state-of-the-art cov-
ering a range of SQLi attacks and obfuscation methods;
widely used or developed by known institutions or secu-
rity experts. Following these criteria, we selected the WAF
TestingFrameworkandSqlMapforcomparison.
The WAF Testing Framework9 tests the attack detection
capabilities of a WAF under test. It is a state-of-the-art
tool developed by Imperva, which is the developer of a
proprietary WAF and several other security solutions. The
toolcomeswithanumberofmaliciousHTTPrequeststhat
containcommonSQLiattacks.TotestaWAF,itsubmitsthe
HTTP requests one by one to the WAF and checks if the
maliciousrequestsareblockedcorrectly.
SqlMap10 is a well-known penetration testing tool to
detectSQLivulnerabilitiesinwebapplicationsandservices.
It generates a large and diverse set of SQLi attacks, which
cover all common SQLi attack techniques. To evade de-
tection of WAFs, SqlMap uses several tamper scripts. Each
9.Downloadedfrom
https://www.imperva.com/Resources/FreeEvaluationTools
10.Version1.0.7.42downloadedfromhttps://sqlmap.org

18
TABLE6
TamperscriptsofSqlMapselectedforourexperiments.
TamperScriptName ShortDescription
between.py InsertsaclausewiththeSQLkeywordBETWEEN
commalesslimit.py Replacesinstanceslike’LIMITM,N’with’LIMITNOFFSETM’
commalessmid.py Replacesinstanceslike’MID(A,B,C)’with’MID(AFROMBFORC)’
concat2concatws.py Replacesinstanceslike’CONCAT(A,B)’with’CONCAT_WS(MID(CHAR(0),0,0),A,B)’
equaltolike.py Replacesalloccurrencesofoperatorequal(’=’)withoperator’LIKE’
greatest.py Replacesgreaterthanoperator(’>’)with’GREATEST’counterpart
halfversionedmorekeywords.py AddsversionedMySQLcommentbeforeeachkeyword
ifnull2ifisnull.py Replacesinstanceslike’IFNULL(A,B)’with’IF(ISNULL(A),B,A)’
informationschemacomment.py Addsacommenttotheendofalloccurrencesof"information_schema"identifier
lowercase.py Changeseachkeywordcharactertolowercase
modsecurityversioned.py SurroundstheattackstringwithaMySQLversion-specificcomment(randomlygeneratedversionnumber)
modsecurityzeroversioned.py SurroundstheattackstringwithaMySQLversion-specificcomment(versionnumbersetto0)
multiplespaces.py AddsmultiplespacesaroundSQLkeywords
randomcase.py ChangesrandomlythecaseoflettersinaSQLkeyword
randomcomments.py AddrandomcommentstoSQLkeywords
unionalltounion.py ReplacesUNIONALLSELECTwithUNIONSELECT
uppercase.py Changeseachkeywordcharactertouppercase
versionedmorekeywords.py Surroundseachkeywordwithaversion-specificMySQLcomment
TABLE7 how computation intensive these experiments are, we test
ResultsfortestingtheproprietaryWAFwiththe onlyarepresentativeparameterofeachgroupandinterpret
WAFTestingFrameworkandSqlMap.
the result as a performance indicator for the other parame-
tersinthesamegroup.Table7reportsforbothtoolsthetotal
WAFTestingFramework SqlMap
Parameter #TC
Total
#TCBypass #TC
Total
#TCBypass numberofgeneratedtestcases(TC Total)andthenumberof
Group1 19 0 3283.9 0.0 test cases bypassing the proprietary WAF (TC Bypass). The
Group2 19 0 3281.6 0.0 WAFTestingFrameworkexecutesforeachtestedparameter
Group3 19 0 3278.9 0.3
19testcases.ForthetestedparameterofGroup4,threeofthe
Group4 19 3 3260.5 66.5
19attacksarebypassing.Forallothertestedparameters,the
WAF Testing Framework does not find a bypassing attack.
SqlMap generates a similar number of test cases for each
tamper script applies a specific obfuscation method to a
tested parameter (on average between 3260.5 and 3283.9
SQLi attack (e.g. randomly changes the case of letters
test cases). For the parameter of Group 4, SqlMap finds
in a SQL keyword). Since some tamper scripts are only
on average 66.5 bypassing attacks and for the parameter
meanttobeappliedwithparticularWAFs,webapplication
of Group 3, SqlMap finds on average only 0.3 bypassing
frameworks (e.g. ASP or PHP), or database management
attacks.Fortheotherparameters,SqlMapdoesnotfindany
systems, we selected a number of tamper scripts that are
bypassingattacks.
applicabletooursubjectapplications(i.e.,applicabletothe
proprietaryWAF/ModSecurity,SOAPwebserviceswritten The fact that both tools find the most bypassing attacks
in PHP/Java, and MySQL). Table 6 lists the tamper scripts for Group 4 can be explained with the fact that the input
selectedforourexperimentsandgivesabriefdescriptionfor length constraint for this group is the least strict (refer to
each.NotethatSqlMapdoesnotreporthowmanyorwhich Table4).Thisalsoconfirmsthetrendobservedintheresults
attacks bypassed a WAF under test. Therefore, we routed for ML-Driven, which found the most bypassing attacks
the HTTP traffic between SqlMap and the WAF under test forGroup4aswell.Fortheothergroups,theWAFTesting
through a custom HTTP proxy, which determines whether Framework and SqlMap do not reliably find bypassing
eachgeneratedattackbypassedtheWAForwasblocked. attacks, because the generated attacks are either too long
To compare ML-Driven with the WAF Testing Frame- to satisfy the input length constraint or contain a pattern
work and SqlMap, we use both tools to test ModSecurity thatisblacklisted.
and our industry partner’s proprietary WAF. The configu- For the experiment with ModSecurity, we use the WAF
rationofbothWAFsisthesameasintheotherreportedex- Testing Framework and SqlMap to test the same nine pa-
periments.SinceSqlMap’sattackgenerationisrandomized, rametersasselectedfortheevaluationofML-Driven(refer
we repeated each experiment involving SqlMap 10 times toRQ1).TheWAFTestingFrameworkexecutesagain19test
and report the averages. The attack generation in the WAF cases per tested parameter and SqlMap executes a similar
Testing Framework is deterministic and, hence, we report number of test cases as in the previous experiment (~3270
theresultofasinglerun.Wedonotimposeanylimitonthe testcasesperparameter).However,neithertheWAFTesting
numberofgeneratedtestcases;bothtoolsareconfiguredto Framework nor SqlMap find any bypassing attack for any
executeasmanytestcasesastheyarecapableofgenerating. ofthetestedparameters.
For the experiment with the proprietary WAF, we ran- WhencomparingtheresultsoftheWAFTestingFrame-
domly selected from each of the four parameter groups work and SqlMap with ML-Driven (refer to Section 5.1),
(refer to Table 4) one representative parameter to test. We we find that the formers are either completely ineffective
found in the evaluation of RQ1 that parameters in a same or significantly less effective than ML-Driven. For most of
group share a similar number of bypassing attacks. Given the tested parameters, both tools fail to find any bypassing

19
200
150
100
50
0
1 2 3 4 5 6 7 8 9 10
Iteration
D cp
1200
1000
800
600
400
200
0
D t
TABLE8
Sliceencodings.
ML-Driven E (Tree)
ML-Driven E (Forest)
Slice Literal Slice Literal
S1d or Sb !
Sf1 or 1 S3 1
S5 /**/ S6 ∼ 1
S26 # S57 1
S2 S29 0
S0 0 S15 )
Sf true Sc "
RandomForest than with RandomTree. For RandomForest,
the number of path conditions is close to 200 after 10
generations,comparedwith50forRandomTree.
Forbothtechniques,thenumberofbypassingtestsused
to train the model and the number of path conditions
Fig.15.Numberofpathconditions(redy-axisontheleft)andbypassing
tests(bluey-axisontheright)forML-Driven EwithRandomTreeand obtained from the model are concurrently increasing. This
RandomForest. is no surprise as more test cases lead to refined models.
ForRandomForest,thatleadstoevenmorepathconditions
attack, while ML-Driven finds a considerable number of sincemanymoretreesarebuilt.
them. For the few parameters, for which the alternative In general, path conditions can help determine the rea-
tools find bypassing attacks, ML-Driven finds an order son why a set of attacks is bypassing. This knowledge can
of magnitude more bypassing attacks. Furthermore, the be utilized to stop further attack attempts from succeeding
attacks found by the alternative tools are a subset of the by inferring a string pattern from the path condition that
attacks found by ML-Driven and, hence, using the alter- matchesalltheattacksdescribedbyit.Suchastringpattern
native tools in combination with ML-Driven would not can be in turn added to the WAF’s rule set to block all
providemoredistinctbypassingattacks.Anotheradvantage furtherattackscontainingthesamestringpattern.
ofML-DrivenoverthealternativetoolsisthatML-Driven To better explain the benefits of having more attack
abstractspathconditionsfromthebypassingattacks,which patterns,letusdescribeexamplesofpathconditionsandthe
helps the firewall administrator to repair the WAF (refer to attackstheycharacterizethatareobtainedfromatestrunof
Section6). the industrial WAF used in our evaluation. In particular,
let us consider an example of a path condition: pc 1 =
S1d∧Sf1∧S5∧¬S11∧¬S25∧¬S26∧¬S1b∧¬S15∧¬S2f.
5.4 RQ4:Arewelearningnew,usefulattackpatternsas
Table8showstheliteralsthatarerepresentedbythecorre-
thenumberofdistinct,bypassingattacksincreases? spondingslices.Anexampleattackcharacterizedbypc 1is0
As explained in Section 3.3, the ML-Driven techniques or 1/**/,whichisanobfuscatedvariationofatautology
periodically build a model (i.e., decision trees) that is used attack, e.g. " or 1=1. All attacks characterized by pc 1
toguidethegenerationofnewattacks.However,thismodel containtheslicesS1d,Sf1andS5.IfaWAFblocksinputs
canalsobeusedtoabstractcommonstringpatternsshared containing any of the three slices, the attacks characterized
by and possibly causing bypassing attacks. Therefore, for bypc 1 donolongerbypass.
RQ4weanalyzethemodelsthatarelearnedduringthetest As shown by our quantitative analysis, the number of
runs of ML-Driven E. For both RandomForest and Ran- discovered path conditions increases during test execution.
domTree, we analyze how the number of path conditions With more path conditions, the reasons why attacks are
increasesastheresultofgeneratingmoredistinctbypassing bypassingcanbemorepreciselycharacterized.Toillustrate
attacks. thisphenomenon,weanalyzethepathconditionsobtained
Fig. 15 depicts the average number of path conditions in different generations of the same test run. To limit the
thatcanbeextractedfromamodel(red)andthenumberof numberofpathconditionsinthisexample,weonlyconsider
bypassingtestswithwhichthemodelistrained(blue).Since path conditions that contain the slice S1d, like in pc 1. This
the ML-Driven techniques retrain the model at the end of slice represents the SQL keyword or and can for example
each generation, the corresponding training iterations (or bepartofaSQLtautologyattack,e.g.," or 1=1.
EA generations) are depicted on the horizontal axis. These The previously analyzed path condition pc 1 is obtained
curves are based on the average of all test runs performed from the first generation of a test run. In contrast, Table 10
withtheModSecuritycasestudy. showsmorepathconditionsfromthesametestrunobtained
Thenumberofdistinct,bypassingtests,whichareused afterthefifthgenerations.Table9depictsthestringpatterns
totrainthemodel,issteadilyincreasingforbothtechniques. thatcanbedevisedfromthepathconditions.
This is due to fact that the further a test run progresses, The first notable difference between both sets of path
the more bypassing tests are found and are used, in turn, conditionsistheirnumber.Inthefirstgeneration,onlyone
to retrain the model. The number of path conditions that path condition contains slice S1d while there are eight of
can be extracted from a model is also steadily increasing them by the fifth generation. When analyzing the patterns
forbothtechniques,althoughbeginningfromgeneration4, identified by the path conditions, there are several inter-
there are significantly more path conditions extracted with esting observations. First, pc 2 to pc 7 identify patterns of

20
TABLE9 Algorithm5AstrategytorepairafaultyWAFrulesetusing
Thistableshowsthepatternlearnedfromeachpathconditionand bypassingattacksandpathconditions.
exampleattackscontainingthepattern(thepatterncharacterizedby
1: Inputs:
thepathconditionsishighlightedinred).
A:asetofbypassingattackssuchthat|A|>0
PC:asetofpathconditionslearnedfromA
Generations Id Pattern ExampleSQLiAttack
R:asetofregularexpressionssuchthat
1 pc1 or 1,/**/ 0or 1/**/ ∀a∈A(cid:64)r∈R:rmatchesa
5 pc2 or, 1 'ortruelike 1||'
5 pc3 or,),# ')ornotfalse#
2: Output:
5 pc4 or, 0 1ortrue>( 0) R(cid:48):asetofregularexpressionssuchthat
5 5 p p c c 5 6 o o r r , , t 0 rue,# ' 0 o ) r o ∼ r tr ! u '' e − # − ∀a∈A∃r∈R(cid:48) :rmatchesa
5 5 p p c c 7 8 o o r r , , " /**/,#, ,0,! " ' | o | r/* t * r / ue !0 o i r s " true# 3: R(cid:48) ←R
5 pc9 or,/**/,1,∼ 1 1or/**/0<(∼ 1) 4: whilePC (cid:54)=∅do
5: s←selectMostFrequentSlice(PC)
6: PC s ←getPathConditionsContainingSlice(s)
bypassing attacks that use slice S1d, but require S5 to be 7: A s ←getCharacterisedAttacks(PC s )
absent (¬S5), thus, suggesting the pattern identified in the 8: Selectr i ∈RthatmatchesattackssimilartoA s
fi iz r e s s tg b e y n p e a r s a s t i i n o g n a w tt a a s ck in s c c o o m n p ta le in te in .F g o s r li e c x e a S m 1 p d le c , o p m c 5 b c in h e a d ra w ct i e t r h - 1 9 0 : : M R(cid:48) o ← dif ( y R r (cid:48) u \ le { r r i i } t ) o ∪ r i ∗ {r s i ∗ u } chthatitmatchesA s
thebooleanidentifiertrueandthecommentsymbol#,e.g., 11: PC ←PC\PC s
12: endwhile
" or true#. Such attacks are not matched by the pattern 13: returnR(cid:48)
representedbypc 1 and,thus,wouldstillbypasstheWAFif
onlypc 1 wouldbeconsideredinfixingtheWAF.
Toconclude,weseefromtheexampleabovethathaving
setofregularexpressionsR(cid:48),whichresultsfrommodifying
more path conditions helps derive a better understanding some regular expressions in R such that they match all
of the patterns shared by bypassing attacks. In turn, this attacks in A. We will use a running example in which A
putsafirewalladministratorinabetterpositiontodevisean andPC areinitializedwiththeattacksandpathconditions
effectivepatchforaWAF’sruleset,aswewilldemonstrate from generation five of the previous examples (refer to
inSection6. Table 9). R is initialized with the regular expressions from
the proprietary WAF used in our evaluation. Note that the
examples are not artificial as the regular expressions were
6 USING ATTACK PATTERNS TO REPAIR A WAF
actively protecting the industrial web service application
In this section, we demonstrate how the identified bypass- used in our evaluation. The attacks in Table 9 would have
ing attacks and corresponding path conditions can be used bypassedtheWAFdeployedintheproductionsystem.
toimprovetheWAF’sruleset.Wealsodiscussthebenefits
The strategy starts in line 3 by initializing the output
ofML-Driven EcomparedtotheotherML-Drivenstrate-
variable R(cid:48) by assigning R to it. The while loop from
gies,RAN,SqlMapandWAFTestingFramework.
line 4 to 12 is repeated until all path conditions in PC are
processed. In line 5, the loop begins by selecting a slice
6.1 RepairStrategy s that is the most frequently contained slice among the
Typically, a rule set uses regular expressions to match path conditions in PC. Line 6 selects all path conditions
knownmaliciousattacks(refertoSection2.1).Ourgoalisto PC s ⊂PCthatcontainslices.Then,line7selectsallattacks
modifytheseregularexpressionsinsuchawaythattheby- A s ⊂ A that are characterized by the path conditions in
passing attacks found by ML-Driven do no longer bypass PC s.Intherunningexample,thesliceS1disassignedtos
the WAF. We investigated a first attempt to semi-automate because it is part of eight path conditions (pc 2 to pc 9) and,
the WAF repairing process in our recent work [11]. In hence, is part of more path conditions than any other slice.
particular, we use multi-objective optimization algorithms Thepathconditionspc 2 topc 9 (seeTable10)areassignedto
tooptimizetwogoals:(i)maximizingthenumberofblocked PC sbecausetheycontainsliceS1d.Accordingly,theattacks
attacks and (ii) minimizing the number legitimate requests characterizedbythepathconditionspc 2 topc 9 areassigned
beingblocked(falsepositives). toA s (refertoTable9).
In this paper, we consider a general strategy for mod- Inline8,asecurityanalystmanuallyinspectstheregular
ifying the regular expressions as outlined in Algorithm 5. expressions in R and identifies a regular expression r i that
While parts of the strategy can be automated [11], regular shouldbemodifiedinordertocorrectlyidentifythebypass-
expressions derived from attack patterns (line 8 and 9) still ingattacksinA s.DependingontheregularexpressionsR,
requiremanualinspectionandadaptationdependingonthe theremightalreadyexistanexpressionr i ∈Rthatidentifies
WAFunderevaluation. Therequiredinputsforthestrategy attackssimilartothoseinA s and,hence,couldbemodified
arethetestoutputsofML-Driven,i.e.,asetAofbypassing to also account for A s. Alternatively, if no such regular
attacks and a set PC of path conditions learned from A, expression exists, a new regular expression can be created
and a set R of regular expressions used by the WAF under or,ifthereismorethanonecandidateregularexpressionfor
test to match known attacks. Note that the attacks in A modification, several regular expressions can be modified
are not matched by any regular expression in R, otherwise sothateachexpressionmatchesasubsetofA s.Thesecurity
the attacks would not bypass in the first place, and, hence, analystisfreetomakethisdecisionbasedonhowheintends
∀a∈A(cid:64)r ∈R:rmatchesa.Theoutputofthestrategyisa to logically structure the rule set. In the running example,

21
TABLE10
PathConditionsfromgeneration5.
Id Pathcondition
pc2 S1d∧S57∧¬S25∧¬S26∧¬Sc∧¬S14∧¬S1∧¬S3e∧¬S0∧¬S38∧¬S29∧¬S5∧¬Se1∧¬S1c∧¬S1de∧¬S76∧¬S67
pc3 S1d∧S26∧S15∧¬Sf∧¬S1c∧¬Se1∧¬S25∧¬S5∧¬Sc∧¬S14∧¬S1de∧¬S3e∧¬S76∧¬S29∧¬S38∧¬S67
pc4 S1d∧S29∧¬Se1∧¬S25∧¬S5∧¬S14∧¬S1de∧¬S3e∧¬S76∧¬S38∧¬S67
pc5 S1d∧Sf∧S26∧¬S1c∧¬Se1∧¬S25∧¬S5∧¬Sc∧¬S14∧¬S1de∧¬S3e∧¬S76∧¬S29∧¬S38∧¬S67
pc6 S1d∧S0∧¬S25∧¬S26∧¬Sc∧¬S14∧¬S3e∧¬S38∧¬S29∧¬S5∧¬Se1∧¬S1c∧¬S1de∧¬S76∧¬S67
pc7 S1d∧Sc∧¬S1c∧¬Se1∧¬S25∧¬S5∧¬S14∧¬S1de∧¬S3e∧¬S76∧¬S29∧¬S38∧¬S67
pc8 S1d∧S5∧S26∧S2∧S0∧Sb∧¬Sa8∧¬S7c3∧¬Sf∧¬S1e1∧¬S25∧¬Sd∧¬Sc∧¬S14∧¬S15∧¬S26d∧¬S60∧¬S2e∧
¬S2d∧¬S38∧¬S3
pc9 S1d∧S3∧S5∧S6∧¬Sf∧¬S25∧¬Sf1∧¬Sc∧¬S26∧¬S1b∧¬S5a∧¬S14∧¬S71
weassignthefollowingregularexpressiontor i: andthemainloopends.
Note that the proposed strategy helps a security expert
(?i)'[\s]+or
efficiently deal with the typically large number of path
Theregularexpressionbeginswith(?i),whichenables conditions found by ML-Driven by grouping conditions
case-insensitive matching. It matches strings that contain containingsimilarattackpatterns.Groupingpatternshelps
an apostrophe followed by at least one whitespace ([\s]+) the security experts to consider relevant patterns together
followedbytheSQLkeywordor.Weselectthisexpression whendevisinganimprovedregularexpressionand,hence,
formodificationbecauseitistheonlyexpressionintherule theydonothavetoconsidereachpatternindividually.The
set that tries to match attacks containing the SQL keyword strategy is defined in such a way that the most frequent
or.SinceallattacksinA
s
alsocontainor,theexpressionis attackpatternsaretackledfirst.
asuitablecandidateformodification.
Inline9,thesecurityanalystextendstheregularexpres- 6.2 Suitability of other techniques for the purpose of
sion r i so that it also matches the attacks in A s. The path repairingaWAF
conditions in PC s provide guidance on how r i could be The testing techniques and tools discussed throughout this
extended. In the running example, when we contrast the
paper find bypassing attacks with varying effectiveness.
expression r i with the path conditions in PC s, we make Thissectiondiscusseshowsuitablethedifferenttechniques
severalobservationsregardingwhyr i doesnotidentifythe areforthepurposeofrepairingaWAF.
attacksinA s:(i)unlikeinr i,notallattacksinA s startwith Inourexperiments,SqlMapandtheWAFTestingFrame-
an apostrophe, but they start either with an apostrophe, a work did find none or very few bypassing attacks and,
doublequote(e.g.pc 7),oradigit(e.g.pc 6);(ii)unlikeinr i, hence,donotprovidemuchusefulinformationforrepairing
none of the path conditions requires a leading whitespace aWAFasmanybypassingattackswouldremainuncovered.
before the literal or; and (iii) r i does not account for SQL RAN is more effective in finding bypassing attacks than
commentcharacters,i.e.,#and/**/,whicharefrequently
SqlMap and the WAF Testing Framework, but it does not
used in bypassing attacks (e.g. pc 3, pc 5, pc 8, and pc 9). identify common bypassing attack patterns. In absence of
Basedontheseobservations,wedeviseanimprovedregular such patterns, a security analyst has to translate a possibly
expressionr i ∗ toavoidthementionedshortcomings: largenumberofbypassingattacksintoanWAFpatch.This
limitationaffectsnotonlyRANbutalsotheothertools(i.e.,
(?i)(('|"|\d).∗or)|(or.∗(/**/|#))
SqlMap and WAF Testing Framework) as they provide the
The modified expression r i ∗ consists of two parts. The setofbypassingattackswithoutanyadditionalinformation
first part is (('|"|\d).∗or) and addresses (i) as well about which substrings are associated with bypassing the
as (ii). It addresses (i) by replacing the apostrophe with WAF.Instead,ourML-Driventechniquesprovideboththe
('|"|\d) and it addresses (ii) by replacing [\s]+ with set of bypassing attacks (which are larger in number) and
an arbitrary character sequence (denoted by .∗). Therefore, theassociatedattackpatternsidentifiedbymachinelearning
the first part matches strings that contain either an apos- algorithms(i.e.,RandomTreeandRandomForest).
trophe, a double quote, or a digit, followed by an arbitrary Amongst the ML-Driven techniques, ML-Driven E
charactersequence,andfollowedbyor.Thesecondpartis wasfoundtobethemostefficient.Havingmoresuccessful
(or.∗(/**/|#)) and addresses (iii) as it matches strings bypassing attacks provides additional benefits for security
that contain or and a SQL comment character (/**/ or analysts in charge of repairing the vulnerable WAF. First,
#). Since both parts are joined with an alternation (|), the a lower number of distinct attacks will lead to less attack
stringsmatchedbyr i ∗istheunionsetofthestringsmatched patterns being identified and less new regular expressions
bythefirstpartandthesecondpart. to be added to the WAF rule set. Therefore, ML-Driven
With the performed changes, r∗ matches all attacks in B/D may miss some distinct attacks, leading to less robust
i
A s. In line 11, we remove the old expression r i from the patchesasthefixedWAFwouldnotbeabletodetect/match
output set R(cid:48) and add r i ∗ to R(cid:48). Since all attacks in A s the missed patterns. Second, machine learning algorithms
are now correctly identified, we remove in line 11 the path better identify useful and useless attack patterns (or path
conditions PC s from PC and continue with the next loop conditions) when more bypassing attacks are provided as
iteration until all path conditions in PC are processed. In shown in Section 5.4. For example, let us assume that
the running example, PC is empty after the first iteration ML-DrivenB/Dgenerateonesinglebypassingattackwith

22
TABLE11 set and thus all attacks are blocked. Similarly, for the 46
ComparisonoftheattackpatternsfoundbyML-Driven E, parametersforwhichnoattackisfound,theexpectedinput
ML-Driven BandML-Driven D.
formatpreventsattacks.However,itisnotpossibletodefine
such strict validation rules for all parameters, since the
Id Pattern ML-E ML-B ML-D
pc1 or 1,/**/ (cid:51) (cid:51) (cid:51) inputsmightvarysignificantlyintermsofcharactersetand
pc2 or, 1 (cid:51) (cid:51) (cid:55) length. This is the case for the other 29 parameters where
pc3 or,),# (cid:51) (cid:51) (cid:51)
the expected input format is very general and the input
pc4 or, 0 (cid:51) (cid:51) (cid:51)
pc5 or,true,# (cid:51) (cid:55) (cid:55) validation rules rather loose, thus being prone to attacks.
pc6 or,0 (cid:51) (cid:51) (cid:51) For example, the vulnerable parameter Address is expected
pc7 or," (cid:51) (cid:51) (cid:51) tobeastringwithamaximumof35characters,aconstraint
p p c c 8 9 o o r r , , / / * * * * / / , , # 1 , ,∼ ,0 1 ,! (cid:51) (cid:51) (cid:51) (cid:55) (cid:55) (cid:55) withwhichmanyoftheSQLiattackscomply.
Another major difference between the two case studies
are the number of bypassing attacks per tested parameter.
the following slices: S 1=’, S 2= , S 3=“a”=“a”, S 4=#. With ForModSecurity,about1,000bypassingattacksperparam-
onesingleattack,itmaybedifficultforsecurityanalyststo eter are found while, for the proprietary WAF, they are on
determine which of these slices is actually associated with average10,000.Thissignificantdifferencecanbeattributed
bypassing the WAF. Therefore, deeper analysis (or more totheattackdetectioncapabilitiesofeachrespectivefirewall
attacks) is needed to determine which slices should form and highlights the difficulty of customizing a rule set for a
regularexpressionstoaddtotheWAF’sruleset. particularITenvironmentinpractice.Inourexperiment,we
To illustrate the practical usefulness of the three useadefaultrulesetforModSecurity,whiletheproprietary
ML-Driven techniques, let us now compare the gener- WAF has a customized rule set to match a particular IT
ated attacks patterns for the running example used in Sec- system. Such a customization is often necessary to achieve
tion 6.1. It corresponds to one of the regular expressions an acceptable false positive rate, but comes at the cost of
that were actively protecting the industrial web service reducedattackdetectioncapabilitiesdueinparttothelack
application used in our evaluation. Table 11 lists the attack ofsuitabletoolstotestthefirewalls.
patterns that were found in the same amount of time by
ML-Driven E, ML-Driven B and ML-Driven D, respec-
tively. As we can notice, ML-Driven E generated more 7.2 ApplicationoftheProposedTechniques
attackspatternscomparedtotheotherML-Drivenvariants: We have proposed and evaluated three variants of a
ML-Driven E misses pc 5 and pc 8 while ML-Driven D machine learning driven technique for the generation of
further misses pc 2 and pc 9. Assuming the analyst would SQLi attacks, namely ML-Driven E, ML-Driven D, and
rely on ML-Driven B, she would add the following reg- ML-Driven B. ML-Driven D and ML-Driven B entail
ular expression containing all found attack patterns: r = different strategies in allocating the test generation budget.
pc 1 |pc 2 |pc 3 |pc 4 |pc 6 |pc 7 |pc 9, i.e., r matches the attacks sat- ML-Driven E reconciles these differences and delivers a
isfying either pc 1-pc 4, pc 6-pc 7, or pc 9. However, this patch better performance. We have compared all these variants
would miss attacks found by ML-Driven E as the gener- with RAN, the baseline technique considered in our work,
atedrwouldnotmatchanyattackscontainingeitherpc 5 or on ModSecurity (a popular open-source WAF) and a pro-
pc 8. The patches generated with ML-Driven D would be prietary WAF. Our experiments show that ML-Driven E
lessrobustcomparedtoML-Driven EandML-Driven B outperformsalltheothertechniques.
astheresultingregularexpressionswouldnotmatchattacks We have also demonstrated the usefulness of mining
satisfyingthemissingfourpatterns. more bypassing attacks in devising string patterns to fix
Theexampleaboveshowsthatgeneratingmoredistinct WAFs. In our context, we experimented with RandomTree
attacksleadstouncoveringmoresuccessfulattackpatterns and RandomForest as machine classifiers for ML-Driven
andimplementingmorerobustpatchestotheWAF. E. Since we show that the latter helps extract more path
conditionsthatareusefulinidentifyingpatternsandfixing
7 DISCUSSION WAFs,werecommendtheuseofRandomForest.
This section discusses some practical implications of our
ML-Drivenapproachanditsempiricalresults.. 8 CONCLUSION
Web application firewalls (WAFs) play an important role
7.1 DifferencesbetweenCaseStudies
to protect online systems. The rising occurrence of new
When comparing the testing results of the two case stud- kinds of attacks and their increasing sophistication require
ies some notable differences stand out. First, bypassing thatfirewallsbeupdatedandtestedregularly,asotherwise
attacks could be found for each parameter protected by attacks might remain undetected and reach the systems
ModSecurity, whereas with the proprietary WAF, only 29 underprotection.
out of75 parameters leadto bypassingattacks. This canbe We propose ML-Driven, a search-based approach that
attributed to the fact that the latter strictly validates each combines machine learning and evolutionary algorithms
input to follow an expected format. For example, a value to automatically test the attack detection capabilities of
provided to the parameter credit card number must consist WAFs. The approach automatically generates a diverse set
of 16 to 19 digits and, otherwise, the request is rejected. of attacks, sends them to a WAF under test, and checks
SQL injection attacks typically require a larger character if they are correctly identified. By incrementally learning

23
fromtheteststhatareblockedorbypassingthefirewall,our [4] S. Anand, E. K. Burke, T. Y. Chen, J. Clark, M. B. Cohen,
approachselectsteststhatexhibitstringpatternswithhigh W. Grieskamp, M. Harman, M. J. Harrold, and P. McMinn. An
orchestratedsurveyofmethodologiesforautomatedsoftwaretest
bypassing probabilities (according the machine learning)
casegeneration. JournalofSystemsandSoftware,86(8):1978–2001,
and mutates them using an attack grammar designed to 2013.
generate new and hopefully successful attacks. Identified [5] N. Antunes, N. Laranjeiro, M. Vieira, and H. Madeira.
bypassing attacks can be used to learn path conditions, Command injection vulnerability scanner for web services.
http://eden.dei.uc.pt/mvieira/.
whichcharacterizesuccessfulattackpatterns.
[6] N.Antunes,N.Laranjeiro,M.Vieira,andH.Madeira. Effective
Withsuchasetofbypassingattacksandpathconditions detectionofSQL/XPathinjectionvulnerabilitiesinwebservices.
thatcharacterizethem,asecurityexpertcanfixorfine-tune In Proceedings of the 6th IEEE International Conference on Services
Computing(SCC’09),pages260–267,2009.
the WAF rules in order to block imminent SQLi attacks. In
[7] D. Appelt, N. Alshahwan, and L. Briand. Assessing the impact
theattacker-defenderwar,timeisvital.Beingabletoquickly offirewallsanddatabaseproxiesonsqlinjectiontesting. InPro-
learn and anticipate more attacks that can circumvent a ceedingsofthe1stInternationalWorkshoponFutureInternetTesting,
firewall, in a timely manner, is very important to secure 2013.
[8] D. Appelt, A. Nguyen, Cu D. Panichella, and L. Briand. Au-
businessdataandservices.
tomated testing of web application firewalls: Technical report.
Though our approach was applied to SQL injection TechnicalReportTR-SnT-2016-1,UniversityofLuxembourg,2016.
attacks in this paper, it can be adapted to other forms of [9] D. Appelt, C. D. Nguyen, and L. Briand. Behind an application
firewall, are we safe from sql injection attacks? In Software
attacks by making use of other attack grammars targeting
Testing,VerificationandValidation(ICST),2015IEEE8thInternational
differenttypesofvulnerabilities. Conferenceon,pages1–10.IEEE,2015.
Our key contributions in this work include (i) enhanc- [10] D.Appelt,C.D.Nguyen,L.C.Briand,andN.Alshahwan. Auto-
ing our preliminary techniques by consolidating them and matedtestingforsqlinjectionvulnerabilities:Aninputmutation
approach. In Proceedings of the 2014 International Symposium on
improving their performance, (ii) comparing two different
Software Testing and Analysis, ISSTA 2014, pages 259–269, New
andadequatemachinelearningclassifiers,(iii)carryingout York,NY,USA,2014.ACM.
alarge-scaleevaluationontwopopularWAFsand(iv)com- [11] D.Appelt,A.Panichella,andL.C.Briand. Automaticallyrepair-
ing web application firewalls based on successful SQL injection
paring our approach with state-of-the-art tools. Evaluation
attacks.In28thIEEEInternationalSymposiumonSoftwareReliability
results suggest that the performance of ML-Driven (and
Engineering, ISSRE 2017, Toulouse, France, October 23-26, 2017,
itsenhancedvariantinparticular)iseffectiveatgenerating pages339–350,2017.
many undetected attacks and provides a good basis to [12] W. Banzhaf, F. D. Francone, R. E. Keller, and P. Nordin. Genetic
Programming: An Introduction: on the Automatic Evolution of Com-
identify attack patterns to protect against. Further, it also
puterProgramsandItsApplications. MorganKaufmannPublishers
faressignificantlybetterthanthebestavailabletools. Inc.,SanFrancisco,CA,USA,1998.
In our future work, we will investigate automated ap- [13] J. Bau, E. Bursztein, D. Gupta, and J. Mitchell. State of the art:
proaches to generate effective patches for the WAF under Automated black-box web application vulnerability testing. In
SecurityandPrivacy(SP),2010IEEESymposiumon,pages332–345.
test starting from the learned attack patterns. We reported
IEEE,2010.
on an initial attempt to automate the repairing process in [14] S.W.BoydandA.D.Keromytis.Sqlrand:Preventingsqlinjection
a recent paper [11], where we generated patches that block attacks. InAppliedCryptographyandNetworkSecurity,pages292–
302.Springer,2004.
as many bypassing attacks as possible while limiting the
[15] L.Breiman. Randomforests. Machinelearning,45(1):5–32,2001.
blocking of legitimate inputs. Investigating further, more [16] J.Coffey,L.White,N.Wilde,andS.Simmons. Locatingsoftware
effective, repairing strategies that better exploit the attack featuresinasoacompositeapplication. InWebServices(ECOWS),
patterns generated by ML-Driven E is part of our future 2010IEEE8thEuropeanConferenceon,pages99–106,2010.
[17] L.Desmet,F.Piessens,W.Joosen,andP.Verbaeten. Bridgingthe
agenda. Finally, we plan to investigate various strategies
gapbetweenwebapplicationfirewallsandwebapplications. In
(e.g., data re-sampling strategies, weighted training, and ProceedingsofthefourthACMworkshoponFormalmethodsinsecurity,
penalty-basedtraining)toimprovetheeffectivenessandthe pages67–77.ACM,2006.
efficiency of ML-Driven by addressing the data imbalance [18] A. Doupé, M. Cova, and G. Vigna. Why johnny canâA˘Z´t pen-
test: An analysis of black-box web vulnerability scanners. In
problem.
InternationalConferenceonDetectionofIntrusionsandMalware,and
VulnerabilityAssessment(DIMVA),pages111–131.Springer,2010.
[19] M. Felderer, M. BÃijchler, M. Johns, A. D. Brucker, R. Breu, and
ACKNOWLEDGEMENTS
A.Pretschner. Securitytesting. AdvancesinComputers,101:1–51,
ThisworkbuildsonDennisAppelt’sPh.D.dissertation.The 2016.
[20] X.Fu,X.Lu,B.Peltsverger,S.Chen,K.Qian,andL.Tao. Astatic
project has received funding from the European Research
analysisframeworkfordetectingsqlinjectionvulnerabilities. In
Council (ERC) under the European Union’s Horizon 2020 31stAnnualInternationalComputerSoftwareandApplicationsConfer-
research and innovation programme (grant agreement No ence(COMPSAC2007),volume1,pages87–96,July2007.
[21] P.Godefroid,A.Kiezun,andM.Y.Levin. Grammar-basedwhite-
694277).
boxfuzzing. InACMSigplanNotices,volume43,pages206–215.
ACM,2008.
REFERENCES [22] P.Godefroid,M.Y.Levin,andD.Molnar. Sage:whiteboxfuzzing
forsecuritytesting. Queue,10(1):20,2012.
[1] Verified firewall policy transformations for test case generation. [23] P.Godefroid,M.Y.Levin,D.A.Molnar,etal.Automatedwhitebox
In Software Testing, Verification and Validation (ICST), 2010 Third fuzztesting. InNDSS,volume8,pages151–166,2008.
InternationalConferenceon,pages345–354.IEEE,2010. [24] W. Halfond, J. Viegas, and A. Orso. A classification of sql-
[2] Management of an Academic HPC Cluster: The UL Experience. injectionattacksandcountermeasures. InProceedingsoftheIEEE
In Proc. of the 2014 Intl. Conf. on High Performance Computing & InternationalSymposiumonSecureSoftwareEngineering,volume1,
Simulation(HPCS2014),pages959–967,Bologna,Italy,July2014. pages13–15.IEEE,2006.
IEEE. [25] W. G. Halfond, S. Anand, and A. Orso. Precise interface identi-
[3] E.Al-Shaer,A.El-Atawy,andT.Samak. Automatedpseudo-live fication to improve testing and analysis of web applications. In
testing of firewall configuration enforcement. Selected Areas in Proceedings of the 18th International Symposium on Software Testing
Communications,IEEEJournalon,27(3):302–314,2009. andAnalysis(ISSTA’09),pages285–296,2009.

24
[26] W. G. Halfond and A. Orso. Amnesia: analysis and monitoring [39] A.Panichella,F.Kifetew,andP.Tonella.Automatedtestcasegen-
for neutralizing sql-injection attacks. In Proceedings of the 20th eration as a many-objective optimisation problem with dynamic
IEEE/ACMinternationalConferenceonAutomatedsoftwareengineer- selectionofthetargets. IEEETransactionsonSoftwareEngineering,
ing,pages174–183.ACM,2005. PP(99):1–1,2017.
[27] W. G. J. Halfond and A. Orso. Preventing SQL injection attacks [40] A.Panichella,F.M.Kifetew,andP.Tonella.Reformulatingbranch
usingAMNESIA. InProceedingsofthe28thInternationalConference coverageasamany-objectiveoptimizationproblem. In8thIEEE
onSoftwareEngineering(ICSE’06),pages795–798,2006. InternationalConference onSoftware Testing,Verification andValida-
[28] M. Hall, E. Frank, G. Holmes, B. Pfahringer, P. Reutemann, and tion,ICST2015,Graz,Austria,April13-17,2015,pages1–10,2015.
I.H.Witten.Thewekadataminingsoftware:Anupdate.SIGKDD [41] A. Petrowski and S. Ben-Hamida. Evolutionary Algorithms. John
Explor.Newsl.,11(1):10–18,Nov.2009. Wiley&Sons,2017.
[29] J. Hwang, T. Xie, F. Chen, and A. X. Liu. Systematic structural [42] J. R. Quinlan. C4.5: Programs for Machine Learning, volume 1.
testing of firewall policies. In Reliable Distributed Systems, 2008. Morgankaufmann,1993.
SRDS’08.IEEESymposiumon,pages105–114.IEEE,2008. [43] D.Senn,D.Basin,andG.Caronni. Firewallconformancetesting.
[30] J.JürjensandG.Wimmel. Specification-basedtestingoffirewalls. In F. Khendek and R. Dssouli, editors, Testing of Communicating
In D. Bjørner, M. Broy, and A. Zamulin, editors, Perspectives Systems, volume 3502 of Lecture Notes in Computer Science, pages
of System Informatics, volume 2244 of Lecture Notes in Computer 226–241.SpringerBerlinHeidelberg,2005.
Science,pages308–316.SpringerBerlinHeidelberg,2001. [44] S.Shamshiri,J.M.Rojas,G.Fraser,andP.McMinn. Randomor
[31] G. Karafotias, M. Hoogendoorn, and A. E. Eiben. Parameter geneticalgorithmsearchforobject-orientedtestsuitegeneration?
controlinevolutionaryalgorithms:Trendsandchallenges. IEEE InProceedingsofthe2015AnnualConferenceonGeneticandEvolu-
TransactionsonEvolutionaryComputation,19(2):167–187,April2015. tionaryComputation,GECCO’15,pages1367–1374,NewYork,NY,
[32] A.Kieyzun,P.J.Guo,K.Jayaraman,andM.D.Ernst. Automatic USA,2015.ACM.
creationofSQLinjectionandcross-sitescriptingattacks. InPro- [45] L. K. Shar and H. B. K. Tan. Defeating sql injection. Computer,
ceedingsofthe31stInternationalConferenceonSoftwareEngineering (3):69–77,2013.
(ICSE’09),pages199–209,2009. [46] M.Soltani,A.Panichella,andA.vanDeursen. Aguidedgenetic
[33] Y.-F.Li,P.K.Das,andD.L.Dowe.Twodecadesofwebapplication algorithmforautomatedcrashreproduction. InProceedingsofthe
testingâA˘Tˇasurveyofrecentadvances. InformationSystems,43:20 39th International Conference on Software Engineering, ICSE 2017,
–54,2014. BuenosAires,Argentina,May20-28,2017,pages209–220,2017.
[34] A.Liu,Y.Yuan,D.Wijesekera,andA.Stavrou. Sqlprob:Aproxy- [47] M.Sutton,A.Greene,andP.Amini. Fuzzing:bruteforcevulnerabil-
based architecture towards preventing sql injection attacks. In itydiscovery. PearsonEducation,2007.
Proceedingsofthe2009ACMSymposiumonAppliedComputing,SAC [48] O.Tripp,O.Weisman,andL.Guy.Findingyourwayinthetesting
’09,pages2054–2061,NewYork,NY,USA,2009.ACM. jungle:alearningapproachtowebsecuritytesting. InProceedings
[35] H. Liu and H. B. Kuan Tan. Testing input validation in web ofthe2013InternationalSymposiumonSoftwareTestingandAnalysis,
applicationsthroughautomatedmodelrecovery.JournalofSystems pages347–357.ACM,2013.
andSoftware,81(2):222–233,2008. [49] M.Cˇrepinšek,S.-H.Liu,andM.Mernik.Explorationandexploita-
[36] P.McMinn. Search-basedsoftwaretestdatageneration:asurvey. tion in evolutionary algorithms: A survey. ACM Comput. Surv.,
SoftwareTesting,VerificationandReliability,14(2):105–156,2004. 45(3),2013.
[37] R.McNally,K.Yiu,D.Grove,andD.Gerhardy. Fuzzing:thestate [50] J.WilliamsandD.Wichers. Owasp,top10,thetenmostcritical
oftheart. Technicalreport,DTICDocument,2012. web application security risks. Technical report, The Open Web
[38] J. Offutt, Y. Wu, X. Du, and H. Huang. Bypass testing of web ApplicationSecurityProject,2013.
applications. InSoftwareReliabilityEngineering,2004.ISSRE2004. [51] I.H.WittenandE.Frank. DataMining:Practicalmachinelearning
15thInternationalSymposiumon,pages187–197.IEEE,2004. toolsandtechniques. MorganKaufmann,2011.
WAF-A-MoLE: Evading Web Application Firewalls through
Adversarial Machine Learning
LucaDemetrio AndreaValenza
luca.demetrio@dibris.unige.it andrea.valenza@dibris.unige.it
UniversitàdiGenova UniversitàdiGenova
GabrieleCosta GiovanniLagorio
gabriele.costa@imtlucca.it giovanni.lagorio@unige.it
IMTSchoolforAdvancedStudiesLucca UniversitàdiGenova
ABSTRACT 1 admin' OR 1=1#
Web Application Firewalls are widely used in production envi- 2 admin' OR 0X1=1 or 0x726!=0x726 OR 0x1Dd
ronmentstomitigatesecuritythreatslikeSQLinjections.Many not IN/*(seleCt 0X0)>c^Bj>N]*/ ((SeLeCT
industrialproductsrelyonsignature-basedtechniques,butma- 476),(SELECT (SElEct 477)),0X1de) oR
chinelearningapproachesarebecomingmoreandmorepopular. 8308 noT lIkE 8308\x0c AnD truE OR '
Themaingoalofanadversaryistocraftsemanticallymalicious FZ6/q' LiKE 'fz6/qI' anD TRUE anD '>U'
payloadstobypassthesyntacticanalysisperformedbyaWAF. != '>uz'#t'%'03;Nd
Inthispaper,wepresentWAF-A-MoLE,atoolthatmodelsthe
presence of an adversary. This tool leverages on a set of muta-
tionoperatorsthatalterthesyntaxofapayloadwithoutaffecting Figure1:Twosemanticallyequivalentpayloads.
theoriginalsemantics.Weevaluatetheperformanceofthetool
againstexistingWAFs,thatwetrainedusingourpubliclyavailable
SQLquerydataset.WeshowthatWAF-A-MoLEbypassesallthe
possibleexploitationpatterns,e.g.,payloadscarryingaSQLinjec-
consideredmachinelearningbasedWAFs.
tion.SinceWAFsworkatapplication-level,theyhavetodealwith
highlyexpressivelanguagessuchasSQLandHTML.Clearly,this
KEYWORDS
exacerbatesthedetectionproblem.
webapplicationfirewall,adversarialmachinelearning,sqlinjection, Toclarifythisaspect,consideraclassicalSQLinjectionscenario
mutationalfuzzing wheretheattackercraftsamaliciouspayloadxsuchthatthequery
SELECT * FROM users WHERE name='x' AND pw='y'alwayssuc-
1 INTRODUCTION
ceeds(independentlyfromy).Figure1showstwoinstancesofsuch
Mostsecuritybreachesoccurduetotheexploitationofsomevulner- apayload.Noticethatthetwopayloadsaresemanticallyequivalent.
abilities.Ideally,thebestwaytoimprovethesecurityofasystem Asamatteroffact,bothreducetheabovequerytoSELECT * FROM
istodetectallitsvulnerabilitiesandpatchthem.Unfortunately, users WHERE name='admin' OR ⊤ #...where⊤isatautology
thisisrarelyfeasibleduetotheextremecomplexityofrealsystems and...isatrailofcommentedcharacters.IdeallyaWAFshould
andhighcostsofathoroughassessment.Inmanycontexts,pay- rejectboththesepayloads.However,whenclassificationisbasedon
loadsarrivingfromtheInternetaretheprimarythreat,withthe ameresyntacticalanalysis,thismightnothappen.Hence,thegoal
attackerusingthemtodiscoverandexploitsomeexistingvulner- ofanattackeramountstolookingforsomemaliciouspayloadthat
abilities.Thus,protectingasystemagainstmaliciouspayloadsis isundetectedbytheWAF.Wepresentatechniquetoeffectivelyand
crucial.Commonprotectionmechanismsincludeinputfiltering, efficientlygeneratesuchmaliciouspayloads,thatbypassML-based
sanitization,andotherdomain-specifictechniques,e.g.,prepared WAF.Ourapproachstartsfromatargetmaliciouspayloadthat
statements.Implementingeffectiveinputpoliciesisnontrivialand, theWAFcorrectlydetects.Then,byiterativelyapplyingasetof
sometimes,eveninfeasible(e.g.,whenasystemmustbeintegrated mutationoperators,wegeneratenewpayloads.Sincemutationop-
inmanyheterogeneouscontexts). eratorsaresemantics-preserving,thenewpayloadsareequivalent
Forthisreason,mitigationsolutionsareoftenputinplace.For fromthepointofviewoftheadversary.However,theygraduallyre-
instance,IntrusionDetectionSystems(IDS)aimtodetectsuspicious ducetheconfidenceoftheWAFclassificationalgorithm.Eventually,
activities.Clearly,thesemechanismshavenoeffectonexisting thisprocessconvergestoapayloadclassifiedbelowtherejection
vulnerabilitiesthatsilentlypersistinthesystem.However,when threshold.Toevaluatetheeffectivenessofourmethodologywe
IDSscanpreciselyidentifyintrusionattempts,theysignificantly implementedaworkingprototype,calledWAF-A-MoLE.Thenwe
reducetheoveralldamage.TheverycoreofanyIDSisitsdetection appliedWAF-A-MoLEtodifferentML-basedWAFs,andevaluated
algorithm:theoveralleffectivenessonlydependsonwhetheritcan theirrobustnessagainstourtechnique.
discriminatebetweenharmfulandharmlesspackets/flows. Contributionsofthepaper.Themaincontributionsofthiswork
WebApplicationFirewalls(WAFs)areaprominentfamilyof aresummarizedasfollows:(i)wedevelopatoolforproducing
IDS,widelyadopted[16]toprotectICTinfrastructures.Theirde- adversarialexamplesagainstWAFsbyleveragingonasetofsyntac-
tectionalgorithmappliestoHTTPrequests,wheretheylookfor ticalmutations,(ii)weproduceadatasetofbothsaneandinjection
0202
naJ
7
]RC.sc[
1v25910.1002:viXra

queries,(iii)andwereviewthestateoftheartofmachinelearning
SQLinjectionclassifiersandwebypassthemusingWAF-A-MoLE.
2 PRELIMINARIES
WebApplicationFirewalls(WAFs)arecommonlyusedtoprevent
application-levelexploitsofwebapplications.Intuitively,theidea
isthataWAFcandetectanddropdangerousHTTPrequeststo
mitigatepotentialvulnerabilitiesofwebapplications.Themost
commondetectionmechanismsincludesignature-basedmatching Figure2:Anoutlineofthemutationalfuzztestingapproach.
andclassificationviamachinelearning.
Signature-basedWAFsidentifyapayloadaccordingtoalistof
rules,typicallywrittenbysomedevelopersormaintainedbyacom-
input: Model m, Payload p0, Threshold t
munity.Forinstance,rulescanbeencodedthroughsomepolicy
output: head(Q)
specificationlanguagethatdefinesthesyntaxoflegal/illegalpay-
loads.Nowadays,thesignature-basedapproachiswidelyusedand,
perhaps,themostpopularsignature-basedWAFisModSecurity1. 1 Q := create_priority_queue ()
However, recently the machine learning-based approach has 2 v := classify(m, p0)
received increasing attention. For instance, both FortiNet2 and 3 enqueue(Q, p0, v)
PaloAlto3includeML-baseddetectionintheirWAFproducts,since 4 while v >t
MLcanovercomesomelimitationsofsignature-basedWAFs,i.e., 5 p := mutate(head(Q))
theextremecomplexityofdevelopingalistofsyntacticrulesthat 6 v := classify(m, p)
precisely characterizes malicious payloads. Since ML WAFs are 7 enqueue(Q, p, v)
trainedonexistinglegalandillegalpayloads,theirconfigurationis
almostautomatic.
Figure3:CorealgorithmofWAF-A-MoLE.
Adversarialmachinelearning(AML)[6,22]studiesthethreats
posedbyanattackeraimingtomisleadmachinelearningalgorithms.
Morespecifically,hereweareinterestedinevasionattacks,where
theadversarycraftsmaliciouspayloadsthatarewronglyclassified calledmutants,arethenexecuted,compared(accordingtosome
bythevictimlearningalgorithm.Theadversarialstrategyvaries performance metric) and ordered. Then, the process is iterated
withthetargetMLalgorithm.Manyexistingsystemshavebeen ontheteststhatperformedbetteruntilasuccessfultestisfound.
showntobevulnerableandseveralauthors,e.g.[7,10,18,32],pro- Clearly,thisapproachrequiresbothacomparisoncriterionandaset
posedtechniquesforsystematicallygeneratingmalicioussamples. ofmutationoperators.Thesearetypicallyapplication-dependent.
Intuitively,thecraftingprocessworksbyintroducingasemantics- Figure2schematicallydepictsthisapproach.
preserving perturbation in the payload, that interferes with the
classification algorithms. Notice that, often, a formal semantics
3.1 Algorithmdescription
oftheclassificationdomainisnotavailable,e.g.,itisinformally
InourcontextatestisaSQLinjectionanditsexecutionamounts
provided through an oracle such as a human classifier. The ob-
tosubmittingittothetargetWAF.Thecomparisonisbasedonthe
jective of the adversary may be written as a constrained mini-
mizationproblemx∗ =argmin
x,C(x)
D(f(x),ct ),where f isthe confidencevaluegeneratedbythedetectionalgorithmoftheWAF.
ThepayloadpoolisthedatastructurecontainingtheSQLinjection
victimclassifier,ct isthedesiredclasstheadversarywantstoreach,
D isadistancefunction,andC(x)representsalltheconstraints candidatestobemutatedduringthenextround.Belowwedescribe
inmoredetailthesetofmutationoperatorsandthepayloadpool.
thatcannotbeviolatedduringthesearchforadversarialexamples.
ApseudocodeimplementationofthecorealgorithmofWAF-A-
Sinceweconsiderbinaryclassifiers,wecanrewriteourproblem
asx∗ =argmin f(x),wheretheoutputof f isboundedbe- MoLEisshowninFigure3.Thealgorithmtakesthelearningmodel
tween0and1,a
x
n
,
d
C(
w
x)
eareinterestedinreachingthebenignclass
m:X→[0,1],whereXisthefeaturespace,aninitialpayloadp0
andathresholdt,i.e.,aconfidencevalueunderwhichapayloadis
representedby0.
consideredharmless.WAF-A-MoLEimplementsthepayloadpool
3 OVERVIEWOFWAF-A-MOLE (seeSection3.3)asapriorityqueueQ(line1).ThepayloadsinQ
areprioritizedaccordingtotheconfidencevaluereturnedbythe
Ourmethodologybelongstotheclassofguidedmutationalfuzz
classificationalgorithm,namelyclassify,associatedtom.Theclas-
testingapproaches[17,38].Briefly,theideaistostartfromafailing
sificationalgorithmassignstoeachpayloadanx ∈X,byextracting
test,thatgetsrepeatedlytransformedthroughtherandomappli-
afeaturevector,andcomputesm(x).
cationofsomepredefinedmutationoperators.Themodifiedtests,
Initially,Qonlycontainsp0(lines2–3).Themainloop(lines4–7)
behavesasfollows.TheheadelementofQ,i.e.,thepayloadhaving
1https://modsecurity.org
thelowestconfidencescore,isextractedandmutated(line5),by
2https://www.fortinet.com/blog/business-and-technology/fortiweb-release-6-0--ai-
applyingasetofmutationoperators(seeSection3.2).Theobtained
based-machine-learning-for-advanced-thr.html
3https://www.paloaltonetworks.com/detection-response payload,p,isfinallyclassified(line6)anden-queued(lines7).The
2

Operator Shortdefinition Example
CaseSwapping CS(...a...B...)→...A...b... CS(admin' OR 1=1#)→ADmIn' oR 1=1#
WhitespaceSubstitution WS(...k1k2...)→...k1␣k2... WS(admin' OR 1=1#)→admin'\n OR \t 1=1#
CommentInjection CI(...k1k2...)→...k1 /**/k2... CI(admin' OR 1=1#)→admin'/**/OR 1=1#
CommentRewriting CR(.../*s0 */...#s1 )→.../*s
0
′*/...#s
1
′ CR(admin'/**/OR 1=1#)→admin'/*abc*/OR 1=1#xyz
IntegerEncoding IE(...n...)→...0x[n] 16 IE(admin' OR 1=1#)→admin' OR 0x1=1#
OperatorSwapping OS(...⊕...)→...⊞...(with⊕≡⊞) OS(admin' OR 1=1#)→admin' OR 1 LIKE 1#
LogicalInvariant LI(...e...)→...eAND⊤... LI(admin' OR 1=1#)→admin' OR 1=1 AND 2<>3#
Table1:Listofmutationoperators.
terminationofthealgorithmoccurswhenapreceivesascoreless labeledwithapossibleclassificationvalue(inpercentage).The
orequaltothethresholdt (line4). correspondingqueueisgivenbythesequenceofthenodesinthe
mutationtreeorderedbytheassociatedclassificationvalue.
3.2 Mutationoperators Afterapplyingamutation(actuallyafterafullmutationround,
Amutationoperatoris afunctionthatchangesthe syntaxofa seeSection3.4),thepayloadisevaluatedandaddedtothepriority
payloadsothatthesemanticsoftheinjectedqueriesispreserved. queue,alongwithinformationaboutthepayloadthatgenerated
Belowwedescribetheconsideredmutationoperators. it.Keepingallindividualsintheinitialpopulationhelpsavoiding
CS.TheCaseSwappingoperatorrandomlychangesthecapitaliza- localminima:whenapayloadisunabletocreatebetterpayloads,
tionofthekeywordsinaquery(e.g.,SelecttosELecT).SinceSQL thealgorithmtriestobacktrackonoldpayloadstocreateanew
iscaseinsensitive,thesemanticsofthequeryisnotaffected. branchonthemutationtree.
WS.WhitespaceSubstitutionreliesontheequivalencebetweensev-
3.4 Efficiency
eralalternativecharactersthatonlyactasseparators(whitespaces)
betweenthequerytokens.Forinstance,whitespacesinclude\n The main bottleneck of our algorithm is the classification step.
(linefeed),\r(carriagereturn)and\t(horizontaltab).Eachofthese Indeed,theclassificationofapayloadrequirestheextractionof
characterscanbereplacedbyanarbitrary,non-emptysequenceof a vector of features. Although a WAF classifier is efficient, the
theotherswithoutalteringthesemanticsofthequery. featureextractionprocessmayrequirenon-negligiblestringparsing
IC.Inlinecomments(/*...*/)canbearbitrarilyinsertedbetween operations(seeSection4).Forexample,theprocedurecarriedout
thetokensofaquery.Sincecommentsarenotinterpreted,theyare byatoken-basedclassifier(seeSection4.2fordetails)requiresnon-
semanticspreserving.TheCommentInjectionoperatorrandomly trivialcomputationtoparsetheSQLquerylanguage(beingcontext
addsinlinecommentsbetweenthetokens. free).Instead,allthemutationoperatorsdescribedinSection3.2
CR.Followingtheabovereasoning,theCommentRewritingopera- relyonefficientstringparsing,basedonregularexpressions.
torrandomlymodifiesthecontentofacomment. Wemitigatethisissuebyfollowingamutationpreemptionstrat-
IE.TheIntegerEncodingoperatormodifiestherepresentationof egy,i.e.,wecreateamutationroundwheremultiplepayloadsare
numericalconstants.Thisincludesalternativebaserepresentations, generatedatonce.Allthesemutatedpayloadsarestoredforthe
e.g.,fromdecimaltohexadecimal,aswellasstatementnesting,e.g., classification.Thenwerunalltheclassificationstepsinparallel
(SELECT 42)isequivalentto42. andwedischargethemutantsthatincreasetheclassificationvalue
OS.Someoperatorscanbereplacedbyothersthatbehaveinthe oftheirparent.Inthiswaywetakeadvantageoftheparallelization
same way. For instance, the behavior of = (equality check) can supportofmodernCPUs.
besimulatedbyLIKE(patternmatching).Wecallthismutation Formemoryefficiency,weonlyenqueueamutatedpayloadif
OperatorSwapping. itimprovestheclassificationvalueofitsparent.Inthiswaywe
LI.ALogicalInvariantoperatormodifiesabooleanexpressionby mitigatethepotential,exponentialblow-upofthemutationtree
addingopaquepredicates.4 (seeSection3.3).Onthenegativeside,eachbranchofthemutation
Table1providesacompactlist,includingashort,mnemonic treeonlyevolvesmonotonicallywhichmightresultinthealgorithm
definition,oftheoperatorsdescribedabove. stagnatingonlocalminima.However,ourexperimentsshowthat
this does not prevent our algorithm from finding an injectable
3.3 Mutationtree
payload(seeSection5).
ThepriorityqueueofFigure3containsasequentialrepresentation
ofmutationtree.Startingfromarootelement,i.e.,theinitialpayload 4 WAFTRAININGANDBENCHMARKING
(p0inFigure3),amutationtreecontainselementsobtainedthrough Ourtechniqueappliestoaninputmodelrepresentingawell-trained
theapplicationofsomemutationoperator.Apossibleinstanceof WAF,i.e.,aWAFthateffectivelydetectsmaliciouspayloads.Ideally,
amutationtreeisshowninFigure4.Eachedgeislabeledwith togenerateapayloadthatbypassesadeployedWAF,theinput
anidentifieroftheappliedmutationoperator.Also,eachnodeis algorithmshouldrelyonthesamedetectionmodel.Inthecaseof
4Thatis,heuristicallygeneratedtrueandfalseexpressionstobecombinedinconjunc- ML-basedWAF,themodelistheresultofthetrainingprocessover
tionanddisjunction(respectively)withthepayloadclauses. asampledataset,whileforsignature-basedWAFsthemodelisthe
3

Figure4:Apossiblemutationtreeofaninitialpayload.
setofallthecollectedsignaturesthatareusedasacomparisonfor Dmayoptionally(squarebrackets)terminatewithaLIMITclause.
futureinputdata. Thequeriesoperateonseveralparametertypes,includingfieldsf,
Unfortunately, it is very common that neither the detection tablest,valuesv,stringss andbooleanexpressionse,e′.Finally,
modelnorthetrainingdatasetarepubliclyavailable.Reasonably, weuse¯·todenoteavector,i.e.,afinite,comma-separatedlistof
thishappensbecausetheWAFmanufacturers(correctly)consider elements.Theactualvaluesfort and f aretakenfromanactual
suchknowledgeanadvantagefortheadversary.Remarkably,this targetdatabase(thisfeatureisprovidedbyrandgen).Forv,weuse
alsohappensfortheresearchprototypes.5Thus,wehadtocreate differentvaluesdependingonthetypeofquerywewanttogener-
atrainingdatasetandconfiguretheclassificationalgorithms.The ate.Forthebenignqueries,wegeneratepayloadswitharandom
followingsectionsdescribetheissueswefacedduringthisprocess generator,adictionaryofnations,adictionaryofvalueswhich
andhowwesolvedthem. arecompatiblewiththefieldtypetosimulatearealapplication
payload.Forexample,inadatabasecontainingpeoplenameswe
4.1 Dataset useEnglishfirstandlastnames.Weareinterestedinthestructure
Tothebestofourknowledge,nodatasetofbenignSQLqueriesis ofthequery,hencethesevaluesforthepayloadaresuitableforour
publiclyavailable.Themainreasonisprobablythatthenotionof analysis.
“benign”isapplication-dependentandnouniversaldefinitionexists. As mentioned above, the malicious values are generated by
Ontheotherhand,therearemanymaliciouspayloads,thatone sqlmapandOWASPZAP.
canextractfromexistingpenetrationtestingtoolssuchassqlmap6
andOWASPZAP7.Weconsiderthepayloadsgeneratedbythese 4.2 Classificationalgorithms
tools,asanyWAFshouldbetrainedonwell-knownattacks. Belowwedescribetheclassificationalgorithmsthatweusedfor
Webuiltourdatasetthroughanautomaticprocedure8.Inpar- ourexperiments.Inparticular,weconsiderdifferenttechniques,
ticular,weusedrandgen9 togeneratethequeries.Startingfrom builtonthreefeatureextractionmethods:characters,tokenand
agrammarG,thetoolreturnsasetofqueriesthatbelongtothe graphbased.
languagedenotedbyG.Noticeably,queriesgeneratedbyrandgen
Character-basedfeatures. WAF-Brain10isbasedonarecurrent-
alsoincludeactualvalues,e.g.,tableandcolumnnames,referring
neuralnetwork.Thenetworkdividestheinputqueryinblocks
toagivenexistingdatabase.Thus,thequeriesinthedatasetcanbe
of exactly five consecutive characters. Its goal is to predict the
submittedandevaluatedagainstarealtarget.
sixthcharacterofthesequencebasedonthepreviousfive.Ifthe
Tocreateourlabeleddataset,weassumethatSQLqueriesare
predictioniscorrect,theblockofcharactersismorelikelytobe
alwayscreatedbytheapplicationwhenausersubmitsapayload,
partofamaliciouspayload.Thisprocessisrepeatedforeveryblock
eitherbenignormalicious.Tosimulatethisbehavior,wegenerate
offivecharactersformingthetargetquery.
asingleinitialgrammarthatsupportsmultiplequerytypes.Then,
TheneuralnetworkofWAF-Brainisstructuredasfollows.The
weprovidedifferentdictionariesofvaluesforeachterminalsymbol
inputlayerisaGatedRecurrentUnit(GRU)[12]madeoffiveneu-
(i.e.,t,f,v)thatrepresentsapossiblevalueofaparticularcolumn
rons,followedbytwofully-connectedlayers,i.e.,adropoutlayer
insidethedatabase.
followedbyanotherfullyconnectedlayer.Finally,WAF-Braincom-
Thequerygrammaristhefollowing.
putestheaverageofallthepredictionerrorsovertheinputquery
Q ::= S|U |D|I
S ::= SELECT(f¯|∗)FROMt WHEREe[LIMITv¯] andscoresitasmaliciousiftheresultisaboveafixedthreshold
U ::= UPDATEt SETf =vWHEREe[LIMITv¯] chosenaprioribytheuser.Sincethethresholdisnotgivenbythe
classifieritself,asalltheotherdetailsofthetrainingandcross-
D ::= DELETEFROMt WHEREe[LIMITv¯]
I ::= INSERTINTOt (f¯)VALUES(v¯) validationphases,wesetitto0.5,whichisthestandardthreshold
e ::= f ⋛v|f LIKEs|eANDe′|eORe′ forclassificationtasks.
Token-basedfeatures. Thetoken-basedclassifiersrepresentinput
Briefly,thequeriesQcanbeselectS,updateU,deleteDorinsert
queries as histograms of symbols, namely tokens. A token is a
I.Thesyntaxofeachqueryisstandard,onlynoticethatS,U and
portionoftheinputthatcorrespondstosomesyntacticgroup,e.g.,
5AllmaintainersoftheWAFsconsideredinthisworkwerecontacted,butnoone akeyword,comparisonoperatorsorliteralvalues.
providedtheirdatasets. WetookinspirationfromthereviewwrittenbyKomiyaetal.[28]
6https://github.com/sqlmapproject/sqlmap
7https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project andJoshietal[24]andwedevelopedatokenizerforproducing
8Thedatasetisavailableathttps://github.com/blindusername/wafamole-dataset
9https://github.com/MariaDB/randgen 10https://github.com/BBVA/waf-brain
4

C γ avд(A) σ A R P
NaiveBayes / / 54.2% 1.0% Paranoia1/2 86.10% 86.10% 100%
RandomForest / / 87.3% 0.7% ModSecurityCSR Paranoia3/4 91.85% 91.85% 100%
Token-based
LinearSVM 19.30 / 80.5% 1.4% Paranoia5 96.46% 96.46% 100%
GaussianSVM 278.25 0.013 93.1% 0.9%
WAF-Brain RNN 98.27% 96.73 99.8%
Dir.Prop. 4.64 0.26 99.85% 0.07%
NaiveBayes 50.16% 98.71% 50.08%
Undir.Prop. 2.15 0.71 99.10% 0.2%
SQLiGoT Randomforest 98.33% 98.33% 100%
Dir.Unprop. 2.15 0.26 99.74% 0.1% Token-based
LinearSVM 98.75% 98.76% 100%
Undir.Unprop. 2.15 0.26 98.89% 0.2%
GaussianSVM 97.82% 97.82% 100%
Table2:Trainingphaseresults.
Dir.Prop. 90.61% 97.30% 85.82%
Undir.Prop. 96.38% 97.31% 95.54%
SQLiGoT
Dir.Unprop. 90.52% 97.12% 85.80%
Undir.Unprop. 96.25% 97.05% 95.53%
thefeaturesvectortobeusedbythesemodels.Ontopofthat,we
Table3:Benchmarktable.
implementeddifferentmodels:(i)aNaiveBayes(NB)classifier,(ii)
arandomforest(RF)classifierwithanensembleof25trees,(iii)
alinearSVM(L-SVM),andagaussianSVM(G-SVM).Wetrained
themusinga5-foldcross-validationwith20,000sanequeriesand
differentSQLiGoTclassifiers.Boththehyper-parametersandthe
20,000injections,andweused15%ofthequeriesforthevalidation
scoresarealmostthesameforallthedifferentversionsofSQLiGoT.
set.Tothisextent,wecodedourexperimentusingscikit-learn[33],
whichisaPythonlibrarycontainingalreadyimplementedmachine
4.3 Benchmark
learningalgorithms.Afterthefeatureextractionphase,thenumber
Wecarriedoutbenchmarkexperimentstoassessthedetectionrates
ofsamplesdroppedto768benignand7,963injectionqueries.The
oftheclassifiersdiscussedabove.Foralltheclassifiersusedforthis
tokenizationmethodisbasicallyanaggregationmethod:onlya
benchmark,weformedadatasetof8,000sanequeriesand8,000
subsetofallsymbolsaretakenintoaccount.Thedatasetisunbal-
SQLinjectionqueries,andweclassifiedthemusingthemodelswe
anced,asthevarietyofsanequeriesisoutnumberedbythevariety
havetrained.Table3showstheresultsofourexperiment.
ofSQLinjections.Toaddressthisissue,wesetupscikit-learnac-
Weevaluatedtheperformanceofeachclassifierbyaccounting
cordingly,byusingalossfunctionthattakesintoaccounttheclass
threedifferentmetrics:(i)accuracy,(ii)recall,and(iii)precision.
imbalance[9].Table2showstheresultsofthetrainingphasewhere
(i)Cistheregularizationparameter[36]thatcontrolsthestability WedenotethetruepositivesasTP,truenegativesasTN,false
ofthesolution,(ii)γ isthekernelparameter(onlyforthegaussian positivesasFP andfalsenegativesasFN.Accuracyiscomputed
SVM)[1,21],and(iii)avд(A)andσ aretheaverageandstandard asA = TP+T T N P+ + T F N P+FN ,recalliscomputedasR = TP T + P FN and
deviationoftheaccuracycomputedduringthecross-validation precisioniscomputedasP = TP T + P FP .Theaccuracymeasureshow
phaseoverthevalidationset. many samples have been correctly classified, i.e., a sane query
classifiedassaneoraninjectedqueryclassifiedasmalicious.The
Graph-basedfeatures. Karetal.[25]developedSQLiGoT,anSQL recallmeasureshowgoodtheclassifierisatidentifyingsamples
injectiondetectorthatrepresentsaSQLqueryasagraph,both fromtherelevantclass,inthiscasetheinjectionpayloads.Scoring
directed and undirected. Each node in this graph is a token of ahighrecallvaluemeansthattheclassifierlabeledmostofthereal
theSQLlanguage,plusallsystemreservedanduserdefinedtable positivesinthedatasetaspositives.Theprecisionmeasureshow
names,variables,procedures,viewsandcolumnnames.Moreover, manyofthesamplesclassifiedasrelevantareactuallyrelevant.
theedgesareweighteduniformlyorproportionallytothedistances SincetheNaiveBayesalgorithmtriestodiscriminatebetween
in terms of adjacency. We omit all the details of the model, as inputclassesbyconsideringeachvariableindependentonetoan-
theyarewelldescribedinthepaper.Karetal.releasedthehyper- other,itmissestherealstructureoftheSQLsyntax.Hence,itcannot
parameter they found on their dataset, but since bothC andγ properlycapturethecomplexityoftheproblem.Allotherclassi-
dependondata,wehadtotrainthesemodelsfromscratch. fiersmaybecomparedwithdifferentlevelsofparanoiaoffered
We performed a 10-fold cross-validation for SQLiGoT, using byModSecurity,showingtheireffectivenessasWAFs.WAF-Brain
20,000benignand20,000maliciousqueries,againusingthescikit- resultsarecomparabletowhattheauthorclaimsonhisGitHub
learn library. After the feature extraction phase, the dataset is repository.
shrunkto:(i)3216sane12,659andmaliciousdataforthedirected
graphversions,(ii)and3268sane12,682andmaliciousdataforthe 5 EVADINGMACHINELEARNINGWAFS
undirectedgraphversionsofSQLiGoT.Again,manyqueriespossess
Inthissection,weexperimentallyassessWAF-A-MoLEagainstthe
thesamestructureasothers,andthisislikelytohappenforsane
classifiersintroducedabove.Theexperimentswereperformedona
queries.Asalreadysaidinthepreviousparagraph,wearedealing DigitalOcean11dropletVMwith6CPUsand16GBofRAM.Fora
withimbalancebetweenthetwoclasses,andwetreatthisissueby
baselinecomparisonweusedanunguidedmutationalfuzzer.The
usingabalancedaccuracylossfunction,providedbythescikit-learn
framework.Table2showstheresultofthetrainingphaseofthe 11https://www.digitalocean.com/
5

WAF-Brain TokenRF TokenNB WAF-Brain TokenRF TokenNB
100 100 100 100 100 100
0 0 0 10 0 0
TokenL-SVM TokenG-SVM SQLiGoTUU TokenL-SVM TokenG-SVM SQLiGoTUU
100 100 100 100 100 100
0 0 20 0 0 95
SQLiGoTDU SQLiGoTDP SQLiGoTUP SQLiGoTDU SQLiGoTDP SQLiGoTUP
100 100 100 100 100 100
20 0 0 60 20 99.999
0 300 600 0 300 600 0 300 600 10−310−1101 10−310−1101 10−310−1 101
Figure5:Guided(solid)vs.unguided(dotted)searchstrategiesappliedtoinitialpayloadadmin’ OR 1=1#.
unguidedfuzzerrandomlyappliesthemutationoperatorsofSec- Findingadversarialexamplesisnon-trivial. SQLiGoTclassifiers
tion3.2.Moreover,weexecuted100instancesoftheunguidedfuzzer resisttheunguidedevaluationasitisunlikelythatamutationcan
oneachclassifier.Then,wecomparedasinglerunofWAF-A-MoLE movethesampleawayfromaplateauregionwheretheconfidence
againstthebestpayloadgeneratedbythe100unguidedinstances ofbeingaSQLinjectionishigh.Themainreasonsare:(i)SQLiGoT
overtime.BoththeWAF-A-MoLEandtheunguidedfuzzerswere considered a large number of tokens (so reducing the collision
configuredtostartfromthepayloadadmin' OR 1=1#,initially problemthataffectsotherclassifiers,sincethecompressionfactor
detectedwith100%confidencebyeachclassifier. appliedbythefeatureextractorislower);(ii)Thestructureofthe
featurevectorisinherentlyredundant,i.e.,eachpairofadjacent
5.1 Assessmentresults variablesdescribethesametoken;(iii)themodelsareregularized,
hencethedecisionfunctionissmootherbetweeninputpointsand
Figure5showstheevolutionoftheconfidencescoreforeachclas-
itmanagestogeneralizeovernewsamples.
sifier.Ineachplot,wecomparethebestsampleobtainedbyWAF-
A-MoLE(solidline)andthebestsamplegeneratedbyallthe100 WAF-A-MoLEeffectivelyevadesWAFs. Movingrandomlyinthe
processesoftheunguidedfuzzer(dashedline). inputspaceisnotaneffectivestrategy.WAF-A-MoLEfindsadver-
Thefirstgroupofplots(left)showtheevolutionoftheconfi- sarialsamplesbyleveragingonhintsgivenbyclassifieroutputs.
dencescoresagainstthenumberofmutationrounds.Thesecond Theguidedapproachaccomplisheswhattheunguidedapproach
group(right),showstheconfidencescoreovertheactualtimeof failedto,bymovingpointsawayfromplateausandputtingthem
computation.Inparticular,weshowthefirst10secondsofcompu- inregionsoflowconfidenceofbeingrecognizedasSQLinjection.
tation.Sincesomescoresquicklydegradeinthefirstmilliseconds Moreover,amongtheSQLiGoTclassifiers,theundirectedunpro-
ofcomputation,wereportthex axisinlogscale. portionalisthemostresilientvariant.Recallingthedefinitionof
thealgorithm[25],thefeatureextractorassignsuniformweights
5.2 Interpretationoftheresults
totokensinthesamewindowinsteadofbalancingthescorew.r.t.
Ourexperimentshighlightafewfactsthatwediscussbelow. thedistanceofthecurrenttoken.Hence,theclassifiergainssome
invarianceoverthesequenceofextractedtokens,makingitmore
Featurechoicematters. AsexplainedinSection4.2,alltheconsid- robusttoadversarialnoise.
eredclassifiersarebasedonsyntacticfeatures.However,different
featuresetchangetherobustnessofaclassifier.Forinstance,WAF- 5.3 Discussionandlimitations
Brainquicklylostconfidencewhenthepayloadmutated,because
Ourexperimentsshowthat,startingfromatargetmaliciouspay-
WAF-Brainistrainedfromuninterpreted,fixed-lengthsequences
loads,WAF-A-MoLEeffectivelydegradestheconfidencescoresof
ofcharactersandourmutationoperatorscanenlargeapayload
theconsideredclassifiers.Inthissectionwediscussimplications
beyondtheadequacyofthelengthassumedbyWAF-Brain.Also
andlimitationsofthisresult.
Token-basedclassifiersdonotperformwellagainstmutations.The
reasonisthatmaliciousandbenignpayloadsoverlapinthefeature Generalityoftheexperiments. AsdiscussedinSection4.1,the
space.AllSQLiGoTversionsshowedtoberobustagainsttheun- classifiersweretrainedwithadatasetthatwehadtobuildfrom
guidedapproach.TheseclassifiersusetheSVMalgorithmassome scratch.Thishasclearconsequencesonourexperimentalresults.
ofthetokenbasedclassifiers,buttheirfeaturesetimposesmore Hence,toextendthevalidityofourresults,newexperimentsshould
structureinsidethefeaturerepresentation.Hence,randommuta- beexecutedfromother,real-world,datasets.
tionshaveanegligibleprobabilitytoevadethem.Instead,since Anotherlimitationisthatwedidnottakeintoaccountthero-
WAF-A-MoLEreliesonaguidedstrategy,itcaneffectivelycraft bustnessofWAFscombiningsignaturesandMLtechniques,called
adversarialexamples(althoughmoreeffortisneeded). hybrid.Thesesystemsarebecomingmoreandmorecommon.
6

Adversarialattacksmitigation. Demontisetal.[15]showedthe directions:visualizationanddetection,achievedbyamulti-agent
effectofthepresenceofregularizationwhenaclassifierisunder systemcalledidMAS-SQL.TotacklethetaskofdetectingSQLin-
attack.Withoutregularizationanattackermaycraftanadversarial jectionattacks,theauthorssetuptwodifferentclassifiers,namely
exampleagainstthetarget,duetothehighirregularityofthevictim aNeuralNetworkandanSVM.Makiouetal.[29]developedan
function. Adding the regularization parameter has the effect of hybridapproachthatusesbothmachinelearningtechniquesand
smoothingthedecisionboundaryofthefunctionbetweensamples, patternmatchingagainstaknowndatasetofattacks.Thelearning
reducingtheamountoflocalminimaandmaxima.Ontopofthat, algorithmusedfordetectinginjectionsisaNaiveBayes[30].They
theadversaryneedstoincreasetheamountofperturbationstocraft lookfor45differenttokensinsidetheinputquery,chosenbydo-
adversarialexamples.Allmodelswetrainedhavebeenproperly mainexperts.Similarly,Joshietal.[24]useaNaiveBayesclassifier
regularized. that,givenaSQLqueryasinput,extractssyntactictokensusing
Grosseetal.[19]proposethesocalledadversarialtraining,that spacesasseparator.Thealgorithmproducesafeaturevectorthat
basicallyisare-fitoftheclassifieralsoincludingtheattackpoints. countshowmanyinstancesofaparticularwordoccursintheinput
Thisdefensesystemleadstobetterrobustnessagainstadversarial query.Thevocabularyofallthepossibleobservabletokensisset
examples,atthecostofworseaccuracyscores.Again,asshownby apriori.Komiyaetal.[28]proposeasurveyofdifferentmachine
Carlinietal.[10]thisisnotasolution,butitmayslowdownthe learningalgorithmsforSQLinjectionattackdetection.
adversaryinfindingadversarialexamples. Evading machine learning classifiers: The techniques that are
usedinthestateoftheartaredividedintwodifferentcategories:
(i)gradientand(ii)black-boxmethods.Foracomprehensiveex-
6 RELATEDWORK
planationofthesetechniques,Biggioetal.[8]exposethestateof
Inthissection,wepresentsomeworkrelatedtoWAFs,aswellas theartofadversarialmachinelearningindetail.Theattackercan
evasiontechniquesthathavebeenproposedtobypassthem. computethegradientofthevictimclassifierw.r.t.theinputthey
Attacksagainstsignature-basedWAFs:Appeltetal.[3,4]pro- usetotesttheclassifier.Biggioetal.[7]proposeatechniquefor
poseatechniquetobypasssignature-basedWAFs.Theirtechnique findingadversarialexamplesagainstbothlinearandnonlinear
is a search-based approach in which they create new payloads classifiers,byleveragingontheinformationgivenbythegradient
fromexistingblockedpayloads.Theproblemwithimplementinga ofthetargetmodel.Similarly,Goodfellowetal.[18]presentFast
search-basedapproachinthiscontextishard:theobviousevalu- GradientSignMethod(FGSM),whichisusedtoperturbimagesto
ationfunctionforapayloadagainstthetargetWAFisadecision shifttheconfidenceoftherealclasstowardsanotherone.Papernot
functionwithvaluesPASSED/BLOCKED.Search-basedapproaches etal.[32]proposeanattackthatcomputesthebesttwofeaturesto
performpoorlyiftheevaluationfunctionhasmanyplateaus.To perturbinordertomostincreasetheconfidenceofitbelongingto
mitigatethisissue,theauthorsproposeanapproximateevaluation acertainclass.Thismethodleveragesongradientinformationtoo.
functionwhichreturnstheprobabilityofapayloadofbeing“near” Iftheattackerhasinformationregardingaparticularsystem,but
thePASSEDorBLOCKEDstate.Inthebestcasescenario,thisfunc- theycannotaccessit,theycantrytolearnasurrogateclassifier,
tionsmoothstheplateauandthesearchalgorithmconvergesto asproposedbyPapernotetal.[31].Manypapersthatcraftattacks
thePASSEDstate. inotherdomains[14,27,35]belongtothiscategory.Iftheattacker
AutomatabasedWAFs:Halfondetal.[20]proposeAMNESIA, doesnothaveaccesstothemodel,ortheyhavenoinformation
atooltodetectandpreventSQLinjectionattacks.Thealgorithm onhowtoreconstructitlocally,theytreatthiscaseasablack-box
worksbycreatingaNon-DeterministicFiniteAutomarepresenting optimizationproblem.Ilyasetal.[23]applyanevolutionstrategy
alltheSQLqueriesthattheapplicationcangenerate.Themain tolimitthenumberofqueriesthataresenttothevictimmodel
issues with this approach are that an attack can bypass it (i) if tocraftanadversarialexample.Xuetal.[37]proposeatechnique
the model is too conservative and includes queries that cannot thatusesageneticalgorithmforcraftingadversarialexamplesthat
begeneratedbytheapplicationor(ii)iftheattackhasthesame bypassPDFmalwareclassifiers.Andersonetal.[2]evadedifferent
structureofaquerygeneratedbytheapplication.Bandhakaviet malwaredetectorsbyalteringmalwaresamplesusingsemantics
al.[5]developedCANDID,atoolthatdetectsSQLinjectionattempts invarianttransformations,byleveragingonlyonthescoreprovided
via candidate selection. This approach consists of transforming bythevictimclassifier.
queriesintoacanonicalformandevaluatingeachincomingquery
againstcandidateonesgeneratedbytheapplication.
MachinelearningWAFs:Ceccatoetal.[11]proposeaclustering
7 CONCLUSION
methodfordetectingSQLinjectionattacksagainstavictimservice.
Thealgorithmlearnsfromthequeriesthatareprocessedinsidethe Weprovidedexperimentalevidencethatmachinelearningbased
webapplicationunderanalysis,usinganunsupervisedone-class WAFscanbeevaded.Ourtechniquetakesadvantageofanadver-
learningapproach,namelyK-medoids[26].Newsamplesarecom- sarialapproachtocraftmaliciouspayloadsthatareclassifiedas
paredtotheclosestmedoidandflaggedasmaliciousiftheiredit benign.Moreover,weshowedthatWAF-A-MoLEefficientlycon-
distancew.r.t.thechosenmedoidishigherthanthediameterofthe vergestobypassingpayloads.Weshowtheresultsofthistechnique
cluster.Karetal.[25]developSQLiGoT,asupportvectormachine appliedtoexistingWAFs,bothviaaguidedandunguidedapproach.
classifier(SVM)[13]thatexpressesqueriesasgraphsoftokens, Weleveragedonasetofsyntacticmutationsthatdonotalterthe
whoseedgesrepresenttheadjacencyofSQL-tokens.Thisisthe originalsemanticsoftheinputquery.Finally,webuiltadatasetof
classifierweusedinouranalysis.Pinzonetal.[34]exploretwo SQLqueriesandwereleaseditpublicly.
7

Our work highlights that machine learning based WAFs are [23] AndrewIlyas,LoganEngstrom,AnishAthalye,andJessyLin.2018. Black-
exposedtoaconcreteriskofbeingbypassed.Futuredirections boxadversarialattackswithlimitedqueriesandinformation. arXivpreprint
arXiv:1804.08598(2018).
includetestingWAFsbasedonothertechniquessuchashybrid
[24] AnamikaJoshiandVGeetha.2014.SQLInjectiondetectionusingmachinelearn-
ones,findingnewmutationstoimproveourapproach,andtake ing.In2014InternationalConferenceonControl,Instrumentation,Communication
advantageofouradversarialtechniquetoimprovedetectionof andComputationalTechnologies(ICCICCT).IEEE,1111–1115.
[25] DebabrataKar,SuvasiniPanigrahi,andSrikanthSundararajan.2016.SQLiGoT:
maliciouspayloads. DetectingSQLinjectionattacksusinggraphoftokensandSVM.Computers&
Security60(2016),206–225.
[26] LeonardKaufmannandPeterRousseeuw.1987.ClusteringbyMeansofMedoids.
REFERENCES DataAnalysisbasedontheL1-NormandRelatedMethods(011987),405–416.
[27] BojanKolosnjaji,AmbraDemontis,BattistaBiggio,DavideMaiorca,Giorgio
[1] MarkAAizerman.1964. Theoreticalfoundationsofthepotentialfunction Giacinto,ClaudiaEckert,andFabioRoli.2018. AdversarialMalwareBinaries:
methodinpatternrecognitionlearning.Automationandremotecontrol25(1964), EvadingDeepLearningforMalwareDetectioninExecutables.arXivpreprint
821–837. arXiv:1803.04173(2018).
[2] HyrumSAnderson,AnantKharkar,BobbyFilar,andPhilRoth.2017.Evading [28] RyoheiKomiya,IncheonPaik,andMasayukiHisada.2011. Classificationof
machinelearningmalwaredetection.BlackHat(2017). maliciouswebcodebymachinelearning.In20113rdInternationalConferenceon
[3] DennisAppelt,CuDNguyen,andLionelBriand.2015.Behindanapplication AwarenessScienceandTechnology(iCAST).IEEE,406–411.
firewall,arewesafefromsqlinjectionattacks?.In2015IEEE8thInternational [29] AbdelhamidMakiou,YoucefBegriche,andAhmedSerhrouchni.2014.Improving
ConferenceonSoftwareTesting,VerificationandValidation(ICST).IEEE,1–10. WebApplicationFirewallstodetectadvancedSQLinjectionattacks.In201410th
[4] DennisAppelt,CuDNguyen,AnnibalePanichella,andLionelCBriand.2018. InternationalConferenceonInformationAssuranceandSecurity.IEEE,35–40.
Amachine-learning-drivenevolutionaryapproachfortestingwebapplication [30] MelvinEarlMaron.1961.Automaticindexing:anexperimentalinquiry.Journal
firewalls.IEEETransactionsonReliability67,3(2018),733–757. oftheACM(JACM)8,3(1961),404–417.
[5] SruthiBandhakavi,PrithviBisht,PMadhusudan,andVNVenkatakrishnan.2007. [31] NicolasPapernot,PatrickMcDaniel,IanGoodfellow,SomeshJha,ZBerkay
CANDID:preventingsqlinjectionattacksusingdynamiccandidateevaluations. Celik,andAnanthramSwami.2017.Practicalblack-boxattacksagainstmachine
InProceedingsofthe14thACMconferenceonComputerandcommunications learning.InProceedingsofthe2017ACMonAsiaConferenceonComputerand
security.ACM,12–24. CommunicationsSecurity.ACM,506–519.
[6] MarcoBarreno,BlaineNelson,RussellSears,AnthonyDJoseph,andJDoug [32] NicolasPapernot,PatrickMcDaniel,SomeshJha,MattFredrikson,ZBerkayCelik,
Tygar.2006.Canmachinelearningbesecure?.InProceedingsofthe2006ACM andAnanthramSwami.2016. Thelimitationsofdeeplearninginadversarial
SymposiumonInformation,computerandcommunicationssecurity.ACM,16–25. settings.InSecurityandPrivacy(EuroS&P),2016IEEEEuropeanSymposiumon.
[7] BattistaBiggio,IginoCorona,DavideMaiorca,BlaineNelson,NedimŠrndić, IEEE,372–387.
PavelLaskov,GiorgioGiacinto,andFabioRoli.2013. Evasionattacksagainst [33] F.Pedregosa,G.Varoquaux,A.Gramfort,V.Michel,B.Thirion,O.Grisel,M.
machinelearningattesttime.InJointEuropeanconferenceonmachinelearning Blondel,P.Prettenhofer,R.Weiss,V.Dubourg,J.Vanderplas,A.Passos,D.Cour-
andknowledgediscoveryindatabases.Springer,387–402. napeau,M.Brucher,M.Perrot,andE.Duchesnay.2011.Scikit-learn:Machine
[8] BattistaBiggioandFabioRoli.2018.Wildpatterns:Tenyearsaftertheriseof LearninginPython.JournalofMachineLearningResearch12(2011),2825–2830.
adversarialmachinelearning.PatternRecognition84(2018),317–331. [34] CristianIPinzon,JuanFDePaz,AlvaroHerrero,EmilioCorchado,JavierBajo,
[9] KayHenningBrodersen,ChengSoonOng,KlaasEnnoStephan,andJoachimM andJuanMCorchado.2013.idMAS-SQL:intrusiondetectionbasedonMASto
Buhmann.2010.Thebalancedaccuracyanditsposteriordistribution.In2010 detectandblockSQLinjectionthroughdatamining.InformationSciences231
20thInternationalConferenceonPatternRecognition.IEEE,3121–3124. (2013),15–31.
[10] NicholasCarliniandDavidWagner.2017. Adversarialexamplesarenoteas- [35] IshaiRosenberg,AsafShabtai,LiorRokach,andYuvalElovici.2018. Generic
ilydetected:Bypassingtendetectionmethods.InProceedingsofthe10thACM black-boxend-to-endattackagainststateoftheartAPIcallbasedmalware
WorkshoponArtificialIntelligenceandSecurity.ACM,3–14. classifiers.InInternationalSymposiumonResearchinAttacks,Intrusions,and
[11] MarianoCeccato,CuDNguyen,DennisAppelt,andLionelCBriand.2016. Defenses.Springer,490–510.
SOFIA:anautomatedsecurityoracleforblack-boxtestingofSQL-injection [36] AndreyNikolayevichTikhonov.1943.Onthestabilityofinverseproblems.In
vulnerabilities.InProceedingsofthe31stIEEE/ACMInternationalConferenceon Dokl.Akad.NaukSSSR,Vol.39.195–198.
AutomatedSoftwareEngineering.ACM,167–177. [37] WXu,YQi,andDEvans.2016.AutomaticallyEvadingClassifiers:ACaseStudy
[12] KyunghyunCho,BartVanMerriënboer,CaglarGulcehre,DzmitryBahdanau, onPDFMalwareClassifiers.NDSS.
FethiBougares,HolgerSchwenk,andYoshuaBengio.2014. Learningphrase [38] AndreasZeller,RahulGopinath,MarcelBöhme,GordonFraser,andChristian
representationsusingRNNencoder-decoderforstatisticalmachinetranslation. Holler.2019.Mutation-BasedFuzzing.InTheFuzzingBook.SaarlandUniversity.
arXivpreprintarXiv:1406.1078(2014). https://www.fuzzingbook.org/html/MutationFuzzer.htmlRetrieved2019-05-21
[13] CorinnaCortesandVladimirVapnik.1995.Support-vectornetworks.Machine 19:57:59+02:00.
learning20,3(1995),273–297.
[14] LucaDemetrio,BattistaBiggio,GiovanniLagorio,FabioRoli,andAlessandro
Armando.2019. ExplainingVulnerabilitiesofDeepLearningtoAdversarial
MalwareBinaries.arXivpreprintarXiv:1901.03583(2019).
[15] AmbraDemontis,MarcoMelis,MauraPintor,MatthewJagielski,BattistaBiggio,
AlinaOprea,CristinaNita-Rotaru,andFabioRoli.2018. OntheIntriguing
ConnectionsofRegularization,InputGradientsandTransferabilityofEvasion
andPoisoningAttacks.arXivpreprintarXiv:1809.02861(2018).
[16] JeremyD’Hoinne,AdamHils,andClaudioNeiva.2017.MagicQuadrantforWeb
ApplicationFirewalls.TechnicalReport.Gartner,Inc.
[17] ParulGarg.[n.d.]. Fuzzing–Mutationvs.Generation. https://resources.
infosecinstitute.com/fuzzing-mutation-vs-generation/. [Online;accessed29-
June-2019].
[18] IanGoodfellow,JonathonShlens,andChristianSzegedy.2015.Explainingand
HarnessingAdversarialExamples.InInternationalConferenceonLearningRepre-
sentations. http://arxiv.org/abs/1412.6572
[19] KathrinGrosse,PraveenManoharan,NicolasPapernot,MichaelBackes,and
PatrickMcDaniel.2017.Onthe(statistical)detectionofadversarialexamples.
arXivpreprintarXiv:1702.06280(2017).
[20] WilliamGJHalfondandAlessandroOrso.2005.AMNESIA:analysisandmonitor-
ingforNEutralizingSQL-injectionattacks.InProceedingsofthe20thIEEE/ACM
internationalConferenceonAutomatedsoftwareengineering.ACM,174–183.
[21] ThomasHofmann,BernhardSchölkopf,andAlexanderJSmola.2008. Kernel
methodsinmachinelearning.Theannalsofstatistics(2008),1171–1220.
[22] LingHuang,AnthonyDJoseph,BlaineNelson,BenjaminIPRubinstein,and
JDTygar.2011. Adversarialmachinelearning.InProceedingsofthe4thACM
workshoponSecurityandartificialintelligence.ACM,43–58.
8
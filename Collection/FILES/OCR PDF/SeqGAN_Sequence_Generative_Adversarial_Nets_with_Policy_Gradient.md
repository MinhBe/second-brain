Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence (AAAI-17)
SeqGAN: Sequence Generative
Adversarial Nets with Policy Gradient
LantaoYu,† WeinanZhang,†∗ JunWang,‡ YongYu†
†ShanghaiJiaoTongUniversity,‡UniversityCollegeLondon
{yulantao,wnzhang,yyu}@apex.sjtu.edu.cn,j.wang@cs.ucl.ac.uk
Abstract ofsequenceincreases.Toaddressthisproblem,(Bengioetal.
2015)proposedatrainingstrategycalledscheduledsampling
Asanewwayoftraininggenerativemodels,GenerativeAd- (SS),wherethegenerativemodelispartiallyfedwithitsown
versarialNet(GAN)thatusesadiscriminativemodeltoguide
syntheticdataasprefix(observedtokens)ratherthanthetrue
thetrainingofthegenerativemodelhasenjoyedconsiderable
datawhendecidingthenexttokeninthetrainingstage.Nev-
successingeneratingreal-valueddata.However,ithaslimi-
ertheless,(Husza´r2015)showedthatSSisaninconsistent
tationswhenthegoalisforgeneratingsequencesofdiscrete
trainingstrategyandfailstoaddresstheproblemfundamen-
tokens.Amajorreasonliesinthatthediscreteoutputsfromthe
generativemodelmakeitdifficulttopassthegradientupdate tally.Anotherpossiblesolutionofthetraining/inferencedis-
fromthediscriminativemodeltothegenerativemodel.Also, crepancyproblemistobuildthelossfunctionontheentire
thediscriminativemodelcanonlyassessacompletesequence, generatedsequenceinsteadofeachtransition.Forinstance,
whileforapartiallygeneratedsequence,itisnon-trivialto intheapplicationofmachinetranslation,ataskspecificse-
balanceitscurrentscoreandthefutureoneoncetheentire quencescore/loss,bilingualevaluationunderstudy(BLEU)
sequencehasbeengenerated.Inthispaper,weproposease- (Papinenietal.2002),canbeadoptedtoguidethesequence
quencegenerationframework,calledSeqGAN,tosolvethe
generation.However,inmanyotherpracticalapplications,
problems.Modelingthedatageneratorasastochasticpolicyin
suchaspoemgeneration(ZhangandLapata2014)andchat-
reinforcementlearning(RL),SeqGANbypassesthegenerator
bot(Hingston2009),ataskspecificlossmaynotbedirectly
differentiationproblembydirectlyperforminggradientpolicy
availabletoscoreageneratedsequenceaccurately.
update.TheRLrewardsignalcomesfromtheGANdiscrimi-
natorjudgedonacompletesequence,andispassedbackto Generaladversarialnet(GAN)proposedby(Goodfellow
theintermediatestate-actionstepsusingMonteCarlosearch. andothers2014)isapromisingframeworkforalleviatingthe
Extensiveexperimentsonsyntheticdataandreal-worldtasks aboveproblem.Specifically,inGANadiscriminativenetD
demonstratesignificantimprovementsoverstrongbaselines. learnstodistinguishwhetheragivendatainstanceisrealor
not,andagenerativenetGlearnstoconfuseDbygenerating
Introduction high quality data. This approach has been successful and
beenmostlyappliedincomputervisiontasksofgenerating
Generatingsequentialsyntheticdatathatmimicstherealone samplesofnaturalimages(Dentonetal.2015).
isanimportantprobleminunsupervisedlearning.Recently,
Unfortunately,applyingGANtogeneratingsequenceshas
recurrent neural networks (RNNs) with long short-term
twoproblems.Firstly,GANisdesignedforgeneratingreal-
memory(LSTM)cells(HochreiterandSchmidhuber1997)
valued,continuousdatabuthasdifficultiesindirectlygenerat-
haveshownexcellentperformancerangingfromnaturallan-
ingsequencesofdiscretetokens,suchastexts(Husza´r2015).
guagegenerationtohandwritinggeneration(Wenetal.2015;
ThereasonisthatinGANs,thegeneratorstartswithrandom
Graves 2013). The most common approach to training an
samplingfirstandthenadetermistictransform,govermented
RNN is to maximize the log predictive likelihood of each
bythemodelparameters.Assuch,thegradientoftheloss
true token in the training sequence given the previous ob-
fromD w.r.t.theoutputsbyGisusedtoguidethegenera-
servedtokens(Salakhutdinov2009).However,asarguedin
tive model G (paramters) to slightly change the generated
(Bengio et al. 2015), the maximum likelihood approaches
valuetomakeitmorerealistic.Ifthegenerateddataisbased
suffer from so-called exposure bias in the inference stage:
on discrete tokens, the “slight change” guidance from the
themodelgeneratesasequenceiterativelyandpredictsnext
discriminativenetmakeslittlesensebecausethereisprob-
tokenconditionedonitspreviouslypredictedonesthatmay
ably no corresponding token for such slight change in the
beneverobservedinthetrainingdata.Suchadiscrepancybe-
limiteddictionaryspace(Goodfellow2016).Secondly,GAN
tweentrainingandinferencecanincuraccumulativelyalong
canonlygivethescore/lossforanentiresequencewhenit
withthesequenceandwillbecomeprominentasthelength
hasbeengenerated;forapartiallygeneratedsequence,itis
∗WeinanZhangisthecorrespondingauthor. non-trivialtobalancehowgoodasitisnowandthefuture
Copyright(cid:2)c 2017,AssociationfortheAdvancementofArtificial scoreastheentiresequence.
Intelligence(www.aaai.org).Allrightsreserved. In this paper, to address the above two issues, we fol-
2852

low(BachmanandPrecup2015;Bahdanauetal.2016)and toadjusttheoutputcontinuously,whichdoesnotworkon
considerthesequencegenerationprocedureasasequential discretedatageneration(Goodfellow2016).
decision making process. The generative model is treated Ontheotherhand,alotofeffortshavebeenmadetogen-
asanagentofreinforcementlearning(RL);thestateisthe eratestructuredsequences.Recurrentneuralnetworkscanbe
generated tokens so far and the action is the next token to trainedtoproducesequencesoftokensinmanyapplications
begenerated.Unliketheworkin(Bahdanauetal.2016)that suchasmachinetranslation(Sutskever,Vinyals,andLe2014;
requires a task-specific sequence score, such as BLEU in Bahdanau,Cho,andBengio2014).Themostpopularwayof
machinetranslation,togivethereward,weemployadiscrim- trainingRNNsistomaximizethelikelihoodofeachtoken
inatortoevaluatethesequenceandfeedbacktheevaluation in the training data whereas (Bengio et al. 2015) pointed
toguidethelearningofthegenerativemodel.Tosolvethe out that the discrepancy between training and generating
problemthatthegradientcannotpassbacktothegenerative makesthemaximumlikelihoodestimationsuboptimaland
modelwhentheoutputisdiscrete,weregardthegenerative proposedscheduledsamplingstrategy(SS).Later(Husza´r
modelasastochasticparametrizedpolicy.Inourpolicygra- 2015)theorizedthattheobjectivefunctionunderneathSSis
dient,weemployMonteCarlo(MC)searchtoapproximate improperandexplainedthereasonwhyGANstendtogen-
thestate-actionvalue.Wedirectlytrainthepolicy(genera- eratenatural-lookingsamplesintheory.Consequently,the
tivemodel)viapolicygradient(Suttonetal.1999),which GANshavegreatpotentialbutarenotpracticallyfeasibleto
naturallyavoidsthedifferentiationdifficultyfordiscretedata discreteprobabilisticmodelscurrently.
inaconventionalGAN. As pointed out by (Bachman and Precup 2015), the se-
Extensive experiments based on synthetic and real data quence data generation can be formulated as a sequential
are conducted to investigate the efficacy and properties of decisionmakingprocess,whichcanbepotentiallybesolved
the proposed SeqGAN. In our synthetic data environment, byreinforcementlearningtechniques.Modelingthesequence
SeqGANsignificantlyoutperformsthemaximumlikelihood generatorasapolicyofpickingthenexttoken,policygradi-
methods,scheduledsamplingandPG-BLEU.Inthreereal- entmethods(Suttonetal.1999)canbeadoptedtooptimize
worldtasks,i.e.poemgeneration,speechlanguagegeneration thegeneratoroncethereisan(implicit)rewardfunctionto
and music generation, SeqGAN significantly outperforms guide the policy. For most practical sequence generation
thecomparedbaselinesinvariousmetricsincludinghuman tasks,e.g.machinetranslation(Sutskever,Vinyals,andLe
expertjudgement. 2014), the reward signal is meaningful only for the entire
sequence,forinstanceinthegameofGo(Silveretal.2016),
RelatedWork therewardsignalisonlysetattheendofthegame.Inthose
cases,state-actionevaluationmethodssuchasMonteCarlo
Deepgenerativemodelshaverecentlydrawnsignificantat- (tree) search have been adopted (Browne et al. 2012). By
tention,andtheabilityoflearningoverlarge(unlabeled)data contract,ourproposedSeqGANextendsGANswiththeRL-
endowsthemwithmorepotentialandvitality(Salakhutdinov basedgeneratortosolvethesequencegenerationproblem,
2009;Bengioetal.2013).(Hinton,Osindero,andTeh2006) wherearewardsignalisprovidedbythediscriminatoratthe
first proposed to use the contrastive divergence algorithm endofeachepisodeviaMonteCarloapproach,andthegen-
toefficientlytrainingdeepbeliefnets(DBN).(Bengioetal. eratorpickstheactionandlearnsthepolicyusingestimated
2013)proposeddenoisingautoencoder(DAE)thatlearnsthe overallrewards.
datadistributioninasupervisedlearningfashion.BothDBN
andDAElearnalowdimensionalrepresentation(encoding) SequenceGenerativeAdversarialNets
foreachdatainstanceandgenerateitfromadecodingnet-
work.Recently,variationalautoencoder(VAE)thatcombines The sequence generation problem is denoted as follows.
deeplearningwithstatisticalinferenceintendedtorepresent Givenadatasetofreal-worldstructuredsequences,traina
adatainstanceinalatenthiddenspace(KingmaandWelling θ-parameterizedgenerativemodelGθ toproduceasequence
2014),whilestillutilizing(deep)neuralnetworksfornon- Y 1:T =(y 1 ,...,yt,...,yT),yt ∈Y,whereY isthevocabu-
linearmapping.Theinferenceisdoneviavariationalmethods. laryofcandidatetokens.Weinterpretthisproblembasedon
Allthesegenerativemodelsaretrainedbymaximizing(the reinforcementlearning.Intimestept,thestatesisthecurrent
lowerboundof)trainingdatalikelihood,which,asmentioned producedtokens(y 1 ,...,yt−1 )andtheactionaisthenext
by(Goodfellowandothers2014),suffersfromthedifficulty tokenyt toselect.ThusthepolicymodelGθ(yt |Y 1:t−1 )is
ofapproximatingintractableprobabilisticcomputations. stochastic, whereas the state transition is deterministic af-
ter an action has been chosen, i.e. δa = 1 for the next
(Goodfellow and others 2014) proposed an alternative s,s(cid:2)
trainingmethodologytogenerativemodels,i.e.GANs,where states(cid:2) =Y 1:tifthecurrentstates=Y 1:t−1 andtheaction
thetrainingprocedureisaminimaxgamebetweenagener- a=yt;forothernextstatess(cid:2)(cid:2),δ s a ,s(cid:2)(cid:2) =0.
ative model and a discriminative model. This framework Additionally,wealsotrainaφ-parameterizeddiscrimina-
bypassesthedifficultyofmaximumlikelihoodlearningand tivemodelDφ (Goodfellowandothers2014)toprovidea
has gained striking successes in natural image generation guidanceforimprovinggeneratorGθ.Dφ(Y 1:T)isaprob-
(Dentonetal.2015).However,littleprogresshasbeenmade ability indicating how likely a sequence Y 1:T is from real
inapplyingGANstosequencediscretedatagenerationprob- sequencedataornot.AsillustratedinFigure1,thediscrimi-
lems,e.g.naturallanguagegeneration(Husza´r2015).Thisis nativemodelDφ istrainedbyprovidingpositiveexamples
duetothegeneratornetworkinGANisdesignedtobeable fromtherealsequencedataandnegativeexamplesfromthe
2853

G Next MC D whereY 1 n :t =(y 1 ,...,yt)andY t n +1:T issampledbasedon
True data action search the roll-out policy Gβ and the current state. In our experi-
Reward
State ment,Gβ issetthesameasthegenerator,butonecanuse
Real World Train D Reward asimplifiedversionifthespeedisthepriority(Silveretal.
G Generate Reward 2016).Toreducethevarianceandgetmoreaccurateassess-
Reward mentoftheactionvalue,weruntheroll-outpolicystarting
fromcurrentstatetilltheendofthesequenceforN timesto
Policy Gradient
getabatchofoutputsamples.Thus,wehave:
t F h i e gu re re al 1 d : a T ta he an il d lu t s h t e ra g ti e o n n er o a f te S d eq d G at A a N by .L G e . ft R : i D gh i t s :G tra i i s ne tr d a o in v e e d r Q (cid:5) G D θ φ (s (cid:6) =Y 1:t−1 ,a=yt)= (4)
bypolicygradientwherethefinalrewardsignalisprovided N 1 N n=1 D φ (Y 1 n :T ), Y 1 n :T ∈MCGβ(Y 1:t ;N) for t<T
byDandispassedbacktotheintermediateactionvaluevia D φ (Y 1:t ) for t=T,
MonteCarlosearch.
where,weseethatwhennointermediatereward,thefunction
isiterativelydefinedasthenext-statevaluestartingfromstate
syntheticsequencesgeneratedfromthegenerativemodelGθ. s(cid:2) =Y 1:tandrollingouttotheend.
Atthesametime,thegenerativemodelGθ isupdatedbyem-
AbenefitofusingthediscriminatorDφasarewardfunc-
tionisthatitcanbedynamicallyupdatedtofurtherimprove
ployingapolicygradientandMCsearchonthebasisofthe
thegenerativemodeliteratively.Oncewehaveasetofmore
expectedendrewardreceivedfromthediscriminativemodel
realisticgeneratedsequences,weshallre-trainthediscrimi-
Dφ.Therewardisestimatedbythelikelihoodthatitwould
natormodelasfollows:
foolthediscriminativemodelDφ.Thespecificformulation
isgiveninthenextsubsection. m
φ
in−E Y∼p
data
[logDφ(Y)]−E Y∼Gθ [log(1−Dφ(Y))]. (5)
SeqGANviaPolicyGradient
Eachtimewhenanewdiscriminatormodelhasbeenob-
Following (Sutton et al. 1999), when there is no interme-
tained,wearereadytoupdatethegenerator.Theproposed
diatereward,theobjectiveofthegeneratormodel(policy)
Gθ(yt |Y 1:t−1 )istogenerateasequencefromthestartstate policybasedmethodreliesuponoptimizingaparametrized
s tomaximizeitsexpectedendreward: policytodirectlymaximizethelong-termreward.Following
0
(cid:2) (Sutton et al. 1999), the gradient of the objective function
J(θ)=E[RT |s0,θ]= Gθ(y1 |s0)·Q G
D
θ
φ
(s0,y1), (1) J(θ)w.r.t.thegenerator’sparametersθcanbederivedas
y1∈Y
(cid:2) (cid:3) (cid:4)
t w he he re r w eR ar T di i s s f t r h o e m re t w he ar d d is f c o r r im ac in o a m to p r le D te φ s , e w q h u i e c n h ce w . e N w ot i e ll t d h i a s t - ∇ θJ(θ)=E Y1:t−1∼Gθ yt∈Y ∇ θGθ(yt |Y 1:t−1 )·QG D θ φ (Y 1:t−1 ,yt) .
cuss later. Q G θ(s,a) is the action-value function of a se- (6)
D
φ
quence,i.e.theexpectedaccumulativerewardstartingfrom Theaboveformisduetothedeterministicstatetransition
states,takingactiona,andthenfollowingpolicyGθ.The and zero intermediate rewards. The detailed derivation is
rationaloftheobjectivefunctionforasequenceisthatstart- providedinthesupplementarymaterial1.Usinglikelihood
ingfromagiveninitialstate,thegoalofthegeneratoristo ratios(Glynn1990;Suttonetal.1999),webuildanunbiased
generate a sequence which would make the discriminator estimationforEq.(6)(ononeepisode):
consideritisreal.
The next question is how to estimate the action-value
(cid:2)T (cid:2)
( f W un i c ll t i i a o m n. s In 19 th 9 i 2 s ) p a a n p d er c , o w n e si u d s e e r t t h h e eR es E ti I m N a F t O ed R p C r E ob a a l b g i o li r t i y th o m f ∇ θ J(θ)(cid:6) T 1 ∇ θ G θ(yt|Y1:t−1)·QG D θ φ (Y1:t−1,yt) (7)
beingrealbythediscriminatorDφ(Y
1
n
:T
)asthereward.For-
(cid:2)T (cid:2)
t=1yt∈Y
mally,wehave: =
T
1 G θ(yt|Y1:t−1)∇ θlogG θ(yt|Y1:t−1)·QG
D
θ
φ
(Y1:t−1,yt)
However,t Q he G D θ φ di ( s a cr = im y i T n , a s to = ro Y n 1 l : y T− p 1 ro ) v = id D es φ a (Y r 1 e : w T a ). rdvaluef ( o 2 r ) = T 1 (cid:2) t= T 1y E t y ∈ t Y ∼Gθ(yt|Y1:t−1)[∇ θlogG θ(yt|Y1:t−1)·QG D θ φ (Y1:t−1,yt)],
t=1
afinishedsequence.Sinceweactuallycareaboutthelong-
termreward,ateverytimestep,weshouldnotonlyconsider whereY 1:t−1 istheobservedintermediatestatesampled
thefitnessofprevioustokens(prefix)butalsotheresulted fromGθ.SincetheexpectationE[·]canbeapproximatedby
future outcome. This is similar to playing the games such samplingmethods,wethenupdatethegenerator’sparameters
asGoorChesswhereplayerssometimeswouldgiveupthe as:
immediate interests for the long-term victory (Silver et al. θ←θ+αh ∇ θJ(θ), (8)
2016).Thus,toevaluatetheaction-valueforanintermediate
state,weapplyMonteCarlosearchwitharoll-outpolicyGβ where αh ∈ R+ denotes the corresponding learning rate
tosampletheunknownlastT −ttokens.Werepresentan ath-thstep.Alsotheadvancedgradientalgorithmssuchas
N-timeMonteCarlosearchas AdamandRMSpropcanbeadoptedhere.
(cid:3) (cid:4)
Y1 1 :T,...,Y1 N :T =MC Gβ(Y1:t;N), (3) 1https://arxiv.org/abs/1609.05473
2854

Algorithm1SequenceGenerativeAdversarialNets Short-TermMemory(LSTM)cells(HochreiterandSchmid-
Require: generatorpolicyGθ;roll-outpolicyGβ;discriminator huber1997)toimplementtheupdatefunctionginEq.(9).It
Dφ;asequencedatasetS ={X1:T } isworthnoticingthatmostoftheRNNvariants,suchasthe
1: InitializeGθ,Dφwithrandomweightsθ,φ. gatedrecurrentunit(GRU)(Choetal.2014)andsoftatten-
2: Pre-trainGθusingMLEonS tionmechanism(Bahdanau,Cho,andBengio2014),canbe
3: β ←θ usedasageneratorinSeqGAN.
4: GeneratenegativesamplesusingGθfortrainingDφ
5: Pre-trainDφviaminimizingthecrossentropy
TheDiscriminativeModelforSequences
6: repeat
7: forg-stepsdo Deep discriminative models such as deep neural network
8: GenerateasequenceY1:T =(y1,...,yT)∼Gθ (DNN) (Vesely` et al. 2013), convolutional neural network
9: fortin1:T do (CNN)(Kim2014)andrecurrentconvolutionalneuralnet-
10: ComputeQ(a=yt;s=Y1:t−1)byEq.(4) work (RCNN) (Lai et al. 2015) have shown a high perfor-
11: endfor manceincomplicatedsequenceclassificationtasks.Inthis
12: UpdategeneratorparametersviapolicygradientEq.(8)
paper, we choose the CNN as our discriminator as CNN
13: endfor
has recently been shown of great effectiveness in text (to-
14: ford-stepsdo
kensequence)classification(ZhangandLeCun2015).Most
15: UsecurrentGθtogeneratenegativeexamplesandcom-
binewithgivenpositiveexamplesS discriminativemodelscanonlyperformclassificationwell
16: TraindiscriminatorDφforkepochsbyEq.(5) foranentiresequenceratherthantheunfinishedone.Inthis
17: endfor paper,wealsofocusonthesituationwherethediscriminator
18: β ←θ predictstheprobabilitythatafinishedsequenceisreal.2
19: untilSeqGANconverges Wefirstrepresentaninputsequencex
1
,...,xT as:
E 1:T =x 1 ⊕x 2 ⊕...⊕x T, (11)
In summary, Algorithm 1 shows full details of the pro- wherex t ∈Rk isthek-dimensionaltokenembeddingand
posed SeqGAN. At the beginning of the training, we use ⊕istheconcatenationoperatortobuildthematrixE 1:T ∈
themaximumlikelihoodestimation(MLE)topre-trainGθ RT×k. Then a kernel w ∈ Rl×k applies a convolutional
ontrainingsetS.Wefoundthesupervisedsignalfromthe operation to a window size of l words to produce a new
pre-trained discriminator is informative to help adjust the featuremap:
generatorefficiently. ci =ρ(w⊗E i:i+l−1+b), (12)
Afterthepre-training,thegeneratoranddiscriminatorare where ⊗ operator is the summation of elementwise pro-
trained alternatively. As the generator gets progressed via duction, b is a bias term and ρ is a non-linear function.
trainingong-stepsupdates,thediscriminatorneedstobere- Wecanusevariousnumbersofkernelswithdifferentwin-
trainedperiodicallytokeepsagoodpacewiththegenerator. dow sizes to extract different features. Finally we apply
Whentrainingthediscriminator,positiveexamplesarefrom a max-over-time pooling operation over the feature maps
thegivendatasetS,whereasnegativeexamplesaregenerated c˜=max{c
1
,...,cT−l+1 }.
fromourgenerator.Inordertokeepthebalance,thenumber
Toenhancetheperformance,wealsoaddthehighwayar-
ofnegativeexampleswegenerateforeachd-stepisthesame
chitecture(Srivastava,Greff,andSchmidhuber2015)based
asthepositiveexamples.Andtoreducethevariabilityofthe
onthepooledfeaturemaps.Finally,afullyconnectedlayer
estimation,weusedifferentsetsofnegativesamplescom-
withsigmoidactivationisusedtooutputtheprobabilitythat
binedwithpositiveones,whichissimilartobootstrapping
theinputsequenceisreal.Theoptimizationtargetistomin-
(Quinlan1996).
imizethecrossentropybetweenthegroundtruthlabeland
thepredictedprobabilityasformulatedinEq.(5).
TheGenerativeModelforSequences
Detailedimplementationsofthegenerativeanddiscrimi-
Weuserecurrentneuralnetworks(RNNs)(Hochreiterand nativemodelsareprovidedinthesupplementarymaterial.
Schmidhuber 1997) as the generative model. An RNN
maps the input embedding representations x 1 ,...,x T of SyntheticDataExperiments
the sequence x
1
,...,xT into a sequence of hidden states
h 1 ,...,h T byusingtheupdatefunctiongrecursively. TotesttheefficacyandaddourunderstandingofSeqGAN,
weconductasimulatedtestwithsyntheticdata3.Tosimulate
h t =g(h t−1,x t) (9) thereal-worldstructuredsequences,weconsideralanguage
model to capture the dependency of the tokens. We use a
Moreover,asoftmaxoutputlayerzmapsthehiddenstates
randomlyinitializedLSTMasthetruemodel,aka,theoracle,
intotheoutputtokendistribution
togeneratetherealdatadistributionp(xt |x
1
,...,xt−1 )for
p(yt |x1,...,xt)=z(h t)=softmax(c+Vh t), (10) thefollowingexperiments.
wheretheparametersareabiasvectorcandaweightma-
2Inourwork,thegeneratedsequencehasafixedlengthT,but
trixV.Todealwiththecommonvanishingandexploding
notethatCNNisalsocapableofthevariable-lengthsequencedis-
gradientproblem(Goodfellow,Bengio,andCourville2016) criminationwiththemax-over-timepoolingtechnique(Kim2014).
ofthebackpropagationthroughtime,weleveragetheLong 3Experimentcode:https://github.com/LantaoYu/SeqGAN
2855

EvaluationMetric
Table1:Sequencegenerationperformancecomparison.The
Thebenefitofhavingsuchoracleisthatfirstly,itprovides
p-valueisbetweenSeqGANandthebaselinefromT-test.
thetrainingdatasetandsecondlyevaluatestheexactperfor-
manceofthegenerativemodels,whichwillnotbepossible Algorithm Random MLE SS PG-BLEU SeqGAN
withrealdata.WeknowthatMLEistryingtominimizethe NLL 10.310 9.038 8.985 8.946 8.736
cross-entropy between the true data distribution p and our p-value <10−6 <10−6 <10−6 <10−6
approximationq,i.e.−E x∼plogq(x).However,themostac-
curatewayofevaluatinggenerativemodelsisthatwedraw
somesamplesfromitandlethumanobserversreviewthem
basedontheirpriorknowledge.Weassumethatthehuman
observerhaslearnedanaccuratemodelofthenaturaldistribu-
tionp (x).Theninordertoincreasethechanceofpass-
human
ingTuringTest,weactuallyneedtominimizetheexactop-
positeaveragenegativelog-likelihood−E x∼qlogp
human
(x)
(Husza´r 2015), with the role of p and q exchanged. In our
syntheticdataexperiments,wecanconsidertheoracletobe
thehumanobserverforreal-worldproblems,thusaperfect
Figure2:Negativelog-likelihoodconvergencew.r.t.thetrain-
evaluationmetricshouldbe
ing epochs. The vertical dashed line represents the end of
(cid:7)(cid:2)T (cid:8)
NLL oracle =−E Y1:T∼Gθ logG oracle (yt |Y1:t−1) , (13) pre-trainingforSeqGAN,SSandPG-BLEU.
t=1
whereGθ andG
oracle
denoteourgenerativemodelandthe
Results
oraclerespectively.
Attheteststage,weuseGθ togenerate100,000sequence TheNLL
oracle
performanceofgeneratingsequencesfromthe
samplesandcalculateNLL oracle foreachsamplebyG oracle comparedpoliciesisprovidedinTable1.Sincetheevaluation
andtheiraveragescore.Alsosignificancetestsareperformed metricisfundamentallyinstructive,wecanseetheimpact
tocomparethestatisticalpropertiesofthegenerationperfor- ofSeqGAN,whichoutperformsotherbaselinessignificantly.
mancebetweenthebaselinesandSeqGAN. A significance T-test on the NLL score distribution of
oracle
thegeneratedsequencesfromthecomparedmodelsisalso
TrainingSetting
performed,whichdemonstratesthesignificantimprovement
Tosetupthesyntheticdataexperiments,wefirstinitialize ofSeqGANoverallcomparedmodels.
theparametersofanLSTMnetworkfollowingthenormal ThelearningcurvesshowninFigure2illustratethesuperi-
distributionN(0,1)astheoracledescribingtherealdatadis-
orityofSeqGANexplicitly.Afterabout150trainingepochs,
tributionG oracle (xt |x 1 ,...,xt−1 ).Thenweuseittogenerate boththemaximumlikelihoodestimationandtheschedule
10,000sequencesoflength20asthetrainingsetS forthe sampling methods converge to a relatively high NLL
oracle
generativemodels. score,whereasSeqGANcanimprovethelimitofthegenera-
InSeqGANalgorithm,thetrainingsetforthediscriminator torwiththesamestructureasthebaselinessignificantly.This
iscomprisedbythegeneratedexampleswiththelabel0and indicatestheprospectofapplyingadversarialtrainingstrate-
theinstancesfromS withthelabel1.Fordifferenttasks,one giestodiscretesequencegenerativemodelstobreakthrough
shoulddesignspecificstructurefortheconvolutionallayer thelimitationsofMLE.Additionally,SeqGANoutperforms
andinoursyntheticdataexperiments,thekernelsizeisfrom PG-BLEU,whichmeansthediscriminativesignalinGAN
1toT andthenumberofeachkernelsizeisbetween100to is more general and effective than a predefined score (e.g.
2004.Dropout(Srivastavaetal.2014)andL2regularization BLEU)toguidethegenerativepolicytocapturetheunderly-
areusedtoavoidover-fitting. ingdistributionofthesequencedata.
FourgenerativemodelsarecomparedwithSeqGAN.The
first model is a random token generation. The second one Discussion
is the MLE trained LSTM Gθ. The third one is scheduled
Inoursyntheticdataexperiments,wefindthatthestability
sampling(Bengioetal.2015).ThefourthoneisthePolicy
ofSeqGANdependsonthetrainingstrategy.Morespecifi-
GradientwithBLEU(PG-BLEU).Inthescheduledsampling,
cally,theg-steps,d-stepsandk parametersinAlgorithm1
thetrainingprocessgraduallychangesfromafullyguided
havealargeeffectontheconvergenceandperformanceof
schemefeedingthetrueprevioustokensintoLSTM,towards
SeqGAN.Figure3showstheeffectoftheseparameters.In
alessguidedschemewhichmostlyfeedstheLSTMwithits
Figure3(a),theg-stepsismuchlargerthanthed-stepsand
generatedtokens.Acurriculumrateωisusedtocontrolthe
epoch number k, which means we train the generator for
probabilityofreplacingthetruetokenswiththegenerated
manytimesuntilweupdatethediscriminator.Thisstrategy
ones.Togetagoodandstableperformance,wedecreaseωby
leads to a fast convergence but as the generator improves
0.002foreverytrainingepoch.InthePG-BLEUalgorithm,
quickly,thediscriminatorcannotgetfullytrainedandthus
weuseBLEU,ametricmeasuringthesimilaritybetweena
will provide a misleading signal gradually. In Figure 3(b),
generatedsequenceandreferences(trainingdata),toscore
withmorediscriminatortrainingepochs,theunstabletraining
thefinishedsamplesfromMonteCarlosearch.
processisalleviated.InFigure3(c),wetrainthegenerator
4Implementationdetailsareinthesupplementarymaterial. for only one epoch and then before the discriminator gets
2856

Table2:Chinesepoemgenerationperformancecomparison.
Algorithm Humanscore p-value BLEU-2 p-value
MLE 0.4165 0.0034 0.6670 <10−6
SeqGAN 0.5356 0.7389
Realdata 0.6011 0.746
Table3:Obamapoliticalspeechgenerationperformance.
(a) g-steps=100, d-steps=1,(b) g-steps=30, d-steps=1,
k=10 k=30 Algorithm BLEU-3 p-value BLEU-4 p-value
MLE 0.519 <10−6 0.416 0.00014
SeqGAN 0.556 0.427
Table4:Musicgenerationperformancecomparison.
Algorithm BLEU-4 p-value MSE p-value
MLE 0.9210 <10−6 22.38 0.00034
SeqGAN 0.9406 20.62
(c) g-steps=1,d-steps=1,k=10 (d) g-steps=1,d-steps=5,k=3
twentycharactersintotal.Tofocusonafullyautomaticso-
Figure3:Negativelog-likelihoodconvergenceperformance lutionandstaygeneral,wedidnotuseanypriorknowledge
of SeqGAN with different training strategies. The vertical ofspecialstructurerulesinChinesepoemssuchasspecific
dashedlinerepresentsthebeginningofadversarialtraining. phonological rules. In the Obama political speech genera-
tiontask,weuseacorpus6,whichisacollectionof11,092
paragraphsfromObama’spoliticalspeeches.
fooled,weupdateitimmediatelybasedonthemorerealistic WeuseBLEUscoreasanevaluationmetrictomeasure
negativeexamples.Insuchacase,SeqGANlearnsstably. the similarity degree between the generated texts and the
Thed-stepsinallthreetrainingstrategiesdescribedabove human-createdtexts.BLEUisoriginallydesignedtoauto-
is set to 1, which means we only generate one set of neg- maticallyjudgethemachinetranslationquality(Papineniet
ativeexampleswiththesamenumberasthegivendataset, al.2002).Thekeypointistocomparethesimilaritybetween
andthentrainthediscriminatoronitforvariousk epochs. theresultscreatedbymachineandthereferencesprovided
But actually we can utilize the potentially unlimited num- byhuman.Specifically,forpoemevaluation,wesetn-gram
berofnegativeexamplestoimprovethediscriminator.This tobe2(BLEU-2)sincemostwords(dependency)inclassical
trick can be considered as a type of bootstrapping, where Chinesepoemsconsistofoneortwocharacters(Yi,Li,and
wecombinethefixedpositiveexampleswithdifferentneg- Sun2016)andforthesimilarreason,weuseBLEU-3and
ativeexamplestoobtainmultipletrainingsets.Figure3(d) BLEU-4toevaluateObamaspeechgenerationperformance.
showsthistechniquecanimprovetheoverallperformance Inourwork,weusethewholetestsetasthereferencesin-
with good stability, since the discriminator is shown more steadoftryingtofindsomereferencesforthefollowingline
negativeexamplesandeachtimethepositiveexamplesare giventhepreviousline(He,Zhou,andJiang2012).Therea-
emphasized,whichwillleadtoamorecomprehensiveguid- son is in generation tasks we only provide some positive
ancefortraininggenerator.Thisisinlinewiththetheoremin examplesandthenletthemodelcatchthepatternsofthem
(Goodfellowandothers2014).Whenanalyzingtheconver- andgeneratenewones.InadditiontoBLEU,wealsochoose
genceofgenerativeadversarialnets,animportantassumption poemgenerationasacaseforhumanjudgementsinceapoem
isthatthediscriminatorisallowedtoreachitsoptimumgiven isacreativetextconstructionandhumanevaluationisideal.
G.Onlyifthediscriminatoriscapableofdifferentiatingreal Specifically,wemixthe20realpoemsand20eachgener-
datafromunnaturaldataconsistently,thesupervisedsignal atedfromSeqGANandMLE.Then70expertsonChinese
fromitcanbemeaningfulandthewholeadversarialtraining poemsareinvitedtojudgewhethereachofthe60poemis
processcanbestableandeffective. createdbyhumanormachines.Onceregardedtobereal,it
gets+1score,otherwise0.Finally,theaveragescoreforeach
Real-worldScenarios algorithmiscalculated.
To complement the previous experiments, we also test Se- TheexperimentresultsareshowninTables2and3,from
qGAN on several real-world tasks, i.e. poem composition, whichwecanseethesignificantadvantageofSeqGANover
speechlanguagegenerationandmusicgeneration. theMLEintextgeneration.Particularly,forpoemcomposi-
tion,SeqGANperformscomparablytorealhumandata.
TextGeneration
MusicGeneration
For text generation scenarios, we apply the proposed Seq-
GANtogenerateChinesepoemsandBarackObamapolitical Formusiccomposition,weuseNottingham7datasetasour
speeches.Inthepoemcompositiontask,weuseacorpus5 trainingdata,whichisacollectionof695musicoffolktunes
of16,394Chinesequatrains,eachcontainingfourlinesof
6https://github.com/samim23/obama-rnn
5http://homepages.inf.ed.ac.uk/mlap/Data/EMNLP14/ 7http://www.iro.umontreal.ca/∼lisa/deep/data
2857

inmidifileformat.Westudythesolotrackofeachmusic. Goodfellow, I. 2016. Generative adversarial networks for text.
In our work, we use 88 numbers to represent 88 pitches, http://goo.gl/Wg9DR7.
whichcorrespondtothe88keysonthepiano.Withthepitch Graves, A. 2013. Generating sequences with recurrent neural
sampling for every 0.4s8, we transform the midi files into networks. arXiv:1308.0850.
sequencesofnumbersfrom1to88withthelength32. He,J.;Zhou,M.;andJiang,L. 2012. Generatingchineseclassical
To model the fitness of the discrete piano key patterns, poemswithstatisticalmachinetranslationmodels. InAAAI.
BLEUisusedastheevaluationmetric.Tomodelthefitness Hingston,P. 2009. Aturingtestforcomputergamebots. IEEE
ofthecontinuouspitchdatapatterns,themeansquarederror TCIAIG1(3):169–186.
(MSE)(Manarisetal.2007)isusedforevaluation. Hinton,G.E.;Osindero,S.;andTeh,Y.-W. 2006. Afastlearning
FromTable4,weseethatSeqGANoutperformstheMLE algorithmfordeepbeliefnets. Neuralcomputation18(7):1527–
significantlyinbothmetricsinthemusicgenerationtask. 1554.
Hochreiter,S.,andSchmidhuber,J.1997.Longshort-termmemory.
Conclusion Neuralcomputation9(8):1735–1780.
Husza´r,F. 2015. How(not)totrainyourgenerativemodel:Sched-
In this paper, we proposed a sequence generation method,
uledsampling,likelihood,adversary? arXiv:1511.05101.
SeqGAN,toeffectivelytraingenerativeadversarialnetsfor
Kim,Y. 2014. Convolutionalneuralnetworksforsentenceclassifi-
structuredsequencesgenerationviapolicygradient.Toour
cation. arXiv:1408.5882.
best knowledge, this is the first work extending GANs to
Kingma,D.P.,andWelling,M. 2014. Auto-encodingvariational
generatesequencesofdiscretetokens.Inoursyntheticdata
bayes. ICLR.
experiments, we used an oracle evaluation mechanism to
Lai,S.;Xu,L.;Liu,K.;andZhao,J. 2015. Recurrentconvolutional
explicitlyillustratethesuperiorityofSeqGANoverstrong
neuralnetworksfortextclassification. InAAAI,2267–2273.
baselines.Forthreereal-worldscenarios,i.e.,poems,speech
Manaris,B.;Roos,P.;Machado,P.;etal. 2007. Acorpus-based
languageandmusicgeneration,SeqGANshowedexcellent
hybrid approach to music analysis and composition. In NCAI,
performanceongeneratingthecreativesequences.Wealso
volume22,839.
performedasetofexperimentstoinvestigatetherobustness
Papineni,K.;Roukos,S.;Ward,T.;andZhu,W.-J. 2002. Bleu:a
andstabilityoftrainingSeqGAN.Forfuturework,weplan
methodforautomaticevaluationofmachinetranslation. InACL,
tobuildMonteCarlotreesearchandvaluenetwork(Silveret
311–318.
al.2016)toimproveactiondecisionmakingforlargescale
Quinlan,J.R. 1996. Bagging,boosting,andc4.5. InAAAI/IAAI,
dataandinthecaseoflonger-termplanning.
Vol.1,725–730.
Salakhutdinov,R. 2009. Learningdeepgenerativemodels. Ph.D.
References
Dissertation,UniversityofToronto.
Bachman,P.,andPrecup,D. 2015. Datagenerationassequential Silver,D.;Huang,A.;Maddison,C.J.;Guez,A.;Sifre,L.;etal.
decisionmaking. InNIPS,3249–3257. 2016. Masteringthegameofgowithdeepneuralnetworksandtree
Bahdanau, D.; Brakel, P.; Xu, K.; et al. 2016. An actor-critic search. Nature529(7587):484–489.
algorithmforsequenceprediction. arXiv:1607.07086. Srivastava,N.;Hinton,G.E.;Krizhevsky,A.;Sutskever,I.;and
Bahdanau,D.;Cho,K.;andBengio,Y.2014.Neuralmachinetrans- Salakhutdinov,R. 2014. Dropout:asimplewaytopreventneural
lationbyjointlylearningtoalignandtranslate. arXiv:1409.0473. networksfromoverfitting. JMLR15(1):1929–1958.
Bengio,Y.;Yao,L.;Alain,G.;andVincent,P. 2013. Generalized Srivastava,R.K.;Greff,K.;andSchmidhuber,J. 2015. Highway
denoisingauto-encodersasgenerativemodels. InNIPS,899–907. networks. arXiv:1505.00387.
Sutskever,I.;Vinyals,O.;andLe,Q.V.2014.Sequencetosequence
Bengio,S.;Vinyals,O.;Jaitly,N.;andShazeer,N.2015.Scheduled
learningwithneuralnetworks. InNIPS,3104–3112.
samplingforsequencepredictionwithrecurrentneuralnetworks.
InNIPS,1171–1179. Sutton,R.S.;McAllester,D.A.;Singh,S.P.;Mansour,Y.;etal.
1999. Policy gradient methods for reinforcement learning with
Browne, C. B.; Powley, E.; Whitehouse, D.; Lucas, S. M.; et al.
functionapproximation. InNIPS,1057–1063.
2012. Asurveyofmontecarlotreesearchmethods. IEEETCIAIG
4(1):1–43. Vesely`,K.;Ghoshal,A.;Burget,L.;andPovey,D. 2013. Sequence-
discriminativetrainingofdeepneuralnetworks.InINTERSPEECH,
Cho,K.;VanMerrie¨nboer,B.;Gulcehre,C.;etal. 2014. Learning
2345–2349.
phraserepresentationsusingRNNencoder-decoderforstatistical
machinetranslation. EMNLP. Wen, T.-H.; Gasic, M.; Mrksic, N.; Su, P.-H.; Vandyke, D.; and
Young,S. 2015. SemanticallyconditionedLSTM-basednaturallan-
Denton,E.L.;Chintala,S.;Fergus,R.;etal. 2015. Deepgenerative
guagegenerationforspokendialoguesystems. arXiv:1508.01745.
imagemodelsusingalaplacianpyramidofadversarialnetworks. In
NIPS,1486–1494. Williams,R.J. 1992. Simplestatisticalgradient-followingalgo-
rithmsforconnectionistreinforcementlearning. Machinelearning
Glynn,P.W. 1990. Likelihoodratiogradientestimationforstochas-
8(3-4):229–256.
ticsystems. CommunicationsoftheACM33(10):75–84.
Yi,X.;Li,R.;andSun,M. 2016. Generatingchineseclassical
Goodfellow,I.,etal. 2014. Generativeadversarialnets. InNIPS,
poemswithRNNencoder-decoder. arXiv:1604.01537.
2672–2680.
Zhang,X.,andLapata,M. 2014. Chinesepoetrygenerationwith
Goodfellow,I.;Bengio,Y.;andCourville,A. 2016. Deeplearning. recurrentneuralnetworks. InEMNLP,670–680.
2015.
Zhang,X.,andLeCun,Y. 2015. Textunderstandingfromscratch.
8http://deeplearning.net/tutorial/rnnrbm.html arXiv:1502.01710.
2858
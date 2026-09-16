16th European Signal Processing Conference (EUSIPCO 2008), Lausanne, Switzerland, August 25-29, 2008, copyright by EURASIP
DATA-AIDED TIME-DOMAIN SYNCHRONIZATION FOR FILTER BANK
MULTICARRIER SYSTEMS
Tilde Fusco, Angelo Petrella and Mario Tanda
Dipartimento di Ingegneria Elettronica e delle Telecomunicazioni,
Universit`a di Napoli Federico II,
via Claudio 21, I-80125Napoli, Italy.
Email: tilfusco@unina.it, angelo.petrella@unina.it and mario.tanda@unina.it
ABSTRACT problem of data-aided synchronization and channel estima-
tioninthefrequencydomainforOFDM/OQAMsystemshas
Inthispaperweconsidertheproblemofdata-aidedjointsym-
beenconsideredwhilein[9]arederiveddata-aidedjointsym-
boltimingandcarrier-frequency offset (CFO)estimationfor
bol timing and frequency offset synchronization schemes in
filter bank based multicarrier systems. Inparticular, we pro-
thetimedomainforFMTsystemsbasedonthedeployment
pose a new joint symbol timing and CFO synchronization
ofappropriatetrainingsequences. Specifically,in[9]theau-
algorithm exploiting the transmission of a training sequence
thorsextendtoFMTsystemsthesynchronizationtechniques
made up of Nrip identical parts, each of duration P. The
forOFDMsystemsproposedin[10]andin[11]exploitingthe
performance of the derived estimator assessed by computer
transmission of a training sequencewith repeated parts.
simulation is compared with that of two data-aided synchro-
Inspired to these works we develop in this paper a syn-
nization algorithms previously proposed in the literature.
chronization scheme for data-aided symbol timing and fre-
quency offset recovery with robust acquisition properties in
1. INTRODUCTION dispersive channels. Specifically, this algorithm exploits the
In the last decade orthogonal frequency division multiplex-
knownstructureofatrainingsequencemadeupofNripiden-
ticalparts,eachofdurationP. Theproposedmethod,asil-
ing(OFDM)systemshaveattractedgreatinterestinwireless
lustratedbycomputersimulation,canassureinamultipath
and wireline transmissions due to their high robustness to
channelaccuratesymboltimingand CFO estimates outper-
multipathchannels. HoweverinOFDMsystemstheadopted
forming thesynchronization algorithms proposed in [9].
pulseshapingfilterisarectangularfunction,thatexhibitsa
The organization of this paper is as follows. In Section
poor frequency-decay. An alternative multicarrier modula-
2 we describe the considered FBMC system model. In Sec-
tionsystem,whichcanprovideabetterspectralcontainment
tion 3wederivetheproposed joint symboltiming andCFO
andhighrobustnesstomultipathchannels,isfilterbankmul-
estimator for multipath channel, based on the least squares
ticarrier(FBMC)system. FBMCsystemsreferredtoasFil-
(LS)approach. NumericalresultsarepresentedinSection 4
teredMultitone(FMT)systemshavebeenproposedforvery
and conclusions are drawn in thefinal Section.
high-speed digital subscriber line (VDSL) standards [1] and
are under investigation also for broadband wireless applica- Notation: j = 4 √ 1,superscript()∗denotesthecomplex
− ·
tions [2], [3]. FBMC systems based on offset QAMmodula- conjugation, []realpart, absolutevalueandarg[]thear-
<· |·| ·
tion(OQAM),knownasOFDM/OQAMsystems,havebeen gument of a complex numberin [0,2π). Moreover lcm a,b
{ }
consideredbythe3GPPstandardizationforumforimproved istheleastcommonmultiplebetweenaandb,δ(t)theDirac
downlink UTRANinterfaces [4]. delta and is theconvolution operator.
⊗
However,asforallthemulticarriermodulation schemes,
one of the major disadvantages of FBMC systems is their 2. FBMC SYSTEM MODEL
sensitivity to carrier frequency and timing errors. Specifi-
Let us consider an FBMC system with a signaling interval
cally, as investigated in [5] and in [6] phase noise and mis-
T, the received signal in multipath channel, in the presence
alignments in time and frequency can considerably degrade
of a timing offset τ, a carrier phase offset φ and a CFO ∆f
the performance of FMT and OFDM/OQAM systems, giv-
can be written as
ing rise to interference between successive symbols and ad-
jacent subcarriers. Therefore, reliable and accurate timing r(t)=ej(2π∆ft+φ)[h(t) s(t τ)]+n(t) (1)
andcarrier-frequency offset (CFO) synchronization schemes ⊗ −
must bedesigned for these systems.
where
Recently, data-aided and non-data-aided (or blind) syn- Nm−1
chronization algorithms for FBMC systems have been con- h(t)= 4 aqδ(t θq)
sidered. Specifically, in [7] it is presented a blind joint CFO −
q=0
andsymboltimingestimatorexploitingtheunconjugatecy- X
clostationarityofthereceivedOFDM/OQAMsignalwhilein is themultipath channelimpulseresponse, s(t)is thetrans-
[8]itisshownthataccurateCFOestimation algorithmscan mitted OFDM/OQAM signal and n(t) denotes the zero-
beobtainedbyusingboththeconjugateandtheunconjugate mean circular complex white Gaussian noise with power
cyclostationarity propertiesof thereceived signal. However, spectral density Sn(f) = σ
n
2 and statistically independent
thederivedestimatorsassureasatisfactoryperformanceonly ofs(t). Thereceivedsignalr(t)isfilteredwithanideallow-
when a large number of OFDM/OQAM symbols is consid- pass filter with a bandwidth of 1/Ts and sampled with a
ered and in the case of non-dispersive channel. In [12] the frequency fs =1/Ts where Ts denotes thesampling period
ThisworkwassupportedinpartbytheEuropeanCommission Nm−1
under Project PHYDYAS (FP7-ICT-2007-1-211887) and in part r(kTs)=ej(2π∆fTsk+φ) aqs(kTs τ θq)+n(kTs). (2)
− −
bytheItalianMinistryofUniversity(MIUR)projectS.Co.P.E.
q=0
X

16th European Signal Processing Conference (EUSIPCO 2008), Lausanne, Switzerland, August 25-29, 2008, copyright by EURASIP
In this paper we will focus our analysis on two FBMC-
based schemes: OFDM offset QAM (OFDM/OQAM) and
1 2 ... P ... 1 2 ... P
Filtered MultiTone (FMT). In particular, into the case of
OFDM/OQAM systems the useful signal s(kTs) sampled
with a sampling frequency fs =N/T is equalto 1 ... Nrip
| {z } | {z }
∞
s(kTs)=
r
2 N Nu
" p= X −∞ X l∈A
aR l (p)ejk(2 N πl+π 2 ) g(kTs − pT)
Figure 1: Training FBMC signal.
∞
+j aI l (p)ejk(2 N πl+π 2 ) g kTs − T 2 − pT and
p= X −∞ X l∈A (cid:16) (cid:17) #
(3)
∆fˆ LS(τˆLS)=
2πP
1
Ts
arg
{
R(τˆLS)
}
(8)
where the sequences aR(p) and aI(p) denote the real and
l l with
imaginary parts of the complex data symbols transmitted
on the lth subcarrier during the pth OFDM/OQAM sym- NripP−P−1
bol while g(t) is the real transmitted pulse-shaping filter, 4 ∗
R(τ˜)= r (kTs+τ˜)r(kTs+PTs+τ˜) (9)
assumed to be a square-root raised cosine (SRRC) Nyquist
filter with a roll-off factor α (0 α 1) and unit energy. k= X Ng−1
≤ ≤
Moreover, in (3) N is the number of subcarriers, of which
and
Nu are data subcarriers and Nv = N Nu remain unmod-
−
ulated (virtual subcarriers), while
A
is the set of indices of NripP−P−1
data
In
s
t
u
o
bca
th
rr
e
ier
c
s
a
.
se of an FMT system the baseband
Q(τ˜)= 4
|
r(kTs+τ˜)
|
2
discrete-time transmitted signal obtained by sampling the k= X Ng−1
continuous-timesignalwithasamplingfrequencyfs=K/T (10)
is given by NripP−P−1
∞
+
|
r(kTs+PTs+τ˜)
|
2.
s(kTs) =
K
a l (p)g(kTs
pT)ej2
N
πkl
(4)
k=
X
Ng−1
r
Nu
p= X −∞ X l∈A
−
Let us observe that if we divide the timing metric in
(7) by Q(τ˜) we obtain the joint symbol timing and CFO
whereK =(1+α)N isassumedtobeanintegeranda(p)is
l estimator
the complex data symbol transmitted on the lth subcarrier
of thepth FMT symbol.
2 R(τ˜)
3. JOINT SYMBOL TIMING AND CFO LS
τˆTR1 =argm
τ˜
ax
Q
|
(τ˜)
| (11)
(cid:26) (cid:27)
ESTIMATOR
and
1
I
t
n
im
t
i
h
n
i
g
ss
e
e
s
c
t
t
im
ion
at
w
or
e
b
d
a
e
s
r
e
iv
d
e
o
a
n
d
t
a
h
ta
e
-a
L
i
S
de
a
d
p
j
p
o
r
i
o
n
a
t
c
C
h
F
w
O
hi
a
c
n
h
d
e
s
x
y
p
m
lo
b
it
o
s
l ∆fˆ TR1 (τˆTR1 )=
2πPTs
arg
{
R(τˆTR1 )
}
. (12)
thetransmissionofatrainingsequencemadeupofNripiden- Thejointestimatorin(11)andin(12)representsamod-
tical blocks each of duration PTs (see Fig. 1). Precisely, ified version of the synchronization algorithm for FMT sys-
thetraining sequence can beobtained by transmitting a se- tem proposed by Tonello and Rossi in [9] and it is referred
quenceofNTR FBMCsymbolsperiodicofperiodN,thatis to as Tonello Rossi 1 (TR1). In [9] it is also considered a
a l (p) =aT l R ∀ l ∈ A and ∀ p ∈{ 0,...,NTR − 1 } . In this way joint symbol timing and CFO estimator for AWGN channel
we obtain thetraining sequence periodic of period P exploiting the knowledge of a pseudo-noise sequence peri-
odic of period P. This synchronization algorithm referred
sTR(kTs)=sTR(kTs+PTs) (5)
to as TR2 can be obtained by considering the minimization
problem
with P = lcm N,K for FMT systems and P = N for
{ }
OFDM/OQAM systems. Thus, a joint symbol timing and
CFOestimatorcanbeobtainedbyconsideringtheminimiza- (∆fˆ TR2 ,τˆTR2 )=
tion problem
NripP−P−1
(∆fˆ,τˆ)=arg
∆
m
f˜
i
,
n
τ˜ 
NripP−P−1
|
r(kTs+τ˜)
=arg
∆
m
f˜
i
,
n
τ˜ 
 k= X Ng−1
|
s∗
TR
(kTs)sTR(kTs+PTs)
(13)
 k= X Ng−1
 2

−
r(kTs+PTs+τ˜)e−j2π∆f˜TsP 2 −
r∗(kTs+τ˜)r(kTs+PTs+τ˜)e−j2π∆f˜TsP
(cid:12) (cid:27)
.
(cid:12) (cid:27) (6) After simple algebraic manipulations we ob (cid:12) (cid:12)tain the joint
(cid:12)
where ∆f˜and τ˜ are trial values for CFO and timing o(cid:12)ffset, symbol timing and CFO estimator
respectively, while NgTs is the length of the pulse shaping
filter g(t). The minimization in (6) leads to the following 2 S(τ˜)
joint CFO and symbol timing estimator referred to as LS
τˆTR2 =argm
τ˜
ax
T
|
(τ˜)
| (14)
(cid:26) (cid:27)
estimator
1
τˆLS =argm
τ˜
ax
{
2
|
R(τ˜)
|−
Q(τ˜)
}
(7) ∆fˆ TR2 (τˆTR2 )=
2πPTs
arg
{
S(τˆTR2 )
}
(15)

16th European Signal Processing Conference (EUSIPCO 2008), Lausanne, Switzerland, August 25-29, 2008, copyright by EURASIP
with
x 105 TR2 Cost Function
NripP−P−1 10
∗
S(τ˜)= r (kTs+τ˜)sTR(kTs)
k=
X
Ng−1 (16) 5
×
r(kTs+PTs+τ˜)s∗
TR
(kTs+PTs) 0
0 10 20 30 40 50 60 70
d
and
LS Cost Function
NripP−P−1 0
T(τ˜)= sTR(kTs)2sTR(kTs+PTs)2
| | | | −0.5
k=
X
Ng−1
−1
NripP−P−1
10 20 30 40 50 60 70
+ r(kTs+τ˜)2r(kTs+τ˜+PTs)2. d
| | | |
k=
X
Ng−1
(17) 1
TR1 Cost Function
It is worthwhile to note that the considered LS, TR1
and TR2 CFO estimators in (8), (12) and (15), respec- 0.95
tively, provide a closed form solution for the CFO estimate
and do not require the knowledge of the signal-to-noise ra- 0.9
tio (SNR) and of the channel. Moreover, in the case of 0 10 20 30 40 50 60 70
OFDM/OQAMsystems theycan assure unambiguousCFO d
estimatesif ∆fTs <1/(2N),whileinthecaseofFMTsys-
| |
temstheir acquisition range is reduced to ∆fTs <1/(2P).
| |
Ontheotherhand,theconsideredLS,TR1andTR2symbol
Figure 2: Cost functions of the considered symbol timing
timing estimators do not present a closed form solution but
estimators for OFDM/OQAM systems in a single run and
they require a maximization with respect to the continuous
in theabsence of noise.
parameter τ˜. This maximization is performed in two steps:
in the first it is performed a coarse search with a step-size
Ts/100 followed, in the second step, by a parabolic interpo-
lation. x 104 TR2 Cost Function
It is of interest to underline that in the case of FMT 2
systems the amount of redundancy needed to transmit
the training sequence is greater than to that used in the 1
case of OFDM/OQAM systems. In fact, in the case of
OFDM/OQAM systems the training sequence is composed 0
by Nrip identical OFDM/OQAM symbols while in the case 0 100 200 300 400 500 600
τ
of FMT systems it is necessary to transmit a training se-
quence of total length NripP, where P = l.c.m N,K can LS Cost Function
bemuch greater than N. { } 0
In figures2 and 3 we report thecost function of theLS,
TR1andTR2symboltimingmetricsin(7),(11)andin(14), −0.2
respectively, for a noiseless and distortionless transmission.
Precisely,Fig. 2showsthebehavioroftheconsideredsymbol −0.4
timing estimators in the case of an OFDM/OQAM system 0 2 4 6 8 10 12
τ
with N = 64 subcarriers while in Fig. 3 an FMT system
with N = 64 and K = 72 is considered. The results show TR1 Cost Function
that the TR2 and the LS symbol timing estimators exhibit 1
a sharp peak at the actual timing value τ =10Ts while the
TR1 cost function is more flat around its maximum. 0.95
4. NUMERICAL RESULTS 0.9
0 5 10 15 20 25
InthissectiontheperformanceoftheproposedjointLSsym- τ
boltimingand CFO estimator iscompared with thatof the
considered modified versions of the data-aided synchroniza-
tionalgorithmsTR1andTR2proposedbyTonelloandRossi
in [9]. Figure 3: Cost functions of the considered symbol timing
Anumberof104 MonteCarlo trialshasbeen performed estimatorsinasinglerun,intheabsenceofnoiseandforan
underthe following conditions FMT system with N =64 and K =72.
1. The prototype filter is obtained by truncating the sam-
pledversionofanSRRCNyquistfilterwitharolloff fac-
torα. Specifically,itisaFIRfilteroflengthNg =4K for 3. The size of the set of subcarriers and the roll-off param-
FMTsystemsandNg =4N forOFDM/OQAMsystems. eter for the considered FMT system are N = 64 and
2. ThevalueofthenormalizedCFO,ofthetimingoffsetand α=0.125, respectively.
of the carrier phase are fixed at ∆ν = ∆fTsN = 0.03, 4. Thesizeofthesetofsubcarriersandtheroll-offparame-
τ =3Ts and φ=π/8, respectively. terfortheconsideredOFDM/OQAMsystemareN =64

16th European Signal Processing Conference (EUSIPCO 2008), Lausanne, Switzerland, August 25-29, 2008, copyright by EURASIP
and α=0.6, respectively. REFERENCES
5. The multipath channel has been modeled using the
COST 207 Hilly Terrain (HT) Rayleigh fading channel [1] G. Cherubini, E. Eleftheriou, S. O¨l¸cer, and J.M. Cioffi,
in [13]. “Filter bank modulation techniques for very high-speed
digital subscriber lines,” IEEE Commun. Mag., vol. 38,
6. Thecomplex datasymbols a(p),whentheFMTsystem
l
pp.98-104, May 2000.
is considered, belong to a QPSK constellation.
7. The data symbols aR(p) and aI(p), when the [2] N. Benvenuto, S. Tomasin, and L. Tomba, “Equalisa-
l l
OFDM/OQAMsystem is considered, belong to a BPSK tion methods in OFDM and FMT systems for broad-
constellation. band wireless communications,” IEEE Trans. on Com-
mun.,vol. 50, no. 5, pp. 1016-1028, June2002.
4.1 OFDM/OQAM System [3] T. Ihalainen, T. Hidalgo Stitz, M. Rinne, and M. Ren-
Inthisfirstsetofsimulationswehavetestedtheperformance fors,“Channelequalizationinfilterbankbasedmulticar-
of the considered algorithms for an OFDM/OQAM system riermodulationforwirelesscommunications,”EURASIP
inAWGN(solidlines)andmultipathchannel(dashedlines). Journal of Applied Signal Processing., vol. 2007.
Precisely,figures4and5showthemeansquarederror(MSE) [4] D. Lacroix, N. Goudard, and M. Alard, “OFDM with
of the considered joint CFO and symbol timing estimators GuardIntervalVersusOFDM/OffsetQAMforHighData
as a function of the SNR= 4 1 for a training sequence with Rate UMTS Downlink Transmission,” Proc. of VTC’01
σn 2 Fall, Atlantic City,NJ, USA,Oct. 2001.
Nrip = 5 identical blocks each of length N. As indicated
[5] P. K. Remvik and N. Holte,“Carrier frequency offset ro-
in figure 4 in AWGN channel the TR2 symbol timing esti-
bustnessforOFDMsystemswithdifferentpulseshaping
mator exhibits the best performance for all the considered
filters,” Proc. of GLOBECOM 1997, vol. 1, pp. 11-15,
SNRvalues, while in the considered COST 207 HT channel
Nov.1997.
theproposedLSsymboltimingestimatorassuresthelowest
MSEand,moreover,itsperformancedoesnotpresentafloor [6] T. Fusco, A. Petrella, and M. Tanda, “Sensitivity of
forhigh SNRvalues. Itisworthwhile toemphasizethat the Multi-UserFilter-BankMulticarrierSystemstoSynchro-
consideredTR1andLSsymboltimingestimators exhibitin nization Errors,” Proc. of ISCCSP 2008, March 2008.
multipathchannelacontainedperformancelosswithrespect [7] H.B¨olcskei,“Blindestimationofsymboltimingandcar-
tothatachievedinAWGNwhiletheTR2symboltimingesti- rier frequency offset in wireless OFDM systems,” IEEE
matorpresentsasevereperformancedegradationinthecase Trans. Commun.,vol. 49, pp.988-999, June 2001.
ofdispersivechannel. AsshowninFig. 5inAWGNchannel
[8] T. Fusco and M. Tanda, “Blind frequency-offset estima-
theconsidered CFOestimators exhibitnearlythesameper-
tion for OFDM/OQAM systems,” IEEE Trans. Signal
formancewhileinmultipathchannelthegreateraccuracyof
Processing, vol. 55, pp. 1828-1838, May 2007.
the proposed LS symbol timing estimator has beneficial ef-
fectsalso on theperformance oftheLSCFO estimator that [9] A. Tonello and F. Rossi, “Synchronization and Channel
assures for high SNR values thelowest MSE. Estimation forFilteredMultitoneModulation,” inProc.
of WPMC 2004, AbanoTerme, pp. 590-594, Sept. 2004.
4.2 FMT System [10] T.M. Schmidl and D.C. Cox, “Robust frequency and
In this subsection we present the performance of the con- timing synchronization for OFDM,” IEEE Trans. Com-
sidered algorithms for FMT systems in AWGN (solid lines) mun.,vol. 45, pp.1613-1621, Dec. 1997.
and multipath channel (dashed lines). Precisely, figures 6 [11] F. Tufvesson, O. Edfors and M. Faulkner, “Time and
and 7 show the MSE of the considered joint CFO and sym- frequencysynchronizationforOFDMusingPN-sequence
bol timing estimators as a function of the SNR for a train- preambles,”inProc.ofVTC1999,vol.4,pp.2203-2207,
ing sequence with Nrip = 2 identical blocks each of dura- Amsterdam, Netherlands,Sept. 1999.
tion P = l.c.m 64,72 = 576. We can note that, as in the [12] T. H. Stitz, T. Ihalainen, and M. Renfors, “Practical
{ }
OFDM/OQAMcase,intheFMTcaseandinAWGNchannel Issuesinfrequencydomainsynchronizationforfilterbank
the TR2 symbol timing estimator exhibits the best perfor- basedmulticarriertransmission,”Proc.ofISCCSP2008,
mance, while in multipath channel the proposed LS symbol March 2008.
timing estimator assures the lowest MSE. In regard to the
[13] COST 207, “Digital land mobile radio communica-
performance of the CFO estimators, we can note that as in
tions”, Office for Official Publications of the European
the case of OFDM/OQAM systems, the LS CFO estimator
Communities, Final Report, Luxemburg,1989.
guaranties practically the same performance in AWGN and
multipath channel, outperforming all the other estimators
for high SNRvalues.
5. SUMMARY AND CONCLUSIONS
In this paper the problem of data-aided symbol timing and
CFO estimation in FBMC systems has been considered. A
synchronization scheme based on a training sequence made
upofNripidenticalpartseachofdurationP hasbeenconsid-
ered. TheproposedmethodisbasedontheLSapproachand
operates in the time domain before running the receiver fil-
terbank. Moreover,itdoesnotrequiretheknowledgeofthe
channelimpulseresponseandof theSNR.Theperformance
of thederived LS estimator has been assessed via computer
simulation and compared with that of modified versions of
twojointsymboltimingandCFOestimatorspreviouslypro-
posed by Tonello and Rossi in [9]. The numerical results
have shown that in a multipath channel it can outperform
theestimators proposed in [9].

103
102
101
100
10−1
10−2
10−3
−5 0 5 10 15 20 25 30 35 40
)τ(ESM
TR2
LS
TR1
SNR [dB]
Figure4: Performanceoftheconsideredsymboltimingesti-
matorsinAWGN(solidlines)andmultipathchannel(dashed
lines) as a function of SNR and for an OFDM/OQAM sys-
tem with N =64 and α=0.6.
10−1
10−2
10−3
10−4
10−5
10−6
10−7
10−8
−5 0 5 10 15 20 25 30 35 40
)ν∆(ESM
103
102
101
100
10−1
10−2
10−3
−5 0 5 10 15 20 25 30 35 40
TR2
LS
TR1
SNR [dB]
Figure 5: Performance of theconsidered CFO estimators in
AWGN(solidlines)andmultipathchannel(dashedlines)as
a function of SNR and for an OFDM/OQAM system with
N =64 and α=0.6.
)τ(ESM
TR2
LS
TR1
SNR [dB]
Figure6: Performanceoftheconsideredsymboltimingesti-
matorsinAWGN(solidlines)andmultipathchannel(dashed
lines) as a function of SNR and for an FMT system with
N =64 and K =72.
10−4
10−5
10−6
10−7
10−8
10−9
10−10
10−11
−5 0 5 10 15 20 25 30 35 40
)ν∆(ESM
16th European Signal Processing Conference (EUSIPCO 2008), Lausanne, Switzerland, August 25-29, 2008, copyright by EURASIP
TR2
LS
TR1
SNR [dB]
Figure 7: Performance of the considered CFO estimators in
AWGN(solidlines)andmultipathchannel(dashedlines)as
afunctionofSNRandforanFMTsystemwithN =64and
K =72.
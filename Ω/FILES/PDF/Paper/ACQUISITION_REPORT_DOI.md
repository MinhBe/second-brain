# Acquisition report

## Summary

| mode | status | requested | downloaded | from cache | failed |
| --- | --- | --- | --- | --- | --- |
| DOI_DOWNLOAD | partial | 23 | 18 | 15 | 5 |

Failures by class:

- `blocked_403`: 1
- `blocked_challenge`: 2
- `subscription_only`: 2

## Downloaded

| # | title / DOI | method | path | sha256 |
| --- | --- | --- | --- | --- |
| 1 | ModSec-Learn: Boosting ModSecurity with Machine Learning (preprint) | arxiv_preprint | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\ModSec-Learn_Boosting_ModSecurity_with_Machine_Learning_preprint.pdf | 488255783644 |
| 2 | WAF-A-MoLE | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\WAF-A-MoLE.pdf | bb07fc242dd0 |
| 3 | WAF-A-MoLE: An adversarial tool for assessing ML-based WAFs | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\WAF-A-MoLE_An_adversarial_tool_for_assessing_ML-based_WAFs.pdf | a383560f63b7 |
| 4 | 10.48550/arXiv.2312.13041 | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\10.48550_arXiv.2312.13041.pdf | 9e32572e0853 |
| 5 | SeqGAN: Sequence Generative Adversarial Nets with Policy Gradient | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\SeqGAN_Sequence_Generative_Adversarial_Nets_with_Policy_Gradient.pdf | 695925fe3cf3 |
| 6 | 10.48550/arXiv.1907.00503 | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\10.48550_arXiv.1907.00503.pdf | 4361a02973c5 |
| 7 | SMOTE: Synthetic Minority Over-sampling Technique | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\SMOTE_Synthetic_Minority_Over-sampling_Technique.pdf | 8eece9837dbc |
| 8 | 10.48550/arXiv.2407.08839 | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\10.48550_arXiv.2407.08839.pdf | 2644af7a3c6d |
| 9 | Architectural Selection Framework for Synthetic Network Traffic: Quantifying the Fidelity–Utility Trade-off | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\Architectural_Selection_Framework_for_Synthetic_Network_Traffic_Quantifying_the_Fidelity_Utility_Trade-off.pdf | 4441d0adc0eb |
| 10 | Multi-Agent Honeypot-Based Request-Response Context Dataset for Improved SQL Injection Detection Performance (preprint) | arxiv_preprint | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\Multi-Agent_Honeypot-Based_Request-Response_Context_Dataset_for_Improved_SQL_Injection_Detection_Performance_preprint.pdf | bd6c4a0b2bcf |
| 11 | 10.48550/arXiv.2608.27172 | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\10.48550_arXiv.2608.27172.pdf | b581e409dc1b |
| 12 | AdvSQLi: Generating Adversarial SQL Injections Against Real-World WAF-as-a-Service | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\AdvSQLi_Generating_Adversarial_SQL_Injections_Against_Real-World_WAF-as-a-Service.pdf | 2e0c2634dfca |
| 13 | Generative Adversarial Network (GAN)-Based Autonomous Penetration Testing for Web Applications. | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\Generative_Adversarial_Network_GAN_-Based_Autonomous_Penetration_Testing_for_Web_Applications.pdf | 4bb697494f91 |
| 14 | CTTGAN: Traffic Data Synthesizing Scheme Based on Conditional GAN. | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\CTTGAN_Traffic_Data_Synthesizing_Scheme_Based_on_Conditional_GAN.pdf | 453c0cd2e91c |
| 15 | A Machine-Learning-Driven Evolutionary Approach for Testing Web Application Firewalls | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\A_Machine-Learning-Driven_Evolutionary_Approach_for_Testing_Web_Application_Firewalls.pdf | 29aa597ab424 |
| 16 | ModSec-AdvLearn: Countering Adversarial SQL Injections With Robust Machine Learning (preprint) | arxiv_preprint | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\ModSec-AdvLearn_Countering_Adversarial_SQL_Injections_With_Robust_Machine_Learning_preprint.pdf | 7990f381995d |
| 17 | A Comprehensive Survey of Generative Adversarial Networks (GANs) in Cybersecurity Intrusion Detection | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\A_Comprehensive_Survey_of_Generative_Adversarial_Networks_GANs_in_Cybersecurity_Intrusion_Detection.pdf | d6d0bf66e9d2 |
| 18 | Enhancing Autonomous Intrusion Detection System with Generative Adversarial Networks | cache | C:\Users\Admin\Documents\Second Brain\Ω\FILES\PDF\Paper\Enhancing_Autonomous_Intrusion_Detection_System_with_Generative_Adversarial_Networks.pdf | 69ec3b084935 |

3 file(s) marked (preprint) are arXiv preprints, not the published version of record.

## Failed

### blocked_403 (1)

The publisher CDN rejects non-browser clients. Open a manual URL in a real browser and save the PDF.

- `10.3390/jcp2040039` Detection of SQL Injection Attack Using Machine Learning Techniques: A Systematic Literature Review
  - error: js_challenge_page
  - warnings: impersonated_client
  - <https://doi.org/10.3390/jcp2040039>
  - <https://doaj.org/article/b91628631abd42d7a451a37e33f5a934>

### blocked_challenge (2)

The publisher serves a JavaScript challenge that only a real browser can pass. Open the link in your browser and save the PDF.

- `10.3390/computers15060368` Deployment-Oriented Multi-Embedding Machine Learning Framework for SQL Injection Detection and Prevention in a Web Application Firewall
  - error: js_challenge_page
  - warnings: impersonated_client
  - <https://doi.org/10.3390/computers15060368>
  - <https://doaj.org/article/b9172caa127a447bb469de2e2b4a043a>
- `10.3390/fi17010008` GenSQLi: A Generative Artificial Intelligence Framework for Automatically Securing Web Application Firewalls Against Structured Query Language Injection Attacks
  - error: js_challenge_page
  - warnings: impersonated_client
  - <https://doi.org/10.3390/fi17010008>
  - <https://www.mdpi.com/1999-5903/17/1/8/>
  - <https://doaj.org/article/a70d313adcea411eae02140e8f1e24d7>

### subscription_only (2)

No open-access copy exists. Use a library subscription, VPN, or contact the authors.

- `10.1016/j.cose.2022.103054` Synthetic attack data generation model applying generative adversarial network for intrusion detection
  - error: subscription_only
  - <https://doi.org/10.1016/j.cose.2022.103054>
- `10.1007/s00779-019-01332-y` GAN-based imbalanced data intrusion detection system
  - error: subscription_only
  - <https://doi.org/10.1007/s00779-019-01332-y>

## Manual download

| # | DOI | save as | open |
| --- | --- | --- | --- |
| 1 | `10.3390/computers15060368` | `Deployment-Oriented_Multi-Embedding_Machine_Learning_Framework_for_SQL_Injection_Detection_and_Prevention_in_a_Web_Appli.pdf` | <https://doi.org/10.3390/computers15060368> |
| 2 | `10.3390/fi17010008` | `GenSQLi_A_Generative_Artificial_Intelligence_Framework_for_Automatically_Securing_Web_Application_Firewalls_Against_Stru.pdf` | <https://doi.org/10.3390/fi17010008> |
| 3 | `10.3390/jcp2040039` | `Detection_of_SQL_Injection_Attack_Using_Machine_Learning_Techniques_A_Systematic_Literature_Review.pdf` | <https://doi.org/10.3390/jcp2040039> |

1. Open the link in a real browser and download the PDF.
2. Save it into `C:/Users/Admin/Documents/Second Brain/Ω/FILES/PDF/Paper` using exactly the `save as` name.
3. Run the same command again: the file is verified and adopted (`method: cache`); only remaining failures are retried.

2 paper(s) are subscription-only and need library access or the authors; they are not listed above.

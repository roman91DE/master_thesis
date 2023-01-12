---
title: "Pre-Trained Denoising Autoencoders Long Short-Term Memory Networks as probabilistic Models for Estimation of Distribution Genetic Programming"
subtitle: "Kolloquium zur Masterarbeit im M.Sc. Wirtschaftspädagogik "
author: "Roman Hoehn"
institute: "Johannes Gutenberg-Universität Mainz"
date: "Datum: 25.01.2023"
#fontsize: 11pt
link-citations: true
output:
  beamer_presentation:
    #theme: "Madrid"
    fonttheme: "structurebold"
    fig_width: 12
    fig_height: 10
    # keep_tex: true
    fig_caption: no
    number_sections: true
    slide_level: 2
toc: yes
bibliography: ref/ref.bib
csl: csl/harvard-cite-them-right.csl
includes:
      in_header: [header_files/slides.tex]

---








# Einleitung

## Forschungsfrage

*Kann das Suchverhalten der Denoising Autoencoder Genetic Programming (DAE-GP) Metaheuristik durch den Einsatz einer Pre-Training Strategie optimiert werden?*


Welchen Effekt hat Pre-Training auf:

  1. das Generalisierungsverhalten von DAE-GP?
  2. die Qualität der gefundenen Programme (Fitness/Programmlänge)?
  3. die Populationsdiversität?
  4. das Laufzeitverhalten?
  
Anwendungsgebiet: Symbolische Regression, insbesondere am Aifoil Datensatz
  


# Denoising Autoencoder Genetic Programming 

## Übersicht

* Metaheuristik basierend auf genetischer Programmierung (GP)
* Ersetzung der Variationsoperatoren von GP durch künstliche, neuronalen Netzen zur Optimierung des Suchverhaltens^[@dae-gp_2020_rtree]
* Variante des Estimation of Distribution-GP (EDA-GP)
* Einsatz von Pre-Training in mehreren Publikationen als möglicher Weg für eine weitere Optimierung vorgeschlagen^[@dae-gp_2022_symreg] ^[@daegp_explore_exploit]


## Estimation of Distribution Algorithmen (EDA)

* Entwicklung neuer Rekombinationsoperatoren für evolutionäre Algorithmen basierend auf dem Einsatz von probabilistischen Modellen^[@design_of_modern_heuristics]
* Hypothese: Problemspezifische Abhängigkeiten zwischen Entscheidungsvariablen können bei der Erzeugung neuer Individuen besser berücksichtigt werden als bei traditionellen Rekombinationsoperatoren^[@edaOrig1996]
* Weitere Verbreitung im Bereich der genetischen Algorithmen (GA) als für GP

## Denoising Autoencoder Estimation of Distribution Algorithmen (DAE-EDA)

Idee: Einsatz von Denoising Autoencoders^[@dae_orig2008] (DAE) als probabilistisches Modell für genetische Algorithmen ^[@harmless_overfitting_eda]

2 Phasen Ansatz:

  1. Model Building: Modell "lernt" die Eigenschaften von ausgewählten Lösungen hoher Güte durch das Trainieren eines DAEs
  2. Model Sampling: Neue Lösungen werden erzeugt durch das propagieren von bestehenden, mutierten Lösungen durch das erlernte Modell 
  

## Denoising Autoencoder Genetic Programming (DAE-GP)

* Adaptierung des DAE-EDA Algorithmus auf GP
* Darstellung von Individuen als Zeichenketten in prefix Notation
* seq2seq learning Problem: Einsatz von DAE - Long Short Term Memory Netzwerken (DAE-LSTM)

## DAE-GP Ablauf

![Flowchart - Regular DAE-GP](./img/flowcharts/dae-gp.png){height=80%}

## Pre-Training

Idee: Modelle werden vor ihrem eigentlichen Einsatz zum Lösen eines Problems auf möglichst großen Datensätzen vortrainiert

Mögliche Vorteile durch Pre-Training^[@pmlr-v5-erhan09a]: 

1. Geringere Bedarf an Trainings Daten für vortrainierte Modelle
2. Reduktion der Trainingszeiten/Laufzeiten
3. Verbesserung der Güte des Modells
4. Verbessertes Generalisierungsverhalten des Modells


# Aktueller Forschungsstand

## Generalisiertes Royal Tree Problem^[@dae-gp_2020_rtree] (GRT):

  * Einfaches Suchproblem mit hoher Lokalität
  * DAE-GP erzeugt durch Model Sampling Lösungskandidaten mit höherer Fitness als GP 
  * Hohe Güte der erzeugten Lösungskandidaten resultiert in besserer Performance
  * Perfomance Vorteil steigt mit zunehmender Komplexität des GRT Problems
  
  
## Symbolische Regression^[@dae-gp_2022_symreg]:

  * Airfoil Datensatz für Real-World symbolische Regression
  * DAE-GP erzeugt für eine vorgegebene Anzahl von Fitness Evaluationen im Vergleich zu GP:
  
    1. Lösungen mit höherer Fitness
    2. Lösungen  mit geringerer Größe


## Pre-Training für Denoising Autoencoders^[@pmlr-v5-erhan09a]

### Positive Wirkung von Pre-Training auf DAE

1. Gesteigerte Modell Performance (sinkender Testfehler)
2. Besserer Generalisierungsfähigkeit
3. Erhöhter Robustness des Algorithmus (sinkende Varianz des Testfehlers)


### Einfluss der Modell Architektur

* Positiver Effekt steigt mit zunehmender Komplexitität des DAE
* Je mehr versteckte Layer oder die Anzahl an Neuronen pro verstecktem Layer vorhanden sind, desto besserer Effekt des Pre-Trainings
* Für sehr kleine DAE, zeigt Pre-Training jedoch inverse, negative Auswirkung auf die Modell Performance



# Implementation

## Überblick

Gewählte Pre-Training Strategie: 

* (Klassisches) Pre-Training: Einmaliges Pre-Training eines DAE-LSTM mit einer großen Population aus Lösungskandidaten $\hat{P}_{train}$

* Trainingsmethode Early Stopping: Abbruch des Trainings sobald der Testfehler für eine seperate Population $\hat{P}_{test}$ konvergiert

*Ausschluss anderer Pre-Training Strategien wie Re-Use Learning, Few-Shot Learning*

## Pre-Trained DAE-GP Ablauf

![Flowchart - Pre-Trained DAE-GP](./img/flowcharts/pt-dae-gp.png){height=75%}

## Herausforderungen

... hidden neurons ... 


# Untersuchung des Generalisierungsverhalten 

## Fragestellung

Welchen Einfluss hat die Dimension der eingesetzten DAE-LSTMs auf das Generalisierungsverhalten von DAE-GP in Kombination mit Pre-Training?

Experimenteller Aufbau: 

* Ausschließliche Betrachtung des Rekonstruktionsfehlers der ersten Generation (Nutzung von seperaten Test- und Trainingspopulationen)
* DAE-LSTM Training erfolgt über eine fixe Anzahl von $1000$ Epochen (kein frühzeitiger Abbruch bei Konvergenz des Testfehlers)

Insgesamt 12 Subexperimente mit jeweils 10 Durchläufen ($120$ Gesamtdurchläufe):

* Variable Anzahl von Hidden Neurons (50, 100, 200) mit einem Hidden Layer
* Variable Anzahl von Hidden Layers (1, 2, 3) mit 100 Hidden Neurons
* (normales) DAE-GP und pre-trained DAE-GP

## Einfluss der Anzahl von Hidden Layers (1/2)

![Airfoil - Erste Generation Median Trainingsfehler - Variable Anzahl Hidden Layer (1/2)](./img/airfoil_firstGen/airfoil_firstGen_median_training_error_by_layers_6plots.png){height=85%}

## Einfluss der Anzahl von Hidden Layers (2/2)

![Airfoil - Erste Generation Median Trainingsfehler - Variable Anzahl Hidden Layer (2/2)](./img/airfoil_firstGen/airfoil_firstGen_median_training_error_by_layers_3plots.png){height=85%}

## Einfluss der Anzahl von Hidden Neurons (1/2)

![Airfoil - Erste Generation Median Trainingsfehler - Variable Anzahl Hidden Neurons (1/2)](./img/airfoil_firstGen/airfoil_firstGen_median_training_error_by_neurons_6plots.png){height=85%}

## Einfluss der Anzahl von Hidden Neurons (2/2)

![Airfoil - Erste Generation Median Trainingsfehler - Variable Anzahl Hidden Neurons (2/2)](./img/airfoil_firstGen/airfoil_firstGen_median_training_error_by_neurons_6plots.png){height=85%}


## Fazit Generalisierungsverhalten

...

# Untersuchung des Suchverhaltens bei symbolischer Regression

## Fragestellung

Welchen Einfluss hat die Verwendung einer Pre-Training Strategie auf das Suchverhalten von DAE-GP bei der Anwendung auf symbolische Regressionsprobleme?

Aufbau: Betrachtung des Suchverhalten über je $10$ Gesamtduchläufe für DAE-GP und pre-trained DAE-GP

Fokus insbesondere auf:

* Lösungsqualität (Fitness)
* Größe der gefundenen Lösungen (Anzahl an Knoten)
* Populationsdiversität

## Hyperparameter

\begin{table}
\centering\begingroup\fontsize{7}{9}\selectfont

\resizebox{\linewidth}{!}{
\begin{tabular}{l|l}
\hline
\textbf{parameter} & \textbf{value}\\
\hline
populationSize & 500\\
\hline
generations & 30\\
\hline
fitness & RMSE\\
\hline
TrainingMode & Convergence\\
\hline
SamplingSteps & 2\\
\hline
hiddenLayers & 2\\
\hline
Selection & Binary Tournament Selection\\
\hline
Pre-Training PopulationSize(Training/Validation) & 10000/100000\\
\hline
Pre-Training TrainingMode & Early Stopping\\
\hline
\end{tabular}}
\endgroup{}
\end{table}
## Funktions Set Symbolische Regression

\begin{table}[!h]
\centering
\begin{tabular}{l|r}
\hline
\textbf{function.} & \textbf{arity}\\
\hline
addition & 2\\
\hline
subtraction & 2\\
\hline
multiplication & 2\\
\hline
analytic\_quotient & 2\\
\hline
\end{tabular}
\end{table}

## Airfoil - Entwicklung der Fitness über Generationen

![Airfoil Datensatz - Fitness über Generationen](~/masterThesis/master_thesis/img/airfoil_2hl_maxIndSize_fullRun_30gens_withGP/mean_median_fitness_byGens.png){height=90%}



## Airfoil - Verteilung der finalen Fitness

![Airfoil Datensatz - Verteilung der finale Fitness](~/masterThesis/master_thesis/img/airfoil_2hl_maxIndSize_fullRun_30gens/final_fit_boxplot.png){height=90%}

## Airfoil - Größe der besten Lösungskandidaten

![Airfoil Datensatz - Größe der besten Lösung über Generationen](~/masterThesis/master_thesis/img/airfoil_2hl_maxIndSize_fullRun_30gens_withGP/mean_Size_byGens.png)

## Kontrollexperiment: Reduzierung der DAE-LSTM Dimension für Airfoil Datensatz

Frage: Welchen Einfluss hat die Reduktion der DAE-LSTM auf 1 hidden Layer (HL)?

## Airfoil - Entwicklung der Fitness (1 HL)

![Airfoil - Entwicklung der Fitness über Generationen (1 HL)](~/masterThesis/master_thesis/img/airfoil_1hl_maxIndSize_fullRun_30gens/mean_median_fitness_byGens.png)

## Airfoil - Verteilung der finalen Fitness (1HL)

![Airfoil - Verteilung der finalen Fitness (1HL)](~/masterThesis/master_thesis/img/airfoil_1hl_maxIndSize_fullRun_30gens/final_fit_boxplot.png){height=90%}

## Airfoil - Größe der besten Lösungskandidaten(1HL)

![Airfoil - Größe der besten Lösung über Generationen (1HL)](~/masterThesis/master_thesis/img/airfoil_1hl_maxIndSize_fullRun_30gens/mean_Size_byGens.png){height=90%}


## Anwendung auf weitere Datensätzen

Airfoil Datensatz: Ergebnis deuten bei einer ausreichenden Anzahl von Hidden Layern auf einen postitiven Effekt der Pre-Training Strategie hin:

* Höhere Fitness der gefundenen Lösungen
* Kleinere Größe der gefundenen Lösungen

Daher: Ausweitung des Experiments auf weitere Datensätze

## Übersicht Datensätze

\begin{table}[!h]
\centering
\begin{tabular}{l|r|r}
\hline
\textbf{Problem} & \textbf{Observations} & \textbf{Features}\\
\hline
Airfoil & 1503 & 5\\
\hline
Boston\_Housing & 506 & 13\\
\hline
Energy\_Cooling & 768 & 8\\
\hline
Concrete & 1030 & 8\\
\hline
\end{tabular}
\end{table}

## Symbolische Regression - Ergebnisübersicht



|     Problem     | Hidden-Layers |  Set  |  DAE-GP   | Pre-Trained | P-Value | Cliffs-Delta |
|:---------------:|:-------------:|:-----:|:---------:|:-----------:|:-------:|:------------:|
|     Airfoil     |       1       | Train | **33.37** |    35.35    | 0.02**  |     0.64     |
|                 |       1       | Test  | **33.73** |    35.61    |  0.14   |     0.4      |
|     Airfoil     |       2       | Train |   17.48   |  **14.72**  |  0.31   |    -0.28     |
|                 |       2       | Test  |   17.53   |  **14.76**  |  0.57   |    -0.16     |
| Boston_Housing  |       2       | Train |   8.19    |  **8.08**   |  0.29   |    -0.29     |
|                 |       2       | Test  |   8.05    |  **7.97**   |  0.71   |    -0.11     |
| Energy(Cooling) |       2       | Train | **4.53**  |    4.78     | 0.02**  |     0.63     |
|                 |       2       | Test  | **4.67**  |    4.92     |  0.29   |     0.29     |
|    Concrete     |       2       | Train |   17.3    |  **16.31**  |  0.53   |     -0.5     |
|                 |       2       | Test  |   16.67   |  **16.19**  |  0.80   |    -0.25     |



## Symbolische Regression - Übersicht Median Fitness

\begin{tabular}{cc}
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/energyCooling_2hl_maxIndSize_fullRun_30gens/median_fitness_byGens.png} &
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/bostonHousing_2hl_maxIndSize_fullRun_30gens/median_fitness_byGens.png} \\
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/airfoil_2hl_maxIndSize_fullRun_30gens/median_fitness_byGens.png} &
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/concrete_2hl_maxIndSize_fullRun_30gens/median_fitness_byGens.png}
\end{tabular}




## Zusammenfassung Fitness - Symbolische Regression

Keine Evidenz für einen statistisch signifikanten Einfluss von Pre-Training auf die erzielte Lösungsqualität in den durchgeführten Experimenten!

* Airfoil:
* Energy Cooling:
* Boston Housing: 
* Concrete: 


## Auswertung Größe der besten Individuen - Symbolische Regression


|     Problem     | Hid.Layers |  DAE-GP   | Pre-Trained | P-Value | Cliffs-Delta |
|:---------------:|:----------:|:---------:|:-----------:|:-------:|:------------:|
|     Airfoil     |     1      | **33.37** |    35.35    | 0.02**  |     0.64     |
|     Airfoil     |     2      |   17.48   |  **14.72**  |  0.31   |    -0.28     |
| Boston_Housing  |     2      |   8.19    |  **8.08**   |  0.29   |    -0.29     |
| Energy(Cooling) |     2      | **4.53**  |    4.78     | 0.02**  |     0.63     |
|    Concrete     |     2      |   17.3    |  **16.31**  |  0.53   |     -0.5     |
## Durchschnittliche Lösungsgröße - Symbolische Regression


\begin{tabular}{cc}
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/energyCooling_2hl_maxIndSize_fullRun_30gens/mean_Size_byGens.png} &
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/bostonHousing_2hl_maxIndSize_fullRun_30gens/mean_Size_byGens.png} \\
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/airfoil_2hl_maxIndSize_fullRun_30gens/mean_Size_byGens.png} &
\includegraphics[width=0.45\textwidth]{~/masterThesis/master_thesis/img/concrete_2hl_maxIndSize_fullRun_30gens/mean_Size_byGens.png}
\end{tabular}



# Weitere Ansätze

...


# References {.allowframebreaks} 








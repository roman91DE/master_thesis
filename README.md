# Master Thesis

Topic: Pre-Trained Denoising Autoencoders Long Short-Term Memory Networks as probabilistic Models for Estimation of Distribution Genetic Programming

Institution: Johannes Gutenberg University Mainz, Chair of Business Administration and Computer Science (FB 03)

## Abstract

### English

Denoising Autoencoder Genetic Programming (DAE-GP) is an Estimation of Distribution Algorithm in the domain of Genetic Programming that uses Denoising Autoencoders Long Short-Term Memory Networks (DAE-LSTM) as probabilistic models for sampling new populations of solutions.
This thesis investigates the possible benefits and downsides of using pre-training for the DAE-LSTM networks of DAE-GP for four real world symbolic regression problems.
The experiments conducted did show that pre-training can drastically reduce the number of epochs that are necessary for the DAE-LSTM training at each generation of the DAE-GP search.
Another interesting finding was that pre-training also increases the levenshtein edit distance between individual solutions inside the population which is a metric for the diversity of a population.
Unfortunately, pre-training did not yield any improvements in the final fitness or size of solutions, despite significantly increasing the total run-time for DAE-GP.

### Deutsche Fassung

Denoising Autoencoder Genetic Programming (DAE-GP) ist ein Estimation of Distribution Algorithmus (EDA) aus dem Forschungfeld der genetischen Programmierung (GP).
In DAE-GP werden Denoising Autoencoders Long Short-Term Memory Netzwerke (DAE-LSTM) als probabilistische Modelle verwendet um neue Populationen von Lösungen für eine evolutionäre Suche zu erzeugen.
Diese Masterarbeit untersucht die Vor- und Nachteile des Einsatzes einer Pre-Training Strategie für die DAE-LSTM Netzwerke von DAE-GP an vier Datensätzen für symbolische Regression.
Die durchgeführten Experimente haben gezeigt, dass Pre-Training die Anzahl von Trainingsepochen für die DAE-LSTM Netzwerke in jeder Generation statistisch signifikant reduzieren konnte.
Außerdem zeigt sich, dass Pre-Training die Levenshtein Editierdistanz, ein Maß für die Populationsdiversität, signifikant erhöhen konnte.
Leider konnte Pre-Training die Qualität der jeweils besten gefundenen Lösungen, weder im Bezug auf ihre Fitness noch auf ihre Größe, verbessern.
Auch führte Pre-Training in den durchgeführten Experimenten zu einer starken Erhöhung der Laufzeit des DAE-GP Algorithmus.

## Keywords

Genetic Programming, Estimation of Distribution Algorithms, Denoising Autoencoder Genetic Programming, Pre-Training, Long Short-Term Memory Networks, Symbolic Regression

## Documents available:

Full Thesis: `paper.pdf` (RMarkdown Source File: paper.Rmd)

PDF-Slide Show: `slides.pdf` (RMarkdown Source File: slides.Rmd)

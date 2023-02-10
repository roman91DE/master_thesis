# Master Thesis

Topic: Pre-Trained Denoising Autoencoders Long Short-Term Memory Networks as probabilistic Models for Estimation of Distribution Genetic Programming

Institution: Johannes Gutenberg University Mainz, Chair of Business Administration and Computer Science (FB 03)

## Abstract

Denoising Autoencoder Genetic Programming (DAE-GP) is an Estimation of Distribution Algorithm in the domain of Genetic Programming that uses Denoising Autoencoders Long Short-Term Memory Networks (DAE-LSTM) as probabilistic models for sampling new populations of solutions.
This thesis investigates the possible benefits and downsides of using pre-training for the DAE-LSTM networks of DAE-GP for four real world symbolic regression problems.
The Experiments conducted did show that pre-training can drastically reduce the number of training epochs that are necessary at each generation of the DAE-GP search while also increasing the diversity of the population.
Unfortunately pre-training did not show any improvements for both final fitness and the final size of solutions while largely increasing the total run-time for DAE-GP.

## Keywords

Genetic Programming, Estimation of Distribution Algorithms, Denoising Autoencoder Genetic Programming, Pre-Training, Long Short-Term Memory Networks, Symbolic Regression

## Documents available:

Full Thesis: `paper.pdf` (RMarkdown Source File: paper.Rmd)

PDF-Slide Show: `slides.pdf` (RMarkdown Source File: slides.Rmd)

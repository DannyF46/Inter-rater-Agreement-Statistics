# Inter-rater Agreement Statistic calculator

## Overview:
Inter-rater agreement statistics provide a measure of how well two sets of two (or more) categories agree with each other.

For example, say you wanted to determine if a novel medical test is reliable. Your new test either diagnoses a patient with some condition (category A) or it doesn't (category B).
To test its reliability, you can compare it with a standard test that is already known to be valid (i.e. a 2nd set of A and B categories). A more reliable test will have better agreement
with the standard test (more AA and BB entries), and thus the agreement coefficents will be closer to 1. If no correlation is present (similar amounts of AA and BB as AB and BA), then the coefficients are close to 0. If
there is a negative correlation between the two tests (more AB and BA entries), the coefficients are closer to -1.

## Use:
Run the script, select a number of categories, and enter your data into the array of cells that appear. 
Press Enter or click GO to recieve two sets of inter-rater agreement statistics, rounded to the nearest decimal of your choice:
- Cohen's Kappa (κ), its standard error (σ), and 95% confidece interval (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3900052/)
- Gwet's AC1, its standard error (σ), and 95% confidence interval (https://www.ncbi.nlm.nih.gov/books/NBK82266/)

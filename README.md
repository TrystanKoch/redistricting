# Redistricting
Political redistricting based on simple algorithms.

> [!Note]  
> This project is in active initial development. This means,
> - It lacks key features,
> - Existing features may change rapidly, and
> - Documentation and testing are nearly nonexistant.

## Installation

Clone the repository to a local directory. In that directory, on the command line, run

    pip install .

From a python interpreter, you can then import features as if from a library. As it is developed, usable features should appear below.

## Feature Implementation
### - [x] Download census files

This project attempts to maintain a data pipeline that is easily traceable to the original files published by the U.S Census. The functions of the ```data_acquisition``` module will pull the correct files from the Census' website.

```python 
import redistricting.data_acquisition
```

> [!Info]  
> The U.S. Census updates the location and naming of their files occasionally. The filename and url templates in ```config.toml``` are intended to make dealing with these updates less painful.

#### Example
Try downloading the census data for 


### - [x] Loading census blocks to geopandas

Since each state is represented in the census block tables by a FIPS (Federal Information Processing Standards) identification number, 

```python 
import redistricting.cl_argument_parsing
import redistricting.data_loading
```

> [!Info]  
> ```cl_argument_parsing.py``` is intended in the future to deal with all command line arguments of scripts. At the moment, it just contains a part of the FIPS lookup process.

### - [x] Huntington-Hill Apportionment

In order to allow users to experiment with the effects of different total numbers of representatives on the redistricting process, I've included the Huntington-Hill apportionment algorithm to determine the allotted representatives. To reflect current law, 435 is the default.

```python
import redistricting.apportionment
```

### - [ ] Cleaning census block dataframes

``` python
import redistricting.
```

### - [ ] CRS and Projection Handling
### - [ ] Split-line redistricting algorithm
### - [ ] Command line scripts
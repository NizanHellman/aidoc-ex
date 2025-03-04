# aidoc-ex

# Generic Storage API Implementation

## Project Description

We want you to implement a generic storage API. Meaning we want to encapsulate base storage mechanisms (for example the local file system or a remote object storage such as S3) with a single API.

The storage usage can be dynamic and it should support both long term storage, as well as a temporary cache for lengthy calculations, and any future usage with as little code changes as possible. 
Objects stored via this API should still be readable via 3rd side code/applications, meaning that each object should ideally be saved in its native format. Given that we don't know all of the potential usages of the API, it should support easily customizing the format objects of different types are saved according to user needs.

## Requirements
Please define the generic API and implement it for the local file system according to the requirements below. 

The list below is a minimal set of requirements, you may expand it.
Functions signatures written in this section are written as an example and you may change them as you see fit.
You may implement the requirements in whatever order you wish. 

### The API should support saving and loading objects of any type

### The API should enable metadata retrieval regarding the saved objects
How many objects are currently saved in the storage, whether a specific object exists in the storage, and anything else you think might be useful.

### Implement support for at least 3 different types of objects
- Numpy arrays as .npy files
- Dataframes as .csv files
- General types as .json files 

### Write adequate tests

## Implementation Details

The current implementation includes:
- Base Storage interface defining the core API
- Local Storage implementation supporting:
  - JSON files
  - YAML files
  - CSV files
  - NumPy arrays (.npy)
  - Custom class instances

## Installation

```


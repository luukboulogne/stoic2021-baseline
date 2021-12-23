# STOIC2021 Baseline Algorithm

This codebase contains an example submission for the [STOIC2021 COVID-19 AI Challenge](https://stoic2021.grand-challenge.org/). As a baseline algorithm, it implements a simple evaluation pipeline for an [I3D model](https://github.com/hassony2/kinetics_i3d_pytorch) that was trained on the [STOIC2021 training data](https://registry.opendata.aws/stoic2021-training/). You can use this repo as a template for your submission to the Qualification phase of the STOIC2021 challenge.

If something does not work for you, please do not hesitate to [contact us](mailto:luuk.boulogne@radboudumc.nl) or add a post in the [forum](https://grand-challenge.org/forums/forum/stoic2021-602/). If the problem is related to the code of this repository, please create a new issue on GitHub.

## Table of Contents
Before implementing your own algorithm with this template, we recommend to first upload a grand-challenge.org Algorithm based on the unaltered template by following these steps:

* [Prerequisites](#prerequisites)
* [Building, testing and exporting your container](#buildtestexport)
* [Creating an Algorithm on grand-challenge.org](#creating)
* [Uploading your container to your Algorithm](#uploading)
* [Submitting to the STOIC2021 Qualification phase](#submitting) 

Afterwards, you can easily [implement your own algorithm](#implementing), by altering this template and updating the Algorithm you created on grand-challenge.org.

<a id="prerequisites"></a>
## Prerequisites
We recommend using this repository on Linux. If you are using Windows, we recommend installing [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install). Please watch the [official tutorial](https://www.youtube.com/watch?v=PdxXlZJiuxA) by Microsoft for installing WSL 2 with GPU support.

* Have [Docker](https://www.docker.com/get-started) installed.
* Have an account on grand-challenge.org and make sure that you are a [verified user](https://grand-challenge.org/documentation/account-verification/) there.

<a id="buildtestexport"></a>
## Building, testing, and exporting your container 
### Building
To test if your system is set up correctly, you can run `./build.sh` (Linux) or `./build.bat` (Windows), that simply implement this command:

```docker build -t stoicalgorithm .```

Please note that the next step (testing the container) also runs a build, so this step is not necessary if you are certain that everything is set up correctly.

<a name="testing"></a>
### Testing
To test if the docker container works as expected, `test.sh`/`test.bat` will build the container and run it on images provided in the `./test/` folder. It will then check the results (`.json` files produced by your algorithm) against the `.json` files in `./test/`. 

If the tests run successfully, you will see `Tests successfully passed...`.

Note: If you do not have a GPU available on your system, remove the `--gpus all` flag in `test.sh`/`test.bat` to run the test.
Note: When you implemented your own algorithm using this template, please update the the `.json` files in `./test/` according to the output of your algorithm before running `test.sh`/`test.bat`.


### Exporting
Run `export.sh`/`export.bat` to save the docker image to `./STOICAlgorithm.tar.gz`. This script runs `build.sh`/`build.bat` as well as the following command:
`docker save stoicalgorithm | gzip -c > STOICAlgorithm.tar.gz`

<a id="creating"></a>
## Creating an Algorithm on grand-challenge.org
After [building, testing, and exporting your container](#buildtestexport), you are ready to create an Algorithm on grand-challenge.org. Note that there is no need to alter the algorithm implemented in this baseline repository to start this step. Once you have created an Algorithm on grand-challenge.org, you can later upload new docker containers to that same Algorithm as many times as you wish. 

You can create an Algorithm by following [this link](https://grand-challenge.org/algorithms/create/). Some important fields are:
   * Please choose a `Title` and `Description` for your algorithm;
   * Enter `CT` at `Modalities` and `Lung (Thorax)` at `Structures`;
   * Select a logo to represent your algorithm (preferably square image);
   * For the interfaces of the algorithm, please select `CT Image` as `Inputs`, and as `Outputs` select both `Probability COVID-19` and `Probability Severe COVID-19`;
   * Choose `Viewer CIRRUS Core (Public)` as a `Workstation`;
   * At the bottom of the page, indicate that you would like your Docker image to use GPU and how much memory it needs.
After filling in the form, click the "Save" button at the bottom of the page to create your Algorithm.
   
<a id="uploading"></a>
## Uploading your container to your Algorithm  
### Uploading manually
You have now [built, tested, and exported your container](#buildtestexport) and [created an Algorithm on grand-challenge.org](#creating). To upload your container to your Algorithm, go to "Containers" on the page for your Algorithm on grand-challenge.org. Click on "upload a Container" button, and upload your `.tar.gz` file. You can later update your container by uploading a new `.tar.gz` file.

### Linking a GitHub repo
Instead of uploading the `.tar.gz` file directly, you can also link your GitHub repo. Once your repo is linked, grand-challenge.org will automatically build the docker image for you, and add the updated container to your Algorithm. 
* First, click "Link Github Repo". You will then see a dropdown box, where your Github repo is listed only if it has the Grand-Challenge app already installed. Usually this is not the case to begin with, so you should click on "link a new Github Repo". This will guide you through the installation of the Grand-challenge app in your repository.
* After the installation of the app in your repository is complete you should be automatically returned to the Grand Challenge page, where you will find your repository now in the dropdown list (In the case you are not automatically returned to the same page you can [find your algorithm](https://grand-challenge.org/algorithms/) and click "Link Github Repo" again). Select your repository from the dropdown list and click "Save". 
* Finally, you need to tag your repository, this will trigger Grand-Challenge to start building the docker container.

### Make sure your container is Active 
Please note that it can take a while until the container becomes active (The status will change from "Ready: False" to "Active") after uploading it, or after linking your Github repo. Check back later or refresh the URL after some time. 

<a id="submitting"></a>
## Submitting to the STOIC2021 Qualification phase   
[With your Algorithm online](#uploading), you are ready to submit to the STOIC2021 Qualification Leaderboard. On https://stoic2021.grand-challenge.org/, navigate to the "Submit" tab. Navigate to the "Qualification" tab, and select your Algorithm from the drop down list. You can optionally leave a comment with your submission. 

Note that, depending on the availability of compute nodes on grand-challenge.org, it may take some time before the evaluation of your Algorithm finishes and its results can be found on the [Leaderboard](https://stoic2021.grand-challenge.org/evaluation/challenge/leaderboard/).

<a id="implementing"></a>
## Implementing your own algorithm
You can implement your own solution by editing the `predict` function in `./process.py`. Any additional imported packages should be added to `./requirements.txt`, and any additional files and folders you add should be explicitly copied in the `./Dockerfile`. See `./requirements.txt` and `./Dockerfile` for examples. To update your algorithm, you can simply [test](#testing) and [export](exporting) your new Docker container, after which you can [upload it to your Algorithm](#uploading). Once your new container is Active, you can [resubmit](#submitting) your Algorithm.

Please note that your container will not have access to the internet when executing on grand-challenge.org, so all model weights must be present in your container image. You can test this locally using the `--network=none` option of `docker run`.

Good luck with the STOIC2021 COVID-19 AI Challenge!  




## Tip: Running your algorithm on a test folder:
Once you validated that the algorithm works as expected in the [Testing](#testing) step, you might want to simply run the algorithm on the test folder and check the output `.json` files for yourself. If you are on a native Linux system you will need to create a results folder that the docker container can write to as follows (WSL users can skip this step).
   ```
   mkdir ./results
   chmod 777 ./results
   ```
To write the output of the algorithm to the results folder use the following command: 
   ```
   docker run --rm --memory=11g -v ./test:/input/ -v ./results:/output/ STOICAlgorithm
   ```

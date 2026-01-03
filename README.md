<img src="./images/image20.png" style="width:6.5in"
alt="horizontal line" />

**Evan Guarnaccia**

**Technical Account Manager**

**Dataiku**

1/2/26

Dataiku Gitops Integration

# OVERVIEW

This document is a guide to configuring a typical Dataiku gitops
lifecycle, in which project versions are pushed to Github repositories,
and optional tests are run both before moving the project bundle to a
staging area and also before deploying to the production environment. In
this case, the test comprises confirming the presence of the project’s
ML model(s) in Weights and Biases (W&B) before the project can be
staged, and ultimately deployed. Find code files at
[<u>https://github.com/evanguarnaccia</u>](https://github.com/evanguarnaccia)

# GOALS

1.  Provision and configure dev, staging, and prod environments

2.  Connect DSS project to remote Github repository

3.  Install and customize oneai plugin for W&B

4.  Configure Dataiku Github action to check W&B upon commit

5.  Successfully execute tests to deploy to staging and prod

# Milestones

- Configure nodes

- Configure Secrets

- Create Github repository

- Add remote to project

- Initialize Github repository

- Setup Github action

- Create Deployment Test

- Configure One.Ai plugin

- Push ML model to W&B

- Create new project branch

- Test and Deploy

## Configure Nodes

## This pipeline will consist of three nodes, a design node for development, and automation nodes for staging and production.

Create the needed instances in Fleet Manager

<img src="./images/image26.png"
style="width:6.5in;height:2.16667in" />

Go to the design node, and navigate to the big menu in the top right,
and click on “Local Deployer”, as shown below

<img src="./images/image33.png"
style="width:6.5in;height:1.75in" />

From the Local Deployer, select “Deploying Projects”, and then navigate
to the “Infrastructures” tab, and click “+ New Infrastructure” and
populate the fields. Make sure to use the correct “Lifecycle stage”
setting for each.

<img src="./images/image22.png"
style="width:6.5in;height:2.95833in" />

After setting those fields, click “ADD”, and when brought to the
following screen, click “Trust all certificates” and click “Save”

<img src="./images/image39.png"
style="width:6.5in;height:1.56944in" />

If done properly, both infrastructures should be registered with the
deployer. Take note of the IDs used here, as they will be used as
environment variables in Github.

<img src="./images/image17.png"
style="width:6.5in;height:1.29167in" />

## 

## Configure Secrets

To set the secrets, for each instance, generate an API key for the user
by going back to DSS and clicking on the user profile in the top right
of the page. From there, click the gears, and then select the API keys.
Create an API key for this purpose on the page shown below

<img src="./images/image8.png"
style="width:6.5in;height:2.625in" />

Navigate to the “Credentials” tab, and enter the W&B account API key

<img src="./images/image13.png"
style="width:6.5in;height:2.77778in" />

Finally, navigate to the “My Account” tab, and add a credential called
“wandbcred”, and set the value as the previously used W&B account API
key.

<img src="./images/image4.png"
style="width:6.5in;height:2.33333in" />

## Create Github repository

Before a project can be pushed to Github from DSS, a blank repository
must first be created. Create a bare public repository as shown below,
and copy the SSH link to the repository.

<img src="./images/image12.png"
style="width:6.5in;height:2.72222in" />

## 

## 

## 

## 

## Add Remote to Project

Go to DSS and navigate to the “Version Control” tab as shown

<img src="./images/image40.png"
style="width:6.5in;height:1.58333in" />

From there, click on the area shown below, and select “Add remote”

<img src="./images/image34.png"
style="width:6.5in;height:1.73611in" />

Enter the SSH link copied in the previous step, and if done properly, it
should look like this

<img src="./images/image28.png"
style="width:6.5in;height:0.625in" />

## Initialize Github Repository

To initialize the github repository for this project, the first step is
to push the project to it. Go to the menu as shown and click “Push”.
Also take note that the name of the branch is “master”.

<img src="./images/image31.png"
style="width:6.5in;height:1.36111in" />

If done correctly, the Github repository setup earlier should be
populated with files, similar to this

<img src="./images/image2.png"
style="width:6.5in;height:1.80556in" />

## Setup Github Action

From the screen above, click “Add file”, and give it the name
“.github/workflows/pr.yml”. Populate the file with the example code as
shown below. Change the branch name to “master” as noted earlier. In
this case, the Github action needed to be modified, so a mirror was
created of the repository containing the original Github action. Change
the value on line 17 of the file below to match the mirrored repo..

<img src="./images/image29.png"
style="width:6.5in;height:3.86111in" />

Create another file in the same directory called “release.yml” and
populate it with the example code and necessary modifications, as shown
below. Note that there are two additional environment variables:
DATAIKU_INFRA_STAGING_ID and DATAIKU_INFRA_PROD_ID. These are the
infrastructure ids created earlier.

<img src="./images/image24.png"
style="width:6.5in;height:3.19444in" />

The next step is to set the environment variables. Click “Settings” near
the top middle of the screen, click “Secrets and variables”, and then
click “Actions”. Use the tabs in the page shown below to add the secrets
and variables.

<img src="./images/image38.png"
style="width:6.5in;height:2.66667in" />

Navigate to the mirror of the Github action, and edit
“dataiku_gitops_action.py” in two places. First, add the ‘-s’ option to
print to the console, as shown below

<img src="./images/image16.png"
style="width:6.5in;height:2.13889in" />

Finally, comment out this block which checks agreement between commit
SHAs

<img src="./images/image14.png"
style="width:6.5in;height:1.43056in" />

Optionally, add code to append a timestamp to the bundle id, as shown
below, to avoid collisions

<img src="./images/image19.png"
style="width:6.5in;height:0.77778in" />

## 

## 

## 

## 

## 

## 

## Create Deployment Test

The Github action used in this workflow allows a user-defined test to be
run, and as suggested in pr.yml and release.yml, the test is contained
in a file called “[<u>tests.py</u>](http://tests.py)”. Create this file
and populate it with that code, as shown below

<img src="./images/image41.png"
style="width:6.5in;height:3.18056in" />

## Configure oneai plugin

To push ML models directly from DSS to Weights and Biases, a custom
plugin is needed. Download the oneai plugin, and go to DSS. Open the
menu in the top right corner, and under “Administration & Settings”,
click “Plugins”. Click “Add plugin” in the top right corner, and then
upload the zip file.

<img src="./images/image35.png"
style="width:6.5in;height:1.20833in" />

Once the plugin in installed, it should be available as shown below

<img src="./images/image27.png"
style="width:6.5in;height:1.125in" />

Click on “[<u>One.Ai</u>](http://one.ai)” and then “Actions” in the top
right corner. Click “Convert to dev plugin…” so the code can be edited.

Navigate to the “Edit” tab and make changes to runnable.json as shown
below. This will allow the plugin user to set the parameters for pushing
the ML model to W&B  
<img src="./images/image30.png"
style="width:6.5in;height:3.88889in" />

Next, make changes to [<u>runnable.py</u>](http://runnable.py) so that
the parameters are passed to the code which is talking to W&B, as shown
below. Make sure the rest of the code is properly referencing those new
variables.

<img src="./images/image7.png"
style="width:6.5in;height:2.22222in" />

Navigate to the “Settings” tab on this page, and then to “W&B
Credentials”. Create a preset as shown below.

<img src="./images/image5.png"
style="width:6.5in;height:3.65278in" />

## 

## Push ML model to W&B

Go to the project in DSS to be deployed, and click on the ML model in
the flow, as shown below

<img src="./images/image23.png"
style="width:6.5in;height:2.59722in" />

Click on “Publish model to Weights&Biases” and fill in the menu that
pops up, including the preset defined earlier. Click “RUN MACRO”

<img src="./images/image3.png"
style="width:6.5in;height:1.91667in" />

If done properly, the ML model should be pushed successfully to W&B

<img src="./images/image9.png"
style="width:6.5in;height:2.65278in" />

## Create New Project Branch

To make a pull request to the Github repository, first create a new
branch of the project before making changes to the project. Go to the
“Version control” tab, and create a new branch as shown below. For
simplicity, use the current project

<img src="./images/image1.png"
style="width:6.5in;height:1.55556in" />

Make the changes to the project, and navigate back to “Version control”,
and this time select “Push”, as shown below

<img src="./images/image6.png"
style="width:6.5in;height:1.51389in" />

A successful push will look similar to what is shown below

<img src="./images/image36.png"
style="width:6.5in;height:3.05556in" />

## Test and Deploy

If the previous steps have been done properly, the github repo should
have an option to click “Compare & pull request”, as shown below. This
click-through sets in motion the chain of events which apply the tests
and deploy to staging and prod if passed.

<img src="./images/image15.png"
style="width:6.5in;height:1.54167in" />

Click “Create pull request”, as shown below

<img src="./images/image32.png"
style="width:6.5in;height:1.875in" />

Click “Merge pull request”

<img src="./images/image10.png"
style="width:6.5in;height:0.70833in" />

Observe that the tests are being run, and click on “Details”

<img src="./images/image25.png"
style="width:6.5in;height:0.84722in" />

If successful, the output of the tests will be on the console as shown
below

<img src="./images/image11.png"
style="width:6.5in;height:3.875in" />

And the latest version of the project has been deployed to both staging
and production.

<img src="./images/image21.png"
style="width:6.5in;height:1.93056in" />

<img src="./images/image37.png"
style="width:6.5in;height:1.90278in" />

# Dataiku Gitops Integration

## OVERVIEW

This document is a guide to configuring a typical Dataiku gitops lifecycle, in which project versions are pushed to Github repositories, and optional tests are run both before moving the project bundle to a staging area and also before deploying to the production environment. In this case, the test comprises confirming the presence of the project’s ML model(s) in Weights and Biases (W&B) before the project can be staged, and ultimately deployed. Find code files at <span class="c11"><a href="https://www.google.com/url?q=https://github.com/evanguarnaccia&amp;sa=D&amp;source=editors&amp;ust=1767464092301144&amp;usg=AOvVaw3RQk7RRx1UInA9xiSNslK6" class="c5">https://github.com/evanguarnaccia</a></span>

## <span class="c1">GOALS</span>

1.  <span class="c0">Provision and configure dev, staging, and prod environments</span>
2.  <span class="c0">Connect DSS project to remote Github repository</span>
3.  <span class="c0">Install and customize oneai plugin for W&B</span>
4.  <span class="c0">Configure Dataiku Github action to check W&B upon commit</span>
5.  <span class="c0">Successfully execute tests to deploy to staging and prod</span>

## <span class="c1">Milestones</span>

- <span class="c0">Configure nodes</span>
- <span class="c0">Configure Secrets</span>
- <span class="c0">Create Github repository</span>
- <span class="c0">Add remote to project</span>
- <span class="c0">Initialize Github repository</span>
- <span class="c0">Setup Github action</span>
- <span class="c0">Create Deployment Test</span>
- <span class="c0">Configure One.Ai plugin</span>
- <span class="c0">Push ML model to W&B</span>
- <span class="c0">Create new project branch</span>
- <span class="c0">Test and Deploy</span>

### <span class="c8">Configure Nodes</span>

<span class="c0">This pipeline will consist of three nodes, a design node for development, and automation nodes for staging and production.</span>

<span class="c0">Create the needed instances in Fleet Manager</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 208.00px;"><img src="images/image29.png" style="width: 624.00px; height: 208.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Go to the design node, and navigate to the big menu in the top right, and click on “Local Deployer”, as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 168.00px;"><img src="images/image33.png" style="width: 624.00px; height: 168.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">From the Local Deployer, select “Deploying Projects”, and then navigate to the “Infrastructures” tab, and click “+ New Infrastructure” and populate the fields. Make sure to use the correct “Lifecycle stage” setting for each.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 284.00px;"><img src="images/image22.png" style="width: 624.00px; height: 284.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">After setting those fields, click “ADD”, and when brought to the following screen, click “Trust all certificates” and click “Save”</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 150.67px;"><img src="images/image39.png" style="width: 624.00px; height: 150.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">If done properly, both infrastructures should be registered with the deployer. Take note of the IDs used here, as they will be used as environment variables in Github.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 124.00px;"><img src="images/image7.png" style="width: 624.00px; height: 124.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Configure Secrets</span>

<span class="c0">To set the secrets, for each instance, generate an API key for the user by going back to DSS and clicking on the user profile in the top right of the page. From there, click the gears, and then select the API keys. Create an API key for this purpose on the page shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 252.00px;"><img src="images/image10.png" style="width: 624.00px; height: 252.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Navigate to the “Credentials” tab, and enter the W&B account API key</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 266.67px;"><img src="images/image18.png" style="width: 624.00px; height: 266.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Finally, navigate to the “My Account” tab, and add a credential called “wandbcred”, and set the value as the previously used W&B account API key.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 224.00px;"><img src="images/image12.png" style="width: 624.00px; height: 224.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### Create Github repository

<span class="c0">Before a project can be pushed to Github from DSS, a blank repository must first be created. Create a bare public repository as shown below, and copy the SSH link to the repository.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 261.33px;"><img src="images/image17.png" style="width: 624.00px; height: 261.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### Add Remote to Project

<span class="c0">Go to DSS and navigate to the “Version Control” tab as shown</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 152.00px;"><img src="images/image41.png" style="width: 624.00px; height: 152.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">From there, click on the area shown below, and select “Add remote”</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 166.67px;"><img src="images/image40.png" style="width: 624.00px; height: 166.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Enter the SSH link copied in the previous step, and if done properly, it should look like this</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 60.00px;"><img src="images/image11.png" style="width: 624.00px; height: 60.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Initialize Github Repository</span>

<span class="c0">To initialize the github repository for this project, the first step is to push the project to it. Go to the menu as shown and click “Push”. Also take note that the name of the branch is “master”.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 130.67px;"><img src="images/image31.png" style="width: 624.00px; height: 130.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">If done correctly, the Github repository setup earlier should be populated with files, similar to this</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 173.33px;"><img src="images/image8.png" style="width: 624.00px; height: 173.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Setup Github Action</span>

<span class="c0">From the screen above, click “Add file”, and give it the name “.github/workflows/pr.yml”. Populate the file with the example code as shown below. Change the branch name to “master” as noted earlier. In this case, the Github action needed to be modified, so a mirror was created of the repository containing the original Github action. Change the value on line 17 of the file below to match the mirrored repo..</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 370.67px;"><img src="images/image28.png" style="width: 624.00px; height: 370.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Create another file in the same directory called “release.yml” and populate it with the example code and necessary modifications, as shown below. Note that there are two additional environment variables: DATAIKU_INFRA_STAGING_ID and DATAIKU_INFRA_PROD_ID. These are the infrastructure ids created earlier.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 306.67px;"><img src="images/image23.png" style="width: 624.00px; height: 306.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">The next step is to set the environment variables. Click “Settings” near the top middle of the screen, click “Secrets and variables”, and then click “Actions”. Use the tabs in the page shown below to add the secrets and variables.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 256.00px;"><img src="images/image34.png" style="width: 624.00px; height: 256.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Navigate to the mirror of the Github action, and edit “dataiku_gitops_action.py” in two places. First, add the ‘-s’ option to print to the console, as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 205.33px;"><img src="images/image16.png" style="width: 624.00px; height: 205.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Finally, comment out this block which checks agreement between commit SHAs</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 137.33px;"><img src="images/image3.png" style="width: 624.00px; height: 137.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Optionally, add code to append a timestamp to the bundle id, as shown below, to avoid collisions</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 74.67px;"><img src="images/image14.png" style="width: 624.00px; height: 74.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Create Deployment Test</span>

The Github action used in this workflow allows a user-defined test to be run, and as suggested in pr.yml and release.yml, the test is contained in a file called “<span class="c11"><a href="https://www.google.com/url?q=http://tests.py&amp;sa=D&amp;source=editors&amp;ust=1767464092307914&amp;usg=AOvVaw2xZpuo8WIjqmjfTFjGxSE1" class="c5">tests.py</a></span><span class="c0">”. Create this file and populate it with that code, as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 305.33px;"><img src="images/image32.png" style="width: 624.00px; height: 305.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Configure oneai plugin</span>

<span class="c0">To push ML models directly from DSS to Weights and Biases, a custom plugin is needed. Download the oneai plugin, and go to DSS. Open the menu in the top right corner, and under “Administration & Settings”, click “Plugins”. Click “Add plugin” in the top right corner, and then upload the zip file.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 116.00px;"><img src="images/image30.png" style="width: 624.00px; height: 116.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Once the plugin in installed, it should be available as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 108.00px;"><img src="images/image24.png" style="width: 624.00px; height: 108.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

Click on “<span class="c11"><a href="https://www.google.com/url?q=http://one.ai&amp;sa=D&amp;source=editors&amp;ust=1767464092308738&amp;usg=AOvVaw1-ibeG2Uc7m0ouNiEBU_aS" class="c5">One.Ai</a></span><span class="c0">” and then “Actions” in the top right corner. Click “Convert to dev plugin…” so the code can be edited. </span>

Navigate to the “Edit” tab and make changes to runnable.json as shown below. This will allow the plugin user to set the parameters for pushing the ML model to W&B  
<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 373.33px;"><img src="images/image26.png" style="width: 624.00px; height: 373.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

Next, make changes to <span class="c11"><a href="https://www.google.com/url?q=http://runnable.py&amp;sa=D&amp;source=editors&amp;ust=1767464092309288&amp;usg=AOvVaw0bdZ_kE-pBexnBr0mm7DV9" class="c5">runnable.py</a></span><span class="c0"> so that the parameters are passed to the code which is talking to W&B, as shown below. Make sure the rest of the code is properly referencing those new variables.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 213.33px;"><img src="images/image5.png" style="width: 624.00px; height: 213.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Navigate to the “Settings” tab on this page, and then to “W&B Credentials”. Create a preset as shown below.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 350.67px;"><img src="images/image19.png" style="width: 624.00px; height: 350.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Push ML model to W&B</span>

<span class="c0">Go to the project in DSS to be deployed, and click on the ML model in the flow, as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 249.33px;"><img src="images/image21.png" style="width: 624.00px; height: 249.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Click on “Publish model to Weights&Biases” and fill in the menu that pops up, including the preset defined earlier. Click “RUN MACRO”</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 184.00px;"><img src="images/image2.png" style="width: 624.00px; height: 184.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">If done properly, the ML model should be pushed successfully to W&B</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 254.67px;"><img src="images/image13.png" style="width: 624.00px; height: 254.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Create New Project Branch</span>

<span class="c0">To make a pull request to the Github repository, first create a new branch of the project before making changes to the project. Go to the “Version control” tab, and create a new branch as shown below. For simplicity, use the current project</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 149.33px;"><img src="images/image9.png" style="width: 624.00px; height: 149.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Make the changes to the project, and navigate back to “Version control”, and this time select “Push”, as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 145.33px;"><img src="images/image20.png" style="width: 624.00px; height: 145.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">A successful push will look similar to what is shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 293.33px;"><img src="images/image25.png" style="width: 624.00px; height: 293.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

### <span class="c8">Test and Deploy</span>

<span class="c0">If the previous steps have been done properly, the github repo should have an option to click “Compare & pull request”, as shown below. This click-through sets in motion the chain of events which apply the tests and deploy to staging and prod if passed.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 148.00px;"><img src="images/image4.png" style="width: 624.00px; height: 148.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Click “Create pull request”, as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 180.00px;"><img src="images/image35.png" style="width: 624.00px; height: 180.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Click “Merge pull request”</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 68.00px;"><img src="images/image1.png" style="width: 624.00px; height: 68.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">Observe that the tests are being run, and click on “Details”</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 81.33px;"><img src="images/image27.png" style="width: 624.00px; height: 81.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">If successful, the output of the tests will be on the console as shown below</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 372.00px;"><img src="images/image15.png" style="width: 624.00px; height: 372.00px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0">And the latest version of the project has been deployed to both staging and production.</span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 185.33px;"><img src="images/image6.png" style="width: 624.00px; height: 185.33px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span style="overflow: hidden; display: inline-block; margin: 0.00px 0.00px; border: 0.00px solid #000000; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px); width: 624.00px; height: 182.67px;"><img src="images/image38.png" style="width: 624.00px; height: 182.67px; margin-left: 0.00px; margin-top: 0.00px; transform: rotate(0.00rad) translateZ(0px); -webkit-transform: rotate(0.00rad) translateZ(0px);" /></span>

<span class="c0"></span>

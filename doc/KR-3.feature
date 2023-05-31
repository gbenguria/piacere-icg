Feature: PIACERE Design time

    As a PIACERE user I want to generate IaC code for the provisioning and configuration of my infrastructure.


### SCENARIO 1: Generation of infrastructure provisioning code
Given a verified DOML model containing the infrastructure definition
When a user navigates to the DOMLx document
And right-clicks on it
And selects "Piacere"
And selects "Generate IaC code"
Then a compressed folder containing the infrastructural IaC code is generated

### SCENARIO 2: Generation of infrastructure provisioning code for multiple providers
Given a verified DOML model containing the infrastructure definition
And two different providers between the supported ones
And a user selects one of the two as active
When a user navigates to the DOML document
And right-clicks on it
And selects "Piacere"
And selects "Generate IaC code"
Then a compressed folder containing the infrastructural IaC code for the active provider is generated

### SCENARIO 3: Generation of contingent provisioning and configuration code
Given a verified DOML model containing the infrastructure and coherent application definition
When a user navigates to the DOMLx document
And right-clicks on it
And selects "Piacere"
And selects "Generate IaC code"
Then a compressed folder containing the infrastructural and subsequent application configuration IaC code is generated

### SCENARIO 4: Generation of PIACERE monitoring and security agents
Given a verified DOML model containing the infrastructure definition
And at least a virtual machine is defined
When a user navigates to the DOMLx document
And right-clicks on it
And selects "Piacere"
And selects "Generate IaC code"
Then a compressed folder is generated that contains also the monitoring and security agents configuration IaC code
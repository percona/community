how pmm built?

pmm pmm-server pmm-submodules, agent, exporters. 
We need relation on how they relate

pmm-submodules has VERSION file where version is. It also connect all submodules
It also has build scripts, how to build from sources to binaries.
also has script to build rpms

Why api are separated and how they relate ? dbaas-api pmm (that is also just API)


Issues
how to update client ? there is no doc to update it, how to restart agent, exporters and etc.
agent is restarted as part of post, exporters are child processes.
So we need to document how to update client.

Release:
pmm-update still need update with VERSION - link to the release notes. Version is also comes from there.
Merging fixes back to main from release branch.



Dev Setup pmm-update:

toolbox --image docker.io/percona/pmm-server:2.0.0 --container tool-pmm2.0

yum -y install https://packages.endpoint.com/rhel/7/os/x86_64/endpoint-repo-1.7-1.x86_64.rpm
yum install git go gcc make curl

zypper in git go gcc make curl
make init
make test

how to create FB ? when and why ?

what test to run? make test ? formating ?
make test
make format

linter ?


Repos:
https://repo.percona.com/pmm2-components/yum/experimental/7/RPMS/x86_64/
https://repo.percona.com/percona/yum/experimental/2/RPMS/x86_64/

pmm2-server could be changed to point to experimental, but pmm2-client always comes from the release repo, because path is different
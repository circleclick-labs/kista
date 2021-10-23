
# set up python paths so we can find libs and stuff
export PYTHONPATH=`pwd`

export WEB3_INFURA_PROJECT_ID=8ad1bacff3ea416989bc1bf33cf96d40
export WEB3_INFURA_SECRET=34ff1cee78be40e4bba76c6e7eb7da2a

export WEB3_PROVIDER_URI=https://kovan.infura.io/v3/$WEB3_INFURA_PROJECT_ID
export PROVIDER=${WEB3_PROVIDER_URI}

. ./env2.sh

$*

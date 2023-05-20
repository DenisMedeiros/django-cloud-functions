#!/bin/bash

# ROLE_ARN = SECRET - Must be defined as an env var.
FUNCTION_NAME="django-cloud-functions"
FUNCTION_HANDLER="awsentrypoint.main"
FUNCTION_AUTH_TYPE="AWS_IAM" # NONE or AWS_IAM
DESCRIPTION="Django App for Cloud Functions."
RUN_TIME="python3.8"
SITE_PACKAGES_DIR="venv/lib/python3.8/site-packages/"
TIMEOUT=60 # Seconds.
MEMORY_SIZE=128 # MB.
STORAGE=512 # MB.



function logging {
    # First parameter is loglevel, second is message.
    timestamp=$(date +"%Y-%m-%dT%H:%M:%S%z")
    printf "%-20s | %-8s | %-s\n" "$timestamp" "$1" "$2"

}

function create_package {
    logging "INFO" "Creating ZIP package..."
    if [ -f package.zip ]; then
        rm -f package.zip
    fi
    # Find the project dir and defined zip file path.
    project_dir=$(dirname -- "$(readlink -f -- "$0"; )";)
    # Pack all required libraries.
    zip_package="${project_dir}/package.zip"
    cd ${SITE_PACKAGES_DIR} && zip -rq ${zip_package} . && cd -

    # Include django project.
    cd src/ && zip -q -g ${zip_package} -r . && cd -
    logging "INFO" "ZIP package successfully created."
}

function deploy {
    # Check if function exists.
    logging "INFO" "Checking if function '${FUNCTION_NAME}' already exists..."
    aws lambda get-function --function-name "${FUNCTION_NAME}" --no-cli-pager > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        logging "INFO" "Function '${FUNCTION_NAME}' does not exist. Creating new function..."
        aws lambda create-function --function-name "${FUNCTION_NAME}" --description "${DESCRIPTION}" \
            --timeout ${TIMEOUT} --memory-size ${MEMORY_SIZE} --ephemeral-storage "{\"Size\": ${STORAGE}}" \
            --runtime "${RUN_TIME}" --role "${ROLE_ARN}" \
            --handler "${FUNCTION_HANDLER}" --package-type="Zip" --zip-file fileb://package.zip \
            --publish --no-cli-pager
        logging "INFO" "Creating function URL for'${FUNCTION_NAME}'..."
        aws lambda create-function-url-config --function-name "${FUNCTION_NAME}" \
            --auth-type ${FUNCTION_AUTH_TYPE} --no-cli-pager
    else
        logging "INFO" "Function '${FUNCTION_NAME}' already exists. Updating it..."
        aws lambda update-function-code --function-name "${FUNCTION_NAME}" \
            --zip-file fileb://package.zip --no-cli-pager
    fi

    logging "INFO" "Cloud function successfully deployed."
}

function undeploy {
    logging "INFO" "Removing cloud function '${FUNCTION_NAME}'..."
    aws lambda delete-function --function-name "${FUNCTION_NAME}"
    logging "INFO" "Removing function URL for '${FUNCTION_NAME}'..."
    aws lambda delete-function-url-config --function-name "${FUNCTION_NAME}"

}

function main {
    create_package
    # undeploy
    deploy
}


main
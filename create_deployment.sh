#!/bin/bash

function create_deployment_packages() {
    # Get list of directories in code/
    local code_dirs=$(ls -d code/lambdas/*/)

    # Iterate through each directory
    for dir in $code_dirs; do
        # Get the directory name without path
        dir_name=$(basename "$dir")
        echo "Processing $dir_name..."

        # Create a temporary directory for packaging
        mkdir -p "temp_deploy_${dir_name}"
        
        # copy domain
        cp -R "code/domain" "code/lambdas/${dir_name}"

        # Go to code directory
        cd "code/lambdas/${dir_name}"

        # Install Python packages
        pip install -r requirements.txt -t ./python_packages

        # Copy the specific function code
        cp -r ./* "../../../temp_deploy_${dir_name}/"

        cd "../../../temp_deploy_${dir_name}/"
        
        # Copy Python packages to temp directory
        #cp -r python_packages/* "../../temp_deploy_${dir_name}/"
        mv python_packages/* "./"

        rm -rf python_packages    

        # Go to temp directory
        #cd "temp_deploy_${dir_name}"

        # Create ZIP file (from within the temp directory to maintain flat structure)
        zip -r "./${dir_name}_deployment_package.zip" .
      
        # move zip to its own directory
        mv ${dir_name}_deployment_package.zip "../code/lambdas/${dir_name}"

        # Go back to original directory
        cd ..
        
        # Clean up
        rm -rf "temp_deploy_${dir_name}"

        echo "Created deployment package: ${dir_name}_deployment_package.zip"
    done
}

# Execute the function
create_deployment_packages


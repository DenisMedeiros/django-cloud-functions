# django-cloud-functions

This project demonstrate a proof of concept of how to deploy a Django app as a cloud function. This gives us the ability of using features like Django ORM or the Django Template Systema (Jinja2) in regular functions/ apps.

This shows the proof of concept of 2 features:

- A JSON response built using Django ORM queries.
- An HTML response built using Django Templates +  Django ORM queries.

Platforms supported so far:

- AWS Lambda

To be included later:

- Apache OpenWhisk (IBM Cloud)
- Google Cloud Functions
- Azure Cloud Functions

## Project Structure and Caveats

The Django project is defined in the folder [src](./src). Its structure is slightly modified and several
default apps and middleware modules are disabled since they are not necessary in a Cloud function.

The key point to make a Cloud Function using Django is to make sure each script using the Django framework starts with:

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
```

Any Django model **must be imported only after this block above.**

## Cloud Platform Deployment

### AWS Lambda

To deploy this project as a AWS Lambda project, run the steps below.

1. Create a virtual env:

    ```bash
    python3 -m venv venv
    ```

2. Activate the virtual env and create install the requirements. You may modify the file [requirements.txt](./requirements.txt) to include or remove additional libraries you need (e.g specific database library).

    ```bash
    source venv/bin/activate
    python3 -m pip install -r requirements.txt
    ```

3. At this point, it's assumed you already set up the AWS CLI locally and defined an [IAM Role](https://docs.aws.amazon.com/cli/latest/reference/iam/create-role.html). Define an environment variable named `ROLE_ARN` and check the options in the script [deploy-aws-lambda.sh](./deploy-aws-lambda.sh) before running it. Once you are ready, run the script.

    ```bash
    ./deploy-aws-lambda.sh
    ```

    This script will also set up a function URL. If you need more details on how to authenticate your HTTP requests against the URL, see the [SigV4 docs](https://dev.to/aws-builders/signing-requests-with-aws-sdk-in-lambda-functions-476) for more details.

4. Finally, test the endpoint on the paths `/html` (returns a rendered HTML page using Django Template System) and `/json` (returns a JSON response using Django ORM queries).

    ```bash
    # Example only - see how to build the SigV4 authentication.
    curl -X POST https://<server>.lambda-url.<region>.on.aws/html
    curl -X POST https://<server>.lambda-url.<region>.on.aws/json
    ```


## Limitations

Because this project uses the ZIP-based deployment, most of the limitations are due to the support of custom libraries in AWS Lambda platform. For example, newer Django versions require new database library versions, and the AWS Lambda platform does not have the proper system libraries. To overcome this, you should consider using the [Docker image](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html) deployment.